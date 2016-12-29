# -*- coding: utf-8 -*-

__author__ = 'bert'
# from __future__ import absolute_import

import time, urlparse
from django.conf import settings
from django.db.models import F

from core.exceptionutil import unicode_full_stack

from core import emotion

from watchdog.utils import watchdog_fatal, watchdog_error, watchdog_info

from modules.member.models import *
from datetime import datetime

# from weixin.message.handler.weixin_message import WeixinMessageTypes
# from weixin.message.message import util as message_util
# from weixin.message.message.models import Message
# from weixin.message.qa.models import Rule
from weixin.user.models import WeixinUser, get_token_for

from account.social_account.models import SocialAccount
from account import models as account_models

from celery import task

import util as member_util
from account.social_account.account_info import get_social_account_info
from utils.string_util import byte_to_hex, hex_to_byte
from member.member_grade import auto_update_grade
import member_settings
# @task
# def process_error_openid(openid, user_profile):
# 	print 'call process_error_openid start'
# 	_process_error_openid(openid, user_profile)
# 	print 'OK'


@task
def update_member_pay_info(order):
	webapp_user_id = order.webapp_user_id
	member = WebAppUser.get_member_by_webapp_user_id(webapp_user_id)
	if member:
		try:
			unit_price = (member.pay_money + order.final_price)/(member.pay_times + 1)
			Member.objects.filter(id=member.id).update(pay_money=F('pay_money')+order.final_price, pay_times=F('pay_times')+1, unit_price=unit_price, last_pay_time=order.payment_time)
		except:
			notify_message = u"update_member_pay_info member_id:{}, cause:\n{}".format(member.id, unicode_full_stack())
			watchdog_error(notify_message)


def update_member_integral(member_id, follower_member_id, integral_increase_count, event_type, webapp_user_id, reason="", manager=""):
	#time.sleep(0.5)
	integral_increase_count = int(integral_increase_count)
	member = Member.objects.get(id = member_id)
	if follower_member_id:
		follower_member = Member.objects.get(id = follower_member_id)
	else:
		follower_member = None

	if integral_increase_count == 0:
		return None

	current_integral = member.integral + integral_increase_count
	try:
		# update_grade_flag =False
		# if integral_increase_count > 0 and event_type != RETURN_BY_SYSTEM and event_type!=RETURN_BY_CANCEl_ORDER:
		# 	member.experience += integral_increase_count
		# 	update_grade_flag = True
		member.integral = F('integral') + integral_increase_count
		member.save()
		#Member.objects.filter(id = member_id).update(integral=F('integral')+integral_increase_count)
		MemberIntegralLog.objects.create(
				member = member,
				follower_member_token = follower_member.token if follower_member else '',
				integral_count = integral_increase_count,
				event_type = event_type,
				webapp_user_id = webapp_user_id,
				reason=reason,
				current_integral=current_integral,
				manager=manager
			)
	except:
		notify_message = u"update_member_integral member_id:{}, cause:\n{}".format(member.id, unicode_full_stack())
		watchdog_error(notify_message)
	# if update_grade_flag:
	# 	auto_update_grade(member=member)

@task(bind=True)
def increase_intgral_for_be_member_first(self, member_id, webapp_id, event_type):
	try:
		if IntegralStrategySttings.objects.filter(webapp_id=webapp_id).count() > 0:
			integral_stting = IntegralStrategySttings.objects.filter(webapp_id=webapp_id)[0]
			update_member_integral(member_id, 0, integral_stting.be_member_increase_count, event_type, 0)
	except:
		notify_message = u"increase_intgral_for_be_member_first member_id:{}, cause:\n{}".format(member_id, unicode_full_stack())
		watchdog_error(notify_message)
		raise self.retry()

	"""
	防止数据库锁
	"""
	try:
		update_member_from_weixin_api(member_id, webapp_id)
	except:
		notify_message = u"member_id:{} increase_intgral_for_be_member_first update_member_from_weixin_api cause:\n{}".format(member_id, unicode_full_stack())
		watchdog_error(notify_message)



@task
def create_member_info(member_id, name, sex):
	if MemberInfo.objects.filter(member_id=member_id).count() > 0:
		return

	MemberInfo.objects.create(
			member = Member.objects.get(id=member_id),
			name = name,
			sex = sex,
			is_binded=False
			)


@task
def process_oauth_member_relation_and_source(fmt, member_id, is_new_created_member=False):
	print 'received watchdog process_oauth_member_relation_and_source'
	_process_oauth_member_relation_and_source(fmt, member_id, is_new_created_member)
	return 'OK'

def _process_oauth_member_relation_and_source(fmt, member_id, is_new_created_member=False):
	from modules.member.integral_new import increase_for_click_shared_url
	member = Member.objects.get(id=member_id)
	try:
		if fmt and member and fmt != member.token:
			#建立关系，更新会员来源
			follow_member = Member.objects.get(token=fmt)
			if follow_member.webapp_id != member.webapp_id:
				return

			if is_new_created_member:
				MemberFollowRelation.objects.create(member_id=follow_member.id, follower_member_id=member.id, is_fans=is_new_created_member)
				MemberFollowRelation.objects.create(member_id=member.id, follower_member_id=follow_member.id, is_fans=False)
				Member.objects.filter(id=member_A.id).update(fans_count=F(fans_count)+1)
				member.source = SOURCE_BY_URL
				member.save()
			elif MemberFollowRelation.objects.filter(member_id=member.id, follower_member_id=follow_member.id).count() == 0:
				MemberFollowRelation.objects.create(member_id=follow_member.id, follower_member_id=member.id, is_fans=is_new_created_member)
				MemberFollowRelation.objects.create(member_id=member.id, follower_member_id=follow_member.id, is_fans=False)
			#点击分享链接给会员增加积分
			try:
				increase_for_click_shared_url(follow_member, member, request.get_full_path())
			except:
				notify_message = u"increase_for_click_shared_url:('member_id':{}), cause:\n{}".format(member.id, unicode_full_stack())
				watchdog_fatal(notify_message)
	except:
		notify_message = u"('fmt':{}), 处理分享信息process_oauth_member_relation_and_source cause:\n{}".format(fmt, unicode_full_stack())
		watchdog_fatal(notify_message)

def update_member_from_weixin_api(member_id, webapp_id):
	social_account = MemberHasSocialAccount.objects.filter(member_id=member_id)[0].account
	#SocialAccount.objects.get(id=social_account_id)
	user_profile = account_models.UserProfile.objects.get(webapp_id=social_account.webapp_id)
	social_account_info = get_social_account_info(social_account, user_profile)
	#member_grade = MemberGrade.get_default_grade(social_account.webapp_id)
	sex = 0
	if social_account_info:
		member_nickname = social_account_info.nickname if social_account_info else ''
		if isinstance(member_nickname, unicode):
			member_nickname_str = member_nickname.encode('utf-8')
		else:
			member_nickname_str = member_nickname
		username_hexstr = byte_to_hex(member_nickname_str)

		if not username_hexstr:
			username_hexstr = ''
		sex = social_account_info.sex
		if sex == '' or sex == None:
			sex = 0
		Member.objects.filter(id=member_id).update(user_icon=social_account_info.head_img,
					update_time = datetime.now(),
					username_hexstr=username_hexstr,
					#is_subscribed=social_account_info.is_subscribed,
					city=social_account_info.city,
					province=social_account_info.province,
					country=social_account_info.country,
					sex=sex,
					)

	create_member_info(member_id, '', sex)

@task(bind=True)
def record_member_pv(self, member_id, url, page_title=''):
	try:
		"""
		记录会员访问轨迹
		"""
		member = Member.objects.get(id=member_id)
		if member and url.find('api') == -1:
			MemberBrowseRecord.objects.create(
				title = page_title,
				url = url,
				member=member
			)

		#访问商品详情单独写到一张表里，方便统计商品的访问记录  duhao  20161221
		if 'module=mall' in url and 'model=product' in url and 'model=products' not in url:
			result = urlparse.urlparse(url)
			params = urlparse.parse_qs(result.query, True)
			owner_id = params['woid'][0]
			product_id = params['rid'][0]
			referer = ''
			MemberBrowseProductRecord.objects.create(
				title = page_title,
				url = url,
				member=member,
				owner_id=owner_id,
				product_id=product_id,
				referer=referer
			)
	except:
		notify_message = u"record_member_pv,member_id:{} cause:\n{}".format(member_id, unicode_full_stack())
		watchdog_error(notify_message)
		raise self.retry()


@task(bind=True)
def task_member_base_info_update(self, member_id):
	try:
		"""
		task 更新会员头像信息
		"""
		member = Member.objects.get(id=member_id)
		user_profile =  account_models.UserProfile.objects.get(webapp_id=member.webapp_id)
		member_util.member_basic_info_updater(user_profile, member)
		if not member.user_icon or member.user_icon == '':
			member_util.member_basic_info_updater(user_profile, member)
	except:
		notify_message = u"task 更新会员头像信息,member_id:{} cause:\n{}".format(member_id, unicode_full_stack())
		watchdog_error(notify_message)
		raise self.retry()


def post_pay_tasks(request, order):
	"""
		处理分享链接
	"""
	try:
		member = request.member
		follow_member_token  = request.COOKIES.get(member_settings.FOLLOWED_MEMBER_TOKEN_SESSION_KEY, None)
		shared_url_digest = request.COOKIES.get(member_settings.FOLLOWED_MEMBER_SHARED_URL_SESSION_KEY, None)
		if member and follow_member_token and member.token != follow_member_token and shared_url_digest:
			process_payment_with_shared_info.delay(member.id, follow_member_token, shared_url_digest)
	except:
	 	pass

	from middleware import RemoveSharedInfoMiddleware
	request.META[RemoveSharedInfoMiddleware.SHOULD_REMOVE_SHARED_URL_SESSION_FLAG] = True

	"""

		更新会员购买信息
	"""
	update_member_pay_info_task.delay(order.id)


@task(bind=True,max_retries=3)
def process_payment_with_shared_info(self, member_id, follow_member_token, shared_url_digest):
	try:
		member = Member.objects.get(id=member_id)
		try:
			follow_member = Member.objects.get(token = follow_member_token)
		except:
			follow_member = None
		if follow_member and member != follow_member and member.webapp_id == follow_member.webapp_id:
			MemberSharedUrlInfo.objects.filter(member=follow_member, shared_url_digest=shared_url_digest).update(leadto_buy_count=F('leadto_buy_count')+1)
	except:
		notify_message = u"process_payment_with_shared_info member_id:{}, cause:\n{}".format(member_id, unicode_full_stack())
		watchdog_error(notify_message)
		raise self.retry()


@task(bind=True, max_retries=3)
def update_member_pay_info_task(self, order_id):
	from mall.models import Order
	order = Order.objects.get(id = order_id)
	webapp_user_id = order.webapp_user_id
	member = WebAppUser.get_member_by_webapp_user_id(webapp_user_id)
	if member:
		try:
			unit_price = (member.pay_money + order.final_price)/(member.pay_times + 1)
			Member.objects.filter(id=member.id).update(pay_money=F('pay_money')+order.final_price, pay_times=F('pay_times')+1, unit_price=unit_price, last_pay_time=order.payment_time)
		except:
			notify_message = u"update_member_pay_info member_id:{}, cause:\n{}".format(webapp_user_id, unicode_full_stack())
			watchdog_error(notify_message)
			raise self.retry()

@task(bind=True, max_retries=3)
def send_order_template_message(self, webapp_id, order_id, send_point):
	try:
		from market_tools.tools.template_message.module_api import send_order_template_message
		send_order_template_message(webapp_id, order_id, send_point)
	except:
		alert_message = u"post_pay_order_handler 发送模板消息失败, cause:\n{}".format(unicode_full_stack())
		watchdog_warning(alert_message)
		raise self.retry()
