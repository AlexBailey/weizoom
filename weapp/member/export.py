# -*- coding: utf-8 -*-

import time
from datetime import timedelta, datetime, date
import urllib, urllib2
import os
import json

from django.http import HttpResponseRedirect, HttpResponse
from django.template import Context, RequestContext
from django.contrib.auth.decorators import login_required, permission_required
from django.conf import settings
from django.shortcuts import render_to_response
from django.contrib.auth.models import User, Group, Permission
from django.contrib import auth
from django.db.models import Q

from core.jsonresponse import JsonResponse, create_response
from core import dateutil


MEMBER_FIRST_NAV = 'member'
MEMBERS = 'members'
MEMBER_TAG = 'memberTag'
MEMBER_GRADE = 'memberGrade'
MEMBER_QRCODE = 'memberQrcode'
MEMBER_SPREAD = 'memberSpread'

MEMBER_NAV = {
	'section': u'',
	'navs': [
		{
			'name': MEMBERS,
			'title': u'会员列表',
			'url': '/member/member_list/',
            'permission': 'manage_member_list'
		},
		{
			'name': MEMBER_TAG,
			'title': u'会员分组',
			'url': '/member/member_tags/',
            'permission': 'manage_member_tag'
		},
		{
			'name': MEMBER_GRADE,
			'title': u'会员等级',
			'url': '/mall2/member_grade_list/',
            'permission': 'manage_member_grade'
		},
		{
			'name': MEMBER_QRCODE,
			'title': u'推广扫码',
			'url': '/member/member_qrcode/',
            'permission': 'manage_member_qrcode'
		},
		{
			'name': MEMBER_SPREAD,
			'title': u'会员关系',
			'url': '/member/member_spread/',
            'permission': 'manage_member_qrcode'
		}
	]
}

from account.account_util import get_token_for_logined_user
def get_second_navs(request):
	if request.user.username == 'manager':
		pass
	else:
		second_navs = [MEMBER_NAV]#webapp_module_views.get_modules_page_second_navs(request)

	return second_navs





