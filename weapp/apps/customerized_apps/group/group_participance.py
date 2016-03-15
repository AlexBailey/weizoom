# -*- coding: utf-8 -*-

import json
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from core import resource
from core.jsonresponse import create_response
from django.template import RequestContext
from django.shortcuts import render_to_response
from core.exceptionutil import unicode_full_stack
from utils import url_helper
import models as app_models
from modules.member.models import Member

COUNT_PER_PAGE = 20

class GroupParticipance(resource.Resource):
	app = 'apps/group'
	resource = 'group_participance'

	def api_put(request):
		"""
		响应PUT
		"""
		try:
			member_id = request.member.id
			group_relation_id = request.POST['group_relation_id']
			fid = request.POST['fid']
			try:
				fid_member = Member.objects.get(id=fid)
			except:
				response = create_response(500)
				response.errMsg = u'不存在该会员'
				return response.get_response()
			#更新小团购信息
			group_relation = app_models.GroupRelations.objects(id=group_relation_id, member_id=fid).first()
			if group_relation.group_status == app_models.GROUP_RUNNING:
				#更新当前member的参与信息
				total_number = int(group_relation.group_type)
				sync_result = group_relation.modify(
					query={'grouped_number__lt': total_number},
					inc__grouped_number=1,
					push__grouped_member_ids=str(member_id)
				)
				if sync_result:
					try:
						group_detail = app_models.GroupDetail(
							relation_belong_to = group_relation_id,
							owner_id = str(fid),
							grouped_member_id = str(member_id),
							grouped_member_name = request.member.username_for_html,
							created_at = datetime.now()
						)
						group_detail.save()
					except:
						group_relation.update(dec__grouped_number=1,pop__grouped_member_ids=str(member_id))
						response = create_response(500)
						response.errMsg = u'只能参与一次'
						return response.get_response()
				else:
					response = create_response(500)
					response.errMsg = u'团购名额已满'
					return response.get_response()
		except:
			response = create_response(500)
			response.errMsg = u'参与失败'
			response.inner_errMsg = unicode_full_stack()
			return response.get_response()
		response = create_response(200)
		return response.get_response()

	def api_post(request):
		"""
		我要开团
		"""
		group_record_id = request.POST['group_record_id']
		member_id = request.POST['fid']
		product_id =  request.POST['product_id']
		group_type = request.POST['group_type']
		group_days = request.POST['group_days']
		group_price = request.POST['group_price']
		try:
			group_member_info = app_models.GroupRelations(
				belong_to = group_record_id,
				member_id = member_id,
				group_leader_name = request.member.username_for_html,
				product_id = product_id,
				group_type = group_type,
				group_days = group_days,
				group_price = group_price,
				grouped_number = 1,
				grouped_member_ids = list(member_id),
				created_at = datetime.now()
			)
			group_member_info.save()
			data = json.loads(group_member_info.to_json())
			relation_belong_to = data['_id']['$oid']
			group_detail = app_models.GroupDetail(
				relation_belong_to = relation_belong_to,
				owner_id = member_id,
				grouped_member_id = member_id,
				grouped_member_name = request.member.username_for_html,
				created_at = datetime.now()
			)
			group_detail.save()
			response = create_response(200)
			response.data = {
				'relation_belong_to': relation_belong_to
			}
			return response.get_response()
		except:
			response = create_response(500)
			response.errMsg = u'只能开团一次'
		return response.get_response()


class CancelUnpaidGroup(resource.Resource):
	app = 'apps/group'
	resource = 'cancel_unpaid_group'

	def api_put(request):
		"""
		取消未支付的开团信息
		"""
		group_relation_id = request.POST['group_relation_id']
		member_id = request.POST['member_id']
		try:
			group_relation = app_models.GroupRelations.objects.get(id=group_relation_id,member_id=member_id,group_status=app_models.GROUP_NOT_START)
			group_relation.delete()
			response = create_response(200)
		except:
			response = create_response(500)
			response.errMsg = u'取消操作失败'
		return response.get_response()

