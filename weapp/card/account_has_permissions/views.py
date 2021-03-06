# -*- coding: utf-8 -*-

from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required

from core.restful_url_route import view
from market_tools.tools.weizoom_card.models import *
from card import export

########################################################################
# edit_weizoom_card_account_permission: 编辑使用微众卡用户的权限
########################################################################
@login_required
@view(app='card', resource='permissions', action='get')
def edit_weizoom_card_account_permission(request):
    weizoomcardpermission=WeiZoomCardPermission.objects.filter(user_id=request.user.id)
    can_change_shop_config=0
    if weizoomcardpermission:
        can_change_shop_config=weizoomcardpermission[0].can_change_shop_config
    c = RequestContext(request, {
        'first_nav_name': export.MALL_CARD_FIRST_NAV,
        'second_navs': export.get_card_second_navs(request),
        'second_nav_name': export.MALL_CARD_MANAGER_NAV,
        'can_change_shop_config': can_change_shop_config,
    })
    return render_to_response('card/editor/edit_account_has_permissions.html',c )

@login_required
@view(app='card', resource='cardmanager', action='get')
def edit_weizoom_card_account_permission(request):
    is_manage = 'manage' in request.GET
    c = RequestContext(request, {
        'first_nav_name': export.MALL_CARD_FIRST_NAV,
        'second_navs': export.get_card_second_navs(request),
        'second_nav_name': export.MALL_CARD_PERMISSIONS_NAV,
        'is_manage': is_manage
    })
    return render_to_response('card/editor/list_weizoom_card_manager.html', c)