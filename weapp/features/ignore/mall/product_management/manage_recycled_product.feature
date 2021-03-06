#editor：王丽 2015.10.14

Feature: 管理商品回收站商品
"""

	Jobs能通过管理系统管理商城中的"商品回收站列表"
"""

Background:
	Given jobs登录系统
	And jobs已添加商品分类
		"""
		[{
			"name": "分类1"
		}, {
			"name": "分类2"
		}, {
			"name": "分类3"
		}]	
		"""
	And jobs已添加商品规格
		"""
		[{
			"name": "颜色",
			"type": "图片",
			"values": [{
				"name": "黑色",
				"image": "/standard_static/test_resource_img/hangzhou1.jpg"
			}, {
				"name": "白色",
				"image": "/standard_static/test_resource_img/hangzhou2.jpg"
			}]
		}, {
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
			"name": "东坡肘子",
			"status": "待售",
			"categories": "分类1,分类2,分类3",
			"model": {
				"models": {
					"standard": {
						"user_code": "1",
						"price": 11.0,
						"stock_type": "无限"
					}
				}
			}
		}, {
			"name": "叫花鸡",
			"status": "待售",
			"categories": "分类1",
			"is_enable_model": "启用规格",
			"model": {
				"models": {
					"黑色 M": {
						"user_code": "2",
						"price": 8.1,
						"stock_type": "有限",
						"stocks": 3
					},
					"白色 M": {
						"user_code": "3",
						"price": 8.2,
						"stock_type": "有限",
						"stocks": 2
					}
				}
			}
		}, {
			"name": "水晶虾仁",
			"status": "待售",
			"is_enable_model": "启用规格",
			"model": {
				"models": {
					"白色 M": {
						"user_code": "4",
						"price": 7.1,
						"stock_type": "无限"
					}
				}
			}
		}]	
		"""

@product @productRecycle   @mall @mall.product_category
Scenario:1 浏览回收站商品
	Given jobs登录系统
	When jobs将商品批量放入回收站
		"""
		[
			"东坡肘子", 
			"水晶虾仁", 
			"叫花鸡"
		]
		"""
	Then jobs能获得'回收站'商品列表
		"""
		[{
			"name": "水晶虾仁",
			"is_enable_model": "启用规格",
			"categories": [],
			"model": {
				"models": {
					"白色 M": {
						"user_code": "4",
						"price": 7.1,
						"stock_type": "无限"
					}
				}
			}
		}, {
			"name": "叫花鸡",
			"is_enable_model": "启用规格",
			"categories": ["分类1"],
			"model": {
				"models": {
					"黑色 M": {
						"user_code": "2",
						"price": 8.1,
						"stock_type": "有限",
						"stocks": 3
					},
					"白色 M": {
						"user_code": "3",
						"price": 8.2,
						"stock_type": "有限",
						"stocks": 2
					}
				}
			}
		}, {
			"name": "东坡肘子",
			"is_enable_model": "不启用规格",
			"categories": ["分类1", "分类2", "分类3"],
			"model": {
				"models": {
					"standard": {
						"user_code": "1",
						"price": 11.0,
						"stock_type": "无限"
					}
				}
			}
		}]
		"""

@product @productRecycle   @mall @mall.product_category
Scenario:2 永久删除商品
	jobs进行'批量永久删除'或'单个永久删除'后
	1. jobs的回收站商品列表发生变化
	2. jobs的在售商品列表无变化
	2. jobs的待售商品列表无变化

	Given jobs登录系统
	When jobs将商品批量放入回收站
		"""
		[
			"东坡肘子", 
			"水晶虾仁", 
			"叫花鸡"
		]
		"""
	Then jobs能获得'回收站'商品列表
		"""
		[{
			"name": "水晶虾仁"
		}, {
			"name": "叫花鸡"
		}, {
			"name": "东坡肘子"
		}]
		"""
	When jobs-永久删除商品'东坡肘子'
	Then jobs能获得'待售'商品列表
		"""
		[]
		"""
	Then jobs能获得'在售'商品列表
		"""
		[]
		"""
	Then jobs能获得'回收站'商品列表
		"""
		[{
			"name": "水晶虾仁"
		}, {
			"name": "叫花鸡"
		}]
		"""
	When jobs批量永久删除商品
		"""
		[
			"水晶虾仁", 
			"叫花鸡"
		]
		"""
	Then jobs能获得'待售'商品列表
		"""
		[]
		"""
	Then jobs能获得'在售'商品列表
		"""
		[]
		"""
	Then jobs能获得'回收站'商品列表
		"""
		[]
		"""
