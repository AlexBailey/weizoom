# -*- coding: utf-8 -*-

# import logging
from __future__ import absolute_import
import time
from datetime import timedelta, datetime, date
import urllib, urllib2
import os
import json
import subprocess
import shutil
import sys

from django.template.loader import get_template
from django.template import Context, RequestContext
from django.shortcuts import render_to_response
from django.conf import settings
from django.template import Template

from . import pagerender
from termite import pagestore as pagestore_manager
from webapp import models as webapp_models
from core.jsonresponse import create_response
from termite2 import models as termite2_models

########################################################################
# __get_display_info: 构造request的display_info
########################################################################
def __get_display_info(request):
	pagestore = pagestore_manager.get_pagestore('mongo')

	project_id = request.REQUEST.get('project_id', '')
	if 'fake:' in project_id:
		return __get_fake_project_display_info(request)

	#获取project
	# project = request.project
	# is_app_project = False
	# if hasattr(project, 'app_name'):
	# 	app_name = request.project.app_name
	# if hasattr(project,'is_app_project'):
	# 	is_app_project = request.project.is_app_project
	# project_id = project.id
	project = None
	project_id = request.REQUEST.get('project_id')
	is_app_project = False
	app_name = ''
	if project_id.startswith('new_app:'):
		_, app_name, project_id = project_id.split(':')
		is_app_project = True
	else:
		project_id = int(request.REQUEST.get('project_id', 0))

	if is_app_project:
		project = webapp_models.Project()
		project.id = project_id
		project.type = 'appkit'
	else:
		if project_id != 0:
			project = webapp_models.Project.objects.get(id=project_id)
		else:
			workspace = webapp_models.Workspace.objects.get(owner=request.webapp_owner_id, inner_name='home_page')
			project = webapp_models.Project.objects.get(workspace=workspace, type='wepage', is_active=True)
			project_id = project.id

	if request.in_design_mode and request.POST:
		page_component = json.loads(request.POST['page'])
		page = pagestore.get_page(project_id, page_component['cid'])
		page['component'] = page_component
		page_id = page_component['cid']
	else:
		page_id = request.GET.get('page_id', 1)
		if page_id == 'preview':
			page = pagestore.get_page(project_id, page_id)
		else:
			if is_app_project and project_id == '0':
				#新建app的project
				app_settings_module_path = 'apps.customerized_apps.%s.settings' % app_name
				app_settings_module = __import__(app_settings_module_path, {}, {}, ['*',])
				page = json.loads(app_settings_module.NEW_PAGE_JSON)
			else:
				page = pagestore.get_page(project_id, page_id)

	if page_id != 'preview':
		try:
			#使用project中的site_title作为真正的site_title
			#因为在page列表页面直接更新page site_title时是不会更新mongo中page数据中的site_title的
			page['component']['model']['site_title'] = project.site_title
		except:
			pass

	if request.user.is_from_weixin and request.REQUEST.get('project_id').startswith('new_app:') is False:
		#在预览模式下，不显示导航
		__get_navbar(request, page)

	display_info = {
		'project': project,
		'page_id': page_id,
		'page': page
	}

	request.display_info = display_info


'''
底部导航总开关
'''
def __get_is_enable_navbar(request):
	#update by bert at 20151023
	if hasattr(request, 'webapp_owner_info') and hasattr(request.webapp_owner_info, 'global_navbar') and hasattr(request.webapp_owner_info.global_navbar, 'is_enable'):
		navbar = request.webapp_owner_info.global_navbar
	else:
		navbar = termite2_models.TemplateGlobalNavbar.get_object(request.webapp_owner_id)
	return navbar.is_enable

def is_home_page(request):
	# 是否是首页
	project_id = request.REQUEST.get('project_id', 0)
	if 'workspace_id=home_page' in request.get_full_path() and project_id == '0':
		return True

	if project_id == '0':
		return True

	projects = webapp_models.Project.objects.filter(id=project_id)
	if projects.count() > 0:
		if projects[0].is_active:
			return True

	return False

def __is_enable_navbar(request, navbar_component):
	if is_home_page(request):
		'''
		主页是否显示navbar
		'''
		is_enable_navbar = navbar_component['model']['pages']['home']['select']
		if is_enable_navbar:
			return True
		else:
			return False
	else:
		'''
		微页面是否显示navbar
		'''
		return __is_wepage_navbar(navbar_component)


def __is_wepage_navbar(navbar_component):
	return navbar_component['model']['pages']['wepage']['select']


def __get_navbar(request, page):
	if request.in_production_mode:
		if not __get_is_enable_navbar(request):
			return False

		navbar_component = get_navbar_components(request.webapp_owner_id)
		if navbar_component:
			navbar_component['cid'] = 9999999
			navbar_component['model']['index'] = 9999999
			if __is_enable_navbar(request, navbar_component):
				page['component']['components'].append(navbar_component)


def get_navbar_components(webapp_owner_id):
	pagestore = pagestore_manager.get_pagestore('mongo')
	project_id = 'fake:wepage:%s:navbar' % webapp_owner_id
	page_id = 'navbar'
	navbar_page = pagestore.get_page(project_id, page_id)

	if navbar_page is None:
		navbar_page = __get_init_navbar_json()

	navbar_component = navbar_page['component']['components'][0]
	return navbar_component


def __get_init_navbar_json():
	settings_module_path = 'termite2.global_navbar.settings'
	settings_module = __import__(settings_module_path, {}, {}, ['*',])
	return json.loads(settings_module.NEW_PAGE_JSON)


def __get_fake_project_display_info(request):
	pagestore = pagestore_manager.get_pagestore('mongo')
	project_id = request.REQUEST.get('project_id', '')
	_, project_type, webapp_owner_id, page_id, mongodb_id = project_id.split(':')

	project = request.project
	if not project:
		project = webapp_models.Project()
		project.name = 'fake:%s:%s' % (project_type, page_id)
		project.type = project_type
		project.id = project_id

	if mongodb_id == 'new':
		if page_id == 'navbar':
			page = __get_init_navbar_json()
	else:
		project_id = 'fake:%s:%s:%s' % (project_type, webapp_owner_id, page_id)
		page = pagestore.get_page(project_id, page_id)

	display_info = {
		'project': project,
		'page_id': page_id,
		'page': page
	}

	request.display_info = display_info


########################################################################
# create_page: 创建design page
########################################################################
def __preprocess_page(request):
	__get_display_info(request)
	project = request.display_info['project']
	page = request.display_info['page']

	#填充page.component
	page_component = page['component']
	if not 'components' in page_component:
		page_component['components'] = []

	return project, page


def create_page(request, return_html_snippet=False):
	project, page = __preprocess_page(request)
	#将page的class放入request，解决design page下无法为data-role=page设置class的问题
	#TODO: 优化解决方案
	request.page_model = page['component']['model']
	html = pagerender.create_mobile_page_html_content(request, page, page['component'], project)

	if return_html_snippet:
		return html
	else:
		response = create_response(200)
		response.data = html
		return response.get_response()


def create_component(request):
	page = {}
	page_component = json.loads(request.POST['component'])
	page['component'] = page_component
	project = webapp_models.Project()
	project.id = 0
	project.type = 'wepage'
	if page_component.has_key("components"):
		if page_component["components"][0]["type"].split(".")[0] == "appkit":
			project.type = 'appkit'
	html = pagerender.create_mobile_page_html_content(request, page, page['component'], project)

	response = create_response(200)
	response.data = html
	return response.get_response()


def get_site_description(request):
	project, page = __preprocess_page(request)
	return page['component']['model'].get('site_description', '')


def get_site_title(request):
	project, page = __preprocess_page(request)
	return page['component']['model'].get('site_title', '')

