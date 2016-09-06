#_author_:张三香 2016.08.31

Feature:查看自营平台财务审核订单列表
	"""
		1、母订单中如果包含'退款中'、不含'退款成功'状态的子订单，则该母订单显示在财务审核订单列表的【全部】和【退款中】页签里
		2、母订单中如果包含'退款成功'、不包含'退款中'状态的子订单，则该母订单显示在财务审核订单列表的【全部】和【退款成功】页签里
		3、母订单中如果包含'退款中'和'退款成功'状态的子订单，则该母订单显示在财务审核订单列表的【全部】、【退款中】和【退款成功】页签里
		4、以下组合的母订单会显示在财务审核订单列表中对应的页签里：
			|母订单状态 | 子订单1   | 子订单2   | 子订单3 |财务审核列表中显示                                 
			| 待发货    | 待发货    |待发货     |退款中   |全部、退款中
			| 待发货    | 待发货    |待发货     |退款成功 |全部、退款成功
			| 待发货    | 待发货    |已发货     |退款中   |全部、退款中
			| 待发货    | 待发货    |已发货     |退款成功 |全部、退款成功
			| 待发货    | 待发货    |退款中     |退款中   |全部、退款中
			| 待发货    | 待发货    |退款中     |已完成   |全部、退款中
			| 待发货    | 待发货    |退款中     |退款成功 |全部、退款中、退款成功
			| 待发货    | 待发货    |已完成     |退款成功 |全部、退款成功
			| 待发货    | 待发货    |退款成功   |退款成功 |全部、退款成功

			| 已发货    | 已发货    | 已发货    |退款中   |全部、退款中
			| 已发货    | 已发货    | 已发货    |退款成功 |全部、退款成功
			| 已发货    | 已发货    | 退款中    |退款中   |全部、退款中
			| 已发货    | 已发货    | 退款中    |已完成   |全部、退款中
			| 已发货    | 已发货    | 退款中    |退款成功 |全部、退款中、退款成功
			| 已发货    | 已发货    | 已完成    |退款成功 |全部、退款成功
			| 已发货    | 已发货    | 退款成功  |退款成功 |全部、退款成功
			| 退款中    | 退款中    | 退款中    |退款中   |全部、退款中
			| 退款中    | 退款中    | 退款中    |已完成   |全部、退款中
			| 退款中    | 退款中    | 退款中    |退款成功 |全部、退款中、退款成功

			| 退款中    | 退款中    | 已完成    |已完成   |全部、退款中
			| 退款中    | 退款中    | 已完成    |退款成功 |全部、退款中、退款成功
			| 退款中    | 退款中    | 退款成功  |退款成功 |全部、退款中、退款成功

			| 退款成功  | 退款成功  | 退款成功  |退款成功 |全部、退款成功 
		5、退款中和退款完成状态下，鼠标悬停时展示退款金额详情
		6、母订单中如果包含待发货、已发货、已完成、退款完成状态的子订单，则其对应的操作列为空
		7、母订单中退款中状态的子订单，其操作列有【退款成功】按钮
		8、财务审核订单列表查询时，按照子订单进行筛选结果
	"""

Backgroud:
	Given 重置'weizoom_card'的bdd环境
	Given 重置'apiserver'的bdd环境
	Given jobs登录系统
	And jobs设定会员积分策略
		"""
		{
			"integral_each_yuan":2
		}
		"""
	And 设置jobs为自营平台账号
	And jobs已有微众卡支付权限
	And jobs已添加支付方式
		"""
		[{
			"type":"货到付款"
		},{
			"type":"微信支付"
		},{
			"type":"支付宝"
		},{
			"type":"微众卡支付"
		}]
		"""
	#创建微众卡
		Given test登录管理系统::weizoom_card
		When test新建通用卡::weizoom_card
			"""
			[{
				"name":"100元微众卡",
				"prefix_value":"100",
				"type":"virtual",
				"money":"100.00",
				"num":"2",
				"comments":"微众卡"
			}]
			"""
		#微众卡审批出库
		When test下订单::weizoom_card
			"""
			[{
				"card_info":[{
					"name":"100元微众卡",
					"order_num":"2",
					"start_date":"2016-04-07 00:00",
					"end_date":"2019-10-07 00:00"
				}],
				"order_info":{
					"order_id":"0001"
					}
			}]
			"""
		#激活微众
		When test激活卡号'100000001'的卡::weizoom_card

	#创建商品
		Given 给jobs, nokia两个自营平台同步商品，供货商是-商家1
				"""
				{
					"name": "商品1a",
					"promotion_title": "商品1a促销",
					"purchase_price": 9.00,
					"price": 10.00,
					"weight": 1,
					"image": "love.png",
					"stocks": 100,
					"detail": "商品1a描述信息"
				}
				"""
		Given 给jobs, nokia两个自营平台同步商品，供货商是-商家1
				"""
				{
					"name": "商品1b",
					"promotion_title": "商品1b促销",
					"purchase_price": 19.00,
					"price": 20.00,
					"weight": 1,
					"image": "love.png",
					"stocks": 200,
					"detail": "商品1b描述信息"
				}
				"""
		Given 给jobs, nokia两个自营平台同步商品，供货商是-商家2
				"""
				{
					"name": "商品2a",
					"promotion_title": "商品2a促销",
					"purchase_price": 9.00,
					"price": 10.00,
					"weight": 1,
					"image": "love.png",
					"stocks": 100,
					"detail": "商品2a描述信息"
				}
				"""
		Given 给jobs, nokia两个自营平台同步商品，供货商是-商家3
				"""
				{
					"name": "商品3a",
					"promotion_title": "商品3a促销",
					"purchase_price": 9.00,
					"price": 10.00,
					"weight": 1,
					"image": "love.png",
					"stocks": 100,
					"detail": "商品3a描述信息"
				}
				"""
		Given jobs登录系统
		When jobs上架商品池商品"商品1a"
		When jobs上架商品池商品"商品2a"
		When jobs上架商品池商品"商品3a"

	When bill关注jobs的公众号
	When bill访问jobs的webapp::apiserver
	#bill购买多个供货商的商品
		When bill购买jobs的商品::apiserver
			"""
			{
				"order_id": "101",
				"products": [{
					"name": "商品1a",
					"count": 1
				},{
					"name": "商品2a",
					"count": 1
				},{
					"name": "商品3a",
					"count": 1
				}],
				"pay_type":"微信支付",
				"ship_area": "北京市 北京市 海淀区",
				"ship_address": "海淀科技大厦"
			}
			"""
		And bill使用支付方式'微信支付'进行支付::apiserver
	#bill购买单个供货商的商品
		When bill访问jobs的webapp::apiserver
		When bill绑定微众卡
			"""
			{
				"binding_date":"2016-06-16",
				"binding_shop":"jobs",
				"weizoom_card_info":
					{
						"id":"100000001",
						"password":"1234567"
					}
			}
			"""
		When bill购买jobs的商品::apiserver
			"""
			{
				"order_id": "102",
				"products": [{
					"name": "商品1a",
					"count": 1
				}],
				"pay_type":"微信支付",
				"ship_area": "北京市 北京市 海淀区",
				"ship_address": "海淀科技大厦"
			}
			"""
		And bill使用支付方式'微信支付'进行支付::apiserver
		When bill购买jobs的商品::apiserver
			"""
			{
				"order_id": "103",
				"products": [{
					"name": "商品1a",
					"count": 1
				},{
					"name": "商品1b",
					"count": 1
				}],
				"weizoom_card":[{
					"card_name":"100000001",
					"card_pass":"1234567"
					}],
				"pay_type":"支付宝",
				"ship_area": "北京市 北京市 海淀区",
				"ship_address": "海淀科技大厦"
			}
			"""

Scenario:1 查看自营平台财务审核订单列表（多子订单的母订单中包含退款中、不包含退款成功的子订单）
	#101待发货（现金/退现金）（待发货/待发货/退款中）
		Given jobs登录系统
		When jobs'申请退款'自营订单'101-商家3'
			"""
			{
				"cash":10.00,
				"weizoom_card":0.00,
				"coupon_money":0.00,
				"intergal":0,
				"intergal_money":0.00
			}
			"""
		Given jobs登录系统
		Then jobs获得自营财务审核'全部'订单列表
			"""
			[{
				"order_no":"101",
				"buyer":"bill",
				"status": "待发货",
				"final_price":30.00,
				"save_money":"",
				"methods_of_payment": "微信支付",
				"group":[{
					"商家1"：{
						"order_no":"101-商家1",
						"status":"待发货",
						"actions":[],
						"products":
							[{
								"name":"商品1a",
								"price":10.00,
								"count":1
							}]
						},
					"商家2"：{
						"order_no":"101-商家2",
						"status":"待发货",
						"actions":[],
						"products":
							[{
								"name":"商品2a",
								"price":10.00,
								"count":1
							}]
						},
					"商家3"：{
						"order_no":"101-商家3",
						"status":"退款中",
						"refund_details":
							{
								"cash":10.00
							},
						"actions":["退款成功"],
						"products":
							[{
								"name":"商品3a",
								"price":10.00,
								"count":1
							}]
						}
					}]
			}]
			"""
		And jobs获得自营财务审核'退款中'订单列表
			"""
			[{
				"order_no":"101",
				"buyer":"bill",
				"status": "待发货",
				"final_price":30.00,
				"save_money":"",
				"methods_of_payment": "微信支付",
				"group":[{
					"商家1"：{
						"order_no":"101-商家1",
						"status":"待发货",
						"actions":[],
						"products":
							[{
								"name":"商品1a",
								"price":10.00,
								"count":1
							}]
						},
					"商家2"：{
						"order_no":"101-商家2",
						"status":"待发货",
						"actions":[],
						"products":
							[{
								"name":"商品2a",
								"price":10.00,
								"count":1
							}]
						},
					"商家3"：{
						"order_no":"101-商家3",
						"status":"退款中",
						"refund_details":
							{
								"cash":10.00
							},
						"actions":["退款成功"],
						"products":
							[{
								"name":"商品3a",
								"price":10.00,
								"count":1
							}]
						}
					}]
			}]
			"""
		And jobs获得自营财务审核'退款成功'订单列表
			"""
			[]
			"""

	#101待发货（现金/退现金）（退款中/退款中/退款中）
		When jobs'申请退款'自营订单'101-商家2'
			"""
			{
				"cash":10.00,
				"weizoom_card":0.00,
				"coupon_money":0.00,
				"intergal":0,
				"intergal_money":0.00
			}
			"""
		When jobs'申请退款'自营订单'101-商家1'
				"""
				{
					"cash":10.00,
					"weizoom_card":0.00,
					"coupon_money":0.00,
					"intergal":0,
					"intergal_money":0.00
				}
				"""
		Then jobs获得自营财务审核'全部'订单列表
			"""
			[{
				"order_no":"101",
				"buyer":"bill",
				"status": "退款中",
				"final_price":30.00,
				"save_money":"",
				"methods_of_payment": "微信支付",
				"group":[{
					"商家1"：{
						"order_no":"101-商家1",
						"status":"退款中",
						"refund_details":
							{
								"cash":10.00
							},
						"actions":["退款成功"],
						"products":
							[{
								"name":"商品1a",
								"price":10.00,
								"count":1
							}]
						},
					"商家2"：{
						"order_no":"101-商家2",
						"status":"退款中",
						"refund_details":
							{
								"cash":10.00
							},
						"actions":["退款成功"],
						"products":
							[{
								"name":"商品2a",
								"price":10.00,
								"count":1
							}]
						},
					"商家3"：{
						"order_no":"101-商家3",
						"status":"退款中",
						"refund_details":
							{
								"cash":10.00
							},
						"actions":["退款成功"],
						"products":
							[{
								"name":"商品3a",
								"price":10.00,
								"count":1
							}]
						}
					}]
			}]
			"""
		And jobs获得自营财务审核'退款中'订单列表
			"""
			[{
				"order_no":"101",
				"buyer":"bill",
				"status": "退款中",
				"final_price":30.00,
				"save_money":"",
				"methods_of_payment": "微信支付",
				"group":[{
					"商家1"：{
						"order_no":"101-商家1",
						"status":"退款中",
						"refund_details":
							{
								"cash":10.00
							},
						"actions":["退款成功"],
						"products":
							[{
								"name":"商品1a",
								"price":10.00,
								"count":1
							}]
						},
					"商家2"：{
						"order_no":"101-商家2",
						"status":"退款中",
						"refund_details":
							{
								"cash":10.00
							},
						"actions":["退款成功"],
						"products":
							[{
								"name":"商品2a",
								"price":10.00,
								"count":1
							}]
						},
					"商家3"：{
						"order_no":"101-商家3",
						"status":"退款中",
						"refund_details":
							{
								"cash":10.00
							},
						"actions":["退款成功"],
						"products":
							[{
								"name":"商品3a",
								"price":10.00,
								"count":1
							}]
						}
					}]
			}]
			"""
		And jobs获得自营财务审核'退款成功'订单列表
			"""
			[]
			"""

Scenario:2 查看自营平台财务审核订单列表（多子订单的母订单中包含退款成功、不包含退款中子订单）
	#101待发货（现金/退现金+优惠券）（待发货/待发货/退款成功）
		Given jobs登录系统
		When jobs'申请退款'自营订单'101-商家3'
			"""
			{
				"cash":5.00,
				"weizoom_card":0.00,
				"coupon_money":5.00,
				"intergal":0,
				"intergal_money":0.00
			}
			"""
		When jobs通过财务审核'退款成功'自营订单'101-商家3'
		Then jobs获得自营财务审核'全部'订单列表
			"""
			[{
				"order_no":"101",
				"buyer":"bill",
				"status": "待发货",
				"final_price":25.00,
				"save_money":"",
				"methods_of_payment": "微信支付",
				"group":[{
					"商家1"：{
						"order_no":"101-商家1",
						"status":"待发货",
						"actions":[],
						"products":
							[{
								"name":"商品1a",
								"price":10.00,
								"count":1
							}]
						},
					"商家2"：{
						"order_no":"101-商家2",
						"status":"待发货",
						"actions":[],
						"products":
							[{
								"name":"商品2a",
								"price":10.00,
								"count":1
							}]
						},
					"商家3"：{
						"order_no":"101-商家3",
						"status":"退款成功",
						"refund_details":
							{
								"cash":5.00,
								"coupon_money":5.00
							},
						"actions":[],
						"products":
							[{
								"name":"商品3a",
								"price":10.00,
								"count":1
							}]
						}
					}]
			}]
			"""
		And jobs获得自营财务审核'退款中'订单列表
			"""
			[]
			"""
		And jobs获得自营财务审核'退款成功'订单列表
			"""
			[{
				"order_no":"101",
				"buyer":"bill",
				"status": "待发货",
				"final_price":25.00,
				"save_money":"",
				"methods_of_payment": "微信支付",
				"group":[{
					"商家1"：{
						"order_no":"101-商家1",
						"status":"待发货",
						"actions":[],
						"products":
							[{
								"name":"商品1a",
								"price":10.00,
								"count":1
							}]
						},
					"商家2"：{
						"order_no":"101-商家2",
						"status":"待发货",
						"actions":[],
						"products":
							[{
								"name":"商品2a",
								"price":10.00,
								"count":1
							}]
						},
					"商家3"：{
						"order_no":"101-商家3",
						"status":"退款成功",
						"refund_details":
							{
								"cash":5.00,
								"coupon_money":5.00
							},
						"actions":[],
						"products":
							[{
								"name":"商品3a",
								"price":10.00,
								"count":1
							}]
						}
					}]
			}]
			"""

	#101待发货（现金/退现金;退现金;退现金+优惠券）（退款成功/退款成功/退款成功）
		When jobs对自营订单进行发货
				"""
				{
					"order_no": "101-商家2",
					"logistics": "申通快递",
					"number": "101002",
					"shipper": "jobs"
				}
				"""
		When jobs'申请退款'自营订单'101-商家2'
			"""
			{
				"cash":10.00,
				"weizoom_card":0.00,
				"coupon_money":0.00,
				"intergal":0,
				"intergal_money":0.00
			}
			"""
		When jobs'申请退款'自营订单'101-商家1'
			"""
			{
				"cash":10.00,
				"weizoom_card":0.00,
				"coupon_money":0.00,
				"intergal":0,
				"intergal_money":0.00
			}
			"""
		When jobs通过财务审核'退款成功'自营订单'101-商家2'
		When jobs通过财务审核'退款成功'自营订单'101-商家1'
		Then jobs获得自营财务审核'全部'订单列表
			"""
			[{
				"order_no":"101",
				"buyer":"bill",
				"status": "退款成功",
				"final_price":5.00,
				"save_money":"",
				"methods_of_payment": "微信支付",
				"group":[{
					"商家1"：{
						"order_no":"101-商家1",
						"status":"退款成功",
						"refund_details":
							{
								"cash":10.00
							},
						"actions":[],
						"products":
							[{
								"name":"商品1a",
								"price":10.00,
								"count":1
							}]
						},
					"商家2"：{
						"order_no":"101-商家2",
						"status":"退款成功",
						"refund_details":
							{
								"cash":10.00
							},
						"actions":[],
						"products":
							[{
								"name":"商品2a",
								"price":10.00,
								"count":1
							}]
						},
					"商家3"：{
						"order_no":"101-商家3",
						"status":"退款成功",
						"refund_details":
							{
								"cash":5.00,
								"coupon_money":5.00
							},
						"actions":[],
						"products":
							[{
								"name":"商品3a",
								"price":10.00,
								"count":1
							}]
						}
					}]
			}]
			"""
		And jobs获得自营财务审核'退款中'订单列表
			"""
			[]
			"""
		And jobs获得自营财务审核'退款成功'订单列表
			"""
			[{
				"order_no":"101",
				"buyer":"bill",
				"status": "退款成功",
				"final_price":5.00,
				"save_money":"",
				"methods_of_payment": "微信支付",
				"group":[{
					"商家1"：{
						"order_no":"101-商家1",
						"status":"退款成功",
						"refund_details":
							{
								"cash":10.00
							},
						"actions":[],
						"products":
							[{
								"name":"商品1a",
								"price":10.00,
								"count":1
							}]
						},
					"商家2"：{
						"order_no":"101-商家2",
						"status":"退款成功",
						"refund_details":
							{
								"cash":10.00
							},
						"actions":[],
						"products":
							[{
								"name":"商品2a",
								"price":10.00,
								"count":1
							}]
						},
					"商家3"：{
						"order_no":"101-商家3",
						"status":"退款成功",
						"refund_details":
							{
								"cash":5.00,
								"coupon_money":5.00
							},
						"actions":[],
						"products":
							[{
								"name":"商品3a",
								"price":10.00,
								"count":1
							}]
						}
					}]
			}]
			"""

Scenario:3 查看自营平台财务审核订单列表（多子订单的母订单中包含退款中和退款成功子订单）
	#101待发货（现金/退现金;退现金+积分）（待发货/退款中/退款成功）
		Given jobs登录系统
		When jobs'申请退款'自营订单'101-商家2'
			"""
			{
				"cash":10.00,
				"weizoom_card":0.00,
				"coupon_money":0.00,
				"intergal":0,
				"intergal_money":0.00
			}
			"""
		When jobs'申请退款'自营订单'101-商家3'
			"""
			{
				"cash":5.00,
				"weizoom_card":0.00,
				"coupon_money":0.00,
				"intergal":10,
				"intergal_money":5.00
			}
			"""
		When jobs通过财务审核'退款成功'自营订单'101-商家3'
		Then jobs获得自营财务审核'全部'订单列表
			"""
			[{
				"order_no":"101",
				"buyer":"bill",
				"status": "待发货",
				"final_price":25.00,
				"save_money":"",
				"methods_of_payment": "微信支付",
				"group":[{
					"商家1"：{
						"order_no":"101-商家1",
						"status":"待发货",
						"actions":[],
						"products":
							[{
								"name":"商品1a",
								"price":10.00,
								"count":1
							}]
						},
					"商家2"：{
						"order_no":"101-商家2",
						"status":"退款中",
						"refund_details":
							{
								"cash":10.00
							},
						"actions":["退款成功"],
						"products":
							[{
								"name":"商品2a",
								"price":10.00,
								"count":1
							}]
						},
					"商家3"：{
						"order_no":"101-商家3",
						"status":"退款成功",
						"refund_details":
							{
								"cash":5.00,
								"integral_money":5.00
							},
						"actions":[],
						"products":
							[{
								"name":"商品3a",
								"price":10.00,
								"count":1
							}]
						}
					}]
			}]
			"""
		And jobs获得自营财务审核'退款中'订单列表
			"""
			[{
				"order_no":"101",
				"buyer":"bill",
				"status": "待发货",
				"final_price":25.00,
				"save_money":"",
				"methods_of_payment": "微信支付",
				"group":[{
					"商家1"：{
						"order_no":"101-商家1",
						"status":"待发货",
						"actions":[],
						"products":
							[{
								"name":"商品1a",
								"price":10.00,
								"count":1
							}]
						},
					"商家2"：{
						"order_no":"101-商家2",
						"status":"退款中",
						"refund_details":
							{
								"cash":10.00
							},
						"actions":["退款成功"],
						"products":
							[{
								"name":"商品2a",
								"price":10.00,
								"count":1
							}]
						},
					"商家3"：{
						"order_no":"101-商家3",
						"status":"退款成功",
						"refund_details":
							{
								"cash":5.00,
								"integral_money":5.00
							},
						"actions":[],
						"products":
							[{
								"name":"商品3a",
								"price":10.00,
								"count":1
							}]
						}
					}]
			}]
			"""
		And jobs获得自营财务审核'退款成功'订单列表
			"""
			[{
				"order_no":"101",
				"buyer":"bill",
				"status": "待发货",
				"final_price":25.00,
				"save_money":"",
				"methods_of_payment": "微信支付",
				"group":[{
					"商家1"：{
						"order_no":"101-商家1",
						"status":"待发货",
						"actions":[],
						"products":
							[{
								"name":"商品1a",
								"price":10.00,
								"count":1
							}]
						},
					"商家2"：{
						"order_no":"101-商家2",
						"status":"退款中",
						"refund_details":
							{
								"cash":10.00
							},
						"actions":["退款成功"],
						"products":
							[{
								"name":"商品2a",
								"price":10.00,
								"count":1
							}]
						},
					"商家3"：{
						"order_no":"101-商家3",
						"status":"退款成功",
						"refund_details":
							{
								"cash":5.00,
								"integral_money":5.00
							},
						"actions":[],
						"products":
							[{
								"name":"商品3a",
								"price":10.00,
								"count":1
							}]
						}
					}]
			}]
			"""
	#101已发货（现金/退现金;退现金+积分）（已发货/退款中/退款成功）
		When jobs对自营订单进行发货
			"""
			{
				"order_no": "101-商家1",
				"logistics": "申通快递",
				"number": "101001",
				"shipper": "jobs"
			}
			"""
		Then jobs获得自营财务审核'全部'订单列表
			"""
			[{
				"order_no":"101",
				"buyer":"bill",
				"status": "已发货",
				"final_price":25.00,
				"save_money":"",
				"methods_of_payment": "微信支付",
				"group":[{
					"商家1"：{
						"order_no":"101-商家1",
						"status":"已发货",
						"actions":[],
						"products":
							[{
								"name":"商品1a",
								"price":10.00,
								"count":1
							}]
						},
					"商家2"：{
						"order_no":"101-商家2",
						"status":"退款中",
						"refund_details":
							{
								"cash":10.00
							},
						"actions":["退款成功"],
						"products":
							[{
								"name":"商品2a",
								"price":10.00,
								"count":1
							}]
						},
					"商家3"：{
						"order_no":"101-商家3",
						"status":"退款成功",
						"refund_details":
							{
								"cash":5.00,
								"integral_money":5.00
							},
						"actions":[],
						"products":
							[{
								"name":"商品3a",
								"price":10.00,
								"count":1
							}]
						}
					}]
			}]
			"""
		And jobs获得自营财务审核'退款中'订单列表
			"""
			[{
				"order_no":"101",
				"buyer":"bill",
				"status": "已发货",
				"final_price":25.00,
				"save_money":"",
				"methods_of_payment": "微信支付",
				"group":[{
					"商家1"：{
						"order_no":"101-商家1",
						"status":"已发货",
						"actions":[],
						"products":
							[{
								"name":"商品1a",
								"price":10.00,
								"count":1
							}]
						},
					"商家2"：{
						"order_no":"101-商家2",
						"status":"退款中",
						"refund_details":
							{
								"cash":10.00
							},
						"actions":["退款成功"],
						"products":
							[{
								"name":"商品2a",
								"price":10.00,
								"count":1
							}]
						},
					"商家3"：{
						"order_no":"101-商家3",
						"status":"退款成功",
						"refund_details":
							{
								"cash":5.00,
								"integral_money":5.00
							},
						"actions":[],
						"products":
							[{
								"name":"商品3a",
								"price":10.00,
								"count":1
							}]
						}
					}]
			}]
			"""
		And jobs获得自营财务审核'退款成功'订单列表
			"""
			[{
				"order_no":"101",
				"buyer":"bill",
				"status": "已发货",
				"final_price":25.00,
				"save_money":"",
				"methods_of_payment": "微信支付",
				"group":[{
					"商家1"：{
						"order_no":"101-商家1",
						"status":"已发货",
						"actions":[],
						"products":
							[{
								"name":"商品1a",
								"price":10.00,
								"count":1
							}]
						},
					"商家2"：{
						"order_no":"101-商家2",
						"status":"退款中",
						"refund_details":
							{
								"cash":10.00
							},
						"actions":["退款成功"],
						"products":
							[{
								"name":"商品2a",
								"price":10.00,
								"count":1
							}]
						},
					"商家3"：{
						"order_no":"101-商家3",
						"status":"退款成功",
						"refund_details":
							{
								"cash":5.00,
								"integral_money":5.00
							},
						"actions":[],
						"products":
							[{
								"name":"商品3a",
								"price":10.00,
								"count":1
							}]
						}
					}]
			}]
			"""
	#101退款中（现金/退现金;退现金+积分）（已完成/退款中/退款成功）
		When jobs'完成'自营订单'101-商家1'
		Then jobs获得自营财务审核'全部'订单列表
			"""
			[{
				"order_no":"101",
				"buyer":"bill",
				"status": "退款中",
				"final_price":25.00,
				"save_money":"",
				"methods_of_payment": "微信支付",
				"group":[{
					"商家1"：{
						"order_no":"101-商家1",
						"status":"已完成",
						"actions":[],
						"products":
							[{
								"name":"商品1a",
								"price":10.00,
								"count":1
							}]
						},
					"商家2"：{
						"order_no":"101-商家2",
						"status":"退款中",
						"refund_details":
							{
								"cash":10.00
							},
						"actions":["退款成功"],
						"products":
							[{
								"name":"商品2a",
								"price":10.00,
								"count":1
							}]
						},
					"商家3"：{
						"order_no":"101-商家3",
						"status":"退款成功",
						"refund_details":
							{
								"cash":5.00,
								"integral_money":5.00
							},
						"actions":[],
						"products":
							[{
								"name":"商品3a",
								"price":10.00,
								"count":1
							}]
						}
					}]
			}]
			"""
		And jobs获得自营财务审核'退款中'订单列表
			"""
			[{
				"order_no":"101",
				"buyer":"bill",
				"status": "退款中",
				"final_price":25.00,
				"save_money":"",
				"methods_of_payment": "微信支付",
				"group":[{
					"商家1"：{
						"order_no":"101-商家1",
						"status":"已完成",
						"actions":[],
						"products":
							[{
								"name":"商品1a",
								"price":10.00,
								"count":1
							}]
						},
					"商家2"：{
						"order_no":"101-商家2",
						"status":"退款中",
						"refund_details":
							{
								"cash":10.00
							},
						"actions":["退款成功"],
						"products":
							[{
								"name":"商品2a",
								"price":10.00,
								"count":1
							}]
						},
					"商家3"：{
						"order_no":"101-商家3",
						"status":"退款成功",
						"refund_details":
							{
								"cash":5.00,
								"integral_money":5.00
							},
						"actions":[],
						"products":
							[{
								"name":"商品3a",
								"price":10.00,
								"count":1
							}]
						}
					}]
			}]
			"""
		And jobs获得自营财务审核'退款成功'订单列表
			"""
			[{
				"order_no":"101",
				"buyer":"bill",
				"status": "退款中",
				"final_price":25.00,
				"save_money":"",
				"methods_of_payment": "微信支付",
				"group":[{
					"商家1"：{
						"order_no":"101-商家1",
						"status":"已完成",
						"actions":[],
						"products":
							[{
								"name":"商品1a",
								"price":10.00,
								"count":1
							}]
						},
					"商家2"：{
						"order_no":"101-商家2",
						"status":"退款中",
						"refund_details":
							{
								"cash":10.00
							},
						"actions":["退款成功"],
						"products":
							[{
								"name":"商品2a",
								"price":10.00,
								"count":1
							}]
						},
					"商家3"：{
						"order_no":"101-商家3",
						"status":"退款成功",
						"refund_details":
							{
								"cash":5.00,
								"integral_money":5.00
							},
						"actions":[],
						"products":
							[{
								"name":"商品3a",
								"price":10.00,
								"count":1
							}]
						}
					}]
			}]
			"""
	#101退款中（现金/退现金;退现金;退现金+积分）（退款中/退款中/退款成功）
		When jobs'申请退款'自营订单'101-商家1'
			"""
			{
				"cash":10.00,
				"weizoom_card":0.00,
				"coupon_money":0.00,
				"intergal":0,
				"intergal_money":0.00
			}
			"""
		Then jobs获得自营财务审核'全部'订单列表
			"""
			[{
				"order_no":"101",
				"buyer":"bill",
				"status": "退款中",
				"final_price":25.00,
				"save_money":"",
				"methods_of_payment": "微信支付",
				"group":[{
					"商家1"：{
						"order_no":"101-商家1",
						"status":"退款中",
						"refund_details":{
							"cash":10.00
						},
						"actions":["退款成功"],
						"products":
							[{
								"name":"商品1a",
								"price":10.00,
								"count":1
							}]
						},
					"商家2"：{
						"order_no":"101-商家2",
						"status":"退款中",
						"refund_details":
							{
								"cash":10.00
							},
						"actions":["退款成功"],
						"products":
							[{
								"name":"商品2a",
								"price":10.00,
								"count":1
							}]
						},
					"商家3"：{
						"order_no":"101-商家3",
						"status":"退款成功",
						"refund_details":
							{
								"cash":5.00,
								"integral_money":5.00
							},
						"actions":[],
						"products":
							[{
								"name":"商品3a",
								"price":10.00,
								"count":1
							}]
						}
					}]
			}]
			"""
		And jobs获得自营财务审核'退款中'订单列表
			"""
			[{
				"order_no":"101",
				"buyer":"bill",
				"status": "退款中",
				"final_price":25.00,
				"save_money":"",
				"methods_of_payment": "微信支付",
				"group":[{
					"商家1"：{
						"order_no":"101-商家1",
						"status":"退款中",
						"refund_details":{
							"cash":10.00
						},
						"actions":["退款成功"],
						"products":
							[{
								"name":"商品1a",
								"price":10.00,
								"count":1
							}]
						},
					"商家2"：{
						"order_no":"101-商家2",
						"status":"退款中",
						"refund_details":
							{
								"cash":10.00
							},
						"actions":["退款成功"],
						"products":
							[{
								"name":"商品2a",
								"price":10.00,
								"count":1
							}]
						},
					"商家3"：{
						"order_no":"101-商家3",
						"status":"退款成功",
						"refund_details":
							{
								"cash":5.00,
								"integral_money":5.00
							},
						"actions":[],
						"products":
							[{
								"name":"商品3a",
								"price":10.00,
								"count":1
							}]
						}
					}]
			}]
			"""
		And jobs获得自营财务审核'退款成功'订单列表
			"""
			[{
				"order_no":"101",
				"buyer":"bill",
				"status": "退款中",
				"final_price":25.00,
				"save_money":"",
				"methods_of_payment": "微信支付",
				"group":[{
					"商家1"：{
						"order_no":"101-商家1",
						"status":"退款中",
						"refund_details":{
							"cash":10.00
						},
						"actions":["退款成功"],
						"products":
							[{
								"name":"商品1a",
								"price":10.00,
								"count":1
							}]
						},
					"商家2"：{
						"order_no":"101-商家2",
						"status":"退款中",
						"refund_details":
							{
								"cash":10.00
							},
						"actions":["退款成功"],
						"products":
							[{
								"name":"商品2a",
								"price":10.00,
								"count":1
							}]
						},
					"商家3"：{
						"order_no":"101-商家3",
						"status":"退款成功",
						"refund_details":
							{
								"cash":5.00,
								"integral_money":5.00
							},
						"actions":[],
						"products":
							[{
								"name":"商品3a",
								"price":10.00,
								"count":1
							}]
						}
					}]
			}]
			"""
	#101退款中（现金/退现金;退现金;退现金+积分）（退款成功/退款中/退款成功）
		When jobs通过财务审核'退款成功'自营订单'101-商家1'
		Then jobs获得自营财务审核'全部'订单列表
			"""
			[{
				"order_no":"101",
				"buyer":"bill",
				"status": "退款中",
				"final_price":15.00,
				"save_money":"",
				"methods_of_payment": "微信支付",
				"group":[{
					"商家1"：{
						"order_no":"101-商家1",
						"status":"退款成功",
						"refund_details":{
							"cash":10.00
						},
						"actions":[],
						"products":
							[{
								"name":"商品1a",
								"price":10.00,
								"count":1
							}]
						},
					"商家2"：{
						"order_no":"101-商家2",
						"status":"退款中",
						"refund_details":
							{
								"cash":10.00
							},
						"actions":["退款成功"],
						"products":
							[{
								"name":"商品2a",
								"price":10.00,
								"count":1
							}]
						},
					"商家3"：{
						"order_no":"101-商家3",
						"status":"退款成功",
						"refund_details":
							{
								"cash":5.00,
								"integral_money":5.00
							},
						"actions":[],
						"products":
							[{
								"name":"商品3a",
								"price":10.00,
								"count":1
							}]
						}
					}]
			}]
			"""
		And jobs获得自营财务审核'退款中'订单列表
			"""
			[{
				"order_no":"101",
				"buyer":"bill",
				"status": "退款中",
				"final_price":15.00,
				"save_money":"",
				"methods_of_payment": "微信支付",
				"group":[{
					"商家1"：{
						"order_no":"101-商家1",
						"status":"退款成功",
						"refund_details":{
							"cash":10.00
						},
						"actions":[],
						"products":
							[{
								"name":"商品1a",
								"price":10.00,
								"count":1
							}]
						},
					"商家2"：{
						"order_no":"101-商家2",
						"status":"退款中",
						"refund_details":
							{
								"cash":10.00
							},
						"actions":["退款成功"],
						"products":
							[{
								"name":"商品2a",
								"price":10.00,
								"count":1
							}]
						},
					"商家3"：{
						"order_no":"101-商家3",
						"status":"退款成功",
						"refund_details":
							{
								"cash":5.00,
								"integral_money":5.00
							},
						"actions":[],
						"products":
							[{
								"name":"商品3a",
								"price":10.00,
								"count":1
							}]
						}
					}]
			}]
			"""
		And jobs获得自营财务审核'退款成功'订单列表
			"""
			[{
				"order_no":"101",
				"buyer":"bill",
				"status": "退款中",
				"final_price":15.00,
				"save_money":"",
				"methods_of_payment": "微信支付",
				"group":[{
					"商家1"：{
						"order_no":"101-商家1",
						"status":"退款成功",
						"refund_details":{
							"cash":10.00
						},
						"actions":[],
						"products":
							[{
								"name":"商品1a",
								"price":10.00,
								"count":1
							}]
						},
					"商家2"：{
						"order_no":"101-商家2",
						"status":"退款中",
						"refund_details":
							{
								"cash":10.00
							},
						"actions":["退款成功"],
						"products":
							[{
								"name":"商品2a",
								"price":10.00,
								"count":1
							}]
						},
					"商家3"：{
						"order_no":"101-商家3",
						"status":"退款成功",
						"refund_details":
							{
								"cash":5.00,
								"integral_money":5.00
							},
						"actions":[],
						"products":
							[{
								"name":"商品3a",
								"price":10.00,
								"count":1
							}]
						}
					}]
			}]
			"""

Scenario:4 查看自营平台财务审核订单列表（单个子订单的母订单）
	Given jobs登录系统
	#102-单个子订单-货到付款-退优惠券+积分
		When jobs'申请退款'自营订单'102-商家1'
				"""
				{
					"cash":0.00,
					"weizoom_card":0.00,
					"coupon_money":5.00,
					"intergal":10,
					"intergal_money":5.00
				}
				"""
		Then jobs获得自营财务审核'全部'订单列表
				"""
				[{
					"order_no":"102",
					"buyer":"bill",
					"status": "退款中",
					"final_price":10.00,
					"save_money":"",
					"methods_of_payment": "微信支付",
					"group":[{
						"商家1"：{
							"order_no":"102-商家1",
							"status":"退款中",
							"refund_details":
								{
									"coupon_money":5.00,
									"integral_money":5.00
								},
							"actions":["退款成功"],
							"products":
								[{
									"name":"商品1a",
									"price":10.00,
									"count":1
								}]
							}
						}]
				}]
				"""
		And jobs获得自营财务审核'退款中'订单列表
				"""
				[{
					"order_no":"102",
					"buyer":"bill",
					"status": "退款中",
					"final_price":10.00,
					"save_money":"",
					"methods_of_payment": "微信支付",
					"group":[{
						"商家1"：{
							"order_no":"102-商家1",
							"status":"退款中",
							"refund_details":
								{
									"coupon_money":5.00,
									"integral_money":5.00
								},
							"actions":["退款成功"],
							"products":
								[{
									"name":"商品1a",
									"price":10.00,
									"count":1
								}]
							}
						}]
				}]
				"""
		And jobs获得自营财务审核'退款成功'订单列表
			"""
			[]
			"""
		When jobs通过财务审核'退款成功'自营订单'102-商家1'
		Then jobs获得自营财务审核'全部'订单列表
			"""
			[{
				"order_no":"102",
				"buyer":"bill",
				"status": "退款成功",
				"final_price":10.00,
				"save_money":"",
				"methods_of_payment": "微信支付",
				"group":[{
					"商家1"：{
						"order_no":"102-商家1",
						"status":"退款成功",
						"refund_details":
							{
								"coupon_money":5.00,
								"integral_money":5.00
							},
						"actions":[],
						"products":
							[{
								"name":"商品1a",
								"price":10.00,
								"count":1
							}]
						}
					}]
			}]
			"""
		And jobs获得自营财务审核'退款中'订单列表
			"""
			[]
			"""
		And jobs获得自营财务审核'退款成功'订单列表
			"""
			[{
				"order_no":"102",
				"buyer":"bill",
				"status": "退款成功",
				"final_price":10.00,
				"save_money":"",
				"methods_of_payment": "微信支付",
				"group":[{
					"商家1"：{
						"order_no":"102-商家1",
						"status":"退款成功",
						"refund_details":
							{
								"coupon_money":5.00,
								"integral_money":5.00
							},
						"actions":[],
						"products":
							[{
								"name":"商品1a",
								"price":10.00,
								"count":1
							}]
						}
					}]
			}]
			"""
	#103-单个子订单（有运费）-优惠抵扣（微众卡）-退微众卡+优惠券+积分
		When jobs'申请退款'自营订单'103-商家1'
				"""
				{
					"cash":0.00,
					"weizoom_card":21.00,
					"coupon_money":5.00,
					"intergal":10,
					"intergal_money":5.00
				}
				"""
		When jobs通过财务审核'退款成功'自营订单'103-商家1'
		Then jobs获得自营财务审核'全部'订单列表
				"""
				[{
					"order_no":"103",
					"buyer":"bill",
					"status": "退款成功",
					"final_price":10.00,
					"save_money":"",
					"methods_of_payment": "优惠抵扣",
					"group":[{
						"商家1"：{
							"order_no":"103-商家1",
							"status":"退款成功",
							"refund_details":
								{
									"weizoom_card":21.00,
									"coupon_money":5.00,
									"integral_money":5.00
								},
							"actions":[],
							"products":
								[{
									"name":"商品1a",
									"price":10.00,
									"count":1
								},{
									"name":"商品1b",
									"price":20.00,
									"count":1
								}]
							}
						}]
				},{
					"order_no":"102",
					"buyer":"bill",
					"status": "退款成功",
					"final_price":10.00,
					"save_money":"",
					"methods_of_payment": "货到付款",
					"group":[{
						"商家1"：{
							"order_no":"102-商家1",
							"status":"退款成功",
							"refund_details":
								{
									"coupon_money":5.00,
									"integral_money":5.00
								},
							"actions":[],
							"products":
								[{
									"name":"商品1a",
									"price":10.00,
									"count":1
								}]
							}
						}]
				}]
				"""
		And jobs获得自营财务审核'退款中'订单列表
			"""
			[]
			"""
		And jobs获得自营财务审核'退款成功'订单列表
				"""
				[{
					"order_no":"103",
					"buyer":"bill",
					"status": "退款成功",
					"final_price":10.00,
					"save_money":"",
					"methods_of_payment": "优惠抵扣",
					"group":[{
						"商家1"：{
							"order_no":"103-商家1",
							"status":"退款成功",
							"refund_details":
								{
									"weizoom_card":21.00,
									"coupon_money":5.00,
									"integral_money":5.00
								},
							"actions":[],
							"products":
								[{
									"name":"商品1a",
									"price":10.00,
									"count":1
								},{
									"name":"商品1b",
									"price":20.00,
									"count":1
								}]
							}
						}]
				},{
					"order_no":"102",
					"buyer":"bill",
					"status": "退款成功",
					"final_price":10.00,
					"save_money":"",
					"methods_of_payment": "货到付款",
					"group":[{
						"商家1"：{
							"order_no":"102-商家1",
							"status":"退款成功",
							"refund_details":
								{
									"coupon_money":5.00,
									"integral_money":5.00
								},
							"actions":[],
							"products":
								[{
									"name":"商品1a",
									"price":10.00,
									"count":1
								}]
							}
						}]
				}]
				"""


