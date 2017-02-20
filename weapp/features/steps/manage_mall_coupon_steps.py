# -*- coding: utf-8 -*-

import json
from datetime import datetime, timedelta

from behave import given, then, when

from mall.models import Product
from mall.promotion.models import Promotion, Coupon, CouponRule
from test import bdd_util


@when(u'{user_name}添加优惠券规则')
def step_impl(context, user_name):
    __add_coupon_rule(context, user_name)


@given(u'{user_name}已添加了优惠券规则')
def step_impl(context, user_name):
    __add_coupon_rule(context, user_name)


@when(u"{user}设置优惠券规则列表查询条件")
def step_imple(context, user):
    query_param = json.loads(context.text)

    context.query_param = query_param

@then(u'{user_name}能获得优惠券规则列表')
def step_impl(context, user_name):
    url = '/mall2/api/promotion_list/?design_mode=0&version=1&type=coupon&count_per_page=10&page=1'
    if hasattr(context, 'query_param'):
        if context.query_param.get('name'):
            url += '&name=' + context.query_param['name']
        if context.query_param.get('coupon_id'):
            url += '&couponId='+ context.query_param['coupon_id']
        if context.query_param.get('coupon_code'):
            url += '&couponId='+ context.query_param['coupon_code']
        if context.query_param.get('coupon_promotion_type', None):
            if context.query_param['coupon_promotion_type'] == u'通用券':
                coupon_promotion_type = 1
            elif context.query_param['coupon_promotion_type'] == u'多商品券':
                coupon_promotion_type = 2
            elif context.query_param['coupon_promotion_type'] == u'全部':
                coupon_promotion_type = -1
            url += '&promotionType=all&couponPromotionType=%s' % coupon_promotion_type
        if context.query_param.get('start_date'):
            url += '&startDate='+ bdd_util.get_datetime_str(context.query_param['start_date'])[:16]
        if context.query_param.get('end_date'):
            url += '&endDate='+ bdd_util.get_datetime_str(context.query_param['end_date'])[:16]
        if context.query_param.get('promotion_status', u'全部') != u'全部':
            if context.query_param['promotion_status'] == u'未开始':
                status = 1
            elif context.query_param['promotion_status'] == u'进行中':
                status = 2
            elif context.query_param['promotion_status'] == u'已过期':
                context.client.get(url) #先获取一次数据，使status都更新到正常值
                status = 3
            elif context.query_param['promotion_status'] == u'已失效':
                status = 5
            url += '&promotionStatus=%s' % status

    response = context.client.get(url)
    coupon_rules = json.loads(response.content)['data']['items']

    actual = []
    for coupon_rule in coupon_rules:
        rule = {}
        rule["name"] = coupon_rule["name"]
        rule["money"] = coupon_rule["detail"]["money"]
        rule["remained_count"] = coupon_rule["detail"]["remained_count"]
        rule["limit_counts"] = coupon_rule["detail"]["limit_counts"] if coupon_rule["detail"]["limit_counts"] != -1 else "无限"
        if coupon_rule['status'] == '已结束':
            rule["remained_count"] = 0
        rule["use_count"] = coupon_rule["detail"]["use_count"]
        rule["start_date"] = coupon_rule["start_date"]
        rule["end_date"] = coupon_rule["end_date"]
        rule["get_person_count"] = coupon_rule["detail"]["get_person_count"]
        rule["get_number"] = coupon_rule["detail"]["get_count"]
        rule['status'] = coupon_rule['status']
        rule['note'] = coupon_rule["detail"]['note']

        if coupon_rule["detail"]["limit_product"]:
            rule["type"] = "多商品券"
            rule['special_product'] = u"查看专属商品"
        else:
            rule["type"] = "通用券"
            rule['special_product'] = u"全部"
        actual.append(rule)

    expected = json.loads(context.text)
    for item in expected:
        item["start_date"] = "{} 00:00:00".format(bdd_util.get_date_str(item["start_date"]))
        item["end_date"] = "{} 00:00:00".format(bdd_util.get_date_str(item["end_date"]))
        if 'status' in item and item['status'] == "已过期":
            item['status'] = "已结束"



    bdd_util.assert_list(expected, actual)


@when(u"{user_name}更新优惠券规则'{coupon_rule_name}'为")
def step_impl(context, user_name, coupon_rule_name):
    user_id = bdd_util.get_user_id_for(user_name)
    coupon_rule = CouponRule.objects.get(owner_id=user_id, name=coupon_rule_name, is_active=True)
    url = '/mall2/api/coupon_rule/'


    new_one = json.loads(context.text)
    name = new_one.get('name')
    # description = new_one['description']
    description = new_one.get('description')
    note = new_one.get('note')
    data = {
        "rule_id": coupon_rule.id,
    }
    if description:
        data['remark'] = description
    if note:
        data['note'] = note
    if name:
        data['name'] = name

    response = context.client.post(url, data)


@when(u"{user_name}删除优惠券'{coupon_rule_name}'")
def step_impl(context, user_name, coupon_rule_name):
    user_id = bdd_util.get_user_id_for(user_name)
    coupon_rule = CouponRule.objects.get(owner_id=user_id, name=coupon_rule_name, is_active=True)
    promotion = Promotion.objects.get(detail_id=coupon_rule.id)
    url = '/mall2/api/promotion/?_method=delete'

    response = context.client.post(url, {'ids[]': [promotion.id], 'type': 'coupon'})


# todo这是什么鬼
@when(u"{user_name}删除优惠券'{coupon_rule_name}'的码库")
def step_coupon_delete(context, user_name, coupon_rule_name):
    coupon_rule = CouponRule.objects.get(name=coupon_rule_name)
    # Coupon.objects.filter(Q(coupon_rule_id=coupon_rule.id) and
    # ~Q(status=0)
    #                       ).delete()

# 和@then(u'{user_name}能获得优惠券规则列表')重复
@then(u"{user_name}获得优惠券规则列表")
def step_impl(context, user_name):
    """

    e.g.:
        [{
            "coupon_rule": "过期优惠券规则",
            "money": "1.00",
            "create_date": "前天",
            "expire_date": "昨天",
            "status": "已结束"
        },{
            "coupon_rule": "优惠券规则3",
            "money": "10.00",
            "create_date": "前天",
            "expire_date": "后天",
            "status": "进行中"
        }]

    """
    url = '/mall2/api/promotion_list/'
    the_kwargs = {
        "type": "coupon",
    }
    response = context.client.get(url, the_kwargs)
    coupons = json.loads(response.content)['data']['items']

    for coupon in coupons:
        coupon['coupon_rule'] = coupon['detail']['name']
        coupon['create_date'] = coupon['start_date']
        coupon['expire_date'] = coupon['end_date']

        # if coupon['is_manual_generated']:
        # coupon['target'] = u'手工'
        # else:
        # 	coupon['target'] = coupon['member']['username_for_html']

        # coupon['consumer'] = coupon['consumer']['username_for_html']
        coupon['money'] = coupon['detail']["money"]

    # 处理expected中的参数
    today = datetime.today()
    today = today.replace(hour=0, minute=0, second=0, microsecond=0)

    tomorrow = today + timedelta(1)
    day_after_tomorrow = tomorrow + timedelta(1)
    yesterday = today - timedelta(1)
    day_before_yesterday = yesterday - timedelta(1)
    t_format = "%Y-%m-%d %H:%M:%S"
    today = today.strftime(t_format).decode('utf-8')
    tomorrow = tomorrow.strftime(t_format).decode('utf-8')
    day_after_tomorrow = day_after_tomorrow.strftime(t_format).decode('utf-8')
    yesterday = yesterday.strftime(t_format).decode('utf-8')
    day_before_yesterday = day_before_yesterday.strftime(t_format).decode('utf-8')
    name2date = {
        u'今天': today,
        u'明天': tomorrow,
        u'后天': day_after_tomorrow,
        u'昨天': yesterday,
        u'前天': day_before_yesterday
    }

    expected_coupons = json.loads(context.text)
    for expected_coupon in expected_coupons:
        if 'create_date' in expected_coupon:
            expected_coupon['create_date'] = name2date[expected_coupon['create_date']]
        if 'expire_date' in expected_coupon:
            expected_coupon['expire_date'] = name2date[expected_coupon['expire_date']]

    bdd_util.assert_list(expected_coupons, coupons)


@then(u"{user_name}能获得优惠券'{coupon_rule_name}'的码库")
def step_impl(context, user_name, coupon_rule_name):
    db_coupon_rule = CouponRule.objects.get(owner_id=context.webapp_owner_id, name=coupon_rule_name)
    url = '/mall2/api/coupon_list/?id=%d' % db_coupon_rule.id
    response = context.client.get(url)

    bdd_util.assert_api_call_success(response)

    actual = {}
    coupons = json.loads(response.content)['data']['items']
    for coupon in coupons:
        coupon['target'] = coupon['member']['username_for_html']
        coupon['consumer'] = coupon['consumer']['username_for_html']
        coupon['money'] = float(coupon['money'])
        actual[coupon['coupon_id']] = coupon

    expected_coupons = json.loads(context.text)
    bdd_util.assert_dict(expected_coupons, actual)


@when(u"{webapp_owner}失效优惠券'{coupon_rule_name}'")
def step_disable_coupon_rule(context, webapp_owner, coupon_rule_name):
    promotion = Promotion.objects.get(name=coupon_rule_name)
    args = {
        'ids[]': [promotion.id, ],
        'type': 'coupon'
    }
    url = '/mall2/api/promotion/'
    context.client.post(url, args)


@when(u"{webapp_owner_name}为优惠券'{coupon_rule_name}'添加库存")
def step_impl(context, webapp_owner_name, coupon_rule_name):
    infos = json.loads(context.text)
    coupon_rule = CouponRule.objects.get(owner_id=context.webapp_owner_id, name=coupon_rule_name)
    url = "/mall2/api/coupon/?rule_id=%s" % coupon_rule.id
    args = {
        'rule_id': coupon_rule.id,
        'count': infos['count']
    }
    response = context.client.post(url, args)
    response_data = json.loads(response.content)
    if response_data['code'] == 200:
        if "coupon_id_prefix" in infos:
            coupon_id_prefix = infos['coupon_id_prefix']
            coupon_count = len(Coupon.objects.filter(coupon_rule=coupon_rule))
            index = infos['count'] - 1
            for coupon in Coupon.objects.filter(coupon_rule=coupon_rule).order_by("-id")[:infos['count']]:
                coupon_id = "%s%d" % (coupon_id_prefix, coupon_count - index)
                Coupon.objects.filter(id=coupon.id).update(coupon_id=coupon_id)
                index = index - 1



@then(u"{user}获得优惠券规则'{rule_name}'")
def step_impl(context, user, rule_name):


    expected = json.loads(context.text)


    # expected["start_date"] = "{} 00:00:00".format(bdd_util.get_date_str(expected["start_date"]))
    # expected["end_date"] = "{} 00:00:00".format(bdd_util.get_date_str(expected["end_date"]))

    # todo
    del expected["start_date"]
    del expected["end_date"]

    promotion = Promotion.objects.get(name=rule_name)

    url = '/mall2/coupon_rule?id=%d' % promotion.id
    response = context.client.get(url)

    # bdd_util.assert_api_call_success(response)

    coupon_rule = response.context['coupon_rule']
    promotion = response.context['promotion']

    actual = {
        "name": promotion.name,
        "money": coupon_rule.money,
        "limit_counts": u'无限' if coupon_rule.limit_counts == -1 else coupon_rule.limit_counts,
        "using_limit": "满{}元可以使用".format(coupon_rule.valid_restrictions),
        "count": coupon_rule.count,
        # "cr_start_date":coupon_rule.get('start_date', u'今天'),
        # "start_date":"{} 00:00".format(bdd_util.get_date_str(cr_start_date)),
        # "cr_end_date": coupon_rule.get('end_date', u'1天后'),
        # "end_date ":"{} 00:00".format(bdd_util.get_date_str(cr_end_date))
        "description": coupon_rule.remark,
        "note": coupon_rule.note,
        "is_no_order_user": 'true' if coupon_rule.receive_rule == True else False,
    }

    actual['coupon_product'] = ','.join([p.name for p in promotion.products])
    actual['products_status'] = map(
        lambda x: {"name": x['name'], "status": x['status']} if x['status'] != u'在售' else  {"name": x['name'], "status": ""},
        [{"name": p.name, "status": p.status} for p in promotion.products])

    bdd_util.assert_dict(expected, actual)


@then(u'{user}能获得优惠券状态列表')
def step_impl(context, user):
    url = "/mall2/api/promotion_list/?type=coupon"
    response = context.client.get(url)
    bdd_util.assert_api_call_success(response)

    actual = json.loads(response.content)['data']['items']
    for c in actual:
        if c['status'] == u'已结束':
            c['status'] = u'已过期'

    expected = json.loads(context.text)

    bdd_util.assert_list(expected, actual)

#######################################

def __add_coupon_rule(context, webapp_owner_name):
    coupon_rules = json.loads(context.text)
    if type(coupon_rules) == dict:
        coupon_rules = [coupon_rules]

    webapp_owner_id = bdd_util.get_user_id_for(webapp_owner_name)
    for coupon_rule in coupon_rules:
        # __add_coupon_rule(context, coupon_rule, user_name)
        cr_name = coupon_rule['name']
        cr_money = coupon_rule['money']
        cr_count = coupon_rule.get('count', 4)
        cr_limit_counts = coupon_rule.get('limit_counts', -1)
        cr_start_date = coupon_rule.get('start_date', u'今天')
        start_date = "{} 00:00".format(bdd_util.get_date_str(cr_start_date))
        cr_end_date = coupon_rule.get('end_date', u'1天后')
        end_date = "{} 00:00".format(bdd_util.get_date_str(cr_end_date))
        remark = coupon_rule.get('description', '')  #使用说明
        note = coupon_rule.get('note', '')  #备注
        post_data = {
            'name': cr_name,
            'money': cr_money,
            'count': cr_count,
            'limit_counts': -1 if cr_limit_counts == u'无限' else cr_limit_counts,
            'start_date': start_date,
            'end_date': end_date,
            'remark': remark,
            'note': note
        }
        if not "using_limit" in coupon_rule:
            post_data['is_valid_restrictions'] = '0'
        else:
            post_data['is_valid_restrictions'] = '1'
            using_limit = coupon_rule['using_limit']
            end = using_limit.find(u"元")
            if end == -1:
                post_data['valid_restrictions'] = -1
            else:
                post_data['valid_restrictions'] = int(using_limit[1:end])
        if "coupon_product" in coupon_rule:
            post_data['limit_product'] = 1

            product_ids = []
            for product_name in coupon_rule['coupon_product'].split(','):
                product_ids.append(Product.objects.get(

                    name=product_name).id)

            post_data['product_ids'] = ','.join(map(lambda x: str(x), product_ids))

        if coupon_rule.get('is_no_order_user', 'false') == 'true':
            post_data['receive_rule'] = 1
        url = '/mall2/api/coupon_rule/'
        response = context.client.post(url, post_data)
        context.tc.assertEquals(200, response.status_code)
        if json.loads(response.content)['data']['save_success'] and "coupon_id_prefix" in coupon_rule:
            latest_coupon_rule = CouponRule.objects.all().order_by('-id')[0]
            index = 1
            coupon_id_prefix = coupon_rule['coupon_id_prefix']
            for coupon in Coupon.objects.filter(coupon_rule=latest_coupon_rule):
                coupon_id = "%s%d" % (coupon_id_prefix, index)
                Coupon.objects.filter(id=coupon.id).update(coupon_id=coupon_id)
                index += 1

        context.response = response


@then(u"{user}获得优惠券规则添加失败提示'{info}'")
def step_impl(context, user, info):
    save_success = json.loads(context.response.content)['data']['save_success']
    assert not save_success

@then(u"{user}查看优惠券'{coupon_rule_name}'专属商品")
def step_impl(context,user,coupon_rule_name):
    promotion = Promotion.objects.get(name=coupon_rule_name)

    url = '/mall2/api/coupon_rule_products?id=%d' % promotion.id
    response = context.client.get(url)
    actual = json.loads(response.content)['data']['items']

    expected = json.loads(context.text)

    bdd_util.assert_list(expected, actual)