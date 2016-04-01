# -*- coding: utf-8 -*-
import logging
from celery import task
from modules.member.models import *
from mall.models import Order,ORDER_STATUS_SUCCESSED
from utils.dateutil import now,get_date_after_days

import datetime

@task
def update_member_purchase_frequency(webapp_id):
	now = datetime.datetime.now()
	members = Member.objects.filter(webapp_id=webapp_id, status__in=[SUBSCRIBED, CANCEL_SUBSCRIBED])
	date_before_30 = get_date_after_days(now,-30)
	info = "%s:%s" % (webapp_id, now)
	logging.info(info)
	logging.info('start')
	for member in members:
		webapp_user_ids = member.get_webapp_user_ids
		purchase_count_30days = orders.filter(webapp_user_id__in=webapp_user_ids, payment_time__gte=date_before_30,status=ORDER_STATUS_SUCCESSED).count()
		Member.objects.filter(id=member.id).update(purchase_frequency=purchase_count_30days)
	logging.info('end')
