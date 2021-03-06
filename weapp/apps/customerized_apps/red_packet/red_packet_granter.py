# -*- coding: utf-8 -*-
import json

from datetime import date, datetime

from BeautifulSoup import BeautifulSoup
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.db.models import F
from django.contrib.auth.decorators import login_required
from account.models import UserWeixinPayOrderConfig
from core import resource
from core import paginator
from core.exceptionutil import unicode_full_stack
from core.jsonresponse import create_response
from mall.models import PayInterface
from market_tools.tools.template_message.module_api import send_apps_template_message
from modules.member import models as member_models
import models as app_models
import export
from mall import export as mall_export
from modules.member.models import Member, MemberHasSocialAccount
from pay.weixin.api.api_send_red_pack import RedPackMessage
from utils.string_util import byte_to_hex
import os

from watchdog.utils import watchdog_error
from weapp import settings
from weixin.user.models import ComponentAuthedAppid, ComponentAuthedAppidInfo

PAY_INTERFACE_WEIXIN_PAY = 2 #支付方式为微信支付

class RedPacketGranter(resource.Resource):
	app = 'apps/red_packet'
	resource = 'red_packet_granter'

	@login_required
	def api_get(request):
		record_id = request.GET.get('id', None)
		member_id = request.GET.get('member_id', None)
		response = create_response(500)
		if not record_id or not member_id:
			response.errMsg = u'活动信息出错,请重试~'
			return response.get_response()
		record = app_models.RedPacket.objects(id=record_id)
		if record.count() <=0:
			response.errMsg = u'不存在该活动'
			return response.get_response()
		else:
			record = record.first()
		owner_id = record.owner_id
		member_info = app_models.RedPacketParticipance.objects(belong_to=record_id, member_id=member_id, msg_api_status=False)
		if member_info.count() <= 0:
			response.errMsg = u'没有必要给该会员发送模板消息'
			return response.get_response()
		else:
			member_info = member_info.first()
		member_senders_info = member_info.msg_api_failed_members_info
		if not send_apps_template_message(owner_id, member_senders_info):
			response.errMsg = u'发送模板消息失败'
			return response.get_response()
		else:
			response = create_response(200)
			return response.get_response()

	@login_required
	def api_put(request):
		"""
		发红包
		api参数详见：https://pay.weixin.qq.com/wiki/doc/api/cash_coupon.php?chapter=13_5
		@return:
		"""
		record_id = request.POST.get('id', None)
		member_ids = request.POST.get('member_ids', None)
		response = create_response(500)
		if not record_id or not member_ids:
			response.errMsg = u'活动信息出错,请重试~'
			return response.get_response()
		member_ids = member_ids.split(',')
		record = app_models.RedPacket.objects(id=record_id)
		if record.count() <=0:
			response.errMsg = u'不存在该活动'
			return response.get_response()
		else:
			record = record.first()
		owner_id = record.owner_id
		wishing = record.wishing
		record_name = record.name

		#获取商户的支付配置信息 (测试时注释)
		try:
			pay_interface = PayInterface.objects.get(type=PAY_INTERFACE_WEIXIN_PAY, owner_id=owner_id)
			weixin_pay_config = UserWeixinPayOrderConfig.objects.get(id=pay_interface.related_config_id)

			authed_appid = ComponentAuthedAppid.objects.filter(user_id=owner_id, authorizer_appid=weixin_pay_config.app_id, is_active=True)[0]
			appid_info = ComponentAuthedAppidInfo.objects.filter(auth_appid=authed_appid)[0]
			nick_name = appid_info.nick_name
			remark = nick_name
		except:
			response.errMsg = u'该账户未配置支付信息'
			return response.get_response()

		cert_setting = app_models.RedPacketCertSettings.objects(owner_id=str(owner_id))
		if cert_setting.count() > 0:
			cert_setting = cert_setting.first()
		else:
			response.errMsg = u'请首先上传证书文件'
			return response.get_response()
		SSLKEY_PATH = cert_setting.key_path
		SSLCERT_PATH = cert_setting.cert_path
		if '' == SSLKEY_PATH or '' == SSLCERT_PATH:
			response.errMsg = u'请首先上传证书文件'
			return response.get_response()
		try:
			ip = request.META['REMOTE_ADDR']
		except:
			ip = None

		member_info_list = app_models.RedPacketParticipance.objects(
			belong_to=record_id,
			member_id__in=member_ids,
			has_join=True,
			red_packet_status=True,
			is_already_paid=False
		)
		member_id2status = {m.id: m.is_subscribed for m in Member.objects.filter(id__in=member_ids)}
		member_id2openid = {m.member.id: m.account.openid for m in MemberHasSocialAccount.objects.filter(member_id__in=member_ids)}

		if len(member_info_list) <= 0:
			response.errMsg = u'没有符合条件的会员'
			return response.get_response()
		result_data = {}
		member_sets = app_models.RedPacketParticipance.objects(belong_to=record_id)
		for member_info in member_info_list:
			member_id = member_info.member_id
			#非会员不发放
			if not member_id2status[member_id]:
				result_data[member_id] = u'非会员不予发放红包'
				continue
			price = int(member_info.red_packet_money * 100)
			#获取该member_id的固定openid
			openid = member_id2openid[member_id]

			curr_member_set = member_sets.filter(member_id=member_id)

			#生产环境
			red = RedPackMessage(weixin_pay_config.partner_id, weixin_pay_config.app_id, nick_name,
				nick_name,openid,price,price,price,1, wishing, ip,
				u"点赞拼大奖红包",
				remark,
				weixin_pay_config.partner_key)

			#使用微众家帐号测试
			print 'real price:=============>>', price
			# red = RedPackMessage('1231154002', 'wx9fefd1d7a80fbe41', u'微众家',
			# 	u'微众家',"oucARuOuCP3haBrgYmUFU9aOs0SA",price,1,1,1, wishing, ip,
			# 	u"点赞拼大奖红包",
			# 	u'微众家',
			# 	'i15uok48plm49wm37ex62qmr50hk27em')

			result = red.post_data(SSLKEY_PATH, SSLCERT_PATH)
			result = BeautifulSoup(result)
			print result
			return_code = result.return_code.text
			return_msg = result.return_msg.text

			print 'red api returned code:=============>>', return_code
			print 'red api returned msg:=============>>', return_msg
			if return_code == "SUCCESS":
				result_code = result.result_code.text
				print 'red api result code:=============>>', result_code
				if result_code == "SUCCESS":
					#给该会员发送模板消息
					app_url = 'http://%s/m/apps/red_packet/m_red_packet/?webapp_owner_id=%s&id=%s' % (settings.DOMAIN, owner_id, record_id)
					temp_dict = {
						"openid": openid,
						"app_url": app_url,
						"member_id": member_id,
						"detail_data": {
							"task_name": record_name,
							"prize": u"￥ %.2f" % (price/100.0),
							"finish_time": member_info.finished_time.strftime(u"%Y年%m月%d日 %H:%M") if member_info.finished_time else datetime.now().strftime(u"%Y年%m月%d日 %H:%M")
						}
					}
					#更新已发放红包的会员信息
					curr_member_set.update(set__is_already_paid=True)
					result_data[member_id] = u'现金红包发放成功!'
					#发送模板消息
					if not send_apps_template_message(owner_id, temp_dict):
						#记录模板消息发送失败的会员信息
						curr_member_set.update(set__msg_api_failed_members_info=temp_dict)
					else:
						#更新已发放模板消息的会员信息
						curr_member_set.update(set__msg_api_status=True)
				else:
					result_msg = result.err_code_des.text
					print 'red api result msg:=============>>', result_msg
					result_data[member_id] = result_msg
			else:
				response.errMsg = return_msg
				return response.get_response()
			
		response = create_response(200)
		response.data = result_data
		return response.get_response()
