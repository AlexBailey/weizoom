#coding:utf8
"""@package services.virtual_product_service.tasks
virtual_product_service 的Celery task实现

"""
from __future__ import absolute_import
from datetime import datetime

from celery import task

from mall.promotion import models as promotion_models
from mall import models as mall_models
from modules.member import models as member_models
from utils import ding_util
from mall import module_api
import logging

VIRTUAL_ORDER_TYPE = [mall_models.PRODUCT_VIRTUAL_TYPE, mall_models.PRODUCT_WZCARD_TYPE]
# WESHOP_DING_GROUP_ID = '105507196'  #微众商城FT团队钉钉id
WESHOP_DING_GROUP_ID = '80035247'  #发消息测试群

@task
def deliver_virtual_product(request, args):
	"""
	每隔一分钟自动发货一次

	@param request 无用，为了兼容
	@param args dict类型
	"""
	logging.info('start service virtual_product {}'.format(datetime.now().strftime('%Y-%m-%d %H:%M:%S')))

	#获取所有虚拟子订单
	order2products = mall_models.OrderHasProduct.objects.filter(
			order__status=mall_models.ORDER_STATUS_PAYED_NOT_SHIP,
			order__type__in=VIRTUAL_ORDER_TYPE,
			order__origin_order_id__gt=0
		)

	oid2order = {}
	oid2product_id2count = {}
	order_ids = []
	for o2p in order2products:
		order = o2p.order
		order_ids.append(order.order_id)
		product = o2p.product
		oid = order.id
		buy_count = o2p.number

		oid2order[oid] = o2p.order
		if not oid2product_id2count.has_key(oid):
			oid2product_id2count[oid] = {}
		
		if oid2product_id2count[oid].has_key(product.id):
			oid2product_id2count[oid][product.id] += buy_count
		else:
			oid2product_id2count[oid][product.id] = buy_count

		#判断是否有促销活动
		if o2p.promotion_id:
			promotion = None
			try:
				promotion = promotion_models.Promotion.objects.get(id=o2p.promotion_id)
			except Exception, e:
				message = u'获取促销失败\norder id:%s\nproduct id:%d\n商品名称:%s' % (order.order_id, product.id, product.name)
				logging.info(message)
				ding_util.send_to_ding(message, WESHOP_DING_GROUP_ID)

			#判断是否是买赠
			if promotion.type == promotion_models.PROMOTION_TYPE_PREMIUM_SALE:
				premiums = promotion_models.PremiumSaleProduct.objects.filter(premium_sale__id=promotion.detail_id)
				for premium in premiums:
					_product = premium.product
					#判断赠品是否是虚拟类型
					if _product.type in [mall_models.PRODUCT_VIRTUAL_TYPE, mall_models.PRODUCT_WZCARD_TYPE]:
						premium_sale = premium.premium_sale
						if premium.premium_sale.is_enable_cycle_mode:
							premium_product_count = (buy_count / premium_sale.count) * premium.count
						else:
							premium_product_count = premium.count

						logging.info(u'赠品id:%d,名称:%s,个数:%d' % (_product.id, _product.name, premium_product_count))
						if oid2product_id2count[oid].has_key(_product.id):
							oid2product_id2count[oid][_product.id] += premium_product_count
						else:
							oid2product_id2count[oid][_product.id] = premium_product_count

	order2groups = mall_models.OrderHasGroup.objects.filter(order_id__in=order_ids)
	order_id2group_status = {}
	for o2g in order2groups:
		order_id2group_status[o2g.order_id] = o2g.group_status

	logging.info('virtual order count:%d' % len(oid2order))
	for oid in oid2product_id2count:
		can_update_order_status = True  #是否可以更改订单的发货状态
		print 'process order id:', oid
		order = oid2order[oid]

		#判断团购状态
		if order_id2group_status.has_key(order.order_id):
			if order_id2group_status[order.order_id] == 1:
				logging.info(u'团购订单%s可以发货' % order.order_id)
			else:
				can_update_order_status = False
				logging.info(u'团购订单%s团购未成功，跳过发货，团购状态%d' % (order.order_id, order_id2group_status[order.order_id]))
				continue

		#获取会员信息
		member = member_models.WebAppUser.get_member_by_webapp_user_id(order.webapp_user_id)
		if not member:
			message = u'获取member信息失败\n订单id:%s' % order.order_id
			logging.info(message)
			ding_util.send_to_ding(message, WESHOP_DING_GROUP_ID)
			continue

		product_id2count = oid2product_id2count[oid]
		for product_id in product_id2count:
			count = product_id2count[product_id]
			print '  process product id:%d, buy count:%d' % (product_id, count)
			virtual_products = promotion_models.VirtualProduct.objects.filter(product_id=product_id, is_finished=False)
			if virtual_products.count() > 0:
				virtual_product = virtual_products[0]

				#判断该订单里的这个商品是否已经被发过货了，如果发过则不重复发放，且can_update_order_status不变为False
				oids = [order.id]
				if order.origin_order_id > 0:
					oids.append(order.origin_order_id)
				existed_records = promotion_models.VirtualProductHasCode.objects.filter(virtual_product=virtual_product, oid__in=oids)

				if existed_records.count() > 0:
					message = u'该商品已经发过货，无需重复发货\n订单id:%s\n商品id:%d\n福利卡券活动id:%d\n商品名称:%s' % (order.order_id, product_id, virtual_product.id, virtual_product.product.name)
					logging.info(message)
					ding_util.send_to_ding(message, WESHOP_DING_GROUP_ID)
					continue

				#按id顺序发放
				codes = promotion_models.VirtualProductHasCode.objects.filter(virtual_product=virtual_product, status=promotion_models.CODE_STATUS_NOT_GET).order_by('id')

				_c = []
				for code in codes:
					if (not code.can_not_use) and len(_c) < count:
						_c.append(code)

				if len(_c) < count:
					can_update_order_status = False
					message = u'发放虚拟商品时库存不足\n订单id:%s\n商品id:%d\n待发放:%d\n库存:%d\n商品名称:%s\n福利卡券活动id:%d' % (order.order_id, product_id, count, len(_c), virtual_product.product.name, virtual_product.id)
					logging.info(message)
					ding_util.send_to_ding(message, WESHOP_DING_GROUP_ID)
					continue
				
				for code in _c:
					print '    deliver code:', code.code
					code.member_id = member.id
					code.get_time = datetime.now()
					code.oid = order.origin_order_id
					code.order_id = order.order_id
					code.status = promotion_models.CODE_STATUS_GET
					code.save()

					if virtual_product.product.type == mall_models.PRODUCT_WZCARD_TYPE:
						#如果商品是微众卡的话，需要往MemberHasWeizoomCard表里写入一份信息，方便手机卡包里的微众卡能正常显示
						try:
							member_has_wzcard = promotion_models.MemberHasWeizoomCard.objects.create(
								member_id=member.id,
								# member_name=member.username,
								member_name='',
								card_number=code.code,
								card_password=code.password,
								relation_id=code.virtual_product.id,
								source=promotion_models.WEIZOOM_CARD_SOURCE_VIRTUAL
							)
							logging.info(u'订单%s发放微众卡到member_has_wzcard：%d' % (order.order_id, member_has_wzcard.id))
						except Exception, e:
							message = u'微众卡已经发放成功，但写入MemberHasWeizoomCard信息失败\n订单id:%s\n商品id:%d\n商品名称:%s' % (order.order_id, product_id, virtual_product.product.name)
							logging.info(message)
							logging.info(e)
							ding_util.send_to_ding(message, WESHOP_DING_GROUP_ID)
			else:
				can_update_order_status = False
				message = u'虚拟商品发货失败，商品没有关联福利卡券活动\n订单id:%s\n商品id:%d' % (order.order_id, product_id)
				logging.info(message)
				ding_util.send_to_ding(message, WESHOP_DING_GROUP_ID)

		if can_update_order_status:
			#更改订单状态，发货
			logging.info(u'订单发货：%s'% order.order_id)
			module_api.ship_order(order.id, '', '', u'系统', '', False, False)

	return 'OK {}'.format(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
