# -*- coding: utf-8 -*-

#import json
#from datetime import datetime
#from django.http import HttpResponseRedirect
#from django.template import RequestContext
#from django.contrib.auth.decorators import login_required
#from django.shortcuts import render_to_response
#from django.db.models import F

#from core import resource
from core import api_resource
from wapi.decorators import param_required
#from mall import models as mall_models

#from wapi.decorators import wapi_access_required
from wapi.wapi_utils import create_json_response

from stats.manage.brand_value_utils import get_brand_value

from utils import dateutil as utils_dateutil

class BrandValue(api_resource.ApiResource):
	"""
	获取微品牌价值的接口
	"""
	app = 'stats'
	resource = 'brand_value'

	@param_required(['wid', 'dates'])
	def get(args):
		"""
		获取微品牌价值

		@param wid webapp_id
		@param dates 日期列表，多日期用逗号(,)分隔。默认是当天。
		"""
		webapp_id = args.get('wid')
		#print("webapp_id: {}".format(webapp_id))
		dates = args.get('dates')
		if dates is None or len(dates)<1:
			dates = [ utils_dateutil.date2string(utils_dateutil.now()) ]
		else:
			dates = dates.split(',')

		#values = [ {"date":date_str, "bv":get_brand_value(webapp_id, date_str)} for date_str in dates ]
		values = {date_str: get_brand_value(webapp_id, date_str) for date_str in dates}

		#return create_json_response(200, {
		#		"values": values
		#	})
		return {"values": values}
