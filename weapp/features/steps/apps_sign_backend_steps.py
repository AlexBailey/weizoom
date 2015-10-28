#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'mark24'

from behave import *
from test import bdd_util

from features.testenv.model_factory import *
import steps_db_util
#from mall import module_api as mall_api
from mall.promotion import models as  promotion_models
from modules.member import module_api as member_api
from utils import url_helper
import datetime as dt
from mall.promotion.models import CouponRule
from weixin.message.material import models as material_models
import json

def __get_coupon_rule_id(coupon_rule_name):
    coupon_rule = promotion_models.CouponRule.objects.get(name=coupon_rule_name)
    return coupon_rule.id



@when(u'{user}添加签到活动"{sign_name}",并且保存')
def step_impl(context,user,sign_name):
    sign_json = json.loads(context.text)

    status = sign_json['status']
    name = sign_json['name']
    share = {
        "img":sign_json["share_pic"],
        "desc":sign_json["share_describe"]
    }
    reply = {}
    keyword ={}
    keyword_reply = sign_json["keyword_reply"]
    for item in keyword_reply:
        rule = ""
        if item['rule']=="精确":
            rule = "accurate"
        elif item['rule']=="模糊":
            rule = "blur"
        keyword[item["key_word"]] = rule
    reply ={
        "keyword":keyword,
        "content":sign_json["share_describe"]
    }


    prize_settings = {}
    sign_settings = sign_json["sign_settings"]
    for item in sign_settings:
        prize_settings[item["sign_in"]]={
            "integral":item["integral"],
            "coupon":{
                "count":item["prize_counts"],
                "id":__get_coupon_rule_id(item["send_coupon"]),
                "name":item["send_coupon"]
            }
        }

    #模拟登陆Sign页面
    sign_page_response = context.client.get("/apps/sign/sign/").context

    sign  = sign_page_response['sign']
    is_create_new_data = sign_page_response['is_create_new_data']
    project_id = sign_page_response['project_id']
    webapp_owner_id = sign_page_response['webapp_owner_id']
    keywords = sign_page_response['keywords']
    
    activityId = ""
    if sign and sign.id:
        activityId = sign.id

    params = {
        "related_page_id":project_id,
        "status":status,
        
        "name":name,
        "prize_settings":json.dumps(prize_settings),
        "reply":json.dumps(reply),
        "share":json.dumps(share)
     }

    loadPages_response = context.client.get("/apps/api/dynamic_pages/get/",{'project_id': project_id})

    # if is_create_new_data:
    #     response = context.client.post("/apps/sign/api/sign/?_method=put",params)
    # else:
    #     params['id'] = activityId
    #     params['signId'] = activityId
    #     response = context.client.post("/apps/sign/api/sign/?_method=post",params)

    # bdd_util.assert_api_call_success(response)
    bdd_util.assert_api_call_success(loadPages_response)

    print '+++++++++++++++++++++++++++++++++++++++==========START++++'
    print loadPages_response.context
    print '+++++++++++++++++++++++++++XXXXX++++++++++++++END+++++++++'






@then(u'{user}获得签到活动"{sign_name}"')
def step_impl(context,user,sign_name):
    #:88
    pass


@when(u'选择优惠券')
def step_impl(context):
    #331
    pass

@when(u'{user1}进入{user2}签到后台配置页面')
def step_impl(context,user1,user2):
    #341
    pass

@then(u'{user}获得优惠券列表,没有"{coupon}"')
def step_impl(context,user,coupon):
    #334
    pass

@when(u'{user}开启签到活动"{sign_name}"')
def step_impl(context,user,sign_name):
    #338
    pass


@then(u'{user}能获得签到活动{sign_name}的状态为{sign_tag}')
def step_impl(context,user,sign_name,sign_tag):
    #348
    pass
