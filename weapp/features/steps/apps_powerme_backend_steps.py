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
from market_tools.tools.channel_qrcode.models import ChannelQrcodeSettings
from weixin.message.material import models as material_models
from apps.customerized_apps.powerme import models as powerme_models
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


def __get_powermePageJson(args):
	"""
	传入参数，获取模板
	"""
	__page_temple = {
			"type": "appkit.page",
			"cid": 1,
			"pid": None,
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
				"site_title": "微助力",
				"background": ""
			},
			"components": [
				{
					"type": "appkit.powermedescription",
					"cid": 2,
					"pid": 1,
					"auto_select": False,
					"selectable": "yes",
					"force_display_in_property_view": "no",
					"has_global_content": "no",
					"need_server_process_component_data": "no",
					"property_view_title": "微助力",
					"model": {
						"id": "",
						"class": "",
						"name": "",
						"index": 2,
						"datasource": {
							"type": "api",
							"api_name": ""
						},
						"title": args.get("title",""),
						"start_time": args.get("start_time",""),
						"end_time": args.get("end_time",""),
						"valid_time": args.get("valid_time",""),
						"timing": {
							"timing": {
								"select": args.get("timing_status","")
							}
						},
						"timing_value": {
							"day": args.get("timing_value_day",0),
							"hour": "00",
							"minute": "00",
							"second": "00"
						},
						"description": args.get("description",""),
						"reply_content": args.get("reply_content",""),
						"qrcode": args.get("qrcode",{"ticket":"","name":""}),
						"material_image": args.get("material_image",""),
						"background_image": args.get("background_image",""),
						"color": args.get("color",""),
						"rules": args.get("rules","")
					},
					"components": []
				},
				{
					"type": "appkit.submitbutton",
					"cid": 3,
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
						"text": "提交"
					},
					"components": []
				},
				{
					"type": "appkit.componentadder",
					"cid": 4,
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

def __date_delta(start,end):
	"""
	获得日期，相差天数，返回int
	格式：
		start:(str){2015-11-23}
		end :(str){2015-11-30}
	"""
	start = dt.datetime.strptime(start, "%Y-%m-%d").date()
	end = dt.datetime.strptime(end, "%Y-%m-%d").date()
	return (end-start).days

def __date2time(date_str):
	"""
	字符串 今天/明天……
	转化为字符串 "%Y-%m-%d %H:%M"
	"""
	cr_date = date_str
	p_date = bdd_util.get_date_str(cr_date)
	p_time = "{} 00:00".format(bdd_util.get_date_str(cr_date))
	return p_time

def __datetime2str(dt_time):
	"""
	datetime型数据，转为字符串型，日期
	转化为字符串 "%Y-%m-%d %H:%M"
	"""
	dt_time = dt.datetime.strftime(dt_time, "%Y-%m-%d %H:%M")
	return dt_time

def __powerme_name2id(name):
	"""
	给微助力项目的名字，返回id元祖
	返回（related_page_id,powerme_powerme中id）
	"""
	obj = powerme_models.PowerMe.objects.get(name=name)
	return (obj.related_page_id,obj.id)

def __status2name(status_num):
	"""
	微助力：状态值 转 文字
	"""
	status2name_dic = {-1:u"全部",0:u"未开始",1:u"进行中",2:u"已结束"}
	return status2name_dic[status_num]

def __name2status(name):
	"""
	微助力： 文字 转 状态值
	"""
	if name:
		name2status_dic = {u"全部":-1,u"未开始":0,u"进行中":1,u"已结束":2}
		return name2status_dic[name]
	else:
		return -1

def __name2color(name):
	"""
	微助力背景色：文字 转 状态值
	"""
	name2color_dic = {
		u"冬日暖阳":"yellow",
		u"玫瑰茜红":"red",
		u"热带橙色":"orange"
	}
	return name2color_dic[name]

def __color2name(color):
	"""
	微助力背景色：状态值 转 文字
	"""
	color2name_dic = {
		'yellow': u'冬日暖阳',
		'red': u'玫瑰茜红',
		'orange': u'热带橙色'
	}
	return color2name_dic[color]


def __get_qrcode(context,qrcode_name):
	"""
	传入二维码名字，获得二维码，信息字典
	"""

	qrcode_id = ChannelQrcodeSettings.objects.get(owner_id=context.webapp_owner_id, name=qrcode_name).id
	qrcode_i_url = '/new_weixin/qrcode/?setting_id=%s' % str(qrcode_id)
	qrcode_response = context.client.get(qrcode_i_url)
	qrcode_info = qrcode_response.context['qrcode']
	qrcode_ticket_url = "https://mp.weixin.qq.com/cgi-bin/showqrcode?ticket={}".format(qrcode_info.ticket)
	qrcode = {"ticket":qrcode_ticket_url,"name":qrcode_info.name}
	return qrcode

def __get_actions(status):
	"""
	根据输入微助力状态
	返回对于操作列表
	"""
	actions_list = [u"查看",u"预览",u"复制链接"]
	if status == u"已结束":
		actions_list.append(u"删除")
	elif status=="进行中" or "未开始":
		actions_list.append(u"关闭")
	return actions_list

def __Create_PowerMe(context,text,user):
	"""
	模拟用户登录页面
	创建微助力项目
	写入mongo表：
		1.powerme_powerme表
		2.page表
	"""

	design_mode = 0
	version = 1
	text = text

	title = text.get("name","")

	cr_start_date = text.get('start_date', u'今天')
	start_date = bdd_util.get_date_str(cr_start_date)
	start_time = "{} 00:00".format(bdd_util.get_date_str(cr_start_date))

	cr_end_date = text.get('end_date', u'1天后')
	end_date = bdd_util.get_date_str(cr_end_date)
	end_time = "{} 00:00".format(bdd_util.get_date_str(cr_end_date))

	valid_time = "%s~%s"%(start_time,end_time)

	timing_status = text.get("is_show_countdown","")

	timing_value_day = __date_delta(start_date,end_date)

	description = text.get("desc","")
	reply_content = text.get("reply")
	material_image = text.get("share_pic","")
	background_image = text.get("background_pic","")

	qrcode_name = text.get("qr_code","")
	if qrcode_name:
		qrcode_id = ChannelQrcodeSettings.objects.get(owner_id=context.webapp_owner_id, name=qrcode_name).id
		qrcode_i_url = '/new_weixin/qrcode/?setting_id=%s' % str(qrcode_id)
		qrcode_response = context.client.get(qrcode_i_url)
		qrcode_info = qrcode_response.context['qrcode']
		qrcode_ticket_url = "https://mp.weixin.qq.com/cgi-bin/showqrcode?ticket={}".format(qrcode_info.ticket)
		qrcode = {"ticket":qrcode_ticket_url,"name":qrcode_info.name}
	else:
		qrcode = {"ticket":"","name":""}

	zhcolor = text.get("background_color","冬日暖阳")
	color = __name2color(zhcolor)

	rules = text.get("rules","")

	page_args = {
		"title":title,
		"start_time":start_time,
		"end_time":end_time,
		"valid_time":valid_time,
		"timing_status":timing_status,
		"timing_value_day":timing_value_day,
		"description":description,
		"reply_content":reply_content,
		"qrcode":qrcode,
		"material_image":material_image,
		"background_image":background_image,
		"color":color,
		"rules":rules
	}

	#step1：登录页面，获得分配的project_id
	get_pw_response = context.client.get("/apps/powerme/powerme/")
	pw_args_response = get_pw_response.context
	project_id = pw_args_response['project_id']#(str){new_app:powerme:0}

	#step2: 编辑页面获得右边的page_json
	dynamic_url = "/apps/api/dynamic_pages/get/?design_mode={}&project_id={}&version={}".format(design_mode,project_id,version)
	dynamic_response = context.client.get(dynamic_url)
	dynamic_data = dynamic_response.context#resp.context=> data ; resp.content => Http Text

	#step3:发送Page
	page_json = __get_powermePageJson(page_args)

	termite_post_args = {
		"field":"page_content",
		"id":project_id,
		"page_id":"1",
		"page_json": page_json
	}
	termite_url = "/termite2/api/project/?design_mode={}&project_id={}&version={}".format(design_mode,project_id,version)
	post_termite_response = context.client.post(termite_url,termite_post_args)
	related_page_id = json.loads(post_termite_response.content).get("data",{})['project_id']

	#step4:发送powerme_args
	post_powerme_args = {
		"name":title,
		"start_time":start_time,
		"end_time":end_time,
		"timing":timing_status,
		"reply_content":reply_content,
		"material_image":material_image,
		"qrcode":json.dumps(qrcode),
		"related_page_id":related_page_id
	}
	powerme_url ="/apps/powerme/api/powerme/?design_mode={}&project_id={}&version={}&_method=put".format(design_mode,project_id,version)
	post_powerme_response = context.client.post(powerme_url,post_powerme_args)

def __Update_PowerMe(context,text,page_id,powerme_id):
	"""
	模拟用户登录页面
	编辑微助力项目
	写入mongo表：
		1.powerme_powerme表
		2.page表
	"""

	design_mode=0
	version=1
	project_id = "new_app:powerme:"+page_id

	title = text.get("name","")
	cr_start_date = text.get('start_date', u'今天')
	start_date = bdd_util.get_date_str(cr_start_date)
	start_time = "{} 00:00".format(bdd_util.get_date_str(cr_start_date))

	cr_end_date = text.get('end_date', u'1天后')
	end_date = bdd_util.get_date_str(cr_end_date)
	end_time = "{} 00:00".format(bdd_util.get_date_str(cr_end_date))

	valid_time = "%s~%s"%(start_time,end_time)

	timing_status = text.get("is_show_countdown","")

	timing_value_day = __date_delta(start_date,end_date)

	description = text.get("desc","")
	reply_content = text.get("reply")
	material_image = text.get("share_pic","")
	background_image = text.get("background_pic","")

	qrcode_name = text.get("qr_code","")
	if qrcode_name:
		qrcode = __get_qrcode(context,qrcode_name)
	else:
		qrcode = ""

	zhcolor = text.get("background_color","冬日暖阳")
	color = __name2color(zhcolor)

	rules = text.get("rules","")

	page_args = {
		"title":title,
		"start_time":start_time,
		"end_time":end_time,
		"valid_time":valid_time,
		"timing_status":timing_status,
		"timing_value_day":timing_value_day,
		"description":description,
		"reply_content":reply_content,
		"qrcode":qrcode,
		"material_image":material_image,
		"background_image":background_image,
		"color":color,
		"rules":rules
	}

	page_json = __get_powermePageJson(page_args)

	update_page_args = {
		"field":"page_content",
		"id":project_id,
		"page_id":"1",
		"page_json": page_json
	}

	update_powerme_args = {
		"name":title,
		"start_time":start_time,
		"end_time":end_time,
		"timing":timing_status,
		"reply_content":reply_content,
		"material_image":material_image,
		"qrcode":json.dumps(qrcode),
		"id":powerme_id#updated的差别
	}


	#page 更新Page
	update_page_url = "/termite2/api/project/?design_mode={}&project_id={}&version={}".format(design_mode,project_id,version)
	update_page_response = context.client.post(update_page_url,update_page_args)

	#step4:更新Powerme
	update_powerme_url ="/apps/powerme/api/powerme/?design_mode={}&project_id={}&version={}".format(design_mode,project_id,version)
	update_powerme_response = context.client.post(update_powerme_url,update_powerme_args)

def __Delete_PowerMe(context,powerme_id):
	"""
	删除微助力活动
	写入mongo表：
		1.powerme_powerme表

	注释：page表在原后台，没有被删除
	"""
	design_mode = 0
	version = 1
	del_powerme_url = "/apps/powerme/api/powerme/?design_mode={}&version={}&_method=delete".format(design_mode,version)
	del_args ={
		"id":powerme_id
	}
	del_powerme_response = context.client.post(del_powerme_url,del_args)
	return del_powerme_response

def __Stop_PowerMe(context,powerme_id):
	"""
	关闭微助力活动
	"""

	design_mode = 0
	version = 1
	stop_powerme_url = "/apps/powerme/api/powerme_status/?design_mode={}&version={}".format(design_mode,version)
	stop_args ={
		"id":powerme_id,
		"target":'stoped'
	}
	stop_powerme_response = context.client.post(stop_powerme_url,stop_args)
	return stop_powerme_response

def __Search_Powerme(context,search_dic):
	"""
	搜索微助力活动

	输入搜索字典
	返回数据列表
	"""

	design_mode = 0
	version = 1
	page = 1
	enable_paginate = 1
	count_per_page = 10

	name = search_dic["name"]
	start_time = search_dic["start_time"]
	end_time = search_dic["end_time"]
	status = __name2status(search_dic["status"])



	search_url = "/apps/powerme/api/powermes/?design_mode={}&version={}&name={}&status={}&start_time={}&end_time={}&count_per_page={}&page={}&enable_paginate={}".format(
			design_mode,
			version,
			name,
			status,
			start_time,
			end_time,
			count_per_page,
			page,
			enable_paginate)

	search_response = context.client.get(search_url)
	bdd_util.assert_api_call_success(search_response)
	return search_response

def __Search_Powerme_Result(context,search_dic):
	"""
	搜索,微助力参与结果

	输入搜索字典
	返回数据列表
	"""

	design_mode = 0
	version = 1
	page = 1
	enable_paginate = 1
	count_per_page = 10

	id = search_dic["id"]
	participant_name = search_dic["participant_name"]
	start_time = search_dic["start_time"]
	end_time = search_dic["end_time"]



	search_url = "/apps/powerme/api/powerme_participances/?design_mode={}&version={}&id={}&participant_name={}&start_time={}&end_time={}&count_per_page={}&page={}&enable_paginate={}".format(
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



@when(u'{user}新建微助力活动')
def step_impl(context,user):
	text_list = json.loads(context.text)
	for text in text_list:
		__Create_PowerMe(context,text,user)

@then(u'{user}获得微助力活动列表')
def step_impl(context,user):
	design_mode = 0
	count_per_page = 10
	version = 1
	page = 1
	enable_paginate = 1

	actual_list = []
	expected = json.loads(context.text)

	#搜索查看结果
	if hasattr(context,"search_powerme"):
		rec_search_list = context.search_powerme
		for item in rec_search_list:
			tmp = {
				"name":item['name'],
				"status":item['status'],
				"start_time":item['start_time'],
				"end_time":item['end_time'],
				"participant_count":item['participant_count'],
				"total_powerme_value":item['total_power']
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

		rec_powerme_url ="/apps/powerme/api/powermes/?design_mode={}&version={}&count_per_page={}&page={}&enable_paginate={}".format(design_mode,version,count_per_page,page,enable_paginate)
		rec_powerme_response = context.client.get(rec_powerme_url)
		rec_powerme_list = json.loads(rec_powerme_response.content)['data']['items']#[::-1]

		for item in rec_powerme_list:
			tmp = {
				"name":item['name'],
				"status":item['status'],
				"start_time":__date2time(item['start_time']),
				"end_time":__date2time(item['end_time']),
				"participant_count":item['participant_count'],
				"total_powerme_value":item['total_power']
			}
			tmp["actions"] = __get_actions(item['status'])
			actual_list.append(tmp)
		print("actual_data: {}".format(actual_list))
		bdd_util.assert_list(expected,actual_list)


@when(u"{user}编辑微助力活动'{powerme_name}'")
def step_impl(context,user,powerme_name):
	expect = json.loads(context.text)[0]
	powerme_page_id,powerme_id = __powerme_name2id(powerme_name)#纯数字
	__Update_PowerMe(context,expect,powerme_page_id,powerme_id)


@then(u"{user}获得微助力活动'{powerme_name}'")
def step_impl(context,user,powerme_name):
	expect = json.loads(context.text)[0]

	title = expect.get("name","")
	cr_start_date = expect.get('start_date', u'今天')
	start_date = bdd_util.get_date_str(cr_start_date)
	start_time = "{} 00:00".format(bdd_util.get_date_str(cr_start_date))

	cr_end_date = expect.get('end_date', u'1天后')
	end_date = bdd_util.get_date_str(cr_end_date)
	end_time = "{} 00:00".format(bdd_util.get_date_str(cr_end_date))

	# valid_time = "%s~%s"%(start_time,end_time)
	timing_status = expect.get("is_show_countdown","")
	# timing_value_day = __date_delta(start_date,end_date)
	description = expect.get("desc","")
	reply_content = expect.get("reply")
	material_image = expect.get("share_pic","")
	background_image = expect.get("background_pic","")

	qrcode_name = expect.get("qr_code","")
	if qrcode_name:
		qrcode = __get_qrcode(context,qrcode_name)
	else:
		qrcode = ""

	color  = expect.get("background_color","冬日暖阳")
	rules = expect.get("rules","")


	obj = powerme_models.PowerMe.objects.get(name=powerme_name)#纯数字
	related_page_id = obj.related_page_id
	pagestore = pagestore_manager.get_pagestore('mongo')
	page = pagestore.get_page(related_page_id, 1)
	page_component = page['component']['components'][0]['model']

	fe_powerme_dic = {
		"name":title,
		"start_time":start_time,
		"end_time":end_time,
		"is_show_countdown":timing_status,
		"desc":description,
		"reply":reply_content,
		"qr_code":qrcode,
		"share_pic":material_image,
		"background_pic":background_image,
		"background_color":color,
		"rules":rules
	}

	db_powerme_dic = {
		"name": obj.name,
		"start_time":__datetime2str(obj.start_time),
		"end_time":__datetime2str(obj.end_time),
		"is_show_countdown":page_component['timing']['timing']['select'],
		"desc":page_component['description'],
		"reply":obj.reply_content,
		"qr_code":obj.qrcode,
		"share_pic":page_component['material_image'],
		"background_pic": page_component['background_image'],
		"background_color": __color2name(page_component['color']),
		"rules": page_component['rules'],
	}

	bdd_util.assert_dict(db_powerme_dic, fe_powerme_dic)

@when(u"{user}删除微助力活动'{powerme_name}'")
def step_impl(context,user,powerme_name):
	powerme_page_id,powerme_id = __powerme_name2id(powerme_name)#纯数字
	del_response = __Delete_PowerMe(context,powerme_id)
	bdd_util.assert_api_call_success(del_response)


@when(u"{user}关闭微助力活动'{powerme_name}'")
def step_impl(context,user,powerme_name):
	powerme_page_id,powerme_id = __powerme_name2id(powerme_name)#纯数字
	stop_response = __Stop_PowerMe(context,powerme_id)
	bdd_util.assert_api_call_success(stop_response)


@when(u"{user}查看微助力活动'{powerme_name}'")
def step_impl(context,user,powerme_name):
	powerme_page_id,powerme_id = __powerme_name2id(powerme_name)#纯数字
	url ='/apps/powerme/api/powerme_participances/?_method=get&id=%s' % (powerme_id)
	url = bdd_util.nginx(url)
	response = context.client.get(url)
	context.participances = json.loads(response.content)
	context.powerme_id = "%s"%(powerme_id)

@then(u"{webapp_user_name}获得微助力活动'{power_me_rule_name}'的结果列表")
def step_tmpl(context, webapp_user_name, power_me_rule_name):
	if hasattr(context,"search_powerme_result"):
		participances = context.search_powerme_result
	else:
		participances = context.participances['data']['items']
	actual = []
	print(participances)
	for p in participances:
		p_dict = OrderedDict()
		p_dict[u"rank"] = p['ranking']
		p_dict[u"member_name"] = p['username']
		p_dict[u"powerme_value"] = p['power']
		p_dict[u"parti_time"] = bdd_util.get_date_str(p['created_at'])
		actual.append((p_dict))
	print("actual_data: {}".format(actual))
	expected = []
	if context.table:
		for row in context.table:
			cur_p = row.as_dict()
			if cur_p[u'parti_time']:
				cur_p[u'parti_time'] = bdd_util.get_date_str(cur_p[u'parti_time'])
			expected.append(cur_p)
	else:
		expected = json.loads(context.text)
	print("expected: {}".format(expected))

	bdd_util.assert_list(expected, actual)

@when(u"{user}设置微助力活动列表查询条件")
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
		"status": expect.get("status",u"全部")
	}
	search_response = __Search_Powerme(context,search_dic)
	powerme_array = json.loads(search_response.content)['data']['items']
	context.search_powerme = powerme_array

@when(u"{user}访问微助力活动列表第'{page_num}'页")
def step_impl(context,user,page_num):
	count_per_page = context.count_per_page
	context.paging = {'count_per_page':count_per_page,"page_num":page_num}

@when(u"{user}访问微助力活动列表下一页")
def step_impl(context,user):
	paging_dic = context.paging
	count_per_page = paging_dic['count_per_page']
	page_num = int(paging_dic['page_num'])+1
	context.paging = {'count_per_page':count_per_page,"page_num":page_num}

@when(u"{user}访问微助力活动列表上一页")
def step_impl(context,user):
	paging_dic = context.paging
	count_per_page = paging_dic['count_per_page']
	page_num = int(paging_dic['page_num'])-1
	context.paging = {'count_per_page':count_per_page,"page_num":page_num}

@when(u"{user}设置微助力活动结果列表查询条件")
def step_impl(context,user):
	expect = json.loads(context.text)

	if 'parti_start_time' in expect:
		expect['start_time'] = __date2time(expect['parti_start_time']) if expect['parti_start_time'] else ""
		del expect['parti_start_time']

	if 'parti_end_time' in expect:
		expect['end_time'] = __date2time(expect['parti_end_time']) if expect['parti_end_time'] else ""
		del expect['parti_end_time']

	id = context.powerme_id
	participant_name = expect.get("member_name","")
	start_time = expect.get("start_time","")
	end_time = expect.get("end_time","")

	search_dic = {
		"id":id,
		"participant_name":participant_name,
		"start_time":start_time,
		"end_time":end_time
	}
	search_response = __Search_Powerme_Result(context,search_dic)
	powerme_result_array = json.loads(search_response.content)['data']['items']
	context.search_powerme_result = powerme_result_array

@then(u"{user}能批量导出微助力活动'{powerme_name}'")
def step_impl(context,user,powerme_name):
	powerme_page_id,powerme_id = __powerme_name2id(powerme_name)#纯数字
	url ='/apps/powerme/api/powerme_participances_export/?_method=get&export_id=%s' % (powerme_id)
	url = bdd_util.nginx(url)
	response = context.client.get(url)
	bdd_util.assert_api_call_success(response)