# -*- coding: utf-8 -*-

import json
from datetime import datetime

from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.db.models import F
from django.contrib.auth.decorators import login_required

from core import resource
from core import paginator
from core.jsonresponse import create_response

import models as app_models
from mall import export
from apps import request_util
from modules.member import integral as integral_api
from mall.promotion import utils as mall_api
import termite.pagestore as pagestore_manager

FIRST_NAV = export.MALL_PROMOTION_AND_APPS_FIRST_NAV
COUNT_PER_PAGE = 20

class event(resource.Resource):
	app = 'apps/event'
	resource = 'event'
	
	@login_required
	def get(request):
		"""
		响应GET
		"""
		if 'id' in request.GET:
			project_id = 'new_app:event:%s' % request.GET.get('related_page_id', 0)
			try:
				event = app_models.event.objects.get(id=request.GET['id'])
			except:
				c = RequestContext(request, {
					'first_nav_name': FIRST_NAV,
					'second_navs': export.get_promotion_and_apps_second_navs(request),
					'second_nav_name': export.MALL_APPS_SECOND_NAV,
					'third_nav_name': export.MALL_APPS_EVENT_NAV,
					'is_deleted_data': True
				})
				return render_to_response('event/templates/editor/workbench.html', c)
			is_create_new_data = False

		else:
			event = None
			is_create_new_data = True
			project_id = 'new_app:event:0'

		_, app_name, real_project_id = project_id.split(':')
		if real_project_id != '0':
			pagestore = pagestore_manager.get_pagestore('mongo')
			pages = pagestore.get_page_components(real_project_id)
			if not pages:
				c = RequestContext(request, {
					'first_nav_name': FIRST_NAV,
					'second_navs': export.get_promotion_and_apps_second_navs(request),
					'second_nav_name': export.MALL_APPS_SECOND_NAV,
					'third_nav_name': export.MALL_APPS_EVENT_NAV,
					'is_deleted_data': True
				})
				return render_to_response('event/templates/editor/workbench.html', c)
		
		c = RequestContext(request, {
			'first_nav_name': FIRST_NAV,
			'second_navs': export.get_promotion_and_apps_second_navs(request),
			'second_nav_name': export.MALL_APPS_SECOND_NAV,
            'third_nav_name': export.MALL_APPS_EVENT_NAV,
			'event': event,
			'is_create_new_data': is_create_new_data,
			'project_id': project_id,
			'app_name': 'event'
		});
		
		return render_to_response('event/templates/editor/workbench.html', c)
	
	@login_required
	def api_put(request):
		"""
		响应PUT
		"""
		data = request_util.get_fields_to_be_save(request)
		event = app_models.event(**data)
		event.save()
		
		data = json.loads(event.to_json())
		data['id'] = data['_id']['$oid']
		response = create_response(200)
		response.data = data
		return response.get_response()
	
	@login_required
	def api_post(request):
		"""
		响应POST
		"""
		data = request_util.get_fields_to_be_save(request)
		update_data = {}
		update_fields = set(['name', 'start_time', 'end_time'])
		for key, value in data.items():
			if key in update_fields:
				update_data['set__'+key] = value
		app_models.event.objects(id=request.POST['id']).update(**update_data)
		
		response = create_response(200)
		return response.get_response()
	
	@login_required
	def api_delete(request):
		"""
		响应DELETE
		"""
		app_models.event.objects(id=request.POST['id']).delete()
		
		response = create_response(200)
		return response.get_response()
