#_author_:王丽
#_edit_:张三香
#editor:王丽 2015.10.13


Feature: 微商城管理-商品管理-在售商品管理 -“查询”
	"""
		（1）库存查询，任何查询条件下查询都会查询出来库存为”无限“的商品
		（2）库存查询，多规格商品只要有一个规格的库存满足查询条件，就可以查询出来此商品
		（3）销量查询，多规格商品按照各规格商品销量的和去匹配查询条件，进行查询
		#_edit_:张三香
		（4）需求变动2015-9-18：（微商城bug4764）
				商品价格、商品库存和商品销量的查询支持只输入最低值或只输入最高值
				商品库存只输入库存最低值时，能把库存为无限的商品查询出来
		(5)数据准备：
			|  name        |  barCode  |   categories     | price         |  stocks  |  sales  |  created_at       |
			|  商品复合规格|           |                  |  10.5 ~ 40.0  |          |    4    |  2015-07-02 10:20 |
			|  商品单规格  |           |                  |  10.0 ~ 20.0  |          |    2    |  2015-07-02 10:20 |
			|  商品5       |  1234562  |                  |   0           |  100000  |    0    |  2015-08-01 05:36 |
			|  商品3       |  1234562  | 分类1,分类2,分类3|   1           |   98     |    1    |  2015-07-02 10:20 |
			|  商品2       |  1234561  | 分类1,分类2      |   10          |    0     |    0    |  2015-04-03 00:00 |
			|  商品1       |           | 分类1            |  0.01         |   无限   |    5    |  2015-04-02 23:59 |
	"""

Background:
	Given jobs登录系统

	And jobs已添加商品分类
		"""
		[{
			"name": "分类1"
		},{
			"name": "分类2"
		},{
			"name": "分类3"
		},{
			"name": "分类4"
		}]
		"""

	When jobs已添加支付方式
		"""
		[{
			"type": "货到付款",
			"is_active": "启用"
		},{
			"type": "微信支付",
			"is_active": "启用"
		},{
			"type": "支付宝",
			"is_active": "启用"
		}]
		"""

	When jobs开通使用微众卡权限
	When jobs添加支付方式
		"""
		[{
			"type": "微众卡支付",
			"description": "我的微众卡支付",
			"is_active": "启用"
		}]
		"""

	When jobs添加邮费配置
		"""
		[{
			"name":"顺丰",
			"first_weight":1,
			"first_weight_price":15.00,
			"added_weight":1,
			"added_weight_price":5.00
		}]
		"""

	Given jobs已添加商品
		| name    | bar_code |   categories      |shelve_type|  price  |   weight  | stock_type  |  stocks  |  postage  |    created_at      |
		| 商品1   |          | 分类1             |   上架    |  0.01   |   1       |      无限   |    0     |   免运费  |  2015-04-02 23:59  |
		| 商品2   | 1234561  | 分类1,分类2       |   上架    |  10.00  |   0       |      有限   |    0     |    顺丰   |  2015-04-03 00:00  |
		| 商品3   | 1234562  | 分类1,分类2,分类3 |   上架    |   1.00  |   0.0001  |      有限   |   100    |   免运费  |  2015-07-02 10:20  |
		| 商品5   | 1234562  |                   |   上架    |  0.00   |   2       |      有限   |  100000  |    顺丰   |  2015-08-01 05:36  |
		| 商品4   | 1234563  | 分类2             |   下架    |  10.00  |   1       |      无限   |    0     |   免运费  |  2015-04-01 11:12  |

	When bill关注jobs的公众号
	And tom关注jobs的公众号

	When 微信用户批量消费jobs的商品
		|order_id| date       | consumer |   product | payment | pay_type |   price*    | paid_amount*   |  alipay*   | wechat*   | cash*    |     action    |  order_status*  |delivery_time|payment_time  |
		|0001    | 2015-04-05 | bill     | 商品1,1   | 支付    | 支付宝   |   0.01      |    0.01        |  0.01      | 0.00      | 0.00     | jobs,完成     |  已完成         | 2015-04-05  |  2015-04-05  |
		|0002    | 2015-04-06 | bill     | 商品1,1   | 支付    | 微信支付 |   0.01      |    0.01        |  0.00      | 0.01      | 0.00     | jobs,发货     |  已发货         | 2015-04-06  |  2015-04-06  |
		|0003    | 2015-04-07 | bill     | 商品1,1   | 支付    | 微信支付 |   0.01      |    0.01        |  0.00      | 0.01      | 0.00     | jobs,退款     |  退款中         | 2015-04-06  |  2015-04-06  |
		|0004    | 2015-04-07 | bill     | 商品1,1   | 支付    | 货到付款 |   0.01      |    0.01        |  0.00      | 0.00      | 0.01     |               |  待发货         |             |  2015-04-07  |
		|0005    | 2015-07-03 | tom      | 商品3,1   | 支付    | 货到付款 |   1.00      |    1.00        |  0.00      | 0.00      | 0.00     | jobs,取消     |  已取消         |             |  2015-07-03  |
		|0006    | 2015-07-04 | tom      | 商品3,1   | 支付    | 支付宝   |   1.00      |    1.00        |  1.00      | 0.00      | 0.00     | jobs,发货     |  已发货         |  2015-07-03 |  2015-07-03  |
		|0007    | 2015-07-01 | -tom2    | 商品1,1   | 支付    | 支付宝   |   0.01      |    0.01        |  0.01      | 0.00      | 0.00     | jobs,发货     |  已发货         |  2015-07-01 |  2015-07-01  |
		|0008    | 2015-07-10 | tom      | 商品3,1   |         | 微信支付 |   1.00      |    1.00        |  0.00      | 1.00      | 0.00     |               |  待支付         |             |              |
		|0009    | 2015-07-02 | tom      | 商品3,1   |         | 微信支付 |   1.00      |    1.00        |  0.00      | 0.00      | 0.00     | jobs,完成退款 |  退款成功       |  2015-07-02 |  2015-07-02  |

@mall2 @product @saleingProduct
Scenario:1 在售商品列表查询

	#空查询、默认查询（空查询）
		When jobs设置商品查询条件
			"""
			{}
			"""
		Then jobs能获得'在售'商品列表
			|  name  |  barCode  |   categories     | price    |  stocks  |  sales  |  created_at       |
			|  商品5 |  1234562  |                  |   0.00   |  100000  |    0    |  2015-08-01 05:36 |
			|  商品3 |  1234562  | 分类1,分类2,分类3|   1.00   |   98     |    1    |  2015-07-02 10:20 |
			|  商品2 |  1234561  | 分类1,分类2      |   10.00  |    0     |    0    |  2015-04-03 00:00 |
			|  商品1 |           | 分类1            |  0.01    |   无限   |    5    |  2015-04-02 23:59 |

	#商品名称

		#完全匹配
			When jobs设置商品查询条件
				"""
				{
					"name":"商品2"
				}
				"""

			Then jobs能获得'在售'商品列表
				|  name  |  barCode  |      categories      |  price     |  stocks  |  sales  |  created_at       |
				|  商品2 |  1234561  |  分类1,分类2         |  10.00     |    0     |    0    |  2015-04-03 00:00 |

		#部分匹配
			When jobs设置商品查询条件
				"""
				{
					"name":"商品"
				}
				"""
			Then jobs能获得'在售'商品列表
				|  name  |  barCode  |      categories      |  price     |  stocks  |  sales  |  created_at       |
				|  商品5 |  1234562  |                      |  0.00      |  100000  |    0    |  2015-08-01 05:36 |
				|  商品3 |  1234562  |  分类1,分类2,分类3   |  1.00      |   98     |    1    |  2015-07-02 10:20 |
				|  商品2 |  1234561  |  分类1,分类2         |  10.00     |    0     |    0    |  2015-04-03 00:00 |
				|  商品1 |           |  分类1               |  0.01      |   无限   |    5    |  2015-04-02 23:59 |

		#查询结果为空

			When jobs设置商品查询条件
				"""
				{
					"name":"商  2"
				}
				"""
			Then jobs能获得'在售'商品列表
				|  name  |  barCode |      categories      |  price  |  stocks  |  sales  |  created_at    |

	#商品条码

		#完全匹配

			When jobs设置商品查询条件
				"""
				{
					"barCode":"1234562"
				}
				"""
			Then jobs能获得'在售'商品列表
				|  name  |  barCode  |      categories      |  price     |  stocks  |  sales  |  created_at       |
				|  商品5 |  1234562  |                      |  0.00      |  100000  |    0    |  2015-08-01 05:36 |
				|  商品3 |  1234562  |  分类1,分类2,分类3   |  1.00      |   98     |    1    |  2015-07-02 10:20 |

		#查询结果为空
			When jobs设置商品查询条件
				"""
				{
					"barCode":"123456"
				}
				"""

			Then jobs能获得'在售'商品列表
				|  name  |  barCode |      categories      |  price  |  stocks  |  sales  |  created_at    |

	#商品价格
		#只填写'最低价格'0，能查询出价格'大于等于0'的所有商品
			When jobs设置商品查询条件
				"""
				{
					"lowPrice":"0.00",
					"highPrice":""
				}
				"""
			Then jobs能获得'在售'商品列表
				|  name  |  barCode  |   categories     | price    |  stocks  |  sales  |  created_at       |
				|  商品5 |  1234562  |                  |   0.00   |  100000  |    0    |  2015-08-01 05:36 |
				|  商品3 |  1234562  | 分类1,分类2,分类3|   1.00   |   98     |    1    |  2015-07-02 10:20 |
				|  商品2 |  1234561  | 分类1,分类2      |   10.00  |    0     |    0    |  2015-04-03 00:00 |
				|  商品1 |           | 分类1            |  0.01    |   无限   |    5    |  2015-04-02 23:59 |

		#只填写'最高价格'1，能查询出价格'小于等于1'的所有商品
			When jobs设置商品查询条件
				"""
				{
					"lowPrice":"",
					"highPrice":"1.00"
				}
				"""
			Then jobs能获得'在售'商品列表
				|  name  |  barCode  |   categories     | price    |  stocks  |  sales  |  created_at       |
				|  商品5 |  1234562  |                  |   0.00   |  100000  |    0    |  2015-08-01 05:36 |
				|  商品3 |  1234562  | 分类1,分类2,分类3|   1.00   |   98     |    1    |  2015-07-02 10:20 |
				|  商品1 |           | 分类1            |  0.01    |   无限   |    5    |  2015-04-02 23:59 |

		#价格区间查询
			When jobs设置商品查询条件
				"""
				{
					"lowPrice":"0.01",
					"highPrice":"10.00"
				}
				"""
			Then jobs能获得'在售'商品列表
				|  name  |  barCode  |   categories     | price    |  stocks  |  sales  |  created_at       |
				|  商品3 |  1234562  | 分类1,分类2,分类3|   1.00   |   98     |    1    |  2015-07-02 10:20 |
				|  商品2 |  1234561  | 分类1,分类2      |   10.00  |    0     |    0    |  2015-04-03 00:00 |
				|  商品1 |           | 分类1            |  0.01    |   无限   |    5    |  2015-04-02 23:59 |

			When jobs设置商品查询条件
				"""
				{
					"lowPrice":"0.00",
					"highPrice":"0.00"
				}
				"""
			Then jobs能获得'在售'商品列表
				|  name  |  barCode | categories |  price     |  stocks  |  sales  | created_at       |
				|  商品5 |  1234562 |            |  0.00      |  100000  |    0    | 2015-08-01 05:36 |

		#查询结果为空
			When jobs设置商品查询条件
				"""
				{
					"lowPrice":"10.01",
					"highPrice":"100.00"
				}
				"""
			Then jobs能获得'在售'商品列表
				|  name  |  barCode |      categories      |  price  |  stocks  |  sales  |  created_at    |

	#商品库存（只输入最低库存时，能查询出库存为无限的商品）
		#只填写最低库存,能查询出库存为无限的商品
			When jobs设置商品查询条件
				"""
				{
					"lowStocks":"98",
					"highStocks":""
				}
				"""
			Then jobs能获得'在售'商品列表
				|  name  |  barCode  |   categories     | price    |  stocks  |  sales  |  created_at       |
				|  商品5 |  1234562  |                  |   0.00   |  100000  |    0    |  2015-08-01 05:36 |
				|  商品3 |  1234562  | 分类1,分类2,分类3|   1.00   |   98     |    1    |  2015-07-02 10:20 |
				|  商品1 |           | 分类1            |  0.01    |   无限   |    5    |  2015-04-02 23:59 |

		#只填写最高库存,不能查询出库存为无限的商品
			When jobs设置商品查询条件
				"""
				{
					"lowStocks":"",
					"highStocks":"100000"
				}
				"""
			Then jobs能获得'在售'商品列表
				|  name  |  barCode  |   categories     | price    |  stocks  |  sales  |  created_at       |
				|  商品5 |  1234562  |                  |   0.00   |  100000  |    0    |  2015-08-01 05:36 |
				|  商品3 |  1234562  | 分类1,分类2,分类3|   1.00   |   98     |    1    |  2015-07-02 10:20 |
				|  商品2 |  1234561  | 分类1,分类2      |   10.00  |    0     |    0    |  2015-04-03 00:00 |

		#库存区间查询
			When jobs设置商品查询条件
				"""
				{
					"lowStocks":"0",
					"highStocks":"98"
				}
				"""
			Then jobs能获得'在售'商品列表
				|  name  |  barCode  |      categories      |  price     |  stocks  |  sales  |  created_at       |
				|  商品3 |  1234562  |  分类1,分类2,分类3   |  1.00      |   98     |    1    |  2015-07-02 10:20 |
				|  商品2 |  1234561  |  分类1,分类2         |  10.00     |    0     |    0    |  2015-04-03 00:00 |

			When jobs设置商品查询条件
				"""
				{
					"lowStocks":"100000",
					"highStocks":"100000"
				}
				"""

			Then jobs能获得'在售'商品列表
				|  name  |  barCode  |      categories      |  price     |  stocks  |  sales  |  created_at           |
				|  商品5 |  1234562  |                      |  0.00      |  100000  |    0    |  2015-08-01 05:36     |

		#查询结果为无区间数据
			When jobs设置商品查询条件
				"""
				{
					"lowStocks":"10",
					"highStocks":"20"
				}
				"""
			Then jobs能获得'在售'商品列表
				|  name  |  barCode |      categories      |  price  |  stocks  |  sales  |  created_at    |

	#商品销量
		#只填写销量最低值
			When jobs设置商品查询条件
				"""
				{
					"lowSales":"0",
					"highSales":""
				}
				"""
			Then jobs能获得'在售'商品列表
				|  name  |  barCode  |   categories     | price    |  stocks  |  sales  |  created_at       |
				|  商品5 |  1234562  |                  |   0.00   |  100000  |    0    |  2015-08-01 05:36 |
				|  商品3 |  1234562  | 分类1,分类2,分类3|   1.00   |   98     |    1    |  2015-07-02 10:20 |
				|  商品2 |  1234561  | 分类1,分类2      |   10.00  |    0     |    0    |  2015-04-03 00:00 |
				|  商品1 |           | 分类1            |  0.01    |   无限   |    5    |  2015-04-02 23:59 |

		#只填写销量最高值
			When jobs设置商品查询条件
				"""
				{
					"lowSales":"",
					"highSales":"1"
				}
				"""
			Then jobs能获得'在售'商品列表
				|  name  |  barCode  |   categories     | price    |  stocks  |  sales  |  created_at       |
				|  商品5 |  1234562  |                  |   0.00   |  100000  |    0    |  2015-08-01 05:36 |
				|  商品3 |  1234562  | 分类1,分类2,分类3|   1.00   |   98     |    1    |  2015-07-02 10:20 |
				|  商品2 |  1234561  | 分类1,分类2      |   10.00  |    0     |    0    |  2015-04-03 00:00 |

		#销量区间查询
			When jobs设置商品查询条件
				"""
				{
					"lowSales":"0",
					"highSales":"4"
				}
				"""
			Then jobs能获得'在售'商品列表
				|  name  |  barCode  |      categories      |  price     |  stocks  |  sales  |  created_at       |
				|  商品5 |  1234562  |                      |  0.00      |  100000  |    0    |  2015-08-01 05:36 |
				|  商品3 |  1234562  |  分类1,分类2,分类3   |  1.00      |   98     |    1    |  2015-07-02 10:20 |
				|  商品2 |  1234561  |  分类1,分类2         |  10.00     |    0     |    0    |  2015-04-03 00:00 |

			When jobs设置商品查询条件
				"""
				{
					"lowSales":"1",
					"highSales":"1"
				}
				"""
			Then jobs能获得'在售'商品列表
				|  name  |  barCode  |      categories      |  price  |  stocks  |  sales  |  created_at       |
				|  商品3 |  1234562  |  分类1,分类2,分类3   |  1.00   |   98     |    1    |  2015-07-02 10:20 |

		#查询结果为空
			When jobs设置商品查询条件
				"""
				{
					"lowSales":"6",
					"highSales":"10"
				}
				"""
			Then jobs能获得'在售'商品列表
				|  name  |  barCode |      categories      |  price  |  stocks  |  sales  |  created_at    |

	#店内分组

		#查询单个分组商品
			When jobs设置商品查询条件
				"""
				{
					"category":"分类1"
				}
				"""
			Then jobs能获得'在售'商品列表
				|  name  |  barCode  |      categories     |  price     |  stocks  |  sales  |  created_at      |
				|  商品3 |  1234562  |  分类1,分类2,分类3  |  1.00      |   98     |    1    |  2015-07-02 10:20 |
				|  商品2 |  1234561  |  分类1,分类2        |  10.00     |    0     |    0    |  2015-04-03 00:00 |
				|  商品1 |           |  分类1              |  0.01      |   无限   |    5    |  2015-04-02 23:59 |

			When jobs设置商品查询条件
				"""
				{
					"category":"分类3"
				}
				"""
			Then jobs能获得'在售'商品列表
				|  name  |  barCode  |      categories      |  price  |  stocks  |  sales  |  created_at       |
				|  商品3 |  1234562  |  分类1,分类2,分类3   |  1.00   |   98     |    1    |  2015-07-02 10:20 |

		#查询结果为空
			When jobs设置商品查询条件
				"""
				{
					"category":"分类4"
				}
				"""
			Then jobs能获得'在售'商品列表
				|  name  |  barCode |      categories      |  price  |  stocks  |  sales  |  created_at    |

	#创建时间
		#查询商品创建时间
			When jobs设置商品查询条件
				"""
				{
					"startDate":"2015-04-01 00:00",
					"endDate":"2015-04-03 00:00"
				}
				"""
			Then jobs能获得'在售'商品列表
				|  name  |  barCode  |      categories      |  price     |  stocks  |  sales  |  created_at       |
				|  商品2 |  1234561  |  分类1,分类2         |  10.00     |    0     |    0    |  2015-04-03 00:00 |
				|  商品1 |           |  分类1               |  0.01      |   无限   |    5    |  2015-04-02 23:59 |

		#查询结果为空
			When jobs设置商品查询条件
				"""
				{
					"startDate":"2015-7-10 00:00",
					"endDate":"2015-07-20 00:00"
				}
				"""
			Then jobs能获得'在售'商品列表
				|  name  |  barCode |      categories      |  price  |  stocks  |  sales  |  created_at    |

	#条件混合查询
		When jobs设置商品查询条件
			"""
			{
				"name":"商品",
				"barCode":"1234562",
				"lowPrice":"0.00",
				"highPrice":"1.00",
				"lowStocks":"2",
				"highStocks":"100000",
				"lowSales":"0",
				"highSales":"1",
				"category":"分类3",
				"startDate":"2015-07-02 10:20",
				"endDate":"2015-07-20 10:20"
			}
			"""

		Then jobs能获得'在售'商品列表
			|  name  |  barCode  |      categories      |  price  |  stocks  |  sales  |  created_at       |
			|  商品3 |  1234562  |  分类1,分类2,分类3   |  1.00   |   98     |    1    |  2015-07-02 10:20 |

@mall2 @product @saleingProduct
Scenario:2 在售多规格商品列表查询

	Given jobs已添加商品规格
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
			"name": "商品单规格",
			"is_enable_model": "启用规格",
			"created_at": "2015-07-02 10:20",
			"model": {
				"models": {
					"黑色": {
						"price": 10.00,
						"weight": 3,
						"stock_type": "有限",
						"stocks": 3
					},
					"白色": {
						"price": 20.00,
						"weight": 4,
						"stock_type": "无限"
					}
				}
			}
		}]
		"""

	And jobs已添加商品
		"""
		[{
			"name": "商品复合规格",
			"is_enable_model": "启用规格",
			"created_at": "2015-07-02 10:20",
			"model": {
				"models": {
					"黑色 S": {
						"price": 10.50,
						"weight": 1,
						"stock_type": "有限",
						"stocks": 100
					},
					"白色 S": {
						"price": 20.00,
						"weight": 2,
						"stock_type": "有限",
						"stocks": 200
					},
					"黑色 M": {
						"price": 30.00,
						"weight": 3,
						"stock_type": "有限",
						"stocks": 300
					},
					"白色 M": {
						"price": 40.00,
						"weight": 4,
						"stock_type": "有限",
						"stocks": 400
					}
				}
			}
		}]
		"""
	When bill访问jobs的webapp
	And bill购买jobs的商品
		"""
		{
			"products": [{
				"name": "商品单规格",
				"count": 2,
				"model": "黑色"
			}]
		}
		"""
	And bill使用支付方式'货到付款'进行支付
	When bill购买jobs的商品
		"""
		{
			"products": [{
				"name": "商品复合规格",
				"count": 1,
				"model": "白色 S"
			},
			{
				"name": "商品复合规格",
				"count": 3,
				"model": "黑色 M"
			}]
		}
		"""
	And bill使用支付方式'货到付款'进行支付


	#商品价格
		#填写价格最低值和最高值，有一个规格的价格在查询区间
			Given jobs登录系统
			When jobs设置商品查询条件
				"""
				{
					"lowPrice":"10.00",
					"highPrice":"10.00"
				}
				"""
			Then jobs能获得'在售'商品列表
				|    name    |  barCode  |      categories      |   price         |  stocks  |  sales  |  created_at       |
				|  商品单规格|           |                      |  10.00 ~ 20.00  |          |    2    |  2015-07-02 10:20 |
				|  商品2     |  1234561  |  分类1,分类2         |  10.00          |    0     |    0    |  2015-04-03 00:00 |

		#填写价格最低值个最高值，没有任何一个价格在查询区间
			When jobs设置商品查询条件
				"""
				{
					"lowPrice":"60.00",
					"highPrice":"70.00"
				}
				"""
			Then jobs能获得'在售'商品列表
				|    name    |  barCode |      categories      |   price    |  stocks  |  sales  |  created_at    |

		#只填写价格最低值
			When jobs设置商品查询条件
				"""
				{
					"lowPrice":"10.00",
					"highPrice":""
				}
				"""
			Then jobs能获得'在售'商品列表
				|    name      |  barCode  |      categories      |   price         |  stocks  |  sales  |  created_at       |
				|  商品复合规格|           |                      |  10.50 ~ 40.00  |          |    4    |  2015-07-02 10:20 |
				|  商品单规格  |           |                      |  10.00 ~ 20.00  |          |    2    |  2015-07-02 10:20 |
				|  商品2       |  1234561  |  分类1,分类2         |  10.00          |    0     |    0    |  2015-04-03 00:00 |

		#只填写价格最高值
			When jobs设置商品查询条件
				"""
				{
					"lowPrice":"",
					"highPrice":"10.00"
				}
				"""
			Then jobs能获得'在售'商品列表
				|  name        |  barCode  |   categories     | price            |  stocks  |  sales  |  created_at       |
				|  商品单规格  |           |                  |  10.00 ~ 20.00   |          |    2    |  2015-07-02 10:20 |
				|  商品5       |  1234562  |                  |   0.00           |  100000  |    0    |  2015-08-01 05:36 |
				|  商品3       |  1234562  | 分类1,分类2,分类3|   1.00           |   98     |    1    |  2015-07-02 10:20 |
				|  商品2       |  1234561  | 分类1,分类2      |   10.00          |    0     |    0    |  2015-04-03 00:00 |
				|  商品1       |           | 分类1            |  0.01            |   无限   |    5    |  2015-04-02 23:59 |

	#商品库存（只填写库存最低值时，才能查询出库存为无限的商品）

		#只填写库存最低值,存在一个规格的库存为'无限'的商品能查询出来
			When jobs设置商品查询条件
				"""
				{
					"lowStocks":"1",
					"highStocks":""
				}
				"""
			Then jobs能获得'在售'商品列表
				|  name        |  barCode  |   categories     | price            |  stocks  |  sales  |  created_at       |
				|  商品复合规格|           |                  |  10.50 ~ 40.00   |          |    4    |  2015-07-02 10:20 |
				|  商品单规格  |           |                  |  10.00 ~ 20.00   |          |    2    |  2015-07-02 10:20 |
				|  商品5       |  1234562  |                  |   0.00           |  100000  |    0    |  2015-08-01 05:36 |
				|  商品3       |  1234562  | 分类1,分类2,分类3|   1.00           |   98     |    1    |  2015-07-02 10:20 |
				|  商品1       |           | 分类1            |  0.01            |   无限   |    5    |  2015-04-02 23:59 |

		#只填写库存最高值,存在一个规格的库存为'无限'的商品不能查询出来
			When jobs设置商品查询条件
				"""
				{
					"lowStocks":"",
					"highStocks":"1"
				}
				"""
			Then jobs能获得'在售'商品列表
				|     name     |  barCode  |      categories      |   price           |  stocks  |  sales  |  created_at        |
				|  商品单规格  |           |                      |  10.00 ~ 20.00    |          |    2    |  2015-07-02 10:20 |
				|  商品2       |  1234561  | 分类1,分类2          |   10.00           |    0     |    0    |  2015-04-03 00:00  |

		#查询结果为无区间数据
			When jobs设置商品查询条件
				"""
				{
					"lowStocks":"700",
					"highStocks":"1000"
				}
				"""
			Then jobs能获得'在售'商品列表
				|     name     |  barCode |      categories      |   price    |  stocks  |  sales  |  created_at    |

	#商品销量（多规格商品是每个规格的销量之和计算）
		#只填写销量最低值
			When jobs设置商品查询条件
				"""
				{
					"highStocks":"",
					"lowSales":"4"
				}
				"""
			Then jobs能获得'在售'商品列表
				|    name      |  barCode  |      categories      |   price         |  stocks  |  sales  |  created_at       |
				|  商品复合规格|           |                      |  10.50 ~ 40.00  |          |    4    |  2015-07-02 10:20 |
				|  商品1       |           |  分类1               |  0.01           |   无限   |    5    |  2015-04-02 23:59 |

		#只填写销量最高值
			When jobs设置商品查询条件
				"""
				{
					"lowSales":"",
					"highSales":"3"
				}
				"""
			Then jobs能获得'在售'商品列表
				|  name        |  barCode  |   categories     | price               |  stocks  |  sales  |  created_at       |
				|  商品单规格  |           |                  |  10.00 ~ 20.00      |          |    2    |  2015-07-02 10:20 |
				|  商品5       |  1234562  |                  |   0.00              |  100000  |    0    |  2015-08-01 05:36 |
				|  商品3       |  1234562  | 分类1,分类2,分类3|   1.00              |   98     |    1    |  2015-07-02 10:20 |
				|  商品2       |  1234561  | 分类1,分类2      |   10.00             |    0     |    0    |  2015-04-03 00:00 |

		#填写销量最低值和销量最高值,进行查询
			#最低值和最高值不相等
			When jobs设置商品查询条件
				"""
				{
					"lowSales":"2",
					"highSales":"3"
				}
				"""
			Then jobs能获得'在售'商品列表
				|     name     |  barCode  |      categories      |   price            |  stocks  |  sales  |  created_at       |
				|  商品单规格  |           |                      |  10.00 ~ 20.00     |          |    2    |  2015-07-02 10:20 |
			#最低值和最高值相等
			When jobs设置商品查询条件
				"""
				{
					"lowSales":"4",
					"highSales":"4"
				}
				"""
			Then jobs能获得'在售'商品列表
				|     name     |  barCode  |      categories      |   price          |  stocks  |  sales  |  created_at       |
				|  商品复合规格|           |                      |  10.50 ~ 40.00   |          |    4    |  2015-07-02 10:20 |

@mall2 @product @saleingProduct
Scenario:3. 针对线上BUG3669按商品名称查询时，查询结果的商品库存是正确的
		When jobs设置商品查询条件
			"""
			{
				"name":"商品2"
			}
			"""
		Then jobs能获得'在售'商品列表
			|  name  |  barCode  |      categories    |  price     |  stocks  |  sales  |  created_at       |
			|  商品2 |  1234561  |  分类1,分类2       |  10.00     |    0     |    0    |  2015-04-03 00:00 |
