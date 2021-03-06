# -*- coding: utf-8 -*-

import json

from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.db.models import F
from django.contrib.auth.decorators import login_required

from core import resource
from core.jsonresponse import create_response
from webapp import models as webapp_models
from watchdog.utils import watchdog_warning

from termite2 import export

FIRST_NAV = export.WEPAGE_FIRST_NAV

class PageEditor(resource.Resource):
	app = 'termite2'
	resource = 'page_editor'

	@login_required
	def get(request):
		"""
		微站编辑器首页
		"""
		project_id = request.GET.get('project_id', None)
		if not project_id:
			return HttpResponseRedirect('/termite2/pages/')

		is_new_project = 'is_new_project' in request.GET
		project = webapp_models.Project.objects.get(owner=request.manager, id=project_id)

		c = RequestContext(request, {
			'first_nav_name': FIRST_NAV,
			'second_navs': export.get_wepage_second_navs(request),
			'second_nav_name': export.WEPAGE_PAGES_NAV,
			'project': project,
			'is_new_project': is_new_project
		})
		return render_to_response('termite2/workbench.html', c)
