# -*- coding: utf-8 -*-

import json
import qrcode, os

from core import resource
from core.jsonresponse import create_response, JsonResponse
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from cache import webapp_cache
import termite2.models as termite_models
from django.conf import settings
from termite2 import export

class GlobalNavbarStatus(resource.Resource):
    """
    导航
    """
    app = 'termite2'
    resource = 'global_navbar_status'

    @login_required
    def api_post(request):
        """
        是否启用导航
        """
        is_enable = request.POST.get('is_enable', False)
        if is_enable == 'true':
            is_enable = True
        else:
            is_enable = False
            
        global_navbar = termite_models.TemplateGlobalNavbar.get_object(request.manager.id)
        global_navbar.is_enable = is_enable
        global_navbar.save()
        # 如果点击启用，则更新varnish对于首页的缓存
        # if not settings.DEBUG:
        webapp_cache.update_product_list(request.manager.id)
        response = create_response(200)
        response.data = True
        return response.get_response()