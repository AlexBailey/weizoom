# -*- coding: utf-8 -*-
# __author__='justing'
import json
import time

from behave import *

from test import bdd_util
from features.testenv.model_factory import *

from django.test.client import Client

def adict_addNews(addNews):
    adict = {}
    adict['id'] = -99 #
    adict['type'] = 'news'
    adict['display_index'] = 1
    adict['title'] = addNews['title']
    adict['summary'] = addNews.get('summary', '')
    adict['text'] = addNews.get('content','')
    adict['pic_url'] = addNews['cover'][0]['url']
    adict['is_show_cover_pic'] = addNews['cover_in_the_text']
    adict['url'] = addNews.get('jump_url','')
    if adict['url'].strip().startswith('www.'):
        adict['url'] = 'http://' + adict['url'].strip()
    if adict['url']:
        adict['link_target'] = '{"workspace":"custom","workspace_name":"外部链接",'\
        '"data_category":"外部链接","data_item_name":"外部链接","data_path":"%s",'\
        '"data":"%s"}' %(adict['url'], adict['url'])
    else:
        adict['link_target'] = ''
    return adict

@when(u"{user}已添加多图文")
def step_impl(context, user):
    addNewses = json.loads(context.text)
    data = []
    for addNews in addNewses:
        adict = adict_addNews(addNews)
        data.append(adict)
    url = '/new_weixin/api/multi_news/?_method=put'
    response = context.client.post(url, {'data': json.dumps(data)})
    time.sleep(1)
@Then(u"{user}能获取多图文'{news_title}'")
def step_impl(context, user, news_title):
    materials_url = '/new_weixin/api/materials/'
    response = context.client.get(bdd_util.nginx(materials_url))
    newses_info = json.loads(response.content)['data']['items']

    for news_info in newses_info:
        if news_info['type'] == 'multi':
            if news_info['newses'][0]['title'] == news_title:
                multi_id = news_info['id']
                break
    multi_url = '/new_weixin/news_preview/?id=%s' %multi_id
    response = context.client.get(bdd_util.nginx(multi_url))
    actual_datas = json.loads(response.context['newses'])

    for actual_data in actual_datas:
        actual_data['content'] = actual_data.get('text','')
        actual_data['cover'] = [{'url':actual_data.get('pic_url','')}]
        actual_data['cover_in_the_text'] = actual_data.get('is_show_cover_pic')
        actual_data['jump_url'] = actual_data.get('url', '')
    expected_datas = json.loads(context.text)
    for expected_data in expected_datas:
        expected_data['cover_in_the_text'] = True if (expected_data.get('cover_in_the_text', True) in ('true', 'yes', 'True', 'Yes', True)) else False
        if expected_data.get('jump_url',''):
            expected_data['jump_url'] = 'http://' + expected_data['jump_url'].strip()
    bdd_util.assert_list(expected_datas, actual_datas)
