﻿# -*- coding: utf-8 -*-

import time
from datetime import timedelta,datetime

from django.core.management.base import BaseCommand, CommandError
from core.exceptionutil import unicode_full_stack

from watchdog.utils import watchdog_error, watchdog_info, watchdog_warning
from apps.customerized_apps.group import models as app_models
from modules.member.models import Member
from mall.order.util import update_order_status_by_group_status
from apps.customerized_apps.group.group_participance import send_group_template_message

class Command(BaseCommand):
	help = 'start group stats task'
	args = ''

	def handle(self, *args, **options):
		"""
		"""
		try:
			print 'group timer task start...'
			start_time = time.time()

			"""
			所有已到时间还未完成的团购，置为团购失败
			"""
			all_running_group_relations = app_models.GroupRelations.objects(group_status=app_models.GROUP_RUNNING)
			all_running_group_ids = []
			for group_relation in all_running_group_relations:
				all_running_group_ids.append(group_relation.belong_to)
				timing = (group_relation.created_at + timedelta(days=int(group_relation.group_days)) - datetime.today()).total_seconds()
				if timing <= 0:
					group_relation.update(set__group_status=app_models.GROUP_FAILURE)
					update_order_status_by_group_status(group_relation.id,'failure')
			"""
			所有团购活动已结束的团购活动，置为团购失败
			"""
			all_end_group_ids = []
			now_time = datetime.today().strftime('%Y-%m-%d %H:%M')
			all_activities_with_running_groups = app_models.Group.objects(id__in=all_running_group_ids)
			for group in all_activities_with_running_groups:
				data_end_time = group.end_time.strftime('%Y-%m-%d %H:%M')
				if now_time >= data_end_time:
					all_end_group_ids.append(str(group.id))
			all_end_group_relations = all_running_group_relations.filter(belong_to__in=all_end_group_ids)
			for group_relation in all_end_group_relations:
				group_relation.update(set__group_status=app_models.GROUP_FAILURE)
				update_order_status_by_group_status(group_relation.id,'failure')

			"""
			所有已到15分钟还未开团成功的团购，删除团购记录
			"""
			all_not_start_group_relations = app_models.GroupRelations.objects(group_status=app_models.GROUP_NOT_START)
			for group_relation in all_not_start_group_relations:
				timing_minutes = (datetime.today() - group_relation.created_at).total_seconds() / 60
				if timing_minutes >= 15 :
					group_relation.delete()

			"""
			所有已到15分钟还未完成支付的参与他人团购，删除团购参与记录
			"""
			all_unpaid_group_details = app_models.GroupDetail.objects(is_already_paid=False)
			for group_detail in all_unpaid_group_details:
				timing_minutes = (datetime.today() - group_detail.created_at).total_seconds() / 60
				if timing_minutes >= 15 :
					try:
						all_running_group_relations.get(id=group_detail.relation_belong_to).update(
							dec__grouped_number=1,
							pop__grouped_member_ids=group_detail.grouped_member_id
						)
						group_detail.delete()
					except:
						#该团已被删除掉了
						pass

			end_time = time.time()
			diff = (end_time-start_time)*1000
			print 'group timer task end...expend %s' % diff
		except:
			notify_msg = u"处理失败团购错误，cause:\n{}".format(unicode_full_stack())
			watchdog_error(notify_msg)