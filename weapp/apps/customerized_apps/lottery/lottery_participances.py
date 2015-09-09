# -*- coding: utf-8 -*-
import json
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.db.models import F
from django.contrib.auth.decorators import login_required
from django.conf import settings
from datetime import datetime
import os

from core import resource
from core import paginator
from core.jsonresponse import create_response
from modules.member import models as member_models
import models as app_models
from mall import export
from utils.string_util import hex_to_byte, byte_to_hex

FIRST_NAV = 'apps'
COUNT_PER_PAGE = 20

class lotteryParticipances(resource.Resource):
	app = 'apps/lottery'
	resource = 'lottery_participances'
	
	@login_required
	def get(request):
		"""
		响应GET
		"""
		has_data = app_models.lotteryParticipance.objects(belong_to=request.GET['id']).count()
		
		c = RequestContext(request, {
			'first_nav_name': FIRST_NAV,
			'second_navs': export.get_customerized_apps(request),
			'second_nav_name': "lotteries",
			'has_data': has_data,
			'activity_id': request.GET['id']
		})
		
		return render_to_response('lottery/templates/editor/lottery_participances.html', c)
	
	@staticmethod
	def get_datas(request):
		name = request.GET.get('participant_name', '')
		webapp_id = request.user_profile.webapp_id
		prize_type = request.GET.get('prize_type', '-1')
		status = request.GET.get('status', '-1')
		member_ids = []
		if name:
			hexstr = byte_to_hex(name)
			members = member_models.Member.objects.filter(webapp_id=webapp_id,username_hexstr__contains=hexstr)
			print members
			if name.find(u'非')>=0:
				sub_members = member_models.Member.objects.filter(webapp_id=webapp_id,is_subscribed=False)
				members = members|sub_members
		else:
			members = member_models.Member.objects.filter(webapp_id=webapp_id)
		member_ids = [member.id for member in members]

		start_time = request.GET.get('start_time', '')
		end_time = request.GET.get('end_time', '')
		
		params = {'belong_to':request.GET['id']}
		if name:
			params['member_id__in'] = member_ids
		if start_time:
			params['created_at__gte'] = start_time
		if end_time:
			params['created_at__lte'] = end_time
		if prize_type != '-1':
			params['prize_type'] = prize_type
		if status != '-1':
			params['status'] = True if status == '1' else False
		# datas = app_models.lotteryParticipance.objects(**params).order_by('-id')
		datas = app_models.lottoryRecord.objects(**params)
		#进行分页
		count_per_page = int(request.GET.get('count_per_page', COUNT_PER_PAGE))
		cur_page = int(request.GET.get('page', '1'))
		pageinfo, datas = paginator.paginate(datas, cur_page, count_per_page, query_string=request.META['QUERY_STRING'])
		
		return pageinfo, datas
	
	@login_required
	def api_get(request):
		"""
		响应API GET
		"""
		pageinfo, datas = lotteryParticipances.get_datas(request)
		
		memberuser2datas = {}
		member_ids = set()
		for data in datas:
			memberuser2datas.setdefault(data.member_id, []).append(data)
			member_ids.add(data.member_id)
			data.participant_name = u'未知'
			data.participant_icon = '/static/img/user-1.jpg'
		
		member_user2member = {}
		members = member_models.Member.objects.filter(id__in=member_ids)
		for member in members:
			if member.id not in member_user2member:
				member_user2member[member.id] = member
			else:
				member_user2member[member.id] = member

		if len(member_user2member) > 0:
			for member_id, member in member_user2member.items():
				for data in memberuser2datas.get(member_id, ()):
					data.participant_name = member.username_for_html
					data.participant_icon = member.user_icon

		items = []
		for data in datas:
			items.append({
				'id': str(data.id),
				'participant_name': data.participant_name,
				'participant_icon': data.participant_icon,
				'tel': data.tel,
				'prize_title': data.prize_title,
				'prize_name': data.prize_name,
				'status': data.status,
				'created_at': data.created_at.strftime("%Y-%m-%d %H:%M:%S")
			})
		response_data = {
			'items': items,
			'pageinfo': paginator.to_dict(pageinfo),
			'sortAttr': 'id',
			'data': {}
		}
		response = create_response(200)
		response.data = response_data
		return response.get_response()

	@login_required
	def api_post(request):
		"""
		领取奖品
		"""
		app_models.lottoryRecord.objects(id=request.POST['id']).update(set__status=True)
		response = create_response(200)
		return response.get_response()

class lotteryParticipances_Export(resource.Resource):
	'''
	批量导出
	'''
	app = 'apps/lottery'
	resource = 'lottery_participances-export'
	@login_required
	def api_get(request):
		"""
		详情导出
		"""
		export_id = request.GET.get('export_id')

		# app_name = lotteryParticipances_Export.app.split('/')[1]
		# excel_file_name = ('%s_id%s_%s.xls') % (app_name,export_id,datetime.now().strftime('%Y%m%d%H%m%M%S'))
		excel_file_name = u'微信抽奖详情.xls'
		export_file_path = os.path.join(settings.UPLOAD_DIR,excel_file_name)
		#Excel Process Part
		try:
			import xlwt
			name = request.GET.get('participant_name', '')
			webapp_id = request.user_profile.webapp_id
			prize_type = request.GET.get('prize_type', '-1')
			status = request.GET.get('status', '-1')
			member_ids = []
			if name:
				hexstr = byte_to_hex(name)
				members = member_models.Member.objects.filter(webapp_id=webapp_id,username_hexstr__contains=hexstr)
				print members
				if name.find(u'非')>=0:
					sub_members = member_models.Member.objects.filter(webapp_id=webapp_id,is_subscribed=False)
					members = members|sub_members
			else:
				members = member_models.Member.objects.filter(webapp_id=webapp_id)
			member_ids = [member.id for member in members]

			start_time = request.GET.get('start_time', '')
			end_time = request.GET.get('end_time', '')

			params = {'belong_to':request.GET['export_id']}
			if name:
				params['member_id__in'] = member_ids
			if start_time:
				params['created_at__gte'] = start_time
			if end_time:
				params['created_at__lte'] = end_time
			if prize_type != '-1':
				params['prize_type'] = prize_type
			if status != '-1':
				params['status'] = True if status == '1' else False
			data = app_models.lottoryRecord.objects(**params)
			fields_raw = []
			export_data = []

			#from sample to get fields4excel_file
			fields_raw.append(u'编号')
			fields_raw.append(u'用户名')
			fields_raw.append(u'手机号')
			fields_raw.append(u'获奖等级')
			fields_raw.append(u'奖品名称')
			fields_raw.append(u'抽奖时间')
			fields_raw.append(u'领取状态')

			member_ids = [record['member_id'] for record in data ]
			members = member_models.Member.objects.filter(id__in = member_ids)
			member_id2name ={}
			for member in members:
				m_id = member.id
				if member.is_subscribed == True:
					u_name = member.username
				else:
					u_name = u'非会员'
				if m_id not in member_id2name:
					member_id2name[m_id] = u_name
				else:
					member_id2name[m_id] = u_name
			#processing data
			num = 0
			for record in data:
				export_record = []
				num = num+1
				name = member_id2name[record['member_id']]
				tel = record['tel']
				prize_title = record['prize_title']
				prize_name = record['prize_name']
				created_at = record['created_at'].strftime("%Y-%m-%d %H:%M:%S")
				if record['status']:
					status = u'已领取'
				else:
					status = u'未领取'

				export_record.append(num)
				export_record.append(name)
				export_record.append(tel)
				export_record.append(prize_title)
				export_record.append(prize_name)
				export_record.append(created_at)
				export_record.append(status)

				export_data.append(export_record)

			#workbook/sheet
			wb = xlwt.Workbook(encoding='utf-8')
			ws = wb.add_sheet('id%s'%export_id)
			header_style = xlwt.XFStyle()

			##write fields
			row = col = 0
			for h in fields_raw:
				ws.write(row,col,h)
				col += 1

			##write data
			if export_data:
				row = 0
				lens = len(export_data[0])
				for record in export_data:
					row +=1
					for col in range(lens):
						ws.write(row,col,record[col])
				try:
					wb.save(export_file_path)
				except:
					print 'EXPORT EXCEL FILE SAVE ERROR'
					print '/static/upload/%s'%excel_file_name
			else:
				ws.write(1,0,'')
				wb.save(export_file_path)

			response = create_response(200)
			response.data = {'download_path':'/static/upload/%s'%excel_file_name,'filename':excel_file_name,'code':200}
		except :
			response = create_response(500)

		return response.get_response()
