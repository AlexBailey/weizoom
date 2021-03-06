# -*- coding: utf-8 -*-
from __future__ import absolute_import
import json, copy
from datetime import datetime
from operator import attrgetter

from django.db.models import Q

from mall import models
from mall import signals as mall_signals
from account.models import UserProfile
from mall.promotion import models as promotion_model
from core import search_util
from mall.signal_handler import products_not_online_handler_for_promotions
from utils import ding_util
from apps.customerized_apps.group.group_openapi import stop_group_activity_by_pid

from watchdog.utils import watchdog_fatal, watchdog_error
from core.exceptionutil import unicode_full_stack
from django.conf import settings
import logging
import urllib
from django.db.models import F
from eaglet.utils.resource_client import Resource

DING_GROUP_ID = '93756731'
TEST_DING_GROUP_ID = '80035247'

def process_custom_model(custom_model_str):
    """处理custommodels字符串

    Args:
        customModels(str): a str like 2:4_1:3

    Return:
        list: the list like [{
                                'property_id': 2,
                                'property_value_id': 4
                            },{
                                'property_id': 1,
                                'property_value_id': 4
                            }]
    """
    properties = []
    property_infos = custom_model_str.split('_')
    for property_info in property_infos:
        items = property_info.split(':')
        properties.append({
            'property_id': int(items[0]),
            'property_value_id': int(items[1])
        })
    return properties


def extract_product_model(request):
    is_use_custom_models = request.POST.get("is_use_custom_model", '') == u'true'

    use_custom_models = json.loads(request.POST.get('customModels', '[]'))
    if use_custom_models and is_use_custom_models:
        standard_model = {
            "price": 0.0,
            "weight": 0.0,
            "stock_type": models.PRODUCT_STOCK_TYPE_LIMIT,
            "stocks": 0,
            "user_code": '',
            "is_deleted": True
        }
        custom_models = use_custom_models
        for model in custom_models:
            model['properties'] = process_custom_model(model['name'])
            if model.get('stocks') and int(model.get('stocks')) == -1:
                model['stocks'] = 0

    else:
        price = request.POST.get('price', '0.0').strip()
        weight = request.POST.get('weight', '0.0').strip()
        stock_type = int(request.POST.get(
            'stock_type',
            models.PRODUCT_STOCK_TYPE_UNLIMIT)
        )
        stocks = request.POST.get('stocks')
        if stocks and int(stocks) == -1:
            stocks = 0
        stocks = int(stocks) if stocks else 0
        user_code = request.POST.get('user_code', '').strip()
        standard_model = {
            "price": price,
            "weight": weight,
            "stock_type": stock_type,
            "stocks": stocks,
            "user_code": user_code,
        }
        custom_models = []
    return (standard_model, custom_models)

PRODUCT_FILTERS = {
    'product': [ {
        'comparator': lambda product, filter_value: product.sales >= int(filter_value),
        'query_string_field': 'lowSales'
    }, {
        'comparator': lambda product, filter_value: product.sales <= int(filter_value),
        'query_string_field': 'highSales'
    }, {
        'comparator': lambda product, filter_value: (int(filter_value) == -1) or (int(filter_value) in [category['id'] for category in product.categories if category['is_selected']]),
        'query_string_field': 'category'
    }, {
        'comparator': lambda product, filter_value: filter_value == product.bar_code,
        'query_string_field': 'barCode'
    }, {
        'comparator': lambda product, filter_value: product.created_at >= datetime.strptime(filter_value, '%Y-%m-%d %H:%M'),
        'query_string_field': 'startDate'
    }, {
        'comparator': lambda product, filter_value: product.created_at <= datetime.strptime(filter_value, '%Y-%m-%d %H:%M'),
        'query_string_field': 'endDate'
    }],
    'models': [{
        'comparator': lambda model, filter_value: float(model['price']) >= float(filter_value),
        'query_string_field': 'lowPrice'
    }, {
        'comparator': lambda model, filter_value: float(model['price']) <= float(filter_value),
        'query_string_field': 'highPrice'
    }, {
        'comparator': lambda model, filter_value: model['stock_type'] == models.PRODUCT_STOCK_TYPE_UNLIMIT or model['stocks'] >= int(filter_value),
        'query_string_field': 'lowStocks'
    }, {
        'comparator': lambda model, filter_value: model['stock_type'] != models.PRODUCT_STOCK_TYPE_UNLIMIT and 0 <= model['stocks'] <= int(filter_value) or int(filter_value) < 0,
        'query_string_field': 'highStocks'
    }]
}

MALL_PRODUCT_FILTERS = {
    'product': [{
        'comparator': lambda product, filter_value: product.sales >= int(filter_value),
        'query_string_field': 'lowSales'
    }, {
        'comparator': lambda product, filter_value: product.sales <= int(filter_value),
        'query_string_field': 'highSales'
    }, {
        'comparator': lambda product, filter_value: (int(filter_value) == -1) or (int(filter_value) in [category['id'] for category in product.categories if category['is_selected']]),
        'query_string_field': 'category'
    }, {
        'comparator': lambda product, filter_value: filter_value == product.bar_code,
        'query_string_field': 'barCode'
    }
    # , {
    #     'comparator': lambda product, filter_value: product.created_at >= datetime.strptime(filter_value, '%Y-%m-%d %H:%M'),
    #     'query_string_field': 'startDate'
    # }, {
    #     'comparator': lambda product, filter_value: product.created_at <= datetime.strptime(filter_value, '%Y-%m-%d %H:%M'),
    #     'query_string_field': 'endDate'
    # }
    ],
    'models': [{
        'comparator': lambda model, filter_value: float(model['price']) >= float(filter_value),
        'query_string_field': 'lowPrice'
    }, {
        'comparator': lambda model, filter_value: float(model['price']) <= float(filter_value),
        'query_string_field': 'highPrice'
    }, {
        'comparator': lambda model, filter_value: model['stock_type'] == models.PRODUCT_STOCK_TYPE_UNLIMIT or model['stocks'] >= int(filter_value),
        'query_string_field': 'lowStocks'
    }, {
        'comparator': lambda model, filter_value: model['stock_type'] != models.PRODUCT_STOCK_TYPE_UNLIMIT and 0 <= model['stocks'] <= int(filter_value) or int(filter_value) < 0,
        'query_string_field': 'highStocks'
    }]
}

def filter_products(request, products ,mall_type=False, params=None):
    if mall_type:
        current_product_filters = MALL_PRODUCT_FILTERS
    else:
        current_product_filters = PRODUCT_FILTERS

    has_filter = search_util.init_filters(request, current_product_filters, params)
    if not has_filter:
        return products

    filtered_products = []
    products = search_util.filter_objects(products, current_product_filters['product'])
    if not products:
        return filtered_products

    for product in products:
        models = copy.copy(product.models)
        if None in models:
            models.remove(None)
        models = search_util.filter_objects(models, current_product_filters['models'])
        if models:
            filtered_products.append(product)
    return filtered_products


def sorted_products(mall_type, manager_id, product_categories, reverse):
    """根据display_index对在售商品进行排序

    Args:
      products(list): 根据CategoryHasProduct，添加过display的product列表
    """
    #获取与category关联的product集合
    category_ids = (category.id for category in product_categories)
    relations = models.CategoryHasProduct.objects.filter(
        category_id__in=category_ids).select_related('product')
    categoryId2relations = dict()
    for relation in relations:
        categoryId2relations.setdefault(relation.category_id, []).append(relation)
    productIds = set([x.product_id for x in relations])
    products = models.Product.objects.filter(id__in=productIds, is_deleted=False).exclude(
        shelve_type=models.PRODUCT_SHELVE_TYPE_RECYCLED)

    product_pool2status = {}
    if mall_type:
        product_pool = models.ProductPool.objects.filter(woid=manager_id)
        product_pool2status = dict([(pool.product_id, pool.status) for pool in product_pool])

    # 微众商城代码
    #duhao 20151120
    #微众商城的商品-分组管理 页面  商品的状态应该是商品在微众商城里的状态，而不是在商户里的状态
    # if manager_id == 216:
    #     _products = []
    #     for product in products:
    #         if product.owner_id == 216 or (product.weshop_sync > 0 and product.shelve_type == models.PRODUCT_SHELVE_TYPE_ON):
    #             if product.owner_id != 216:
    #                 product.shelve_type = product.weshop_status
    #             _products.append(product)
    #     products = _products

    models.Product.fill_display_price(products)
    models.Product.fill_sales_detail(manager_id, products, productIds)
    #id2product = dict([(product.id, product) for product in products])
    id2product = {}
    producte_id = []
    for product in products:
        if mall_type and product_pool2status:
            if product.id in product_pool2status.keys():
                status_pool = product_pool2status[product.id]
                if status_pool == models.PP_STATUS_ON:
                    product.shelve_type = models.PRODUCT_SHELVE_TYPE_ON
                    status = u'在售'
                elif status_pool == models.PP_STATUS_OFF:
                    product.shelve_type = models.PRODUCT_SHELVE_TYPE_OFF
                    status = u'待售'
                elif status_pool == models.PP_STATUS_DELETE:
                    product.shelve_type = models.PRODUCT_SHELVE_TYPE_OFF
                    status = u'已删除'
                else:
                    product.shelve_type = models.PRODUCT_SHELVE_TYPE_OFF
                    status = u'商品池中'
            else:
                status = product.status
        else:
            status = product.status
        product._status = status
        id2product[product.id] = product

    for c in product_categories:
        products = []
        for i in categoryId2relations.get(c.id, []):
            if id2product.has_key(i.product_id):
                product = copy.copy(id2product[i.product_id])
                product.display_index = i.display_index
                product.join_category_time = i.created_at
                products.append(product)

        products_is_0 = filter(lambda p: p.display_index == 0 or p.shelve_type != models.PRODUCT_SHELVE_TYPE_ON, products)
        #if mall_type:
        products_not_0 = filter(lambda p: p.display_index != 0 and p.shelve_type == models.PRODUCT_SHELVE_TYPE_ON, products)
        #else:
        #    products_not_0 = filter(lambda p: p.display_index != 0, products)
        products_is_0 = sorted(products_is_0, key=attrgetter('shelve_type', 'join_category_time', 'id'), reverse=True)
        products_not_0 = sorted(products_not_0, key=attrgetter('display_index'))
        products = products_not_0 + products_is_0

        # products = sorted(products, key=attrgetter('join_category_time', 'id'), reverse=True)
        # products = sorted(products, key=attrgetter('shelve_type', 'display_index'))
        # products = sorted(products, key=attrgetter('shelve_type'), reverse=reverse)


        c.products = products
    return product_categories

MALL_PRODUCT_DELETED = -1
MALL_PRODUCT_OFF_SHELVE = 0
MALL_PRODUCT_HAS_MORE_MODEL = 1

DELETED_WEIZOOM_PRODUCT_REASON = {
    MALL_PRODUCT_DELETED: u'供货商商品删除',
    MALL_PRODUCT_OFF_SHELVE: u'供货商商品下架',
    MALL_PRODUCT_HAS_MORE_MODEL: u'供货商修改商品为多规格'
}

def delete_weizoom_mall_sync_product(request, product, reason):
    try:
        relations = models.WeizoomHasMallProductRelation.objects.filter(mall_product_id=product.id, is_deleted=False)
        if relations.count() > 0:
            weizoom_store_user_ids = []
            weizoom_product_ids = []
            weizoom_product_id2user_id = dict()
            for relation in relations:
                weizoom_store_user_ids.append(relation.owner_id)
                weizoom_product_ids.append(relation.weizoom_product_id)
                weizoom_product_id2user_id[relation.weizoom_product_id] = relation.owner_id

            use_id2store_name = dict([(profile.user_id, profile.store_name)for profile in UserProfile.objects.filter(user_id__in=weizoom_store_user_ids)])
            products = models.Product.objects.filter(id__in=weizoom_product_ids)
            products.update(is_deleted=True)
            relations.update(is_deleted=True)
            products_not_online_handler_for_promotions(weizoom_product_ids, request,shelve_type='delete')
            # 结束对应自营平台的团购商品
            for pid in weizoom_product_ids:
                is_test = False
                if request.META.get('SERVER_NAME') == "testserver":
                    is_test = True
                stop_group_activity_by_pid(pid, is_test)
            text = u'商品删除提示：\n'
            text += u'商品位置：\n'
            for product in products:
                text += (use_id2store_name[weizoom_product_id2user_id[product.id]] if use_id2store_name[weizoom_product_id2user_id[product.id]] else '') + '-' + (u'在售' if product.shelve_type else u'待售') + '-' + product.name + '\n'
            text += u'供货商：%s\n' % request.user_profile.store_name
            text += u'删除原因：%s\n' % DELETED_WEIZOOM_PRODUCT_REASON[reason]
            text += u'请及时处理！'
            if settings.MODE in ['develop', 'test'] or request.user.username == 'ceshi01':
                ding_util.send_to_ding(text, TEST_DING_GROUP_ID)
            else:
                ding_util.send_to_ding(text, DING_GROUP_ID)
    except:
        error_msg = u"delete_weizoom_mall_sync_product error, cause:\n{}".format(unicode_full_stack())
        watchdog_error(error_msg)

def update_weizoom_mall_sync_product_status(request, product, update_data):
    try:
        relations = models.WeizoomHasMallProductRelation.objects.filter(mall_product_id=product.id, is_deleted=False)
        if relations.count() > 0:
            weizoom_store_user_ids = []
            weizoom_product_ids = []
            weizoom_product_id2user_id = dict()
            for relation in relations:
                weizoom_store_user_ids.append(relation.owner_id)
                weizoom_product_ids.append(relation.weizoom_product_id)
                weizoom_product_id2user_id[relation.weizoom_product_id] = relation.owner_id

            use_id2store_name = dict([(profile.user_id, profile.store_name)for profile in UserProfile.objects.filter(user_id__in=weizoom_store_user_ids)])
            products = models.Product.objects.filter(id__in=weizoom_product_ids)
            text = u'商品更新提示：\n'
            text += u'商品位置：\n'
            for product in products:
                text += (use_id2store_name[weizoom_product_id2user_id[product.id]] if use_id2store_name[weizoom_product_id2user_id[product.id]] else '') + '-' + (u'在售' if product.shelve_type else u'待售') + '-' + product.name + '\n'
            text += u'供货商：%s\n' % request.user_profile.store_name
            text += u'更新内容：%s\n' % u'，'.join(update_data)
            text += u'请及时处理！'
            relations.update(is_updated=True)
            if settings.MODE in ['develop', 'test'] or request.user.username == 'ceshi01':
                ding_util.send_to_ding(text, TEST_DING_GROUP_ID)
            else:
                ding_util.send_to_ding(text, DING_GROUP_ID)
    except:
        error_msg = u"update_weizoom_mall_sync_product_status error, cause:\n{}".format(unicode_full_stack())
        watchdog_error(error_msg)

def get_sync_product_store_name(product_ids):
    # try:
    relations = models.WeizoomHasMallProductRelation.objects.filter(weizoom_product_id__in=product_ids, is_deleted=False)
    product_id2mall_id = {}
    product_id2sync_time = {}
    for relation in relations:
        product_id2mall_id[relation.weizoom_product_id] = relation.mall_id
        product_id2sync_time[relation.weizoom_product_id] = relation.sync_time.strftime('%Y-%m-%d %H:%M')
    mall_ids = product_id2mall_id.values()
    mall_id2store_name = dict([(profile.user_id, profile.store_name) for profile in UserProfile.objects.filter(user_id__in=mall_ids)])
    product_id2store_name = {}
    for product_id in product_id2mall_id.keys():
        product_id2store_name[product_id] = mall_id2store_name[product_id2mall_id[product_id]]
    return product_id2store_name, product_id2sync_time

def weizoom_filter_products(request, products):
    """
    weizoom自营平台筛选商品
    """
    store_name = request.GET.get('supplier', '')
    start_date = request.GET.get('startDate', '')
    end_date = request.GET.get('endDate', '')

    from_supplier_product_ids = []
    from_store_product_ids = []
    if not store_name and not start_date and not end_date:
        return filter_products(request, products)

    # 同步商品
    from weixin.user.module_api import get_all_active_mp_user_ids
    #all_user_ids = get_all_active_mp_user_ids()
    all_mall_userprofiles = UserProfile.objects.filter(webapp_type=0)
    if store_name:
        owner_ids = [profile.user_id for profile in all_mall_userprofiles.filter(store_name__contains=store_name)]
        # 手动添加供货商
        supplier_ids = [supplier.id for supplier in models.Supplier.objects.filter(
                                        owner=request.manager,
                                        name__contains=store_name,
                                        is_delete=False
                                    )]
    else:
        owner_ids = [profile.user_id for profile in all_mall_userprofiles.all()]
        supplier_ids = [supplier.id for supplier in models.Supplier.objects.filter(
                                        owner=request.manager,
                                        is_delete=False
                                    )]

    if start_date and end_date:
        params = dict(
                owner=request.manager,
                mall_id__in=owner_ids,
                is_deleted=False,
                sync_time__gte=start_date,
                sync_time__lte=end_date
            )
        params1 = dict(
                owner=request.manager,
                supplier__in=supplier_ids,
                is_deleted=False,
                created_at__gte=start_date,
                created_at__lte=end_date
            )
    else:
        params = dict(
                owner=request.manager,
                mall_id__in=owner_ids,
                is_deleted=False,
            )
        params1 = dict(
                owner=request.manager,
                supplier__in=supplier_ids,
                is_deleted=False,
            )

    from_supplier_product_ids = [product.id for product in models.Product.objects.filter(**params1)]
    from_store_product_ids = [relation.weizoom_product_id for relation in models.WeizoomHasMallProductRelation.objects.filter(**params)]
    filter_product_ids = from_store_product_ids + from_supplier_product_ids

    filtered_products = filter_products(request, products)
    new_filtered_products = []
    for product in filtered_products:
        if product.id in filter_product_ids:
            new_filtered_products.append(product)
    return new_filtered_products


def handle_group_product(request, product_id, swipe_images, thumbnails_url):
    #添加团购活动商品的操作

    # 处理轮播图
    models.ProductSwipeImage.objects.filter(
        product_id=product_id
    ).delete()
    for swipe_image in swipe_images:
        models.ProductSwipeImage.objects.create(
            product_id=product_id,
            url=swipe_image['url'],
            width=swipe_image['width'],
            height=swipe_image['height']
        )
    # 处理商品规格
    standard_model, custom_models = extract_product_model(request)

    # 处理standard商品规格
    models.ProductModel.objects.filter(
        product_id=product_id, name='standard'
    ).update(
        price=standard_model['price'],
        stock_type=standard_model['stock_type'],
        stocks=standard_model['stocks'],
        is_deleted=False
    )

    # 减少原category的product_count
    user_category_ids = [
        category.id for category in models.ProductCategory.objects.filter(
            owner=request.manager)]
    old_category_ids = set([relation.category_id for relation in models.CategoryHasProduct.objects.filter(
        category_id__in=user_category_ids, product_id=product_id)])
    catetories_ids = request.POST.get('product_category', -1).split(',')

    for category_id in catetories_ids:
        if not category_id.isdigit():
            continue
        category_id = int(category_id)
        if category_id in old_category_ids:
            old_category_ids.remove(category_id)
        else:
            models.CategoryHasProduct.objects.create(
                category_id=category_id, product_id=product_id)
            models.ProductCategory.objects.filter(
                id=category_id
            ).update(product_count=F('product_count') + 1)
    if len(old_category_ids) > 0:
        # 存在被删除的ctegory关系，删除该关系
        models.CategoryHasProduct.objects.filter(
            category_id__in=old_category_ids, product_id=product_id
        ).delete()
        models.ProductCategory.objects.filter(
            id__in=old_category_ids
        ).update(product_count=F('product_count') - 1)


    is_delivery = request.POST.get('is_delivery', False)
    param = {
        'name': request.POST.get('name', '').strip(),
        'thumbnails_url': thumbnails_url,
        'detail': request.POST.get('detail', '').strip(),
        'is_delivery': is_delivery,
    }
    # 微众商城代码
    # if request.POST.get('weshop_sync', None):
    #     param['weshop_sync'] = request.POST['weshop_sync'][0]
    models.Product.objects.record_cache_args(
        ids=[product_id]
    ).filter(
        owner=request.manager,
        id=product_id
    ).update(**param)


def get_product2group(pids, woid='3'):
    #例子
    #pids为list,里面的每一项都是商品id的str

    # pids_url = "http://{}/mall2/api/test/".format(settings.MARKETTOOLS_HOST)
    if not pids:
        return {}
    params = {
        'woid': woid,
        'pids': "_".join(pids)
    }

    resp = Resource.use('marketapp_apiserver').get({
        'resource':'group.group_buy_products',
        'data':params
    })

    if resp and resp['code']:
        data = resp['data']
        product_groups = data['pid2is_in_group_buy']
        product2group = {}
        for product_group in product_groups:
            product2group[product_group["pid"]] = product_group["is_in_group_buy"]
    else:
        product2group = {}

    return product2group

def get_pids(woid):
    params = {
        'woid': woid
    }
    resp = Resource.use('marketapp_apiserver').get({
        'resource': 'group.get_pids_by_woid',
        'data': params
    })

    pids = []
    if resp and resp['code'] == 200:
        data = resp['data']
        if data.has_key("pids_list"):
            pids = data["pids_list"]

    return pids

def get_product_ids_by_classification(first_classification, secondary_classification, woid, product_pool_param={}):
    if secondary_classification == -1:
        subclassification_ids = models.Classification.objects.filter(father_id=first_classification, level=2).values_list('id' ,flat=True)
        product_ids = models.ClassificationHasProduct.objects.filter(
                                classification_id__in=subclassification_ids
                                ).values_list('product_id', flat=True)
    elif secondary_classification > 0:
        product_ids = models.ClassificationHasProduct.objects.filter(
                                classification_id=secondary_classification
                                ).values_list('product_id', flat=True)
    else:
        product_ids = []
    if product_pool_param.has_key('status'):
        pool_status = product_pool_param['status']
    else:
        pool_status = models.PP_STATUS_ON_POOL
    product_ids = models.ProductPool.objects.filter(
        woid=woid,
        product_id__in=product_ids,
        status=pool_status).values_list('product_id', flat=True)
    return product_ids

def get_new_promote_product_count(request):
    new_promote_product_count = 0
    manager_id = request.manager.id
    manager_profile = UserProfile.objects.get(user_id=manager_id)
    if manager_profile.webapp_type:
        promote_detail_models = models.PromoteDetail.objects.filter(promote_status=models.PROMOTING,
                                                                    is_new=True)
        product_ids = promote_detail_models.values_list('product_id', flat=True)
        if 'product_pool' in request.META['HTTP_REFERER']:
            product_status = models.PP_STATUS_ON_POOL
        elif '/mall2/product_list/?shelve_type=1' in request.META['HTTP_REFERER']:
            product_status = models.PP_STATUS_ON
        elif '/mall2/product_list/?shelve_type=0' in request.META['HTTP_REFERER']:
            product_status = models.PP_STATUS_OFF
        else:
            return new_promote_product_count
        ids = models.ProductPool.objects.filter(
            woid=request.user.id,
            product_id__in=product_ids,
            status=product_status
        ).values_list('product_id', flat=True)
        new_promote_product_count = promote_detail_models.filter(product_id__in=ids).count()
    return new_promote_product_count