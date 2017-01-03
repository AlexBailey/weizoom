# -*- coding: utf-8 -*-
from datetime import timedelta, datetime, date
from django.db import models

from django.contrib.auth.models import User
from modules.member.models import Member
from market_tools.prize.models import Prize


#########################################################################
# Lottery：抽奖
#########################################################################
LOTTERY_STATUS_RUNING = 1
LOTTERY_STATUS_STOP = 0
LOTTERY_STATUS_TIMEOUT = 2
LOTTERY_STATUS_NO_START = 3
STATUS2TEXT = {
	LOTTERY_STATUS_RUNING: u'已启动',
	LOTTERY_STATUS_STOP: u'已暂停',
	LOTTERY_STATUS_NO_START: u'未启动',
	LOTTERY_STATUS_TIMEOUT: u'已过期'
}
SCRATCH_CARD = 0  #刮刮卡
GOLDEN_EGG = 1  #砸金蛋
ROULETTE = 2  #大转盘

#中奖机制award_type
ONCE_A_LOTTERY = 0
ONCE_A_DAY = 1
HOURLY = 2
EVERY_TIME = 3
class Lottery(models.Model):
	owner = models.ForeignKey(User)
	name = models.CharField(max_length=100, default='', verbose_name='名称')
	detail = models.TextField(verbose_name='详情')
	type = models.IntegerField(default=SCRATCH_CARD) #抽奖类型
	award_type = models.IntegerField(default=EVERY_TIME) #中奖机制
	award_hour = models.IntegerField(default=0) #中奖间隔时间，当award_type为HOURLY时有效
	daily_play_count = models.IntegerField(default=1, verbose_name='每人每天参与次数')
	expend_integral = models.IntegerField(default=0, verbose_name='消耗积分')
	no_prize_odd = models.IntegerField(default=0) #不中奖概率
	can_repeat = models.BooleanField(default=True) #是否可重复参与
	status = models.IntegerField(default=LOTTERY_STATUS_NO_START)
	is_deleted = models.BooleanField(default=False) #是否删除
	start_at = models.DateTimeField()
	end_at = models.DateTimeField()
	expected_participation_count = models.IntegerField() #预计参与人数
	created_at = models.DateTimeField(auto_now_add=True)
	not_win_desc = models.CharField(max_length=100, default='谢谢参与')

	class Meta(object):
		db_table = 'market_tool_lottery'
		verbose_name = '抽奖'
		verbose_name_plural = '抽奖'
		ordering = ['-id']

	def check_time(self):
		today = datetime.today()

		end_date = self.end_at + timedelta(1)
		if today >= end_date:
			self.status = LOTTERY_STATUS_TIMEOUT
			self.save()

		start_date = self.start_at
		if self.status == LOTTERY_STATUS_NO_START and today >= start_date:
			self.status = LOTTERY_STATUS_RUNING
			self.save()
			
	@staticmethod
	def get_lottery_records(request,member):
		if member is None:
			lottery_records = []
		else:
			lottery_records = LotteryRecord.objects.filter(member=member, prize_level__gt=0)

		for lottery_record in lottery_records:
			lottery_record.url = _build_lottery_link(request, lottery_record.lottery_id)

		return lottery_records

def _build_lottery_link(request, lottery_id):

	workspace_template_info = 'workspace_id=market_tool:lottery&webapp_owner_id=%d&project_id=0' % request.project.owner_id

	return './?module=market_tool:lottery&model=lottery&action=get&lottery_id=%d&%s' % (lottery_id, workspace_template_info)


#########################################################################
# LotteryHasPrize：抽奖活动奖品
#########################################################################
class LotteryHasPrize(models.Model):
	lottery = models.ForeignKey(Lottery)
	prize = models.ForeignKey(Prize)
	prize_type = models.IntegerField(verbose_name='奖品类别') #0实物，1优惠券，2兑换码，3积分
	prize_source = models.CharField(max_length=100, default='', verbose_name='奖品来源')
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta(object):
		db_table = 'market_tool_lottery_has_prize'
		verbose_name = '大转盘奖品'
		verbose_name_plural = '大转盘奖品'


#########################################################################
# LotteryRecord：中奖记录
#########################################################################
class LotteryRecord(models.Model):
	owner = models.ForeignKey(User)
	member = models.ForeignKey(Member)
	lottery = models.ForeignKey(Lottery)
	lottery_name = models.CharField(max_length=100) #活动名称
	prize_type = models.IntegerField() #0实物，1优惠券，2兑换码，3积分
	prize_name = models.CharField(max_length=30) #中奖名称
	prize_level = models.IntegerField(default=0) #中奖等级
	prize_number = models.CharField(max_length=30) #中奖编号
	prize_detail = models.CharField(max_length=30) #中奖详情  奖品名称、优惠券码
	prize_position = models.IntegerField(default=0) #中奖位置
	prize_money = models.DecimalField(max_digits=65, decimal_places=2) #优惠券金额
	created_at = models.DateTimeField(auto_now_add=True)
	awarded_at = models.DateTimeField(auto_now_add=True)
	is_awarded = models.BooleanField(default=False) #是否发奖

	class Meta(object):
		db_table = 'market_tool_lottery_record'
		verbose_name = '中奖记录'
		verbose_name_plural = '中奖记录'
		ordering = ['-id']

NO_LIMIT = 0 #不限制
FORBIDDEN_SALE_LIMIT = 1 #禁售
ONLY_SALE_LIMIT = 2 #仅售

PRE_PRODUCT_STATUS = {
	'NOT_YET': 0, #尚未提交审核
	'SUBMIT': 1, #提交审核
	'REFUSED': 2, #驳回
	'ACCEPT': 3 #审核通过
}

class PreProduct(models.Model):
	"""
	待审核商品
	"""
	owner_id = models.IntegerField(default=0)
	name = models.CharField(max_length=50, default='')  #商品名称
	promotion_title = models.CharField(max_length=50, default='')  #促销标题
	price = models.DecimalField(max_digits=65, decimal_places=2, default=0.00)  #商品价格 (元)
	settlement_price = models.DecimalField(max_digits=65, decimal_places=2, default=0.00)  #结算价 (元)
	weight = models.FloatField(default=0)  #商品重量 (kg)
	stock = models.IntegerField(default=0)  #商品库存 默认-1{大于0: 有限 ,-1:无限}
	valid_time_from = models.DateTimeField(null=True)  #有效范围开始时间
	valid_time_to = models.DateTimeField(null=True)  #有效范围结束时间
	limit_settlement_price = models.DecimalField(max_digits=65, decimal_places=2, default=0.00)  #限时结算价 (元)
	has_limit_time = models.BooleanField(default=False)  #限时结算价是否需要 有效范期
	has_product_model = models.BooleanField(default=False) #是否是多规格商品
	classification_id = models.IntegerField(default=0) #所属分类id(二级分类id)
	limit_zone_type = models.IntegerField(default=NO_LIMIT)
	limit_zone = models.IntegerField(default=0)  # 限制地区的模板id
	has_same_postage = models.BooleanField(default=True) #是否是统一运费{0:统一运费,1:默认模板运费}
	postage_money = models.DecimalField(max_digits=65, decimal_places=2, default=0.00) #统一运费金额
	postage_id = models.IntegerField(default=0)# 默认模板运费id
	remark = models.TextField(default='')  # 备注
	is_updated = models.BooleanField(default=False)  # 是否更新
	review_status = models.IntegerField(default=PRE_PRODUCT_STATUS['NOT_YET'])#审核状态
	refuse_reason = models.TextField(default='')  # 驳回原因
	is_deleted = models.BooleanField(default=False)
	created_at = models.DateTimeField(auto_now_add=True)  # 添加时间
	mall_product_id = models.IntegerField(default=0) #审核通过后与mall_product记录关联

	class Meta(object):
		db_table = 'mall_pre_product'