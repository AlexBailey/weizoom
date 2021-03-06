#editor:王丽 2015.10.13

Feature: 管理待售商品
"""
	Jobs能通过管理系统管理商城中的"待售商品列表"
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
						"price": 11.00,
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
						"price": 8.10,
						"stock_type": "有限",
						"stocks": 3
					},
					"白色 M": {
						"user_code": "3",
						"price": 8.20,
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
						"price": 7.10,
						"stock_type": "无限"
					}
				}
			}
		}]	
		"""

@mall2 @product @toSaleProduct   @mall @mall.product_category
Scenario:1 浏览待售商品
	Given jobs登录系统
	Then jobs能获得'待售'商品列表
		"""
		[{
			"name": "水晶虾仁",
			"is_enable_model": "启用规格",
			"categories": [],
			"model": {
				"models": {
					"白色 M": {
						"user_code": "4",
						"price": 7.10,
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
						"price": 8.10,
						"stock_type": "有限",
						"stocks": 3
					},
					"白色 M": {
						"user_code": "3",
						"price": 8.20,
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
						"price": 11.00,
						"stock_type": "无限"
					}
				}
			}
		}]
		"""

@mall2 @product @toSaleProduct @saleingProduct   @mall @mall.product_category
Scenario:2 上架商品
	jobs进行'批量上架'或'单个上架'后
	1. jobs的待售商品列表发生变化
	2. jobs的在售商品列表发生变化

	Given jobs登录系统
	When jobs'上架'商品'东坡肘子'
	Then jobs能获得'待售'商品列表
		"""
		[{
			"name": "水晶虾仁"
		}, {
			"name": "叫花鸡"
		}]
		"""
	Then jobs能获得'在售'商品列表
		"""
		[{
			"name": "东坡肘子"
		}]
		"""
	When jobs批量上架商品
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
		[{
			"name": "水晶虾仁"
		}, {
			"name": "叫花鸡"
		}, {
			"name": "东坡肘子"
		}]
		"""

@mall2 @product @toSaleProduct @saleingProduct   @mall @mall.product_category
Scenario:3 查看商品规格

	Given jobs登录系统
	Then jobs能获得'待售'商品列表
		"""
		[{
			"name": "水晶虾仁"
		}, {
			"name": "叫花鸡"
		}, {
			"name": "东坡肘子"
		}]
		"""
	When jobs查看商品'水晶虾仁'的规格为
		"""
		[{
			"name": "白色 M",
			"user_code": "4",
			"price": 7.10,
			"stocks": "无限"
		}]
		"""
	When jobs查看商品'叫花鸡'的规格为
		"""
		[{
			"name": "黑色 M",
			"user_code": "2",
			"price": 8.10,
			"stocks": 3
		}, {
			"name": "白色 M",
			"user_code": "3",
			"price": 8.20,
			"stocks": 2
		}]
		"""

@mall2 @product @toSaleProduct @saleingProduct   @mall @mall.product_category
Scenario:4 修改商品规格
	
	Given jobs登录系统
	Then jobs能获得'待售'商品列表
		"""
		[{
			"name": "水晶虾仁",
			"is_enable_model": "启用规格",
			"categories": [],
			"model": {
				"models": {
					"白色 M": {
						"user_code": "4",
						"price": 7.10,
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
						"price": 8.10,
						"stock_type": "有限",
						"stocks": 3
					},
					"白色 M": {
						"user_code": "3",
						"price": 8.20,
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
						"price": 11.00,
						"stock_type": "无限"
					}
				}
			}
		}]
		"""
	When jobs更新商品'水晶虾仁'的库存为
		"""
		[{
			"user_code": "4",
			"stock_type": "有限",
			"stocks": 1
		}]
		"""
	When jobs更新商品'东坡肘子'的库存为
		"""
		[{
			"user_code": "1",
			"stock_type": "有限",
			"stocks": 2
		}]
		"""
	When jobs更新商品'叫花鸡'的库存为
		"""
		[{
			"user_code": "2",
			"stock_type": "有限",
			"stocks": 30
		}, {
			"user_code": "3",
			"stock_type": "无限"
		}]
		"""
	Then jobs能获得'待售'商品列表
		"""
		[{
			"name": "水晶虾仁",
			"is_enable_model": "启用规格",
			"categories": [],
			"model": {
				"models": {
					"白色 M": {
						"user_code": "4",
						"price": 7.10,
						"stock_type": "有限",
						"stocks": 1
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
						"price": 8.10,
						"stock_type": "有限",
						"stocks": 30
					},
					"白色 M": {
						"user_code": "3",
						"price": 8.20,
						"stock_type": "无限"
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
						"price": 11.00,
						"stock_type": "有限",
						"stocks": 2
					}
				}
			}
		}]
		"""
	When jobs查看商品'叫花鸡'的规格为
		"""
		[{
			"name": "黑色 M",
			"user_code": "2",
			"price": 8.10,
			"stocks": 30
		}, {
			"name": "白色 M",
			"user_code": "3",
			"price": 8.20,
			"stocks": "无限"
		}]
		"""

@product @toSaleProduct @saleingProduct @yanhaonan @mall2
Scenario:5 修改商品价格
	Given jobs登录系统
	Then jobs能获得'待售'商品列表
		"""
		[{
			"name": "水晶虾仁",
			"is_enable_model": "启用规格",
			"categories": [],
			"model": {
				"models": {
					"白色 M": {
						"user_code": "4",
						"price": 7.10,
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
						"price": 8.10,
						"stock_type": "有限",
						"stocks": 3
					},
					"白色 M": {
						"user_code": "3",
						"price": 8.20,
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
						"price": 11.00,
						"stock_type": "无限"
					}
				}
			}
		}]
		"""
	When jobs修改商品'水晶虾仁'的价格为
		"""
		[{
			"price": 7.00
		}]
		"""
	When jobs修改商品'东坡肘子'的价格为
		"""
		[{
			"price": 14.00
		}]
		"""
	When jobs修改商品'叫花鸡'的价格为
		"""
		[{
			"user_code": "2",
			"price": 8.00,
			"stock_type": "有限",
			"stocks": 3
		}, {
			"user_code": "3",
			"price": 8.00,
			"stock_type": "有限",
			"stocks": 2
		}]
		"""
	Then jobs能获得'待售'商品列表
		"""
		[{
			"name": "水晶虾仁",
			"is_enable_model": "启用规格",
			"categories": [],
			"model": {
				"models": {
					"白色 M": {
						"user_code": "4",
						"price": 7.00,
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
						"price": 8.00,
						"stock_type": "有限",
						"stocks": 3
					},
					"白色 M": {
						"user_code": "3",
						"price": 8.00,
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
						"price": 14.00,
						"stock_type": "无限"
					}
				}
			}
		}]
		"""
	When jobs查看商品'叫花鸡'的规格为
		"""
		[{
			"name": "黑色 M",
			"user_code": "2",
			"price": 8.00,
			"stocks": 3
		}, {
			"name": "白色 M",
			"user_code": "3",
			"price": 8.00,
			"stocks": 2
		}]
		"""
