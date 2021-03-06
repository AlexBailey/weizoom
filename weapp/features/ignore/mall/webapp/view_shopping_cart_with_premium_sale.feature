Feature: 添加参加买赠活动的商品到购物车后，浏览购物车中的商品

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
	And jobs已添加商品
		"""
		[{
			"name": "商品1",
			"price": 30
		}, {
			"name": "商品2",
			"price": 5
		}, {
			"name": "商品3",
			"is_enable_model": "启用规格",
			"model": {
				"models":{
					"M": {
						"price": 7,
						"stock_type": "有限",
						"stocks": 2
					},
					"S": {
						"price": 8,
						"stock_type": "无限"
					}
				}
			}
		}, {
			"name": "商品4",
			"is_enable_model": "启用规格",
			"model": {
				"models":{
					"M": {
						"price": 9,
						"stock_type": "无限"
					}
				}   
			}
		}, {
			"name": "商品5",
			"is_enable_model": "启用规格",
			"model": {
				"models":{
					"S": {
						"price": 10,
						"stock_type": "无限"
					}
				}
			}
		}]	
		"""
	When jobs创建买赠活动
		"""
		[{
			"name": "商品1买一赠二",
			"start_date": "今天",
			"end_date": "1天后",
			"products": ["商品1"],
			"premium_products": [{
				"name": "商品2",
				"count": 1
			}, {
				"name": "商品3",
				"count": 2
			}],
			"count": 2,
			"is_enable_cycle_mode": true
		}, {
			"name": "商品2买一赠一",
			"start_date": "今天",
			"end_date": "2天后",
			"products": ["商品2"],
			"premium_products": [{
				"name": "商品4",
				"count": 1
			}],
			"count": 1,
			"is_enable_cycle_mode": false
		}, {
			"name": "商品3买一赠一",
			"start_date": "今天",
			"end_date": "1天后",
			"products": ["商品3"],
			"premium_products": [{
				"name": "商品4",
				"count": 1
			}],
			"count": 1,
			"is_enable_cycle_mode": false
		}]
		"""
	And bill关注jobs的公众号


@ui2 @ui-mall @ui-mall.webapp @ui-mall.webapp.shopping_cart
Scenario: 放入1个商品到购物车，商品不满足买赠的购买基数
	调整数量后，会显示/隐藏赠品区域
	
	When bill访问jobs的webapp
	And bill加入jobs的商品到购物车
		"""
		[{
			"name": "商品1",
			"count": 1
		}]
		"""
	When bill访问jobs的webapp:ui
	Then bill能获得购物车:ui
		"""
		{
			"total_product_count": 1,
			"total_price": 30.0,
			"product_groups": [{
				"promotion": null,
				"products": [{
					"name": "商品1",
					"price": 30.0,
					"count": 1
				}]
			}]
		}
		"""
	#验证调整数量后的行为
	When bill增加'1'个购物车中'商品1'的数量:ui
	Then bill能获得购物车:ui
		"""
		{
			"total_product_count": 2,
			"total_price": 60.0,
			"product_groups": [{
				"promotion": {
					"type": "premium_sale",
					"result": {
						"premium_products": [{
							"name": "商品2", 
							"count": 1
						}, {
							"name": "商品3",
							"count": 2
						}]
					}
				},
				"products": [{
					"name": "商品1",
					"price": 30.0,
					"count": 2
				}]
			}]
		}
		"""
	When bill减少'1'个购物车中'商品1'的数量:ui
	Then bill能获得购物车:ui
		"""
		{
			"total_product_count": 1,
			"total_price": 30.0,
			"product_groups": [{
				"promotion": null,
				"products": [{
					"name": "商品1",
					"price": 30.0,
					"count": 1
				}]
			}]
		}
		"""


@ui2 @ui-mall @ui-mall.webapp @ui-mall.webapp.shopping_cart
Scenario: 放入1个商品到购物车，商品数量等于买赠的购买基数
	
	When bill访问jobs的webapp
	And bill加入jobs的商品到购物车
		"""
		[{
			"name": "商品1",
			"count": 2
		}]
		"""
	When bill访问jobs的webapp:ui
	Then bill能获得购物车:ui
		"""
		{
			"total_product_count": 2,
			"total_price": 60.0,
			"product_groups": [{
				"promotion": {
					"type": "premium_sale",
					"result": {
						"premium_products": [{
							"name": "商品2", 
							"count": 1
						}, {
							"name": "商品3",
							"count": 2
						}]
					}
				},
				"products": [{
					"name": "商品1",
					"price": 30.0,
					"count": 2
				}]
			}]
		}
		"""


@ui2 @ui-mall @ui-mall.webapp @ui-mall.webapp.shopping_cart
Scenario: 放入1个商品到购物车，商品数量大于买赠的购买基数，并满足循环买赠
	
	When bill访问jobs的webapp
	And bill加入jobs的商品到购物车
		"""
		[{
			"name": "商品1",
			"count": 5
		}]
		"""
	When bill访问jobs的webapp:ui
	Then bill能获得购物车:ui
		"""
		{
			"total_product_count": 5,
			"total_price": 150.0,
			"product_groups": [{
				"promotion": {
					"type": "premium_sale",
					"result": {
						"premium_products": [{
							"name": "商品2", 
							"count": 2
						}, {
							"name": "商品3",
							"count": 4
						}]
					}
				},
				"products": [{
					"name": "商品1",
					"price": 30.0,
					"count": 5
				}]
			}]
		}
		"""