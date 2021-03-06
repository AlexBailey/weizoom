# -*- coding: utf-8 -*-
# __author__='justing'
import json
import time

from behave import *

from test import bdd_util
from features.testenv.model_factory import *

from django.test.client import Client
from add_multy_text_picture_steps import adict_addNews

@when(u"{user}已添加单图文")
def step_impl(context, user):
    addNewses = json.loads(context.text)
    for addNews in addNewses:
        data = []
        data.append(adict_addNews(addNews))
        url = '/new_weixin/api/single_news/?_method=put'
        response = context.client.post(url, {'data': json.dumps(data)})
        time.sleep(1)
@Then(u"{user}能获取图文'{news_title}'")
def step_impl(context, user, news_title):
    materials_url = '/new_weixin/api/materials/'
    response = context.client.get(bdd_util.nginx(materials_url))
    newses_info = json.loads(response.content)['data']['items']
    for news_info in newses_info:
        if news_info['type'] == 'single':
            if news_info['newses'][0]['title'] == news_title:
                single_id = news_info['id']
                single_url = '/new_weixin/news_preview/?id=%s' %single_id
                break
    response = context.client.get(bdd_util.nginx(single_url))
    actual_data = json.loads(response.context['newses'])[0]
    actual_data['content'] = actual_data.get('text','')
    actual_data['cover'] = [{'url':actual_data.get('pic_url','')}]
    actual_data['cover_in_the_text'] = actual_data.get('is_show_cover_pic')
    actual_data['jump_url'] = actual_data.get('url', '')
    expected_data = json.loads(context.text)
    expected_data['cover_in_the_text'] = True if (expected_data.get('cover_in_the_text', True) in ('true', 'yes', 'True', 'Yes', True)) else False
    if expected_data.get('jump_url',''):
        expected_data['jump_url'] = 'http://' + expected_data['jump_url'].strip()
    bdd_util.assert_dict(expected_data, actual_data)


@Then(u"{user}能获取图文管理列表")
def step_impl(context, user):
    if not hasattr(context,'url'):
        context.url = '/new_weixin/api/materials/?sort_attr=-created_at'
    response = context.client.get(bdd_util.nginx(context.url))
    newses_info = json.loads(response.content)['data']['items']
    actual_data = []
    for news_info in newses_info:
        actual_data.append({'title':news_info['newses'][0]['title']})
    expected_data = json.loads(context.text)
    bdd_util.assert_list(expected_data, actual_data)



