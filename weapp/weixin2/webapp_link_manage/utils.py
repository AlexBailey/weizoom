# -*- coding: utf-8 -*-
from market_tools.tools.card_exchange.export import get_card_exchange_link

__author__ = 'liupeiyu'

import json
import requests
import copy
from datetime import timedelta, datetime
from django.conf import settings
from django.db.models import Q

from eaglet.utils.resource_client import Resource

from mall.models import Product, ProductCategory, PRODUCT_SHELVE_TYPE_ON, ProductPool, PP_STATUS_ON
from mall.promotion.models import CouponRule, Promotion, PROMOTION_TYPE_COUPON
from market_tools.tools.vote.models import Vote
from market_tools.tools.lottery.models import Lottery
from market_tools.tools.red_envelope.models import RedEnvelope
from market_tools.tools.activity.models import Activity
from market_tools.tools.research.models import Research
from market_tools.tools.test_game.models import TestGame
from market_tools.tools.shake.models import Shake
from webapp.modules.cms.models import Article
from webapp.models import Project

from market_tools.tools.member_qrcode.export import get_member_qrcode_webapp_link
from market_tools.tools.complain.export import get_complain_webapp_link
from apps.customerized_apps.shengjing.export import get_shengjing_link_targets
from market_tools.tools.channel_qrcode.export import get_channel_qrcode_webapp_link

from mall.promotion.models import RedEnvelopeRule

from apps.customerized_apps.exsign.export import get_exsign_webapp_link
from account.models import UserProfile
from account.account_util import get_token_for_logined_user

from core.exceptionutil import unicode_full_stack
from watchdog.utils import watchdog_error, watchdog_info

def get_webapp_link_menu_objectes(request):
	"""
	获取微站内部链接的menu的json数据
	"""
	webapp_owner_id = request.manager.id
	workspace_id = request.user_profile.homepage_workspace_id
	mall_type = request.user_profile.webapp_type

	menus = {
		'webappPage': {
			'id': 1,
			'name': '微页面',
			'title':[{
				'name': '微页面',
				'type': 'webappPage',
				'add_btn_title': '新建微页面',
				'add_link': '/termite2/pages/'
			}]
		},
		'product':{
			'id': 2,
			'name': '商品及分组',
			'title': [{
				'name': '已上架商品',
				'type': 'product',
				'add_btn_title': '新建商品',
				'add_link': '' if mall_type else '/mall2/product/'
			},{
				'name': '商品分组',
				'type': 'category',
				'add_btn_title': '新建分组',
				'add_link': '/mall2/category_list/'
			}]
		},
		'webappHome':{
			'id': 3,
			'name': '店铺主页',
			'link': './?workspace_id=home_page&webapp_owner_id={}&workspace_id={}&project_id=0'.format(webapp_owner_id, workspace_id)
		},
		'member': {
			'id': 4,
			'name': '会员主页',
			'link': './?module=user_center&model=user_info&action=get&workspace_id=mall&webapp_owner_id={}'.format(webapp_owner_id)
		},
		'shoppingCart': {
			'id': 5,
			'name': '购物车',
			'link': './?module=mall&model=shopping_cart&action=show&workspace_id=mall&webapp_owner_id={}'.format(webapp_owner_id)
		},
		'marketPage': {
			'id': 6,
			'name': '营销推广',
			'title': [
			{
				'name': '砸金蛋',
				'type': 'egg',
				'add_btn_title': '新建砸金蛋',
				'add_link': '/apps/egg/egg/'
			}, {
				'name': '刮刮卡',
				'type': 'scratch',
				'add_btn_title': '新建刮刮卡',
				'add_link': '/apps/scratch/scratch/'
			}, {
				'name': '抽奖',
				'type': 'lottery',
				'add_btn_title': '新建抽奖',
				'add_link': '/apps/lottery/lottery/'
			}, {
				'name': '幸运码抽奖',
				'type': 'exlottery',
				'add_btn_title': '新建幸运码抽奖',
				'add_link': '/apps/exlottery/exlottery/'
			}, {
				'name': '扫码抽奖',
				'type': 'scanlottery',
				'add_btn_title': '新建扫码抽奖',
				'add_link': '/apps/scanlottery/scanlottery/',
				'users': ['jobs', 'ceshi01', 'sudao']
			},
			# {
			# 	'name': '红包',
			# 	'type': 'red',
			# 	'add_btn_title': '新建红包',
			# 	'add_link': '/market_tools/red_envelope/edit/0/'
			# },
				{
				'name': '优惠券',
				'type': 'coupon',
				'add_btn_title': '新建优惠券',
				'add_link': '/mall2/coupon_rule/'
			}, {
				'name': '微信投票',
				'type': 'vote',
				'add_btn_title': '新建投票',
				'add_link': '/apps/vote/vote'
			}, {
				'name': '用户调研',
				'type': 'survey',
				'add_btn_title': '新建调研',
				'add_link': '/apps/survey/survey'
			}, {
				'name': '活动报名',
				'type': 'event',
				'add_btn_title': '新建活动报名',
				'add_link': '/apps/event/event'
			},{
				'name': '分享红包',
				'type': 'red_envelope',
				'add_btn_title': '新建分享红包',
				'add_link': '/apps/red_envelope/red_envelope_rule/'
			},{
				'name': '微助力',
				'type': 'powerme',
				'add_btn_title': '新建微助力',
				'add_link': '/apps/powerme/powerme/'
			},{
				'name': '用户反馈',
				'type': 'exsurvey',
				'add_btn_title': '新建用户反馈',
				'add_link': '/apps/exsurvey/exsurvey/',
				'users': ['jobs','njtest','ceshi01', 'weizoomjy', 'Aierkang', 'wzjx001', 'weizoomxs', 'weizoommm', 'weshop', 'weizoomclub', 'weizoomshop', 'BITC', 'weizoomhtxp'] #这些帐号可以显示用户反馈

			},{
				'name': '团购',
				'type': 'group',
				'add_btn_title': '新建团购',
				'add_link': '/apps/group/group/'
			},{
				'name': '高级投票',
				'type': 'shvote',
				'add_btn_title': '新建投票',
				'add_link': '/apps/shvote/shvote/',
				'users': ['jobs','jierunda', 'ceshi01']
			},
			# {
			# 	'name': '拼红包',
			# 	'type': 'red_packet',
			# 	'add_btn_title': '新建拼红包',
			# 	'add_link': '/apps/red_packet/red_packet/'
			# }
			# {
			# 	'name': '趣味测试',
			# 	'type': 'test_game',
			# 	'add_btn_title': '新建趣味测试',
			# 	'add_link': '/market_tools/test_game/test_game/create/'
			# }, {
			# 	'name': '摇一摇',
			# 	'type': 'shake',
			# 	'add_btn_title': '新建摇一摇',
			# 	'add_link': '/market_tools/shake/edit/0/'
			# }
			]
		},
		'memberQrcode': {
			'id': 7,
			'name': '推广扫码',
			'link': get_member_qrcode_webapp_link(request)
		},
		'channelQrcode': {
			'id': 10,
			'name': '代言人二维码',
			'link': get_channel_qrcode_webapp_link(request)
		},

		'myOrder': {
			'id': 8,
			'name': '我的订单',
			'link': './?module=mall&model=order_list&action=get&workspace_id=mall&webapp_owner_id=%d' % request.manager.id
		},
		'shengjingCustom': {
			'id': 9,
			'name': '盛景定制APP',
			'title': [{
				'name': '盛景定制APP',
				'type': 'shengjing_app',
				'add_link': '/mall2/product/'
			}]
		},
		'sign': {
			'id': 11,
			'name': '签到',
			'link': 'http://%s/m/apps/sign/m_sign/?webapp_owner_id=%d' % (settings.MARKET_MOBILE_DOMAIN, request.manager.id)
		},
		'cardExchange': {
			'id': 13,
			'name': '微众卡兑换平台',
			'link': get_card_exchange_link(request),
			'users': ['jobs', 'njtest', 'ceshi01', 'fulilaile']
		},
		'evaluate': {
			'id': 14,
			'name': '待评价列表',
			'link': '%s/mall/waiting_review_orders/?woid=%d' % (settings.H5_HOST, request.manager.id)
		},
		'exsign': {
			'id': 15,
			'name': '专项签到',
			'link': get_exsign_webapp_link(request),
			'users': ['jobs', 'ceshi01', 'weshop', 'BITC']
		}
	}


	#替换menu中的百宝箱app 百宝箱独立
	try:
		api_resp = Resource.use('marketapp_apiserver').get({
			'resource':'apps.get_apps_link_menu',
			'data':{'webapp_owner_id': str(request.manager.id)}
		})
		watchdog_info('call marketapp_apiserver: apps.get_apps_link_menu, resp==> \n{}'.format(api_resp))

		if api_resp and api_resp['code'] == 200:
			resp_data = api_resp['data']
			token = get_token_for_logined_user(request.user)
			token_str = '?token=' + token

			for app in copy.deepcopy(menus['marketPage']['title']):
				app_name = app['type']
				if app_name in resp_data.keys():
					menus['marketPage']['title'].remove(app)
					resp_data[app_name]['add_link'] += token_str  # 增加免登录token
					menus['marketPage']['title'].append(resp_data[app_name])
	except:
		notify_message = u"从marketapp获取活动列表失败，cause: \n{}".format(unicode_full_stack())
		watchdog_error(notify_message)

	return menus


def get_webapp_link_objectes_for_type(request, type, query, order_by):
	"""
	获取相应的链接
	"""
	user = request.manager
	webapp_owner_id = user.id
	today = datetime.today()
	type2object = {
		'webappPage': {
			'class': Project,
			'query_name': 'site_title',
			'link_template': './?workspace_id=home_page&webapp_owner_id=%d&project_id={}' % webapp_owner_id,
			'filter': {
				'is_enable': True
			}
		},
		'product': {
			'class': Product, #is_deleted=False,
			'query_name': 'name',
			'link_template': './?woid=%d&module=mall&model=product&rid={}' % webapp_owner_id,
			'filter':{
				"is_deleted": False,
				"shelve_type": PRODUCT_SHELVE_TYPE_ON
			}
		},
		'category': {
			'class': ProductCategory,
			'query_name': 'name',
			'link_template': './?woid=%d&module=mall&model=products&action=list&category_id={}' % webapp_owner_id,
			'filter':{}
		},
		'lottery': {
			'class': Lottery,
			'query_name': 'name',
			'link_template': './?module=market_tool:lottery&model=lottery&action=get&lottery_id={}&workspace_id=market_tool:lottery&webapp_owner_id=%d&project_id=0' % webapp_owner_id,
			'filter': {
				"is_deleted": False,
				"end_at__gt": today
			}
		},
		'red': {
			'class': RedEnvelopeRule,
			'query_name': 'name',
			'link_template': './?module=market_tool:share_red_envelope&model=share_red_envelope&action=get&red_envelope_rule_id={}&webapp_owner_id=%d&project_id=0' % webapp_owner_id,
			'filter': {
				"is_delete": False,
				"receive_method": True,
			}
		},
		'coupon': {
			'class': Promotion,
			'query_name': 'name',
			'link_template': './?module=market_tool:coupon&model=coupon&action=get&workspace_id=market_tool:coupon&webapp_owner_id=%d&project_id=0&rule_id={}' % webapp_owner_id,
			'filter': {
				"type": PROMOTION_TYPE_COUPON,
				"status__lt": 3,
				"end_date__gt": today.strftime('%Y-%m-%d %H:%M:%S')
			}
		},
		'vote': {
			'class': Vote,
			'query_name': 'name',
			'link_template': './?module=market_tool:vote&model=vote&action=get&vote_id={}&workspace_id=market_tool:vote&webapp_owner_id=%d&project_id=0' % webapp_owner_id,
			'filter': {}
		},
		'survey': {
			'class': Research,
			'query_name': 'name',
			'link_template': './?module=market_tool:research&model=research&action=get&research_id={}&workspace_id=market_tool:research&webapp_owner_id=%d&project_id=0' % webapp_owner_id,
			'filter': {
				"is_deleted": False
			}
		},
		'activity': {
			'class': Activity,
			'query_name': 'name',
			'link_template': './?module=market_tool:activity&model=activity&action=get&activity_id={}&workspace_id=market_tool:activity&webapp_owner_id=%d&project_id=0' % webapp_owner_id,
			'filter': {
				"end_date__gt": today
			}
		},
		'test_game': {
			'class': TestGame,
			'query_name': 'name',
			'link_template': './?module=market_tool:test_game&model=test_game&action=get&game_id={}&workspace_id=market_tool:test_game&webapp_owner_id=%d&project_id=0' % webapp_owner_id,
			'filter': {}
		},
		'shengjing_app': {
			'class': '',
			'query_name': 'name',
			'link_template': './?module=market_tool:shengjing_app&model=shengjing_app&action=get&game_id={}&workspace_id=market_tool:shengjing_app&webapp_owner_id=%d&project_id=0' % webapp_owner_id,
			'filter': {}
		},
		'shake': {
			'class': Shake,
			'query_name': 'name',
			'link_template': './?module=market_tool:shake&model=shake&action=get&shake_id={}&workspace_id=market_tool:shake&webapp_owner_id=%d&project_id=0' % webapp_owner_id,
			'filter': {
				"is_deleted": False
			}
		},
	}

	item = type2object[type]
	if type == 'shengjing_app':
		objects = get_shengjing_link_targets(request)
	else:
		kwargs = {
			'owner': user
		}
		# 合并过滤条件
		kwargs.update(item.get('filter', {}))
		if query and len(query) > 0:
			kwargs[item['query_name']+'__contains'] = query
		if request.user_profile.webapp_type == 1:
			if item['class'] == Product:
				product_pool = ProductPool.objects.filter(woid=request.manager.id, status=PP_STATUS_ON)
				
				product_ids = [pool.product_id for pool in product_pool]
				product_pool_kwargs = {}
				product_pool_kwargs['id__in'] = product_ids
				if query and len(query) > 0:
					product_pool_kwargs['name__contains'] = query

				objects = item['class'].objects.filter(Q(**kwargs)|Q(**product_pool_kwargs)).order_by(order_by)
				

			else:
				objects = item['class'].objects.filter(**kwargs).order_by(order_by)
		else:
			objects = item['class'].objects.filter(**kwargs).order_by(order_by)

		if type == 'webappPage':
			objects = objects.order_by('-is_active', '-id')

		if type == 'coupon':
			# 组织detail
			Promotion.fill_details(request.manager, objects, {
	            'with_product': True,
	            'with_concrete_promotion': True
        	})

	return objects, item


def get_menu_item_by_name(request, menu_type, link_type):
	menus = get_webapp_link_menu_objectes(request)

	titles = menus[menu_type]['title']
	for item in titles:
		if item['type'] == link_type:
			return item

	return None


def get_selected_by_link_target(request, menu_type, link_type, link_target_str):
	if link_target_str and len(link_target_str) > 2:
		selected_link_target = json.loads(link_target_str)
		selected_id = selected_link_target['workspace']
		if selected_id == "custom":
			selected_id = 0
		else:
			selected_id = selected_id

		item = get_menu_item_by_name(request, menu_type, link_type)
		if item and item['name'] == selected_link_target['data_category']:
			is_selected_type = True
		else:
			is_selected_type = False
	else:
		is_selected_type = False
		selected_id = 0

	return selected_id, is_selected_type