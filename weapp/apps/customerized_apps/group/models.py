# -*- coding: utf-8 -*-

from datetime import datetime

import mongoengine as models

STATUS_NOT_START = 0
STATUS_RUNNING = 1
STATUS_STOPED = 2
class Group(models.Document):
	owner_id = models.LongField() #创建人id
	related_page_id = models.StringField(default="", max_length=100) #termite page的id
	name = models.StringField(default="", max_length=100) #名称
	start_time = models.DateTimeField() #开始时间
	end_time = models.DateTimeField() #结束时间
	status = models.IntField(default=0) #状态
	created_at = models.DateTimeField() #创建时间
	product = models.StringField(default="") #活动商品
	group_dict = models.DynamicField() #团购活动字典{'0':{'group_type':'5','group_days':'10','group_price':'100.00'},...}
	rules = models.StringField()#团购说明
	material_image = models.StringField()#分享图片
	share_description = models.StringField()#分享描述

	meta = {
		'collection': 'group_group'
	}
	
	# @property
	# def status_text(self):
	# 	if self.status == STATUS_NOT_START:
	# 		return u'未开始'
	# 	elif self.status == STATUS_RUNNING:
	# 		now = datetime.today()
	# 		if now >= self.end_time:
	# 			return u'已结束'
	# 		else:
	# 			return u'进行中'
	# 	elif self.status == STATUS_STOPED:
	# 		return u'已结束'
	# 	else:
	# 		return u'未知'
	#
	# @property
	# def is_finished(self):
	# 	status_text = self.status_text
	# 	if status_text == u'已结束':
	# 		return True
	# 	else:
	# 		return False

class GroupParticipance(models.Document):
	webapp_user_id= models.LongField(default=0) #参与者id
	member_id= models.LongField(default=0) #参与者id
	belong_to = models.StringField(default="", max_length=100) #对应的活动id
	is_group_leader = models.BooleanField(default=False) #是否是团购的团长
	group_status = models.BooleanField(default=False) #团购状态
	is_already_paid = models.BooleanField(default=False) #是否已经支付成功
	is_valid = models.BooleanField(default=True) #该条记录是否有效(针对取关后再次关注的情况)
	created_at = models.DateTimeField() #创建时间
	success_time = models.DateTimeField() #团购成功时间

	meta = {
		'collection': 'group_group_participance'
	}

class GroupRelations(models.Document):
	belong_to = models.StringField(default="", max_length=100) #对应的活动id
	member_id= models.StringField(default="", max_length=20) #团购发起者id
	grouped_member_id = models.StringField(default="", max_length=20, unique_with=['belong_to', 'member_id']) #团购参与者id

	meta = {
		'collection': 'group_group_relations'
	}

class GroupedDetail(models.Document):
	"""
	团购详情记录表
	"""
	belong_to = models.StringField(default="", max_length=100) #对应的活动id
	owner_id = models.LongField() #团购发起者id
	grouped_member_id = models.LongField() #团购参与者id
	grouped_member_name = models.StringField(default='', max_length=1024) #团购参与者昵称
	is_already_paid = models.BooleanField(default=False) #是否已经支付成功
	created_at = models.DateTimeField() #创建时间

	meta = {
		'collection': 'group_grouped_detail'
	}