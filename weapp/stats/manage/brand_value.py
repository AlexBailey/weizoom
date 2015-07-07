# -*- coding: utf-8 -*-

import json
#from datetime import datetime
#from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
#from django.db.models import F

from stats import export
from core import resource
from core import paginator
from core.jsonresponse import create_response
from core.charts_apis import create_line_chart_response
#from weixin.mp_decorators import mp_required
#from market_tools.tools.channel_qrcode.models import ChannelQrcodeSettings, ChannelQrcodeHasMember
#from market_tools.tools.lottery.models import Lottery, LotteryRecord
#import utils.dateutil as dateutil
#from market_tools.tools.lottery.models import STATUS2TEXT as LOTTERY_STATUS2TEXT

from mall.models import *
from utils import dateutil as util_dateutil
import pandas as pd
from core import dateutil
from webapp import models as webapp_models
from webapp import statistics_util as webapp_statistics_util
from core.charts_apis import *
from django.conf import settings
import stats.util as stats_util

FIRST_NAV = export.MANAGEMENT_NAV
DEFAULT_COUNT_PER_PAGE = 20


def compute_brand_value(webapp_id, end_date):
	"""
	根据webapp_id计算品牌价值
	"""
	end_date = util_dateutil.parse_datetime(end_date+" 23:59:59")
	start_date = util_dateutil.get_date_after_days(end_date, -365) # 一年前
	print("start_date:{}, end_date:{}".format(start_date, end_date))
	orders = Order.objects.filter(webapp_id=webapp_id, created_at__range=(start_date, end_date))
	order_count = orders.count()
	print("order count: {}".format(orders.count()))
	if order_count<1:
		return 0.0
	order_data = [(order.webapp_user_id, order.final_price, order.created_at, order.id) for order in orders]
	df = pd.DataFrame(order_data, columns=['wuid', 'fp', 'at', 'id'])
	# 计算购买用户前100人的平均消费金额
	user_avg_consumption = df[['wuid', 'fp']].groupby('wuid').sum().sort('fp', ascending=False).head(100).mean()['fp']  # type: numpy.float64
	print("user average consumption: {}".format(user_avg_consumption))
	# 计算多次购买的用户数数
	buyer_counts = df[df['fp']>1]['wuid'].value_counts()
	buyer_count = len(buyer_counts.keys())
	print("buyer count: {}".format(buyer_count))
	value = user_avg_consumption * buyer_count
	return value


class BrandValue(resource.Resource):
	"""
	微品牌价值
	"""
	app = 'stats'
	resource = 'brand_value'

	@login_required
	def api_get(request):
		"""
		返回微品牌价值的EChart数据

		"""
		#response = create_response(200)
		end_date = request.GET.get('end_date')
		if end_date is None:
			end_date = util_dateutil.now()
		else:
			end_date = util_date.parse_date(end_date)

		webapp_id = request.user_profile.webapp_id
		date_range = pd.date_range(end=end_date, periods=7)
		date_list = []
		values = []
		# TODO: 需要优化。可以一次计算完成
		for date in date_range:
			date_str = util_dateutil.date2string(date.to_datetime())  # 将pd.Timestamp转成datetime
			date_list.append(date_str)
			values.append(compute_brand_value(webapp_id, date_str))
		print("date_list: {}".format(date_list))

		response = create_line_chart_response(
			"",
			"",
			#['2010-10-10', '2010-10-11', '2010-10-12', '2010-10-13'],
			date_list,
			[{
				"name": "品牌价值",
				"values" : values
			}]
			)
		return response

####################################################################
#经营概况 流量、销量统计
####################################################################

class FlowsValue(resource.Resource):
	"""
	流量 统计
	"""
	app = 'stats'
	resource = 'flow_value'

	@login_required
	def api_get(request):
		"""
		获得每日pv、uv统计
		"""
		low_date, high_date, date_range = stats_util.get_date_range(request)
		webapp_id = request.user_profile.webapp_id
		#对当天的统计结果进行更新
		_update_visit_today_daily_statistics(webapp_id)

		statisticses = webapp_models.PageVisitDailyStatistics.objects.filter(webapp_id=webapp_id, url_type=webapp_models.URL_TYPE_ALL, data_date__range=(low_date, high_date))
		date_list = [date.strftime("%Y-%m-%d") for date in dateutil.get_date_range_list(low_date, high_date)]

		date2pv = dict([(s.data_date.strftime('%Y-%m-%d'), s.pv_count) for s in statisticses])
		date2uv = dict([(s.data_date.strftime('%Y-%m-%d'), s.uv_count) for s in statisticses])

		pv_trend_values = []
		uv_trend_values = []
		for date in date_list:
			pv_trend_values.append(date2pv.get(date, 0))
			uv_trend_values.append(date2uv.get(date, 0))

		return create_line_chart_response(
			'',
			'',
			date_list,
			[{
	            "name": "PV",
	            "values" : pv_trend_values
	        }, {
	            "name": "UV",
	            "values" : uv_trend_values
	        }]
		)

def _update_visit_today_daily_statistics(webapp_id):
	"""
	更新今天的pv，uv统计
	"""
	if not settings.IS_UPDATE_PV_UV_REALTIME:
		return

	#先删除当天的pv,uv统计结果，然后重新进行统计
	today = dateutil.get_today()
	webapp_models.PageVisitDailyStatistics.objects.filter(webapp_id=webapp_id, data_date=today).delete()
	webapp_statistics_util.count_visit_daily_pv_uv(webapp_id, today)


class SalesValue(resource.Resource):
	"""
	销量 统计
	"""
	app = 'stats'
	resource = 'sale_value'

	@login_required
	def api_get(request):
		low_date, high_date, date_range = stats_util.get_date_range(request)
		try:
			webapp_id = request.user_profile.webapp_id
			date_list = [date.strftime("%Y-%m-%d") for date in dateutil.get_date_range_list(low_date, high_date)]

			date2count = dict()
			date2price = dict()

			# 11.20从查询mall_purchase_daily_statistics变更为直接统计订单表，解决mall_purchase_daily_statistics遗漏统计订单与统计时间不一样导致的统计结果不同的问题。
			orders = Order.objects.belong_to(webapp_id).filter(created_at__range=(low_date, (high_date+timedelta(days=1))))
			statuses = set([ORDER_STATUS_PAYED_SUCCESSED, ORDER_STATUS_PAYED_NOT_SHIP, ORDER_STATUS_PAYED_SHIPED, ORDER_STATUS_SUCCESSED])
			orders = [order for order in orders if (order.type != 'test') and (order.status in statuses)]
			for order in orders:
				# date = dateutil.normalize_date(order.created_at)
				date = order.created_at.strftime("%Y-%m-%d")
				if order.webapp_id != webapp_id:
					order_price =  Order.get_order_has_price_number(order) + order.postage
				else:
					order_price = order.final_price + order.weizoom_card_money

				if date in date2count:
					old_count = date2count[date]
					date2count[date] = old_count + 1
				else:
					date2count[date] = 1

				if date in date2price:
					old_price = date2price[date]
					date2price[date] = old_price + order_price
				else:
					date2price[date] = order_price

			count_trend_values = []
			price_trend_values = []
			for date in date_list:
				count_trend_values.append(date2count.get(date, 0))
				price_trend_values.append(date2price.get(date, 0.0))

			return create_line_chart_response(
					'',
					'',
					date_list,
					[{
			            "name": "订单数",
			            "values" : count_trend_values
			        }, {
			            "name": "销售额",
			            "values" : price_trend_values
			        }]
				)
		except:
			if settings.DEBUG:
				raise
			else:
				response = create_response(500)
				response.innerErrMsg = unicode_full_stack()
				return response.get_response()