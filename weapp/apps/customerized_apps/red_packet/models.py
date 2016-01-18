# -*- coding: utf-8 -*-

from datetime import datetime

import mongoengine as models

class RedPacketControl(models.Document):
	member_id= models.LongField(default=0) #参与者id
	powered_member_id = models.LongField(default=0) #被助力者id
	belong_to = models.StringField(default="", max_length=100) #对应的活动id
	powerme_control = models.StringField(default="", max_length=100, unique_with=['belong_to', 'member_id', 'powered_member_id'])

	meta = {
		'collection': 'red_packet_red_packet_control'
	}

class RedPacketParticipance(models.Document):
	member_id= models.LongField(default=0) #参与者id
	belong_to = models.StringField(default="", max_length=100) #对应的活动id
	created_at = models.DateTimeField() #创建时间
	has_join = models.BooleanField(default=False) #是否已参与微助力
	power = models.IntField(default=0) #助力值
	powered_member_id = models.DynamicField() #已助力的会员id list

	meta = {
		'collection': 'red_packet_red_packet_participance'
	}


STATUS_NOT_START = 0
STATUS_RUNNING = 1
STATUS_STOPED = 2
class RedPacket(models.Document):
	owner_id = models.LongField() #创建人id
	name = models.StringField(default="", max_length=100) #名称
	start_time = models.DateTimeField() #开始时间
	end_time = models.DateTimeField() #结束时间
	status = models.IntField(default=0) #状态
	related_page_id = models.StringField(default="", max_length=100) #termite page的id
	timing = models.BooleanField(default=True) #是否显示倒计时
	type = models.StringField(default="random", max_length=10) #红包方式,默认为拼手气红包
	random_total_money = models.StringField(default="", max_length=10) #拼手气红包总金额
	random_packets_number = models.StringField(default="", max_length=10) #拼手气红包红包个数
	regular_packets_number = models.StringField(default="", max_length=10) #普通红包红包个数
	regular_per_money = models.StringField(default="", max_length=10) #普通红包单个金额
	money_range = models.StringField(default="", max_length=50) #好友贡献金额区间
	reply_content = models.StringField(default="", max_length=50) #参与活动回复语
	material_image = models.StringField(default="", max_length=1024) #分享的图片链接
	share_description = models.StringField(default="", max_length=1024) #分享描述
	qrcode = models.DynamicField() #带参数二维码ticket,name
	created_at = models.DateTimeField() #创建时间
	
	meta = {
		'collection': 'red_packet_red_packet'
	}
	
	@property
	def status_text(self):
		if self.status == STATUS_NOT_START:
			return u'未开始'
		elif self.status == STATUS_RUNNING:
			now = datetime.today()
			if now >= self.end_time:
				return u'已结束'
			else:
				return u'进行中'
		elif self.status == STATUS_STOPED:
			return u'已结束'
		else:
			return u'未知'
	
	@property
	def is_finished(self):
		status_text = self.status_text
		if status_text == u'已结束':
			return True
		else:
			return False


class RedPacketLog(models.Document):
	belong_to = models.StringField(default="", max_length=100) #对应的活动id
	power_member_id = models.LongField() #助力者id
	be_powered_member_id = models.LongField() #被助力者id
	created_at = models.DateTimeField(default=datetime.now()) #创建时间

	meta = {
		'collection': 'red_packet_red_packet_log'
	}

class RedPacketDetail(models.Document):
	"""
	助力详情表
	"""
	belong_to = models.StringField(default="", max_length=100) #对应的活动id
	owner_id = models.LongField()
	power_member_id = models.LongField() #助力者id
	power_member_name = models.StringField(default='', max_length=1024) #助力者昵称
	has_powered = models.BooleanField(default=False) #是否已助力(针对未关注用户)
	created_at = models.DateTimeField() #创建时间

	meta = {
		'collection': 'red_packet_red_packet_detail'
	}
