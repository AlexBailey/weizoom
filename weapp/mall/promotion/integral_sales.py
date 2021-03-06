# -*- coding: utf-8 -*-
import json
from datetime import datetime
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required

from core import resource
from core.jsonresponse import create_response
from mall import export
from mall.promotion import models as promotion_models  # 注意：不要覆盖此module
from mall.promotion.utils import string_ids2int_ids, verification_multi_product_promotion, verification_multi_product_promotion_weizoom_mall
from modules.member.models import MemberGrade, IntegralStrategySttings


class IntegralSales(resource.Resource):
    app = 'mall2'
    resource = 'integral_sale'
    
    @login_required
    def get(request):
        promotion_id = request.GET.get('id', None)
        if promotion_id:
            promotion = promotion_models.Promotion.objects.get(owner=request.manager, type=promotion_models.PROMOTION_TYPE_INTEGRAL_SALE, id=promotion_id)
            promotion_models.Promotion.fill_details(request.manager, [promotion], {
                'with_product': True,
                'with_concrete_promotion': True
            })
            promotion.products = sorted(promotion.products, key=lambda x: x.id)
            for product in promotion.products:
                product.models = product.models[1:]

            if promotion.member_grade_id:
                try:
                    promotion.member_grade_name = MemberGrade.objects.get(id=promotion.member_grade_id).name
                except:
                    promotion.member_grade_name = MemberGrade.get_default_grade(request.manager_profile.webapp_id).name


            jsons = [{
                "name": "product_models",
                # "content": promotion.products[0].models
                "content": [p.models for p in promotion.products]
            }]

            for rule in promotion.detail['rules']:
                if rule['member_grade_id'] > 0:
                    try:
                        rule['member_grade_name'] = MemberGrade.objects.get(id=rule['member_grade_id']).name
                    except:
                        pass
                else:
                    rule['member_grade_name'] = '全部等级'

            c = RequestContext(request, {
                'first_nav_name': export.MALL_PROMOTION_AND_APPS_FIRST_NAV,
                'second_navs': export.get_promotion_and_apps_second_navs(request),
                'second_nav_name': export.MALL_PROMOTION_SECOND_NAV,
                'third_nav_name': export.MALL_PROMOTION_INTEGRAL_SALE_NAV,
                'promotion': promotion,
                'jsons': jsons
            })

            return render_to_response('mall/editor/promotion/integral_sale_detail.html', c)
        else:
            member_grades = MemberGrade.get_all_grades_list(request.user_profile.webapp_id)
            c = RequestContext(request, {
                'member_grades': member_grades,
                'first_nav_name': export.MALL_PROMOTION_AND_APPS_FIRST_NAV,
                'second_navs': export.get_promotion_and_apps_second_navs(request),
                'second_nav_name': export.MALL_PROMOTION_SECOND_NAV,
                'third_nav_name': export.MALL_PROMOTION_INTEGRAL_SALE_NAV,
            })

            return render_to_response('mall/editor/promotion/create_integral_sale.html', c)

    @login_required
    def api_put(request):
        products = json.loads(request.POST.get('products', '[]'))
        product_ids = list(set([product['id'] for product in products]))
        # product_ids = string_ids2int_ids(product_ids)

        # 保存时校验商品
        save_success, error_product_ids = verification_multi_product_promotion_weizoom_mall(request.manager, product_ids, 'integral_sale')
        if not save_success:
            response = create_response(200)
            response.data = {
                'save_success': False,
                'error_product_ids': error_product_ids
            }
            return response.get_response()

        is_permanant_active = (request.POST.get('is_permanant_active', 'false') == 'true')
        integral_sale = promotion_models.IntegralSale.objects.create(
            owner = request.manager,
            type = promotion_models.INTEGRAL_SALE_TYPE_PARTIAL,
            discount = 0,
            discount_money = 0.0,
            integral_price = 0,
            is_permanant_active = is_permanant_active
        )

        #创建integral rule
        rules = json.loads(request.POST.get('rules'))
        for rule in rules:
            promotion_models.IntegralSaleRule.objects.create(
                owner = request.manager,
                integral_sale = integral_sale,
                member_grade_id = rule['member_grade_id'],
                discount = rule['discount'],
                discount_money = rule['discount_money']
            )

        #创建promotion
        now = datetime.today()
        start_date = datetime.strptime(request.POST.get('start_date', '2000-01-01 00:00'), '%Y-%m-%d %H:%M')
        end_date = datetime.strptime(request.POST.get('end_date', '2000-01-01 00:00'), '%Y-%m-%d %H:%M')
        # 当前实现了Promotion.update信号捕获更新缓存，因此数据插入时状态为活动未开始
        status = promotion_models.PROMOTION_STATUS_NOT_START
        promotion = promotion_models.Promotion.objects.create(
            owner = request.manager,
            type = promotion_models.PROMOTION_TYPE_INTEGRAL_SALE,
            name = request.POST.get('name', ''),
            status = status,
            promotion_title = request.POST.get('promotion_title', ''),
            member_grade_id = 0,
            start_date = datetime.strptime('1900-01-01', '%Y-%m-%d') if integral_sale.is_permanant_active else start_date,
            end_date = datetime.strptime('2999-01-01', '%Y-%m-%d') if integral_sale.is_permanant_active else end_date,
            detail_id = integral_sale.id
        )

        for product_id in product_ids:
            promotion_models.ProductHasPromotion.objects.create(
                product_id = product_id,
                promotion = promotion
            )

        if start_date <= now:
            promotion.status = promotion_models.PROMOTION_STATUS_STARTED
            promotion.save()

        if end_date <= now and not is_permanant_active:
            promotion.status = promotion_models.PROMOTION_STATUS_FINISHED
            promotion.save()

        response = create_response(200)
        response.data = {
            'save_success': True
        }
        return response.get_response()


class IntegralSaleList(resource.Resource):
    app = 'mall2'
    resource = 'integral_sales_list'

    @login_required
    def get(request):
        """获得限时抢购列表.
        """
        endDate = request.GET.get('endDate', '')
        if endDate:
            endDate +=' 00:00'
        integral_strategy = IntegralStrategySttings.objects.get(webapp_id=request.user_profile.webapp_id)
        c = RequestContext(request, {
            'first_nav_name': export.MALL_PROMOTION_AND_APPS_FIRST_NAV,
            'second_navs': export.get_promotion_and_apps_second_navs(request),
            'second_nav_name': export.MALL_PROMOTION_SECOND_NAV,
            'third_nav_name': export.MALL_PROMOTION_INTEGRAL_SALE_NAV,
            'is_order_integral_open': integral_strategy.use_ceiling > 0,
            'endDate': endDate,
            'promotion_status': request.GET.get('status', '-1')
        })

        return render_to_response('mall/editor/promotion/integral_sales.html', c)
