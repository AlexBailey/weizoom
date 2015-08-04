#!/usr/bin/env python
# -*- coding: utf-8 -*-
from behave import when, then, given
import json
from test import bdd_util

@when(u"{webapp_owner}已完成对商品的评价信息审核")
def step_webapp_owner_verified_review(context, webapp_owner):
    """
     [{
        "member": "tom",
        "status": "-1",  -> ('-1', '已屏蔽'),  ('0', '待审核'),  ('1', '已通过'),  ('2', '通过并置顶')
        "product_name": "商品1",
        "order_no": "3"
    }, {
        "member": "bill",
        "status": "1",
        "product_name": "商品1",
        "order_no": "1"
    }]


    """
    url = '/mall2/api/product_review/?design_mode=0&version=1'
    context_dict = json.loads(context.text)
    for i in context_dict:
        product_name = i.get('product_name')
        order_code = i.get('order_no')
        product_review = bdd_util.get_product_review(order_code, product_name)
        args = {
            "product_review_id": product_review.id,
            "status": i.get("status")
        }
        context.client.post(url, args)