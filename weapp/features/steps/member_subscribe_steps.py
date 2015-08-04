# -*- coding: utf-8 -*-
import json
import time

from behave import *

from test import bdd_util
from features.testenv.model_factory import *

from django.test.client import Client
from django.contrib.auth.models import User

from mall.models import *
from modules.member.models import * 
from weixin.user import models as weixn_models
from account import models as account_models
from utils.string_util import byte_to_hex

def __get_user(user_name):
	return User.objects.get(username=user_name)

@given(u'{user}设置积分策略')
def step_impl(context, user):
	if hasattr(context, 'client'):
		context.client.logout()
	context.client = bdd_util.login(user)
	client = context.client
	user = UserFactory(username=user)
	profile = UserProfile.objects.get(user_id=user.id)
	json_data = json.loads(context.text)

	integral_detail = {};
	integral = {}
	
	for key, value in  json_data[0].items():
		if key != 'member_integral_strategy_settings_detail':
			integral[key] = value

	if json_data[0].has_key('member_integral_strategy_settings_detail'):
		integral_detail = json_data[0]['member_integral_strategy_settings_detail'][0]

	if IntegralStrategySttings.objects.filter(webapp_id=profile.webapp_id).count() > 0:
		IntegralStrategySttings.objects.filter(webapp_id=profile.webapp_id).update(**integral)
	for key, value in integral_detail.items():
		if key == 'is_used':
			if value == u'否':
				integral_detail[key] = False
			else:
				integral_detail[key] = True
		else:
			integral_detail[key] = float(value[value.find('+')+1:value.find('*')])

	integral_detail['webapp_id'] = profile.webapp_id
	if IntegralStrategySttingsDetail.objects.filter(webapp_id=profile.webapp_id).count() > 0 and integral_detail:
		IntegralStrategySttingsDetail.objects.filter(webapp_id=profile.webapp_id).update(**integral_detail)
	elif integral_detail:
		

		IntegralStrategySttingsDetail.objects.create(**integral_detail)

@Then(u'{user}可以获得会员列表')
def step_impl(context, user):
	if hasattr(context, 'client'):
		context.client.logout()
	context.client = bdd_util.login(user)
	client = context.client
	user = UserFactory(username=user)
	json_data = json.loads(context.text)
	Member.objects.all().update(is_for_test=False)
	url = '/webapp/user_center/api/members/get/'
	response = context.client.get(bdd_util.nginx(url))
	profile = UserProfile.objects.get(user_id=user.id)
	items = json.loads(response.content)['data']['items']
	actual_members = []
	for member_item in items:
		actual_member = {}
		actual_member['name'] = member_item['username']
		actual_member['integral'] = member_item['integral']
		if member_item['is_subscribed']:
			actual_member['status'] = u"已关注"
		else:
			actual_member['status'] = u"已取消"
		actual_members.append(actual_member)

	bdd_util.assert_list(actual_members, json_data)


@then(u'{webapp_owner_name}能获得{webapp_user_name}的积分日志')
def step_impl(context, webapp_owner_name, webapp_user_name):
	webapp_user_member = bdd_util.get_member_for(webapp_user_name, context.webapp_id)
	url = '/user_center/member/%d/integral_log/' % webapp_user_member.id
	response = context.client.get(url)
	member_logs = response.context['member_logs']
	actual = [{"content":log.event_type, "integral":log.integral_count} for log in member_logs]

	expected = json.loads(context.text)
	bdd_util.assert_list(expected, actual)


@when(u'{member_a}取消关注{user}的公众号')
def step_impl(context, member_a, user):
	if hasattr(context, 'client'):
		context.client.logout()
	context.client = bdd_util.login(user)
	client = context.client
	user = UserFactory(username=user)
	user_profile = UserProfile.objects.get(user_id=user.id)
	openid = '%s_%s' % (member_a, user)
	post_data = """
				<xml><ToUserName><![CDATA[weizoom]]></ToUserName>
				<FromUserName><![CDATA[%s]]></FromUserName>
				<CreateTime>1405079048</CreateTime>
				<MsgType><![CDATA[event]]></MsgType>
				<Event><![CDATA[unsubscribe]]></Event>
				<EventKey><![CDATA[]]></EventKey>
				</xml>
	""" % openid
	url = '/weixin/%s/'% user_profile.webapp_id
	client.post(url, post_data, "text/xml; charset=\"UTF-8\"")

	
