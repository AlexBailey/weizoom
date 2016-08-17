# -*- coding: utf-8 -*-
import json
from behave import *
from mall.promotion.models import CouponRule
from modules.member.models import MemberGrade, MemberTag, Member
from test import bdd_util
import logging
from market_tools.tools.distribution.models import ChannelDistributionQrcodeSettings, ChannelDistributionQrcodeHasMember,\
ChannelDistributionDetail
from django.core.serializers import serialize
from utils.string_util import byte_to_hex
from django.contrib.auth.models import User
from mall.models import Order


@When(u'{user}扫描渠道二维码"{qrcode_name}"')
def step_impl(context, user, qrcode_name):
	qrcode = ChannelDistributionQrcodeSettings.objects.get(bing_member_title=qrcode_name)
	ticket = qrcode.ticket

	owner = User.objects.get(id=qrcode.owner.id)
	webapp_id = bdd_util.get_webapp_id_via_owner_id(qrcode.owner.id)

	# 模拟收到的消息
	openid = '%s_%s' % (user, owner.username)
	url = '/simulator/api/mp_user/qr_subscribe/?version=2'
	data = {
		"timestamp": "1402211023857",
		"webapp_id": webapp_id,
		"ticket": ticket,
		"from_user": openid
	}
	response = context.client.post(url, data)
	response_data = json.loads(response.content)
	context.qa_result = response_data


@When(u'{webapp_user_name}扫描渠道二维码"{qrcode_name}"于{scan_qrcode_time}')
def step_impl(context, webapp_user_name, qrcode_name, scan_qrcode_time):
	context.execute_steps(u'when %s扫描渠道二维码"%s"' % (webapp_user_name, qrcode_name))
	# name = byte_to_hex(webapp_user_name)
	# member_id = Member.objects.filter(username_hexstr__contains=name)[0].id
	# scan_qrcode_time = bdd_util.get_date(scan_qrcode_time)
	# qrcode = ChannelDistributionQrcodeSettings.objects.get(bing_member_title=qrcode_name)
	member = ChannelDistributionQrcodeHasMember.objects.all().order_by('-id')[0]
	member.created_at = scan_qrcode_time
	member.save()


@When(u'{user}完成订单"{order_id}"')
def step_impl(context, user, order_id):
	order = Order.objects.get(order_id=order_id)
	order.status = 5
	order.save()


@When(u'后台执行channel_distribution_update')
def step_impl(context):
	import os
	os.system('python manage.py channel_distribution_update')

@When(u'{user}已返现给{member_name}金额"{money}"')
def step_impl(context, user, member_name, money):

	logging.info(serialize('json',ChannelDistributionQrcodeHasMember.objects.all()))
	member_name = byte_to_hex(member_name)
	bing_member_id = Member.objects.filter(username_hexstr__contains=member_name)[0].id
	qrcode = ChannelDistributionQrcodeSettings.objects.get(bing_member_id=bing_member_id)

	data = {
		'status': 3,
		'qrcode_id': qrcode.id
	}
	response = context.client.post('/new_weixin/api/channel_distribution_change_status/', data)




@Then(u'{user}获得{vip_name}的交易记录列表')
def step_impl(context, user, vip_name):
	member_name = byte_to_hex(vip_name)
	bing_member_id = Member.objects.filter(username_hexstr__contains=member_name)[0].id
	qrcode = ChannelDistributionQrcodeSettings.objects.get(bing_member_id=bing_member_id)
	expected = json.loads(context.text)

	data = {'qrcode_id': qrcode.id}

	response = context.client.get('/new_weixin/api/channel_distribution_transaction_amount/', data)
	logging.info(response)
	datas = json.loads(response.content)['data']['items']
	actual_list = []
	for data in datas:
		dict = {}
		dict['user_name'] = data['name']
		dict['pay_money'] = float(data['cost_money'])
		dict['cash_back_amount'] = float(data['commission'])
		actual_list.append(dict)

	bdd_util.assert_list(expected, actual_list)


@Then(u'{user}获得{vip_name}的奖励明细列表')
def step_impl(context, user, vip_name):
	member_name = byte_to_hex(vip_name)
	bing_member_id = Member.objects.filter(username_hexstr__contains=member_name)[0].id
	qrcode = ChannelDistributionQrcodeSettings.objects.get(bing_member_id=bing_member_id)
	expected = json.loads(context.text)
	# for expected in expecteds:
	# 	user_name = expected['user_name']
	data = {'qrcode_id': qrcode.id}
	response = context.client.get('/new_weixin/api/channel_distribution_detail/', data)
	datas = json.loads(response.content)['data']['items']
	actual_list = []
	for data in datas:
		dict = {}
		dict['cycle_time_start'] = data['time_cycle_start']
		dict['cycle_time_end'] = data['time_cycle_end']
		dict['commission_return_rate'] = float(data['commission_rate'])
		dict['pay_money'] = float(data['total_money'])
		dict['cash_back_amount'] = float(data['commission'])
		actual_list.append(dict)

	bdd_util.assert_list(expected, actual_list)


@When(u'{user}更改{vip_name}的返现状态为"{status}"')
def step_impl(context, user, vip_name, status):
	member_name = byte_to_hex(vip_name)
	bing_member_id = Member.objects.filter(username_hexstr__contains=member_name)[0].id
	qrcode = ChannelDistributionQrcodeSettings.objects.filter(bing_member_id=bing_member_id)
	if status == u"正在返现":
		qrcode.update(status=2)
