﻿# -*- coding: utf-8 -*-

import time
from collections import OrderedDict

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError
from django.utils.importlib import import_module

from utils.cache_util import GET_CACHE, SET_CACHE
from apps.customerized_apps.powerme import models as app_models
from modules.member.models import Member


class Command(BaseCommand):
	help = 'start powerme stats task'
	args = ''
	
	def handle(self, **options):
		print 'powerme timer task start...'
		start_time = time.time()

		powerlog_bid2data = {p.belong_to: p for p in app_models.PowerLog.objects()}
		need_del_powerlogs_ids = []
		for powerme in app_models.PowerMe.objects():
			record_id = str(powerme.id)
			print '================update data start %s' % record_id
			#统计助力值
			if powerlog_bid2data.has_key(record_id):
				power_logs = powerlog_bid2data[record_id]
				power_member_ids = [p.power_member_id for p in power_logs]
				member_id2subscribe = {m.id: m.is_subscribed for m in Member.objects.filter(id__in=power_member_ids)}
				power_logs = [p for p in power_logs if member_id2subscribe[p.power_member_id]]
				power_log_ids = [p.id for p in power_logs]
				need_power_member_ids = [p.be_powered_member_id for p in power_logs]
				#计算助力值
				need_power_member_id2power = {}
				for m_id in need_power_member_ids:
					if not need_power_member_id2power.has_key(m_id):
						need_power_member_id2power[m_id] = 1
					else:
						need_power_member_id2power[m_id] += 1
				for m_id in need_power_member_id2power.keys():
					app_models.PowerMeParticipance.objects(belong_to=record_id,member_id=m_id).update(inc__power=need_power_member_id2power[m_id])
				#更新已关注会员的助力详情记录
				detail_power_member_ids = [p.power_member_id for p in power_logs]
				app_models.PoweredDetail.objects(belong_to=record_id, power_member_id__in=detail_power_member_ids).update(set__has_powered=True)
				need_del_powerlogs_ids += power_log_ids
			print '================update data end %s' % record_id
			#统计助力排名
			print '================set cache start %s' % record_id
			cache_key = 'apps_powerme_%s' % record_id
			participances = app_models.PowerMeParticipance.objects(belong_to=record_id, has_join=True).order_by('-power', 'created_at')
			participances_dict = {}
			participances_list = []
			total_participant_count = participances.count()

			member_ids = [p.member_id for p in participances]
			member_id2member = {m.id: m for m in Member.objects.filter(id__in=member_ids)}
			rank = 0 #排名
			for p in participances:
				rank += 1
				temp_dict = {
					'rank': rank,
					'member_id': p.member_id,
					'user_icon': member_id2member[p.member_id].user_icon,
					'username': member_id2member[p.member_id].username_size_ten,
					'power': p.power
				}
				participances_dict[p.member_id] = temp_dict
				participances_list.append(temp_dict)
			# 取前100位
			participances_list = participances_list[:100]
			SET_CACHE(cache_key,{
				'participances_dict': participances_dict,
				'participances_list': participances_list,
				'total_participant_count': total_participant_count
			})
			print '================set cache end %s' % record_id

		#删除计算过的log
		app_models.PowerLog.objects(id__in=need_del_powerlogs_ids).delete()
		end_time = time.time()
		diff = (end_time-start_time)*1000
		print 'powerme timer task end...expend %s' % diff
