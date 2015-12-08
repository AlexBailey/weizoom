# -*- coding: utf-8 -*-
__author__ = 'kuki'
from behave import *
from test import bdd_util

from features.testenv.model_factory import *
import steps_db_util
from modules.member import module_api as member_api
from utils import url_helper
import datetime as dt
import termite.pagestore as pagestore_manager
from apps.customerized_apps.sign.models import Sign, SignParticipance
from modules.member.models import Member, SOURCE_MEMBER_QRCODE
from utils.string_util import byte_to_hex
import json
import re

def __get_sign_record_id(webapp_owner_id):
	return Sign.objects.get(owner_id=webapp_owner_id).id

@when(u"{webapp_user_name}进入{webapp_owner_name}签到页面进行签到")
def step_tmpl(context, webapp_user_name, webapp_owner_name):
	webapp_owner_id = context.webapp_owner_id
	appRecordId = __get_sign_record_id(webapp_owner_id)
	params = {
		'webapp_owner_id': webapp_owner_id,
		'id': appRecordId
	}
	response = context.client.post('/m/apps/sign/api/sign_participance/?_method=put', params)
	context.datas = json.loads(response.content)['data']

@then(u"{webapp_user_name}获取签到成功的内容")
def step_tmpl(context, webapp_user_name):
	datas = context.datas
	# 构造实际数据
	actual = []
	actual.append({
		'serial_count': datas['serial_count'],
		'daily_prize': {
			'integral': datas['daily_prize']['integral'],
			'coupon': datas['daily_prize']['coupon']['name']
		},
		'curr_prize': {
			'integral': datas['curr_prize']['integral'],
			'coupon': datas['curr_prize']['coupon']['name']
		}
	})
	print("actual_data: {}".format(actual))
	expected = json.loads(context.text)
	print("expected: {}".format(expected))
	bdd_util.assert_list(expected, actual)

@then(u"{user}获得系统回复的消息")
def step_impl(context, user):
	answer = context.text.strip()
	result = context.qa_result["data"]
	begin = result.find('<div class="content">') + len('<div class="content">')
	if result.find('<a href=') != -1: #result存在a标签
		if result.find('market_tool:coupon') != -1: #result存在优惠券
			coupon_begin = result.find('<a')
			coupon_end = result.find('</a><br />', coupon_begin) + len('</a><br />')
			result = result[:coupon_begin]+result[coupon_end:] #截取掉result中优惠券的a标签内容
		end = result.find('<a', begin)
		link_url = '/m/apps/sign/m_sign/?webapp_owner_id=%s' % (context.webapp_owner_id)
		link_url = bdd_util.nginx(link_url)
		context.link_url = link_url
	else:
		end = result.find('</div>', begin)
	actual  = result[begin:end]
	expected = answer
	if answer == ' ' or '':
		expected = ''
	context.tc.assertEquals(expected, actual)


@when(u'{user}点击系统回复的链接')
def step_tmpl(context, user):
	url = "%s&fmt=%s" % (context.link_url, context.member.token)
	response = context.client.get(url)

@when(u"修改{user}的签到时间为前一天")
def step_impl(context, user):
	signParticipance = SignParticipance.objects.get(member_id=context.member.id)
	created_at = signParticipance.created_at
	signParticipance.update(set__created_at = created_at-timedelta(days=1))
	__change_sign_date(context.member.id,1)

#只修改参与时间
def __change_sign_date(member_id,days):
	signParticipance = SignParticipance.objects.get(member_id=member_id)
	latest_date = signParticipance.latest_date
	signParticipance.update(set__latest_date = latest_date-timedelta(days))

@When(u'{webapp_user_name}把{webapp_owner_name}的签到活动链接分享到朋友圈')
def step_impl(context, webapp_user_name, webapp_owner_name):
	context.shared_url = context.link_url

@When(u'{webapp_user_name}点击{shared_webapp_user_name}分享的签到链接进行签到')
def step_impl(context, webapp_user_name, shared_webapp_user_name):
	webapp_owner_id = context.webapp_owner_id
	user = User.objects.get(id=webapp_owner_id)
	openid = "%s_%s" % (webapp_user_name, user.username)
	member = member_api.get_member_by_openid(openid, context.webapp_id)
	if member.is_subscribed: #非会员不可签到
		appRecordId = __get_sign_record_id(webapp_owner_id)
		params = {
			'webapp_owner_id': webapp_owner_id,
			'id': appRecordId
		}
		response = context.client.post('/m/apps/sign/api/sign_participance/?_method=put', params)
	else:
		pass

@When(u'{webapp_user_name}通过弹出的二维码关注{mp_user_name}的公众号')
def step_impl(context, webapp_user_name, mp_user_name):
	context.execute_steps(u"when %s关注%s的公众号" % (webapp_user_name, mp_user_name))
	webapp_owner_id = context.webapp_owner_id
	user = User.objects.get(id=webapp_owner_id)
	openid = "%s_%s" % (webapp_user_name, user.username)
	member = member_api.get_member_by_openid(openid, context.webapp_id)
	# 因没有可用的API处理Member相关的source字段, 暂时直接操作Member对象
	Member.objects.filter(id=member.id).update(source=SOURCE_MEMBER_QRCODE)

@when(u"{user}在微信中向{mp_user_name}的公众号发送消息'{message}'于'{date}'")
def step_impl(context, user, mp_user_name, message, date):
	if not hasattr(context,"latest_date"):
		context.latest_date = {
			user : bdd_util.get_date(date)
		}
	signParticipance = SignParticipance.objects(member_id=context.member.id)
	if signParticipance:
		timedelta = (bdd_util.get_date(date) - context.latest_date[user]).days
		__change_sign_date(context.member.id,timedelta)#将上一次签到时间向前调整
		context.execute_steps(u"when %s在微信中向%s的公众号发送消息'%s'" % (user, mp_user_name, message))
	else:
		context.execute_steps(u"when %s在微信中向%s的公众号发送消息'%s'" % (user, mp_user_name, message))
		#首次签到的话，将首次签到时间置为设定的时间
		signParticipance.update(set__created_at = bdd_util.get_date(date))
	#如果是另一个用户签到了，创建新的最近一次签到时间到dict里
	if user not in context.latest_date:
		context.latest_date[user] = bdd_util.get_date(date)
	#对比时间，记录最后一次签到时间
	if context.latest_date[user] < bdd_util.get_date(date):
		context.latest_date[user] = bdd_util.get_date(date)
	context.need_change_date = True
	#因为无法在这句里更改签到的最后一次签到时间，否则每次跟现在的时间去做对比，都不算是连续签到
	#暂时先把修改最后一次签到时间的操作放在“then获得会员签到统计列表”的steps中