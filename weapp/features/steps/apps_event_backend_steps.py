#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'mark24'

from behave import *
from test import bdd_util
from collections import OrderedDict

from features.testenv.model_factory import *
import steps_db_util
from mall.promotion import models as  promotion_models
from modules.member import module_api as member_api
from utils import url_helper
import datetime as dt
from mall.promotion.models import CouponRule
from weixin.message.material import models as material_models
from apps.customerized_apps.event import models as event_models
import termite.pagestore as pagestore_manager
import json

def __debug_print(content,type_tag=True):
	"""
	debug工具函数
	"""
	if content:
		print('++++++++++++++++++  START ++++++++++++++++++++++++++++++++++++')
		if type_tag:
			print("====== Type ======")
			print(type(content))
			print("===================")
		print(content)
		print('++++++++++++++++++++  END  ++++++++++++++++++++++++++++++++++')
	else:
		pass

def __itemName2item(itemName):
	itemName_dic={u"姓名":'name',u"手机":'phone',u"邮箱":'email',u"QQ号":'qq',u"QQ":'qq',u"qq":'qq',u"职位":"job",u"住址":"addr"}
	if itemName:
		return itemName_dic[itemName]
	else:
		return ""

def __bool2Bool(bo):
	"""
	JS字符串布尔值转化为Python布尔值
	"""
	bool_dic = {'true':True,'false':False,'True':True,'False':False}
	if bo:
		result = bool_dic[bo]
	else:
		result = None
	return result

# def __name2Bool(name):
# 	"""
# 	"是"--> true
# 	"否"--> false
# 	"""
# 	name_dic = {u'是':"true",u'否':"false"}
# 	if name:
# 		return name_dic[name]
# 	else:
# 		return None

def __date2time(date_str):
	"""
	字符串 今天/明天……
	转化为字符串 "%Y-%m-%d %H:%M"
	"""
	cr_date = date_str
	p_time = "{} 00:00".format(bdd_util.get_date_str(cr_date))
	return p_time

def __datetime2str(dt_time):
	"""
	datetime型数据，转为字符串型，日期
	转化为字符串 "%Y-%m-%d %H:%M"
	"""
	dt_time = dt.datetime.strftime(dt_time, "%Y-%m-%d %H:%M")
	return dt_time

# def __limit2name(limit):
# 	"""
# 	传入积分规则，返回名字
# 	"""
# 	limit_dic={
# 	"once_per_user":u"一人一次",
# 	"once_per_day":u"一天一次",
# 	"twice_per_day":u"一天两次",
# 	"no_limit":u"不限"
# 	}
# 	if limit:
# 		return limit_dic[limit]
# 	else:
# 		return ""

# def __name2limit(name):
# 	"""
# 	传入积分名字，返回积分规则
# 	"""
# 	name_dic={
# 		u"一人一次":"once_per_user",
# 		u"一天一次":"once_per_day",
# 		u"一天两次":"twice_per_day",
# 		u"不限":"no_limit"
# 	}
# 	if name:
# 		return name_dic[name]
# 	else:
# 		return ""

# def __name2type(name):
# 	type_dic = {
# 		u"全部":"-1",
# 		u"积分":"integral",
# 		u"优惠券":"coupon",
# 		u"实物":"entity",
# 		u"未中奖":"no_prize"
# 	}
# 	if name:
# 		return type_dic[name]
# 	else:
# 		return ""

# def __delivery2Bool(name):
# 	d_dic ={
# 		u"所有用户":"false",
# 		u'仅限未中奖用户':"true"
# 	}

# 	if name:
# 		return d_dic[name]
# 	else:
# 		return ""

# def __get_coupon_json(coupon_rule_name):
# 	"""
# 	获取优惠券json
# 	"""
# 	coupon_rule = promotion_models.CouponRule.objects.get(name=coupon_rule_name)
# 	coupon ={
# 		"id":coupon_rule.id,
# 		"count":coupon_rule.count,
# 		"name":coupon_rule.name
# 	}
# 	return coupon

def __get_coupon_rule_id(coupon_rule_name):
	"""
	获取优惠券id
	"""
	coupon_rule = promotion_models.CouponRule.objects.get(name=coupon_rule_name)
	return coupon_rule.id

def __event_name2id(name):
	"""
	给活动报名项目的名字，返回id元祖
	返回（related_page_id,event_event中id）
	"""
	obj = event_models.event.objects.get(name=name)
	return (obj.related_page_id,obj.id)

def __status2name(status_num):
	"""
	活动报名：状态值 转 文字
	"""
	status2name_dic = {-1:u"所有活动",0:u"未开始",1:u"进行中",2:u"已结束"}
	return status2name_dic[status_num]

def __name2status(name):
	"""
	活动报名： 文字 转 状态值
	"""
	if name:
		name2status_dic = {u"所有活动":-1,u"未开始":0,u"进行中":1,u"已结束":2}
		return name2status_dic[name]
	else:
		return -1

def __name2prize_type(name):
	name2prize_type_dic = {u"所有奖品":"all",u"优惠券":"coupon",u"积分":"integral"}

	if name:
		return name2prize_type_dic[name]
	else:
		return "all"

def __prize_type2name(prize_type):
	prize_type2name_dic = {"all":u"所有奖品","coupon":u"优惠券","integral":u"积分"}
	if prize_type:
		return prize_type2name_dic[prize_type]
	else:
		return u"所有奖品"

# def __name2coupon_status(name):
# 	"""
# 	活动报名： 文字 转 优惠券领取状态值
# 	"""
# 	if name:
# 		name2status_dic = {u"全部":-1,u"未领取":0,u"已领取":1}
# 		return name2status_dic[name]
# 	else:
# 		return -1


def __get_actions(status):
	"""
	根据输入活动报名状态
	返回对于操作列表
	"""
	actions_list = [u"链接",u"预览",u"查看结果"]
	if status == u"进行中":
		actions_list.insert(0,u"关闭")
	elif status=="已结束":
		actions_list.insert(0,u"删除")
	return actions_list

def name2permission(name):
	name_dic={u"必须关注才可参与":"member",u"无需关注即可参与":"no_member"}
	if name:
		return name_dic[name]
	else:
		return None

def __get_eventPageJson(args):
	"""
	传入参数，获取模板
	"""
	title = args["title"]
	subtitle = args["subtitle"]
	description = args["description"]
	start_time = args["start_time"]
	end_time = args["end_time"]
	valid_time = args["valid_time"]
	permission = name2permission(args["permission"])
	prize = args["prize"]
	items_select = args["items_select"]
	items_add = args["items_add"]

	#处理自带选项
	modules={}
	for expect_item in items_select:
		item_name = __itemName2item(expect_item['item_name'])
		is_selected = __bool2Bool(expect_item['is_selected'])
		modules[item_name]={"select":is_selected}

	#处理自定义添加
	length = len(items_add)
	items = [6+x for x in range(length)] #item列表
	components = [] #组件列表

	for index,expect_additem in enumerate(items_add):
		item_id = 6+index
		item_name = expect_additem['item_name']
		is_required = expect_additem['is_required']

		textitem_tmp ={
				"type": "appkit.textitem",
				"cid": item_id,
				"pid": 3,
				"auto_select": False,
				"selectable": "no",
				"force_display_in_property_view": "no",
				"has_global_content": "no",
				"need_server_process_component_data": "no",
				"is_new_created": True,
				"property_view_title": "",
				"model": {
					"id": "",
					"class": "",
					"name": "",
					"index": item_id,
					"datasource": {
						"type": "api",
						"api_name": ""
					},
					"title": item_name,
					"is_mandatory": is_required
				},
				"components": []
			}
		components.append(textitem_tmp)

	#主模板
	__page_temple = {
		"type": "appkit.page",
		"cid": 1,
		"pid": "null",
		"auto_select": False,
		"selectable": "yes",
		"force_display_in_property_view": "no",
		"has_global_content": "no",
		"need_server_process_component_data": "no",
		"is_new_created": True,
		"property_view_title": "背景",
		"model": {
			"id": "",
			"class": "",
			"name": "",
			"index": 1,
			"datasource": {
				"type": "api",
				"api_name": ""
			},
			"content_padding": "15px",
			"title": "index",
			"event:onload": "",
			"uploadHeight": "568",
			"uploadWidth": "320",
			"site_title": "活动报名",
			"background": ""
		},
		"components": [
			{
				"type": "appkit.surveydescription",
				"cid": 2,
				"pid": 1,
				"auto_select": False,
				"selectable": "yes",
				"force_display_in_property_view": "no",
				"has_global_content": "no",
				"need_server_process_component_data": "no",
				"property_view_title": "调研简介",
				"model": {
					"id": "",
					"class": "",
					"name": "",
					"index": 2,
					"datasource": {
						"type": "api",
						"api_name": ""
					},
					"title": title,
					"subtitle": subtitle,
					"description": "<p>%s</p>"%description,
					"start_time": start_time,
					"end_time": end_time,
					"valid_time": valid_time,
					"permission": permission,
					"prize": prize
				},
				"components": components
			},
			{
				"type": "appkit.textlist",
				"cid": 3,
				"pid": 1,
				"auto_select": False,
				"selectable": "yes",
				"force_display_in_property_view": "no",
				"has_global_content": "no",
				"need_server_process_component_data": "no",
				"property_view_title": "",
				"model": {
					"id": "",
					"class": "",
					"name": "",
					"index": 4,
					"datasource": {
						"type": "api",
						"api_name": ""
					},
					"title": "",
					"modules": modules,

					"items": items,
					"is_mandatory": "true"
				},
				"components":components
			},
			{
				"type": "appkit.submitbutton",
				"cid": 4,
				"pid": 1,
				"auto_select": False,
				"selectable": "no",
				"force_display_in_property_view": "no",
				"has_global_content": "no",
				"need_server_process_component_data": "no",
				"property_view_title": "",
				"model": {
					"id": "",
					"class": "",
					"name": "",
					"index": 99999,
					"datasource": {
						"type": "api",
						"api_name": ""
					},
					"text": "我要报名"
				},
				"components": []
			},
			{
				"type": "appkit.componentadder",
				"cid": 5,
				"pid": 1,
				"auto_select": False,
				"selectable": "yes",
				"force_display_in_property_view": "no",
				"has_global_content": "no",
				"need_server_process_component_data": "no",
				"property_view_title": "添加模块",
				"model": {
					"id": "",
					"class": "",
					"name": "",
					"index": 3,
					"datasource": {
						"type": "api",
						"api_name": ""
					},
					"components": ""
				},
				"components": []
			}
		]
	}
	return json.dumps(__page_temple)

def __prize_settings_process(prize_type,integral,coupon):
	"""
	处理prize_settings

	Tag为page，返回page的prize字典
	Tage为event,返回event_event的prize字典
	"""
	prize = {}

	if prize_type:
		if prize_type == "无奖励":
			prize = {"type":"no_prize","data":None}
		elif prize_type=="积分":
			prize = {"type":"integral","data":integral}
		elif prize_type == "优惠券":
			coupon_name = coupon
			coupon_id = __get_coupon_rule_id(coupon_name)
			prize = {"type":"coupon",
					 "data":{
						"id":coupon_id,
						"name":coupon_name
					 }
					}
		else:
			pass
	return prize


def __Create_Event(context,text,user):
	"""
	模拟用户登录页面
	创建活动报名项目
	写入mongo表：
		1.event_event表
		2.page表
	"""

	design_mode = 0
	version = 1
	text = text

	title = text.get("title","")
	subtitle = text.get("subtitle","")
	description = text.get("content","")

	cr_start_date = text.get('start_date', u'今天')
	start_date = bdd_util.get_date_str(cr_start_date)
	start_time = "{} 00:00".format(bdd_util.get_date_str(cr_start_date))

	cr_end_date = text.get('end_date', u'1天后')
	end_date = bdd_util.get_date_str(cr_end_date)
	end_time = "{} 00:00".format(bdd_util.get_date_str(cr_end_date))

	valid_time = "%s~%s"%(start_time,end_time)

	permission = text.get("permission")

	prize_type = text.get("prize_type","")
	integral = text.get("integral","")
	coupon = text.get("coupon","")
	prize = __prize_settings_process(prize_type,integral,coupon)

	items_select = text.get("items_select","")
	items_add = text.get("items_add","")

	page_args = {
		"title":title,
		"subtitle":subtitle,
		"description":description,
		"start_time":start_time,
		"end_time":end_time,
		"valid_time":valid_time,
		"permission":permission,
		"prize":prize,
		"items_select":items_select,
		"items_add":items_add
	}

	#step1：登录页面，获得分配的project_id
	get_event_response = context.client.get("/apps/event/event/")
	event_args_response = get_event_response.context
	project_id = event_args_response['project_id']#(str){new_app:event:0}

	#step2: 编辑页面获得右边的page_json
	dynamic_url = "/apps/api/dynamic_pages/get/?design_mode={}&project_id={}&version={}".format(design_mode,project_id,version)
	dynamic_response = context.client.get(dynamic_url)
	dynamic_data = dynamic_response.context#resp.context=> data ; resp.content => Http Text

	#step3:发送Page
	page_json = __get_eventPageJson(page_args)

	termite_post_args = {
		"field":"page_content",
		"id":project_id,
		"page_id":"1",
		"page_json": page_json
	}
	termite_url = "/termite2/api/project/?design_mode={}&project_id={}&version={}".format(design_mode,project_id,version)
	post_termite_response = context.client.post(termite_url,termite_post_args)
	related_page_id = json.loads(post_termite_response.content).get("data",{})['project_id']

	#step4:发送event_args
	post_event_args = {
		"name":title,
		"start_time":start_time,
		"end_time":end_time,
		"related_page_id":related_page_id
	}
	event_url ="/apps/event/api/event/?design_mode={}&project_id={}&version={}&_method=put".format(design_mode,project_id,version)
	post_event_response = context.client.post(event_url,post_event_args)

	#跳转,更新状态位
	design_mode = 0
	count_per_page = 1000
	version = 1
	page = 1
	enable_paginate = 1

	rec_event_url ="/apps/event/api/events/?design_mode={}&version={}&count_per_page={}&page={}&enable_paginate={}".format(design_mode,version,count_per_page,page,enable_paginate)
	rec_event_response = context.client.get(rec_event_url)



def __Update_Event(context,text,page_id,event_id):
	"""
	模拟用户登录页面
	编辑活动报名项目
	写入mongo表：
		1.event_event表
		2.page表
	"""

	design_mode=0
	version=1
	project_id = "new_app:event:"+page_id

	title = text.get("title","")
	subtitle = text.get("subtitle","")
	description = text.get("content","")

	cr_start_date = text.get('start_date', u'今天')
	start_date = bdd_util.get_date_str(cr_start_date)
	start_time = "{} 00:00".format(bdd_util.get_date_str(cr_start_date))

	cr_end_date = text.get('end_date', u'1天后')
	end_date = bdd_util.get_date_str(cr_end_date)
	end_time = "{} 00:00".format(bdd_util.get_date_str(cr_end_date))

	valid_time = "%s~%s"%(start_time,end_time)

	permission = text.get("permission")

	prize_type = text.get("prize_type","")
	integral = text.get("integral","")
	coupon = text.get("coupon","")
	prize = __prize_settings_process(prize_type,integral,coupon)

	items_select = text.get("items_select","")
	items_add = text.get("items_add","")

	page_args = {
		"title":title,
		"subtitle":subtitle,
		"description":description,
		"start_time":start_time,
		"end_time":end_time,
		"valid_time":valid_time,
		"permission":permission,
		"prize":prize,
		"items_select":items_select,
		"items_add":items_add
	}

	page_json = __get_eventPageJson(page_args)

	update_page_args = {
		"field":"page_content",
		"id":project_id,
		"page_id":"1",
		"page_json": page_json
	}

	update_event_args = {
		"name":title,
		"start_time":start_time,
		"end_time":end_time,
		"id":event_id
	}
	#page 更新Page
	update_page_url = "/termite2/api/project/?design_mode={}&project_id={}&version={}".format(design_mode,project_id,version)
	update_page_response = context.client.post(update_page_url,update_page_args)

	#step4:更新event
	update_event_url ="/apps/event/api/event/?design_mode={}&project_id={}&version={}".format(design_mode,project_id,version)
	update_event_response = context.client.post(update_event_url,update_event_args)

	#跳转,更新状态位
	design_mode = 0
	count_per_page = 1000
	version = 1
	page = 1
	enable_paginate = 1

	rec_event_url ="/apps/event/api/events/?design_mode={}&version={}&count_per_page={}&page={}&enable_paginate={}".format(design_mode,version,count_per_page,page,enable_paginate)
	rec_event_response = context.client.get(rec_event_url)

def __Delete_Event(context,event_id):
	"""
	删除活动报名
	写入mongo表：
		1.event_event表

	注释：page表在原后台，没有被删除a
	"""
	design_mode = 0
	version = 1
	del_event_url = "/apps/event/api/event/?design_mode={}&version={}&_method=delete".format(design_mode,version)
	del_args ={
		"id":event_id
	}
	del_event_response = context.client.post(del_event_url,del_args)
	return del_event_response

def __Stop_Event(context,event_id):
	"""
	关闭活动报名
	"""

	design_mode = 0
	version = 1
	stop_event_url = "/apps/event/api/event_status/?design_mode={}&version={}".format(design_mode,version)
	stop_args ={
		"id":event_id,
		"target":'stoped'
	}
	stop_event_response = context.client.post(stop_event_url,stop_args)
	return stop_event_response

def __Search_Event(context,search_dic):
	"""
	搜索活动报名

	输入搜索字典
	返回数据列表
	"""

	design_mode = 0
	version = 1
	page = 1
	enable_paginate = 1
	count_per_page = 10

	#分页情况，更新分页参数
	if hasattr(context,"paging"):
		paging_dic = context.paging
		count_per_page = paging_dic['count_per_page']
		page = paging_dic['page_num']

	name = search_dic["name"]
	start_time = search_dic["start_time"]
	end_time = search_dic["end_time"]
	status = search_dic["status"]
	prize_type = search_dic['prize_type']

	search_url = "/apps/event/api/events/?design_mode={}&version={}&name={}&status={}&prize_type={}&start_time={}&end_time={}&count_per_page={}&page={}&enable_paginate={}".format(
			design_mode,
			version,
			name,
			status,
			prize_type,
			start_time,
			end_time,
			count_per_page,
			page,
			enable_paginate)

	search_response = context.client.get(search_url)
	bdd_util.assert_api_call_success(search_response)
	return search_response

def __Search_Event_Result(context,search_dic):
	"""
	搜索,活动报名参与结果

	输入搜索字典
	返回数据列表
	"""

	design_mode = 0
	version = 1
	page = 1
	enable_paginate = 1
	count_per_page = 10

	if hasattr(context,"enable_paginate"):
		enable_paginate = context.enable_paginate
	else:
		enable_paginate = 1
	if hasattr(context,"count_per_page"):
		count_per_page = context.count_per_page
	else:
		count_per_page = 10

	id = search_dic["id"]
	participant_name = search_dic["participant_name"]
	start_time = search_dic["start_time"]
	end_time = search_dic["end_time"]

	search_url = "/apps/event/api/event_participances/?design_mode={}&version={}&id={}&participant_name={}&start_time={}&end_time={}&count_per_page={}&page={}&enable_paginate={}".format(
			design_mode,
			version,
			id,
			participant_name,
			start_time,
			end_time,
			count_per_page,
			page,
			enable_paginate)

	search_response = context.client.get(search_url)
	bdd_util.assert_api_call_success(search_response)
	return search_response

@when(u'{user}新建活动报名')
def step_impl(context,user):
	text_list = json.loads(context.text)
	for text in text_list:
		__Create_Event(context,text,user)

@then(u'{user}获得活动报名列表')
def step_impl(context,user):
	design_mode = 0
	version = 1
	page = 1
	enable_paginate = 1
	if hasattr(context,"count_per_page"):
		count_per_page = context.count_per_page
	else:
		count_per_page = 10

	actual_list = []
	expected = json.loads(context.text)

# 	#搜索查看结果
	if hasattr(context,"search_event"):
		rec_search_list = context.search_event
		for item in rec_search_list:
			tmp = {
				"name":item['name'],
				"status":item['status'],
				"prize_type":item['prize_type'],
				"start_time":item['start_time'],
				"end_time":item['end_time'],
				"participant_count":item['participant_count'],
			}
			tmp["actions"] = __get_actions(item['status'])
			actual_list.append(tmp)

		for expect in expected:
			if 'start_date' in expect:
				expect['start_time'] = __date2time(expect['start_date'])
				del expect['start_date']
			if 'end_date' in expect:
				expect['end_time'] = __date2time(expect['end_date'])
				del expect['end_date']
		print("expected: {}".format(expected))
		print("actual_list:{}".format(actual_list))

		bdd_util.assert_list(expected,actual_list)#assert_list(小集合，大集合)
	#其他查看结果
	else:
		#分页情况，更新分页参数
		if hasattr(context,"paging"):
			paging_dic = context.paging
			count_per_page = paging_dic['count_per_page']
			page = paging_dic['page_num']

		for expect in expected:
			if 'start_date' in expect:
				expect['start_time'] = __date2time(expect['start_date'])
				del expect['start_date']
			if 'end_date' in expect:
				expect['end_time'] = __date2time(expect['end_date'])
				del expect['end_date']


		print("expected: {}".format(expected))

		rec_event_url ="/apps/event/api/events/?design_mode={}&version={}&count_per_page={}&page={}&enable_paginate={}".format(design_mode,version,count_per_page,page,enable_paginate)
		rec_event_response = context.client.get(rec_event_url)
		rec_event_list = json.loads(rec_event_response.content)['data']['items']#[::-1]

		for item in rec_event_list:
			tmp = {
				"name":item['name'],
				"participant_count":item['participant_count'],
				"prize_type":item["prize_type"],
				"start_time":__date2time(item['start_time']),
				"end_time":__date2time(item['end_time']),
				"status":item['status']
			}
			tmp["actions"] = __get_actions(item['status'])
			actual_list.append(tmp)
		print("actual_data: {}".format(actual_list))
		bdd_util.assert_list(expected,actual_list)

@when(u"{user}编辑活动报名活动'{event_name}'")
def step_impl(context,user,event_name):
	expect = json.loads(context.text)[0]
	event_page_id,event_id = __event_name2id(event_name)#纯数字
	__Update_Event(context,expect,event_page_id,event_id)

# @then(u"{user}获得活动报名'{event_name}'")
# def step_impl(context,user,event_name):
# 	expect = json.loads(context.text)[0]

# 	title = expect.get("name","")

# 	cr_start_date = expect.get('start_date', u'今天')
# 	start_date = bdd_util.get_date_str(cr_start_date)
# 	start_time = "{} 00:00".format(bdd_util.get_date_str(cr_start_date))

# 	cr_end_date = expect.get('end_date', u'1天后')
# 	end_date = bdd_util.get_date_str(cr_end_date)
# 	end_time = "{} 00:00".format(bdd_util.get_date_str(cr_end_date))

# 	valid_time = "%s~%s"%(start_time,end_time)

# 	desc = expect.get('desc','')#描述
# 	reduce_integral = expect.get('reduce_integral',0)#消耗积分
# 	send_integral = expect.get('send_integral',0)#参与送积分
# 	send_integral_rules = expect.get('send_integral_rules',"")#送积分规则
# 	event_limit = __name2limit(expect.get('event_limit',u'一人一次'))#活动报名限制
# 	win_rate = expect.get('win_rate','0%').split('%')[0]#中奖率
# 	is_repeat_win = __name2Bool(expect.get('is_repeat_win',"true"))#重复中奖
# 	expect_prize_settings_list = expect.get('prize_settings',[])
# 	page_prize_settings,event_prize_settings = __prize_settings_process(expect_prize_settings_list)


# 	obj = event_models.event.objects.get(name=event_name)#纯数字
# 	related_page_id = obj.related_page_id
# 	pagestore = pagestore_manager.get_pagestore('mongo')
# 	page = pagestore.get_page(related_page_id, 1)
# 	page_component = page['component']['components'][0]['components']

# 	expect_event_dic = {
# 		"name":title,
# 		"start_time":start_time,
# 		"end_time":end_time,
# 		"expend":reduce_integral,#消耗积分
# 		"delivery":send_integral,#参与送积分
# 		"delivery_setting":__delivery2Bool(send_integral_rules),#送积分规则
# 		"limitation":event_limit,#活动报名限制
# 		"chance":win_rate,#中奖率
# 		"allow_repeat":is_repeat_win,#重复中奖
# 		"prize_settings":page_prize_settings
# 	}


# 	actual_prize_list=[]
# 	for comp in page_component:
# 		actual_prize_dic={}
# 		actual_prize_dic['title'] = comp['model']['title']
# 		actual_prize_dic['prize_count'] = comp['model']['prize_count']
# 		actual_prize_dic['image'] = comp['model']['image']
# 		actual_prize_dic['prize'] = {
# 			"type":comp['model']['prize']['type'],
# 			"data":comp['model']['prize']['data']
# 		}
# 		actual_prize_list.append(actual_prize_dic)

# 	actual_event_dic = {
# 		"name": obj.name,
# 		"start_time":__datetime2str(obj.start_time),
# 		"end_time":__datetime2str(obj.end_time),
# 		"expend":obj.expend,#消耗积分
# 		"delivery":obj.delivery,#参与送积分
# 		"delivery_setting":obj.delivery_setting,#送积分规则
# 		"limitation":obj.limitation,#活动报名限制
# 		"chance":obj.chance,#中奖率
# 		"allow_repeat":obj.allow_repeat,#重复中奖
# 		"prize_settings":actual_prize_list,
# 	}

# 	bdd_util.assert_dict(expect_event_dic, actual_event_dic)

@when(u"{user}删除百宝箱活动报名'{event_name}'")
def step_impl(context,user,event_name):
	event_page_id,event_id = __event_name2id(event_name)#纯数字
	del_response = __Delete_Event(context,event_id)
	bdd_util.assert_api_call_success(del_response)

@when(u"{user}关闭活动报名'{event_name}'")
def step_impl(context,user,event_name):
	event_page_id,event_id = __event_name2id(event_name)#纯数字
	stop_response = __Stop_Event(context,event_id)
	bdd_util.assert_api_call_success(stop_response)

@when(u"{user}设置活动报名列表查询条件")
def step_impl(context,user):
	expect = json.loads(context.text)

	if 'start_date' in expect:
		expect['start_time'] = __date2time(expect['start_date']) if expect['start_date'] else ""
		del expect['start_date']

	if 'end_date' in expect:
		expect['end_time'] = __date2time(expect['end_date']) if expect['end_date'] else ""
		del expect['end_date']

	search_dic = {
		"name": expect.get("name",""),
		"start_time": expect.get("start_time",""),
		"end_time": expect.get("end_time",""),
		"status": __name2status(expect.get("status",u"所有活动")),
		"prize_type":__name2prize_type(expect.get("prize_type",u"所有奖品"))
	}


	search_response = __Search_Event(context,search_dic)
	event_array = json.loads(search_response.content)['data']['items']
	context.search_event = event_array

@when(u"{user}访问百宝箱活动报名列表第'{page_num}'页")
def step_impl(context,user,page_num):
	count_per_page = context.count_per_page
	context.paging = {'count_per_page':count_per_page,"page_num":page_num}

@when(u"{user}访问活动报名列表下一页")
def step_impl(context,user):
	paging_dic = context.paging
	count_per_page = paging_dic['count_per_page']
	page_num = int(paging_dic['page_num'])+1
	context.paging = {'count_per_page':count_per_page,"page_num":page_num}

@when(u"{user}访问活动报名列表上一页")
def step_impl(context,user):
	paging_dic = context.paging
	count_per_page = paging_dic['count_per_page']
	page_num = int(paging_dic['page_num'])-1
	context.paging = {'count_per_page':count_per_page,"page_num":page_num}

@when(u"{user}查看活动报名'{event_name}'")
def check_event_list(context,user,event_name):
	design_mode = 0
	version = 1
	page = 1

	if hasattr(context,"enable_paginate"):
		enable_paginate = context.enable_paginate
	else:
		enable_paginate = 1
	if hasattr(context,"count_per_page"):
		count_per_page = context.count_per_page
	else:
		count_per_page = 10


	if hasattr(context,"paging"):
		paging_dic = context.paging
		count_per_page = paging_dic['count_per_page']
		page = paging_dic['page_num']

	event_page_id,event_id = __event_name2id(event_name)#纯数字
	url ='/apps/event/api/event_participances/?design_mode={}&version={}&id={}&count_per_page={}&page={}&enable_paginate={}&_method=get'.format(
			design_mode,
			version,
			event_id,
			count_per_page,
			page,
			enable_paginate,
		)
	url = bdd_util.nginx(url)
	response = context.client.get(url)
	context.participances = json.loads(response.content)
	context.event_id = "%s"%(event_id)


@then(u"{webapp_user_name}获得活动报名'{event_rule_name}'结果列表")
def step_tmpl(context, webapp_user_name, event_rule_name):

	if hasattr(context,"search_event_result"):
		participances = context.search_event_result
	else:
		participances = context.participances['data']['items']

	actual = []
	for p in participances:
		p_dict = {}
		p_dict[u"participant_name"] = p['participant_name']
		p_dict[u"datetime"] = p['created_at']
		p_dict[u"informations"] = p['informations']
		actual.append((p_dict))
	print("actual_data: {}".format(actual))

	expect_list = []
	expected = json.loads(context.text)
	for expect in expected:
		e_dict ={}
		if 'date' in expected:
			expected['datetime'] = __date2time(expect['datet']) if expect['date'] else ""
			del expected['date']
		e_dict["participant_name"] = expect['name']
		# e_dict["datetime"] = expect['date']

		info_dic = expect['info']
		info_li = []
		for k,v in info_dic.iteritems():
			format_info = {}
			format_info['item_name']= k
			format_info['item_value'] = v
			info_li.append(format_info)

		e_dict[u'informations'] = info_li

		expect_list.append(e_dict)


	print("expected: {}".format(expect_list))

	bdd_util.assert_list(expect_list, actual)

@when(u"{user}设置活动报名结果列表查询条件")
def step_impl(context,user):
	expect = json.loads(context.text)

	if 'start_date' in expect:
		expect['start_time'] = __date2time(expect['start_date']) if expect['start_date'] else ""
		del expect['start_date']

	if 'end_date' in expect:
		expect['end_time'] = __date2time(expect['end_date']) if expect['end_date'] else ""
		del expect['end_date']

	print("expected: {}".format(expect))
	id = context.event_id
	participant_name = expect.get("name","")
	start_time = expect.get("start_time","")
	end_time = expect.get("end_time","")

	search_dic = {
		"id":id,
		"participant_name":participant_name,
		"start_time":start_time,
		"end_time":end_time,
	}
	search_response = __Search_Event_Result(context,search_dic)
	event_result_array = json.loads(search_response.content)['data']['items']
	context.search_event_result = event_result_array

@when(u"{user}访问活动报名'{event_name}'的结果列表第'{page_num}'页")
def step_impl(context,user,event_name,page_num):
	count_per_page = context.count_per_page
	context.paging = {'count_per_page':count_per_page,"page_num":page_num}
	check_event_list(context,user,event_name)

@when(u"{user}访问活动报名'{event_name}'的结果列表下一页")
def step_impl(context,user,event_name):
	paging_dic = context.paging
	count_per_page = paging_dic['count_per_page']
	page_num = int(paging_dic['page_num'])+1
	context.paging = {'count_per_page':count_per_page,"page_num":page_num}
	check_event_list(context,user,event_name)

@when(u"{user}访问活动报名'{event_name}'的结果列表上一页")
def step_impl(context,user,event_name):
	paging_dic = context.paging
	count_per_page = paging_dic['count_per_page']
	page_num = int(paging_dic['page_num'])-1
	context.paging = {'count_per_page':count_per_page,"page_num":page_num}
	check_event_list(context,user,event_name)

# @then(u"{user}能批量导出活动报名'{event_name}'")
# def step_impl(context,user,event_name):
# 	event_page_id,event_id = __event_name2id(event_name)#纯数字
# 	url ='/apps/event/api/event_participances_export/?_method=get&export_id=%s' % (event_id)
# 	url = bdd_util.nginx(url)
# 	response = context.client.get(url)
# 	bdd_util.assert_api_call_success(response)