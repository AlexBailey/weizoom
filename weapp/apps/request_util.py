# -*- coding: utf-8 -*-

from django.db.models import F
from django.db import IntegrityError, transaction

from mall.promotion.models import CouponRule
from mall.promotion import models as promotion_models
from market_tools.tools.coupon.util import consume_coupon

__author__ = 'robert'

from datetime import datetime
import json

from django.db.models import Q
from django.http import HttpResponseRedirect, HttpResponse, HttpRequest, Http404
from django.template import Context, RequestContext
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.shortcuts import render_to_response, render
from django.contrib.auth.models import User
from django.contrib import auth

from account.views import save_base64_img_file_local_for_webapp
from customerized_apps import mysql_models as mongo_models

#===============================================================================
# __get_fields_to_be_save : 获得待存储的数据
#===============================================================================
def get_fields_to_be_save(request):
	fields = request.POST.dict()
	fields['created_at'] = datetime.today()

	webapp_user = getattr(request, 'webapp_user', None)
	if webapp_user:
		fields['webapp_user_id'] = request.webapp_user.id

	member = getattr(request, 'member', None)
	if member:
		fields['member_id'] = request.member.id
		fields['owner_id'] = request.user.id
	else:
		fields['owner_id'] = request.manager.id

	if 'prize' in request.POST:
		fields['prize'] = json.loads(fields['prize'])

	if 'termite_data' in fields:
		fields['termite_data'] = json.loads(fields['termite_data'])
		for item in fields['termite_data']:
			att_url = []
			if fields['termite_data'][item]['type']=='appkit.uploadimg':
				fields['uploadImg'] = json.loads(fields['termite_data'][item]['value'])
				for picture in fields['uploadImg']:
					att_url.append(picture)
				fields['termite_data'][item]['value'] = att_url
	return fields

def get_consume_coupon(owner_id, app_name, app_id, rule_id, member_id):
	'''

	@param owner_id:
	@param app_name:
	@param app_id:
	@param rule_id:
	@param member_id:
	@param has_coupon_count: 表示在抽奖活动里某个会员获得优惠券的数量
	@return:
	'''
	coupon = None
	curr_coupon_count = 0
	rules = CouponRule.objects.filter(id=rule_id, owner_id=owner_id)
	if rules.count() <= 0:
		coupon_message = u'该优惠券使用期已过，不能领取！'
		return coupon, coupon_message, curr_coupon_count
	rule = rules.first()
	if rule and rule.end_date <= datetime.today():
		coupon_message = u'该优惠券使用期已过，不能领取！'
	else:
		curr_coupon_count = rule.remained_count
		coupon, coupon_message = consume_coupon(owner_id, rule_id, member_id)
		# with transaction.atomic():
		# 	coupon = promotion_models.Coupon.objects.select_for_update().filter(coupon_rule_id=rule_id, member_id=0, status=promotion_models.COUPON_STATUS_UNGOT).first()
		# 	if coupon:
		# 		coupon.status = promotion_models.COUPON_STATUS_UNUSED
		# 		coupon.member_id = member_id
		# 		coupon.provided_time = datetime.today()
		# 		coupon.coupon_record_id = 0
		# 		coupon.save()
        #
		# 		if has_coupon_count:
		# 			rules.update(remained_count=F('remained_count') - 1, get_count=F('get_count') + 1)
		# 		else:
		# 			rules.update(remained_count=F('remained_count') - 1, get_person_count=F('get_person_count') + 1,
		# 						 get_count=F('get_count') + 1)

	data = {
		'user_id': owner_id,
		'app_name': app_name,
		'app_id': app_id,
		'member_id': member_id,
		'coupon_id': coupon.id if coupon else 0,
		'coupon_msg': coupon_message,
		'created_at': datetime.today()
	}
	consume_coupon_log = mongo_models.ConsumeCouponLog(**data)
	consume_coupon_log.save()
	return coupon, coupon_message, curr_coupon_count


