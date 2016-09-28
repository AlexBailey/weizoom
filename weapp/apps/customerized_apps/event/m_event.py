# -*- coding: utf-8 -*-

import json
from datetime import datetime

from django.conf import settings
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.db.models import F
from django.contrib.auth.decorators import login_required

from core import resource
from core import paginator
from core.jsonresponse import create_response

import models as app_models
import export
from apps import request_util
from termite2 import pagecreater
from termite import pagestore as pagestore_manager
import weixin.user.models as weixin_models

class Mevent(resource.Resource):
	app = 'apps/event'
	resource = 'm_event'
	
	def get(request):
		"""
		响应GET
		"""
		try:
			if 'id' in request.GET:
				id = request.GET['id']
				###############重构之后，访问老数据，直接重定向到重构活动报名##########
				try:
					related_page_id = app_models.event.objects.get(id=id).related_page_id
					m_marketapp_url = 'http://{}/m/apps/event/m_event/?woid={}&page_id={}'.format(settings.MARKET_MOBILE_DOMAIN, request.webapp_owner_id, related_page_id)
					return HttpResponseRedirect(m_marketapp_url)
				except:
					c = RequestContext(request, {
						'is_deleted_data': True
					})
					return render_to_response('workbench/wepage_webapp_page.html', c)
				###############################################################

				isPC = request.GET.get('isPC',0)
				participance_data_count = 0
				isMember = False
				auth_appid_info = None
				permission = ''
				share_page_desc = ''
				description2 = ''
				description_is_empty = False
				thumbnails_url = '/static_v2/img/thumbnails_event.png'
				if not isPC:
					isMember = request.member and request.member.is_subscribed
					# if not isMember:
					# 	from weixin.user.util import get_component_info_from
					# 	component_info = get_component_info_from(request)
					# 	auth_appid = weixin_models.ComponentAuthedAppid.objects.filter(component_info=component_info, user_id=request.GET['webapp_owner_id'])[0]
					# 	auth_appid_info = weixin_models.ComponentAuthedAppidInfo.objects.filter(auth_appid=auth_appid)[0]
				if 'new_app:' in id:
					project_id = id
					activity_status = u"未开始"
				else:
					#termite类型数据
					try:
						record = app_models.event.objects.get(id=id)
					except:
						c = RequestContext(request,{
							'is_deleted_data': True
						})
						return render_to_response('workbench/wepage_webapp_page.html', c)
					activity_status = record.status_text
					share_page_desc = record.name
					now_time = datetime.today().strftime('%Y-%m-%d %H:%M')
					data_start_time = record.start_time.strftime('%Y-%m-%d %H:%M')
					data_end_time = record.end_time.strftime('%Y-%m-%d %H:%M')
					data_status = record.status
					if data_status <= 1:
						if data_start_time <= now_time and now_time < data_end_time:
							record.update(set__status=app_models.STATUS_RUNNING)
							activity_status = u'进行中'
						elif now_time >= data_end_time:
							record.update(set__status=app_models.STATUS_STOPED)
							activity_status = u'已结束'
					project_id = 'new_app:event:%s' % record.related_page_id

					if request.member:
						participance_data_count = app_models.eventParticipance.objects(belong_to=id, member_id=request.member.id).count()

					pagestore = pagestore_manager.get_pagestore('mongo')
					page = pagestore.get_page(record.related_page_id, 1)
					permission = page['component']['components'][0]['model']['permission']
					description2 = page['component']['components'][1]['model']['description2']
					description_is_empty = False if page['component']['components'][1]['model']['description2'] else True
				is_already_participanted = (participance_data_count > 0)
				if  is_already_participanted:
					try:
						event_detail,activity_status = get_result(id,request.member.id)
					except:
						c = RequestContext(request,{
							'is_deleted_data': True
						})
						return render_to_response('event/templates/webapp/is_already_participanted.html', c)
					c = RequestContext(request, {
						'event_detail': event_detail,
						'record_id': id,
						'activity_status': activity_status,
						'page_title': '活动报名',
						'app_name': "event",
						'resource': "event",
						'description2': description2,
						'hide_non_member_cover': True #非会员也可使用该页面
					})
					return render_to_response('event/templates/webapp/is_already_participanted.html', c)
				else:
					request.GET._mutable = True
					request.GET.update({"project_id": project_id})
					request.GET._mutable = False
					html = pagecreater.create_page(request, return_html_snippet=True)
					c = RequestContext(request, {
						'record_id': id,
						'activity_status': activity_status,
						'is_already_participanted': (participance_data_count > 0),
						'page_title': '活动报名',
						'page_html_content': html,
						'app_name': "event",
						'resource': "event",
						'hide_non_member_cover': True, #非会员也可使用该页面
						'isPC': False if request.member else True,
						'isMember': isMember,
						'auth_appid_info': auth_appid_info,
						'permission': permission,
						'share_page_desc': share_page_desc,
						'share_img_url': thumbnails_url,
						'description_is_empty': description_is_empty
					})
					return render_to_response('workbench/wepage_webapp_page.html', c)
			else:
				record = None
				c = RequestContext(request, {
					'record': record
				})
				return render_to_response('event/templates/webapp/m_event.html', c)
		except:
			pass

def get_result(id,member_id):
	event_detail ={}
	event_event = app_models.event.objects.get(id=id)
	event_detail['name'] = event_event['name']
	event_detail['end_time'] = event_event['end_time'].strftime('%Y-%m-%d')

	related_page_id = event_event.related_page_id
	activity_status = event_event.status_text

	pagestore = pagestore_manager.get_pagestore('mongo')
	page = pagestore.get_page(related_page_id, 1)
	page_info = page['component']['components'][0]['model']
	event_detail['subtitle'] = page_info['subtitle']
	event_detail['description'] = page_info['description']
	prize_type = page_info['prize']['type']
	event_detail['prize_type'] = prize_type
	if prize_type == 'coupon':
		prize_data = page_info['prize']['data']['name']
	else:
		prize_data = page_info['prize']['data']
	event_detail['prize_data'] = prize_data

	return event_detail,activity_status