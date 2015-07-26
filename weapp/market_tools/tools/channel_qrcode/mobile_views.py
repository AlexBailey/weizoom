# -*- coding: utf-8 -*-

from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.template import Context, RequestContext
from django.shortcuts import render_to_response
from models import *
from modules.member.models import Member
from  weixin.user.module_api import get_mp_head_img


template_path_items = os.path.dirname(__file__).split(os.sep)
TEMPLATE_DIR = '%s/templates' % template_path_items[-1]

def get_settings(request):
    user_id = request.GET.get('webapp_owner_id', 0)
    ticketid = request.GET.get('ticketid', 0)
    member = request.member
    if user_id == '467':
        if ticketid:
            setting = ChannelQrcodeSettings.objects.get(id=ticketid)
            show_head = False
            if setting.bing_member_id == request.member.id:
                show_head = True
                member = Member.objects.get(id=request.member.id)
                member.user_name = member.username_for_html
                setting.count = ChannelQrcodeHasMember.objects.filter(channel_qrcode_id=setting.id).count()

            c = RequestContext(request, {
                    'page_title': u'首草送好礼，接力扫码等你来传递',
                    'member': member,
                    'setting': setting,
                    'is_hide_weixin_option_menu': False,
                    'head_img': get_mp_head_img(user_id),
                    'show_head': show_head
                })
            return render_to_response('%s/channel_qrcode/webapp/channel_qrcode_img.html' % TEMPLATE_DIR, c)
        else:
            if request.member:
                setting = ChannelQrcodeSettings.objects.filter(bing_member_id=request.member.id, is_bing_member=True)
                if setting.count() > 0:
                    setting = setting[0]
                    new_url = '%s&ticketid=%s' % (request.get_full_path(), setting.id)
                    return HttpResponseRedirect(new_url)
            c = RequestContext(request, {
                    'page_title': u'代言人二维码',})
            return render_to_response('%s/channel_qrcode/webapp/channel_qrcode_context.html' % TEMPLATE_DIR, c)
    else:
        if request.member:
            setting = ChannelQrcodeSettings.objects.filter(bing_member_id=request.member.id, is_bing_member=True)
            if setting.count() > 0:
                setting = setting[0]
                member = Member.objects.get(id=request.member.id)
                member.user_name = member.username_for_html
                setting.count = ChannelQrcodeHasMember.objects.filter(channel_qrcode_id=setting.id).count()
                c = RequestContext(request, {
                    'page_title': u'代言人二维码',
                    'member': member,
                    'setting': setting,
                    'is_hide_weixin_option_menu': True,
                    'head_img': get_mp_head_img(user_id)
                })
                return render_to_response('%s/channel_qrcode/webapp/channel_qrcode.html' % TEMPLATE_DIR, c)

        c = RequestContext(request, {
                'page_title': u'代言人二维码',})
        return render_to_response('%s/channel_qrcode/webapp/channel_qrcode_context.html' % TEMPLATE_DIR, c)




    # if request.member:
    #     setting = ChannelQrcodeSettings.objects.filter(bing_member_id=request.member.id, is_bing_member=True)
    #     if setting.count() > 0:
    #         setting = setting[0]
    #         member = Member.objects.get(id=request.member.id)
    #         member.user_name = member.username_for_html
    #         setting.count = ChannelQrcodeHasMember.objects.filter(channel_qrcode_id=setting.id).count()
            
    #         c = RequestContext(request, {
    #             'page_title': u'代言人二维码',
    #             'member': member,
    #             'setting': setting,
    #             'is_hide_weixin_option_menu': False,
    #             'head_img': get_mp_head_img(user_id)
    #         })
    #         # if user_id == '467':
    #             # from django.http import HttpResponseRedirect
    #             # response = HttpResponseRedirect('https://mp.weixin.qq.com/cgi-bin/showqrcode?ticket=%s' % setting.ticket)
    #             # return response
    #         #return render_to_response('%s/channel_qrcode/webapp/channel_qrcode_img.html' % TEMPLATE_DIR, c)
    #         # else:
    #         return render_to_response('%s/channel_qrcode/webapp/channel_qrcode.html' % TEMPLATE_DIR, c)

    #         new_url = '%s&%s' (request.get_full_path(), )
    #         HttpResponseRedirect()
    #     else:
    #         c = RequestContext(request, {
    #             'page_title': u'代言人二维码',})
    #     return render_to_response('%s/channel_qrcode/webapp/channel_qrcode_context.html' % TEMPLATE_DIR, c)
    # else:
    #     pass

