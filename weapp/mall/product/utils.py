# -*- coding: utf-8 -*-
from __future__ import absolute_import
import json
from datetime import datetime
from operator import attrgetter

from mall import models
from core import search_util


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
    # logger.debug("------------ %(func)s - customModels:%(value)s ----------",
    #              {
    #                 'func': 'extract_product_model',
    #                 'value': request.POST.get('customModels')
    #              })
    # # pdb.set_trace()
    is_use_custom_models = request.POST.get("is_use_custom_model", '') == u'true'

    use_custom_models = json.loads(request.POST.get('customModels', '[]'))
    if use_custom_models and is_use_custom_models:
        standard_model = {
            "price": 0.0,
            "weight": 0.0,
            "stock_type": models.PRODUCT_STOCK_TYPE_LIMIT,
            "stocks": -1,
            "user_code": '',
            "is_deleted": True
        }
        custom_models = use_custom_models
        for model in custom_models:
            model['properties'] = process_custom_model(model['name'])

    else:
        price = json.loads(request.POST.get('price', '0.0').strip())
        weight = json.loads(request.POST.get('weight', '0.0').strip())
        stock_type = int(request.POST.get(
            'stock_type',
            models.PRODUCT_STOCK_TYPE_UNLIMIT)
        )
        stocks = request.POST.get('stocks')
        stocks = int(stocks) if stocks else -1
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
    'product': [{
        'comparator': lambda product, filter_value: filter_value in product.name,
        'query_string_field': 'name'
    }, {
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
        'comparator': lambda model, filter_value: model['price'] >= float(filter_value),
        'query_string_field': 'lowPrice'
    }, {
        'comparator': lambda model, filter_value: model['price'] <= float(filter_value),
        'query_string_field': 'highPrice'
    }, {
        'comparator': lambda model, filter_value: model['stock_type'] == models.PRODUCT_STOCK_TYPE_UNLIMIT or model['stocks'] >= int(filter_value),
        'query_string_field': 'lowStocks'
    }, {
        'comparator': lambda model, filter_value: model['stocks'] <= int(filter_value),
        'query_string_field': 'highStocks'
    }]
}


# def filter_products(request, products):
#     has_filter = search_util.init_filters(request, PRODUCT_FILTERS)
#     if not has_filter:
#         # 没有filter，直接返回
#         return products

#     filtered_products = []
#     products = search_util.filter_objects(products, PRODUCT_FILTERS['product'])
#     if not products:
#         # product filter没有通过，跳过该promotion
#         print 'end in product filter'
#         return filtered_products
#     else:
#         print 'pass product filter'

#     for product in products:
#         models = search_util.filter_objects(
#             product.models,
#             PRODUCT_FILTERS['models']
#         )
#         if models:
#             print 'pass model filter'
#             filtered_products.append(product)
#         else:
#             print 'end in model filter'

#     return filtered_products


def filter_products(request, products):
    has_filter = search_util.init_filters(request, PRODUCT_FILTERS)
    if not has_filter:
        return products

    filtered_products = []
    products = search_util.filter_objects(products, PRODUCT_FILTERS['product'])
    if not products:
        return filtered_products

    for product in products:
        product.fill_model()
        models = search_util.filter_objects(
            product.models,
            PRODUCT_FILTERS['models']
        )
        if models:
            filtered_products.append(product)
    return filtered_products


def sorted_products(manager_id, product_categories, reverse):
    """根据display_index对在售商品进行排序

    Args:
      products(list): 根据CategoryHasProduct，添加过display的product列表
    """
    #获取与category关联的product集合
    category_ids = (category.id for category in product_categories)
    relations = models.CategoryHasProduct.objects.filter(
                    category_id__in=category_ids
    ).select_related('product')

    for c in product_categories:
        category_has_products = relations.filter(category_id=c.id)
        products = [x.product for x in category_has_products]
        models.Product.fill_display_price(products)
        models.Product.fill_sales_detail(manager_id,
                                         products,
                                         [product.id for product in products])
        for i in category_has_products:
            i.product.display_index = i.display_index
            i.product.join_category_time = i.created_at

        products = sorted(products, key=attrgetter('shelve_type', 'display_index'))
        products = sorted(products, key=attrgetter('shelve_type'), reverse=reverse)

        c.products = products
    return product_categories


# TODO: update models ref
#
# def update_one_product(request):
#     try:
#         name = request.POST.get('name')
#         product = models.Product.objects.get(name=name)
#     except models.Product.DoesNotExist:
#         print("Product with id does not exist")


# def validate_product_necessary_arguments(request):
#     """验证商品必要的参数是否已提供

#     Return:

#     """
#     try:
#         # 商品名称验证
#         name_pattern = r'\A\w{1,20}\Z'  # 1 到 20 个字符
#         name = request.POST['name']
#         result = re.match(name_pattern, name, re.UNICODE)
#         name = True if result else False

#         # 商品图片验证
#         swipe_images = json.loads(request.POST['swipe_images'])
#         swipe_images = True if swipe_images else False

#         # 无规格商品必要参数验证
#         if not request.POST.get('is_use_custom_model'):
#             price = request.POST['price']
#             weight = request.POST['weight']
#         # 有规格商品必要参数验证
#         else:
#             is_custom_model_validation = True
#             custom_model = json.loads(request.POST['customModels'])
#             for i in customModels:
#                 price = i['price']
#                 weight = i['weight']
#     except KeyError:
#         return False

