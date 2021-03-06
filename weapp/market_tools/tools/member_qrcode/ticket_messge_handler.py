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

from watchdog.utils import watchdog_fatal, watchdog_error
from weixin.message.handler.event_handler import *

from util import *
"""
"""
class QrcodeHandler(MessageHandler):
	
	def name(self):
		return "answer game handler"
	def handle(self, context, is_from_simulator=False):
		message = context.message
		username = message.fromUserName
		user_profile = context.user_profile

		if not hasattr(context.message, 'event'):
			return None

		if message.event != 'subscribe':
			return None

		if not hasattr(context.message, 'ticket') or context.message.ticket is None:
			return None
		ticket = context.message.ticket

		if not hasattr(context.message, 'eventKey') or context.message.eventKey is None or ticket == '':
			return None
		
		is_member_qrcode = update_member_qrcode_log(user_profile, context.member, ticket)
		#用于优化如果是会员推广扫描则不进入渠道二维码处理买
		context.is_member_qrcode = is_member_qrcode
		return None



	