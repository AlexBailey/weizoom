# -*- coding: utf-8 -*-

from core import api_resource
from wapi.decorators import param_required
#from wapi.wapi_utils import create_json_response

#from mall import models as mall_models
from mall import module_api as mall_api
from modules.member import models as member_models

from utils import dateutil as utils_dateutil

class Product(api_resource.ApiResource):
	"""
	商品
	"""
	app = 'mall'
	resource = 'product'

	@staticmethod
	def to_dict(product):
		data = {
			'id': product.id,
			'owner_id': product.owner_id,
			'name': product.name,
			'physical_unit': product.physical_unit,
			'price': product.price,	
			'introduction': product.introduction,
			'weight': product.weight,
			'thumbnails_url': product.thumbnails_url,
			'pic_url': product.pic_url,
			'detail': product.detail,
			'remark': product.remark,

			'update_time': utils_dateutil.datetime2string(product.update_time),
			'created_at': utils_dateutil.datetime2string(product.created_at),

			'shelve_type': product.shelve_type,

			'purchase_price': product.purchase_price,

			'is_use_cod_pay_interface': product.is_use_cod_pay_interface,
			'is_support_make_thanks_card': product.is_support_make_thanks_card,

			'stock_type': product.stock_type,
			# 微众商城代码
			# 'weshop_status': product.weshop_status,
			'promotion_title': product.promotion_title,
			'is_use_online_pay_interface': product.is_use_online_pay_interface,
			'postage_type': product.postage_type,
			'detail': product.detail,
			'display_index': product.display_index,
			'unified_postage_money': product.unified_postage_money,
			'supplier': product.supplier,
			'type': product.type,
			'shelve_start_time': product.shelve_start_time,
			'shelve_end_time': product.shelve_end_time,
			'shelve_type': product.shelve_type,
			'thumbnails_url': product.thumbnails_url,

			'bar_code': product.bar_code,
			'user_code': product.user_code,
			'is_deleted': product.is_deleted,
			# 微众商城代码
			# 'weshop_sync': product.weshop_sync,
			'is_member_product': product.is_member_product,
			'is_use_custom_model': product.is_use_custom_model,
			'stocks': product.stocks if product.stock_type else '无限',
			'sales': getattr(product, 'sales', 0)
		}
		if product.id!=None:
			data['detail_link']= '/mall2/product/?id=%d&source=onshelf' % product.id,
		if hasattr(product, 'min_limit'):
			data['min_limit'] = product.min_limit
		if hasattr(product, 'price_info'):
			data['price_info'] = product.price_info
		if hasattr(product, 'models') and product.models!=None:
			if len(product.models) > 1:
				data['models'] = product.models[1:]
			else:
				data['models'] = product.models
		if hasattr(product, 'properties'):
			data['properties'] = product.properties
		if hasattr(product, 'product_model_properties'):
			data['product_model_properties'] = product.product_model_properties
		if hasattr(product, 'swipe_images_json'):
			data['swipe_images_json'] = product.swipe_images_json
		if hasattr(product, 'promotion'):
			data['promotion'] = product.promotion
			if hasattr(product, 'master_promotion_title'):
				data['master_promotion_title'] = product.master_promotion_title
			if hasattr(product, 'promotion_model'):
				data['promotion_model'] = product.promotion_model
		if hasattr(product, 'display_price'):
			data['display_price'] = product.display_price
		if hasattr(product, 'product_review'):
			data['product_review'] = product.product_review
		if hasattr(product, 'integral_sale'):
			data['integral_sale'] = product.integral_sale
			if hasattr(product, 'integral_sale_model'):
				data['integral_sale_model'] = product.integral_sale_model
			if hasattr(product, 'integral_sale_promotion_title'):
				data['integral_sale_promotion_title'] = product.integral_sale_promotion_title

		if hasattr(product, 'display_price_range'):
			data['display_price_range'] = product.display_price_range
		if hasattr(product, 'categories'):
			data['categories'] = product.categories
		if hasattr(product, 'total_stocks'):
			data['total_stocks'] = product.total_stocks
		if hasattr(product, 'is_sellout'):
			data['is_sellout'] = product.is_sellout
		if hasattr(product, 'standard_model'):
			data['standard_model'] = product.standard_model
		if hasattr(product, 'current_used_model'):
			data['current_used_model'] = product.current_used_model

		return data

	@param_required(['id', 'woid', 'member_grade_id', 'wuid'])
	def get(args):
		"""
		获取商品详情

		@param id 商品ID
		"""
		product_id = args['id']
		webapp_owner_id = args['woid']
		member_grade_id = args['member_grade_id']
		webapp_user = member_models.WebAppUser.objects.get(id = args['wuid'])
  
		product = mall_api.get_product_detail(webapp_owner_id, product_id, webapp_user, member_grade_id)
		#print("{}".format(product))
		return Product.to_dict(product)
