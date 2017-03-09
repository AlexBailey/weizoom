# -*- coding: utf-8 -*-

__author__ = 'bert'

from weixin.message.handler.keyword_handler import *
import time
from datetime import timedelta, datetime, date
import os
import json
import hashlib
import MySQLdb

from BeautifulSoup import BeautifulSoup

from django.http import HttpResponseRedirect, HttpResponse, HttpRequest
from django.template import Context, RequestContext
from django.contrib.auth.decorators import login_required, permission_required
from django.conf import settings
from django.shortcuts import render_to_response
from django.contrib.auth.models import User, Group, Permission
from django.contrib import auth
from django.test import Client
from django.db.models import Q

from core import emotion

from watchdog.utils import watchdog_fatal, watchdog_error
from weixin.message.handler.event_handler import *

from channel_qrcode_util import *
from mall.promotion import models as promotion_models
from market_tools.tools.channel_qrcode import models

from apps.customerized_apps.rebate import models as rebate_models

"""
"""
class ChannelQrcodeHandler(MessageHandler):

	def name(self):
		return "ChannelQrcodeHandler"

	def handle(self, context, is_from_simulator=False):
		message = context.message

		if message.is_optimization_message:
			print 'ChannelQrcodeHandler only handle is_optimization_message = true'
			return None

		username = message.fromUserName
		user_profile = context.user_profile
		member = context.member

		if not hasattr(context.message, 'event'):
			return None

		if not hasattr(context.message, 'ticket') or context.message.ticket is None:
			return None
		ticket = context.message.ticket

		if not hasattr(context.message, 'eventKey') or context.message.eventKey is None or ticket == '':
			return None

		if member and (hasattr(member, 'is_new') is False):
			member.is_new = False

		#优化处理
		if hasattr(context, 'is_member_qrcode') and (context.is_member_qrcode is True):
			return None

		#检查是否返利活动中有这个
		if rebate_models.Rebate.objects(ticket=ticket, status=rebate_models.STATUS_RUNNING):
			print 'apps.Rebate has the same ticket: %s, so let rebate handler handle it' % ticket
			return None

		if user_profile.user_id in [467,154] and \
			check_new_channel_qrcode_ticket(ticket, user_profile):
			#用户可以重复领取不同的优惠券
			can_has_coupon = False
			qrcode_award = MemberChannelQrcodeAwardContent.objects.get(owner_id=user_profile.user_id)
			award_type = qrcode_award.scanner_award_type
			award_content = qrcode_award.scanner_award_content
			if award_type == AWARD_COUPON:
				if ChannelQrcodeSettings.objects.filter(ticket=ticket, owner_id=user_profile.user_id).count() > 0:
					channel_qrcode = ChannelQrcodeSettings.objects.filter(ticket=ticket, owner_id=user_profile.user_id)[0]
					coupon_ids = ChannelQrcodeToMemberLog.objects.filter(channel_qrcode=channel_qrcode, member=member)[0].coupon_ids
					if award_content not in coupon_ids.split(','):
						can_has_coupon = True

			if member.is_new or can_has_coupon:
				create_new_channel_qrcode_has_memeber(user_profile, context.member, ticket, member.is_new)
			return None

		channel_qrcode = ChannelQrcodeSettings.objects.filter(ticket=ticket, owner_id=user_profile.user_id).first()
		if channel_qrcode:
			if user_profile.user.username in ['ceshi01','kftengyi'] and channel_qrcode.bing_member_id > 0: #腾易微众定制需求
				from modules.member.models import TengyiMember, TengyiMemberRelation
				if TengyiMember.objects.filter(member_id=channel_qrcode.bing_member_id).count() > 0:
					if TengyiMemberRelation.objects.filter(member_id=member.id).count() <= 0:
						print '============================'
						print 'TengyiMemberRelation recoding by channel_qrcode'
						print '============================'
						TengyiMemberRelation.objects.create(
							member_id=member.id,
							recommend_by_member_id=channel_qrcode.bing_member_id,
						)
			create_channel_qrcode_has_memeber_restructure(channel_qrcode, user_profile, context.member, ticket, member.is_new)
			msg_type, detail = get_response_msg_info_restructure(channel_qrcode, user_profile)
			if msg_type != None:
				#from_weixin_user = self._get_from_weixin_user(message)
				#token = self._get_token_for_weixin_user(user_profile, from_weixin_user, is_from_simulator)
				if msg_type == 'text' and detail:
					if is_from_simulator:
						return generator.get_text_response(username, message.toUserName, emotion.change_emotion_to_img(detail), username, user_profile)
					else:
						return generator.get_text_response(username, message.toUserName, detail, username, user_profile)
				if msg_type == 'news' and get_material_news_info(detail):
					news = get_material_news_info(detail)
					return generator.get_news_response(username, message.toUserName, news, username)
		# elif check_channel_qrcode_ticket(ticket, user_profile):
		# 	#if member.is_new:
		# 	create_channel_qrcode_has_memeber(user_profile, context.member, ticket, member.is_new)

		# 	msg_type, detail = get_response_msg_info(ticket, user_profile)

		# 	if msg_type != None:
		# 		from_weixin_user = self._get_from_weixin_user(message)
		# 		#token = self._get_token_for_weixin_user(user_profile, from_weixin_user, is_from_simulator)
		# 		if msg_type == 'text' and detail:
		# 			if is_from_simulator:
		# 				return generator.get_text_response(username, message.toUserName, emotion.change_emotion_to_img(detail), username, user_profile)
		# 			else:
		# 				return generator.get_text_response(username, message.toUserName, detail, username, user_profile)
		# 		if msg_type == 'news' and get_material_news_info(detail):
		# 			news = get_material_news_info(detail)
		# 			return generator.get_news_response(username, message.toUserName, news, username)

		return None

