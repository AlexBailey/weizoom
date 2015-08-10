# __author__ : "冯雪静"
Feature: 在webapp中购买有会员折扣的商品
	bill能在webapp中购买jobs添加的"会员价的商品"


Background:
	Given jobs登录系统
	And jobs已添加商品规格
		"""
		[{
			"name": "尺寸",
			"type": "文字",
			"values": [{
				"name": "M"
			}, {
				"name": "S"
			}]
		}]
		"""
	When jobs添加会员等级
		"""
		[{
			"name": "铜牌会员",
			"upgrade": "手动升级",
			"shop_discount": "9"
		}, {
			"name": "银牌会员",
			"upgrade": "手动升级",
			"shop_discount": "8"
		}, {
			"name": "金牌会员",
			"upgrade": "手动升级",
			"shop_discount": "7"
		}]
		"""
	Then jobs能获取会员等级列表
		"""
		[{
			"name": "普通会员",
			"upgrade": "自动升级",
			"shop_discount": "10"
		}, {
			"name": "铜牌会员",
			"upgrade": "手动升级",
			"shop_discount": "9"
		}, {
			"name": "银牌会员",
			"upgrade": "手动升级",
			"shop_discount": "8"
		}, {
			"name": "金牌会员",
			"upgrade": "手动升级",
			"shop_discount": "7"
		}]
		"""
	When jobs已添加支付方式
		"""
		[{
			"type": "货到付款",
			"description": "我的货到付款",
			"is_active": "启用"
		},{
			"type": "微信支付",
			"description": "我的微信支付",
			"is_active": "启用",
			"weixin_appid": "12345",
			"weixin_partner_id": "22345",
			"weixin_partner_key": "32345",
			"weixin_sign": "42345"
		}]
		"""
	And jobs已添加商品
		"""
		[{
			"name": "商品1",
			"price": 100.00,
			"member_price": true,
			"model": {
				"models": {
					"standard": {
						"price": 100.00,
						"stock_type": "有限",
						"stocks": 2
					}
				}
			}
		}, {
			"name": "商品2",
			"member_price": true,
			"is_enable_model": "启用规格",
			"model": {
				"models":{
					"M": {
						"price": 300.00,
						"stock_type": "无限"
					},
					"S": {
						"price": 300.00,
						"stock_type": "无限"
					}
				}
			}
		}, {
			"name": "商品3",
			"price": 200.00
		}]
		"""
	And bill关注jobs的公众号
	And tom关注jobs的公众号
	Then jobs可以获得会员列表
		"""
		[{
			"name": "tom",
			"member_rank": "普通会员"
		}, {
			"name": "bill",
			"member_rank": "铜牌会员"
		}]
		"""


Scenario: 1 购买单个会员价商品
	jobs添加商品后
	1. tom能在webapp中购买jobs添加的会员价商品
	2. tom是普通会员没有会员折扣
	3. bill能在webapp中购买jobs添加的会员价商品
	4. bill是铜牌会员有会员折扣

	When tom访问jobs的webapp
	And tom购买jobs的商品
		"""
		{
			"products": [{
				"name": "商品1",
				"count": 1
			}]
		}
		"""
	Then tom成功创建订单
		"""
		{
			"status": "待支付",
			"final_price": 100.00,
			"products": [{
				"name": "商品1",
				"price": 100.00,
				"count": 1
			}]
		}
		"""
	When bill访问jobs的webapp
	And bill购买jobs的商品
		"""
		{
			"products": [{
				"name": "商品1",
				"count": 1
			}]
		}
		"""
	Then bill成功创建订单
		"""
		{
			"status": "待支付",
			"final_price": 90.00,
			"members_money": 10.00,
			"products": [{
				"name": "商品1",
				"member_price": 90.00,
				"type": "members",
				"count": 1
			}]
		}
		"""


Scenario: 2 购买多个会员价商品
	jobs添加商品后
	1. bill能在webapp中把jobs添加的会员价商品添加到购物车
	2. bill能获取购物车的商品
	3. bill能从购物车进行购买jobs的商品

	When bill访问jobs的webapp
	And bill加入jobs的商品到购物车
		"""
		[{
			"name": "商品1",
			"count": 1
		}, {
			"name": "商品2",
			"model": {
				"models":{
					"M": {
						"count": 1
					}
				}
			}
		}, {
			"name": "商品2",
			"model": {
				"models":{
					"S": {
						"count": 1
					}
				}
			}
		}]
		"""
	Then bill能获得购物车
		"""
		{
			"product_groups": [{
				"products": [{
					"name": "商品1",
					"member_price": 90.00,
					"count": 1
				}]
			}, {
				"products": [{
					"name": "商品2",
					"member_price": 270.00,
					"count": 1,
					"model": "M"
				}]
			}, {
				"products": [{
					"name": "商品2",
					"member_price": 270.00,
					"count": 1,
					"model": "S"
				}]
			}],
			"invalid_products": []
		}
		"""
	When bill从购物车发起购买操作
		"""
		{
			"action": "click",
			"context": [{
				"name": "商品1"
			}, {
				"name": "商品2",
				"model": "M"
			}, {
				"name": "商品2",
				"model": "S"
			}]
		}
		"""
	Then bill成功创建订单
		"""
		{
			"status": "待支付",
			"final_price": 630.00,
			"members_money": 70.00,
			"products": [{
				"name": "商品1",
				"member_price": 90.00,
				"count": 1
			}, {
				"name": "商品2",
				"member_price": 270.00,
				"count": 1,
				"model": "M"
			}, {
				"name": "商品2",
				"member_price": 270.00,
				"count": 1,
				"model": "S"
			}]
		}
		"""


Scenario: 3 购买多个商品包括会员价商品
	jobs添加商品后
	1. bill能在webapp中购买jobs的商品
	2. bill购买的商品中有普通商品和会员价商品
	
	When bill访问jobs的webapp
	And bill加入jobs的商品到购物车
		"""
		[{
			"name": "商品1",
			"count": 1
		}, {
			"name": "商品3",
			"count": 1
		}]
		"""
	Then bill能获得购物车
		"""
		{
			"product_groups": [{
				"products": [{
					"name": "商品1",
					"member_price": 90.00,
					"count": 1
				}]
			}, {
				"products": [{
					"name": "商品3",
					"price": 200.00
			}],
			"invalid_products": []
		}
		"""
	When bill从购物车发起购买操作
		"""
		{
			"action": "click",
			"context": [{
				"name": "商品1"
			}, {
				"name": "商品3"
			}]
		}
		"""
	Then bill成功创建订单
		"""
		{
			"status": "待支付",
			"final_price": 290.00,
			"members_money": 10.00,
			"products": [{
				"name": "商品1",
				"member_price": 90.00,
				"count": 1
			}, {
				"name": "商品2",
				"price": 200.00,
				"count": 1
			}]
		}
		"""


Scenario: 4 订单完成后，达到自动升级的条件
	jobs添加商品后
	1. tom能在webapp中购买jobs的商品后，完成订单后
	2. tom达到自动升级的条件，并升级
	
	Given jobs登录系统
	When jobs开启自动升级
		"""
		{
			"upgrade": "自动升级",
			"condition": ["满足一个条件即可"]
		}
		"""
	When jobs更新会员等级'铜牌会员'
		"""
		{
			"name": "铜牌会员",
			"upgrade": "自动升级",
			"pay_money": 500.00,
			"pay_times": 20,
			"upgrade_lower_bound": 10000,
			"shop_discount": "9"
		}
		"""
	And jobs更新会员等级'银牌会员'
		"""
		{
			"name": "银牌会员",
			"upgrade": "自动升级",
			"pay_money": 1000.00,
			"pay_times": 30,
			"upgrade_lower_bound": 30000,
			"shop_discount": "8"
		}
		"""
	Then jobs能获取会员等级列表
		"""
		[{
			"name": "普通会员",
			"upgrade": "自动升级",
			"shop_discount": "10"
		}, {
			"name": "铜牌会员",
			"upgrade": "自动升级",
			"pay_money": 500.00,
			"pay_times": 20,
			"upgrade_lower_bound": 10000,
			"shop_discount": "9"
		}, {
			"name": "银牌会员",
			"upgrade": "自动升级",
			"pay_money": 1000.00,
			"pay_times": 30,
			"upgrade_lower_bound": 30000,
			"shop_discount": "8"
		}, {
			"name": "金牌会员",
			"upgrade": "手动升级",
			"shop_discount": "7"
		}]
		"""
	When tom访问jobs的webapp
	And tom购买jobs的商品
		"""
		{
			"ship_name": "tom",
			"ship_tel": "13811223344",
			"ship_area": "北京市 北京市 海淀区",
			"ship_address": "泰兴大厦",
			"products": [{
				"name": "商品2",
				"model": "M",
				"count": 2
			}]
		}
		"""
	When tom使用支付方式'货到付款'进行支付
	Then tom支付订单成功
		"""
		{
			"status": "待发货",
			"final_price": 600.00,
			"products": [{
				"name": "商品2",
				"price": 300.00,
				"model": "M",
				"count": 2
			}]
		}
		"""
	Given jobs登录系统
	Then jobs可以获得最新订单详情
		"""
		{
			"status": "待发货",
			"actions": ["发货", "取消订单"],
			"final_price": 600.00,
			"ship_name": "tom",
			"ship_tel": "13811223344",
			"ship_area": "北京市 北京市 海淀区 泰兴大厦",
			"products": [{
				"name": "商品2",
				"price": 300.00,
				"model": "M",
				"count": 2
			}]
		}
		"""
	When jobs对最新订单进行发货
	Then jobs可以获得最新订单详情
		"""
		{
			"status": "已发货",
			"actions": ["标记完成", "取消订单", "修改物流"]
			"final_price": 600.00,
			"ship_name": "tom",
			"ship_tel": "13811223344",
			"ship_area": "北京市 北京市 海淀区 泰兴大厦",
			"products": [{
				"name": "商品2",
				"price": 300.00,
				"model": "M",
				"count": 2
			}]
		}
		"""
	#tom已经满足一个升级条件，自动升级为铜牌会员
	When jobs'完成'最新订单
	Then jobs可以获得会员列表
		"""
		[{
			"name": "tom",
			"member_rank": "铜牌会员",
			"pay_money": 600.00,
			"pay_times": 1,
			"upgrade_lower_bound": 0
		}, {
			"name": "bill",
			"member_rank": "铜牌会员",
			"pay_money": 0.00,
			"pay_times": 0,
			"upgrade_lower_bound": 0
		}]
		"""