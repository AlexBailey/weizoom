# __author__ : "王新蕊"
# __author__ : "王丽"
Feature: 群发优惠券
"""
	筛选出会员发送优惠券
	#除已跑路外
"""

Background:
	Given jobs登录系统

	And jobs已添加商品
		"""
		[{
			"name": "商品1",
			"price": 200.00
		},{
			"name": "商品2",
			"price": 200.00
		},{
			"name": "商品3",
			"price": 200.00
		},{
			"name": "商品4",
			"price": 200.00
		},{
			"name": "商品5",
			"price": 200.00
		}]
		"""

	#添加"进行中"单品优惠券
		Given jobs已添加了优惠券规则
			"""
			[{
				"name": "单品券1",
				"money": 10.00,
				"limit_counts": "无限",
				"count": 10,
				"start_date": "今天",
				"end_date": "1天后",
				"coupon_id_prefix": "coupon1_id_",
				"coupon_product": "商品1"
			}]
			"""
		Then jobs能获得优惠券'单品券1'的码库
			"""
			{
				"coupon1_id_1": {
					"money": 10.00,
					"status": "未领取",
					"consumer": "",
					"target": ""
				},
				"coupon1_id_2": {
					"money": 10.00,
					"status": "未领取",
					"consumer": "",
					"target": ""
				},
				"coupon1_id_3": {
					"money": 10.00,
					"status": "未领取",
					"consumer": "",
					"target": ""
				},
				"coupon1_id_4": {
					"money": 10.00,
					"status": "未领取",
					"consumer": "",
					"target": ""
				},
				"coupon1_id_5": {
					"money": 10.00,
					"status": "未领取",
					"consumer": "",
					"target": ""
				},
				"coupon1_id_6": {
					"money": 10.00,
					"status": "未领取",
					"consumer": "",
					"target": ""
				},
				"coupon1_id_7": {
					"money": 10.00,
					"status": "未领取",
					"consumer": "",
					"target": ""
				},
				"coupon1_id_8": {
					"money": 10.00,
					"status": "未领取",
					"consumer": "",
					"target": ""
				},
				"coupon1_id_9": {
					"money": 10.00,
					"status": "未领取",
					"consumer": "",
					"target": ""
				},
				"coupon1_id_10": {
					"money": 10.00,
					"status": "未领取",
					"consumer": "",
					"target": ""
				}
			}
			"""

	#添加"已过期"的单品优惠券
		Given jobs已添加了优惠券规则
			"""
			[{
				"name": "单品券2",
				"money": 10.00,
				"limit_counts": "无限",
				"count": 5,
				"start_date": "2天前",
				"end_date": "1天前",
				"coupon_id_prefix": "coupon2_id_",
				"coupon_product": "商品2"
			}]
			"""
		Then jobs能获得优惠券'单品券2'的码库
			"""
			{
				"coupon2_id_1": {
					"money": 10.00,
					"status": "已过期",
					"consumer": "",
					"target": ""
				},
				"coupon2_id_2": {
					"money": 10.00,
					"status": "已过期",
					"consumer": "",
					"target": ""
				},
				"coupon2_id_3": {
					"money": 10.00,
					"status": "已过期",
					"consumer": "",
					"target": ""
				},
				"coupon2_id_4": {
					"money": 10.00,
					"status": "已过期",
					"consumer": "",
					"target": ""
				},
				"coupon2_id_5": {
					"money": 10.00,
					"status": "已过期",
					"consumer": "",
					"target": ""
				}
			}
			"""

	#添加"进行中"数量不足单品优惠券
		Given jobs已添加了优惠券规则
			"""
			[{
				"name": "单品券3",
				"money": 10.00,
				"limit_counts": 1,
				"count": 3,
				"start_date": "今天",
				"end_date": "1天后",
				"coupon_id_prefix": "coupon3_id_",
				"coupon_product": "商品3"
			}]
			"""
		Then jobs能获得优惠券'单品券3'的码库
			"""
			{
				"coupon3_id_1": {
					"money": 10.00,
					"status": "未领取",
					"consumer": "",
					"target": ""
				},
				"coupon3_id_2": {
					"money": 10.00,
					"status": "未领取",
					"consumer": "",
					"target": ""
				},
				"coupon3_id_3": {
					"money": 10.00,
					"status": "未领取",
					"consumer": "",
					"target": ""
				}
			}
			"""

	#添加"未开始"单品优惠券
		Given jobs已添加了优惠券规则
			"""
			[{
				"name": "单品券4",
				"money": 10.00,
				"limit_counts": "无限",
				"count": 2,
				"start_date": "1天后",
				"end_date": "2天后",
				"coupon_id_prefix": "coupon4_id_",
				"coupon_product": "商品4"
			}]
			"""
		Then jobs能获得优惠券'单品券4'的码库
			"""
			{
				"coupon4_id_1": {
					"money": 10.00,
					"status": "未领取",
					"consumer": "",
					"target": ""
				},
				"coupon4_id_2": {
					"money": 10.00,
					"status": "未领取",
					"consumer": "",
					"target": ""
				}
			}
			"""

	#添加"已失效"单品优惠券
		Given jobs已添加了优惠券规则
			"""
			[{
				"name": "单品券5",
				"money": 10.00,
				"limit_counts": "无限",
				"count": 2,
				"start_date": "1天前",
				"end_date": "2天后",
				"coupon_id_prefix": "coupon5_id_",
				"coupon_product": "商品5"
			}]
			"""
		When jobs失效优惠券'单品券5'
		Then jobs能获得优惠券'单品券5'的码库
			"""
			{
				"coupon5_id_1": {
					"money": 10.00,
					"status": "已失效",
					"consumer": "",
					"target": ""
				},
				"coupon5_id_2": {
					"money": 10.00,
					"status": "已失效",
					"consumer": "",
					"target": ""
				}
			}
			"""

	#构造系统会员
		Given nokia关注jobs的公众号
		And tom关注jobs的公众号
		And tom2关注jobs的公众号
		And tom3关注jobs的公众号
		And tom5关注jobs的公众号

		And tom5取消关注jobs的公众号

@memberList @promotionCoupon
Scenario:1 选择优惠券的列表
	Given jobs登录系统

	#优惠券库存满足人数发放，已过期、已失效的优惠不能进入选择优惠券列表，
	#只有"进行中"和"未开始"的优惠券可以选择
		When jobs设置会员查询条件
			"""
			[{
				"name":"tom",
				"status":"全部"
			}]
			"""


		When jobs选择会员
			| member_name | member_rank |
			|     tom     |   普通会员  |
			|     tom5    |   普通会员  |

		When jobs批量发优惠券
			"""
			[{
				"modification_method":"给选中的人发优惠券(已取消关注的除外)"
			}]
			"""
		Then jobs获得发送提示您将为'tom'发放优惠券
		Then jobs获得选择优惠券列表
			"""
			[{
				"name":"单品券4",
				"type":"单品券",
				"money":10.00,
				"start_date": "1天后",
				"end_date": "2天后",
				"limit_counts":"不限",
				"is_select":"true"
			},{
				"name":"单品券3",
				"type":"单品券",
				"money":10.00,
				"start_date": "今天",
				"end_date": "1天后",
				"limit_counts": 1,
				"is_select":"true"
			},{
				"name":"单品券1",
				"type":"单品券",
				"money":10.00,
				"start_date": "今天",
				"end_date": "1天后",
				"limit_counts":"不限",
				"is_select":"true"
			}]
			"""

	#"进行中"和"未开始"的优惠券进入选择优惠券列表，库存不足的不能选择
		When jobs设置会员查询条件
			"""
			[{
				"name":"",
				"status":"全部"
			}]
			"""

		When jobs批量发优惠券
			"""
			[{
				"modification_method":"给筛选出来的所有人发优惠券(已取消关注的除外)"
			}]
			"""
		Then jobs获得发送提示您将为'4'人发放优惠券
		Then jobs获得选择优惠券列表
			"""
			[{
				"name":"单品券4",
				"type":"单品券",
				"money":10.00,
				"start_date": "1天后",
				"end_date": "2天后",
				"limit_counts":"不限",
				"is_select":"false"
			},{
				"name":"单品券3",
				"type":"单品券",
				"money":10.00,
				"start_date": "今天",
				"end_date": "1天后",
				"limit_counts": 1,
				"is_select":"false"
			},{
				"name":"单品券1",
				"type":"单品券",
				"money":10.00,
				"start_date": "今天",
				"end_date": "1天后",
				"limit_counts":"不限",
				"is_select":"true"
			}]
			"""

	#筛选结果只有一人，选择给所有的人发优惠券，也是提示接收的者的名字
		When jobs设置会员查询条件
			"""
			[{
				"name":"tom3",
				"status":"全部"
			}]
			"""

		When jobs批量发优惠券
			"""
			[{
				"modification_method":"给筛选出来的所有人发优惠券(已取消关注的除外)"
			}]
			"""
		#Then jobs获得发送提示您将为'tom3'发放优惠券
		Then jobs获得选择优惠券列表
			"""
			[{
				"name":"单品券4",
				"type":"单品券",
				"money":10.00,
				"start_date": "1天后",
				"end_date": "2天后",
				"limit_counts":"不限",
				"is_select":"true"
			},{
				"name":"单品券3",
				"type":"单品券",
				"money":10.00,
				"start_date": "今天",
				"end_date": "1天后",
				"limit_counts": 1,
				"is_select":"true"
			},{
				"name":"单品券1",
				"type":"单品券",
				"money":10.00,
				"start_date": "今天",
				"end_date": "1天后",
				"limit_counts":"不限",
				"is_select":"true"
			}]
			"""

@memberList @promotionCoupon
Scenario:2 给筛选出选中的部分会员发送优惠券

	Given jobs登录系统

	#给筛选出来的选中的部分会员发放优惠券
		When jobs设置会员查询条件
			"""
			[{
				"name":"tom",
				"status":"全部"
			}]
			"""
		When jobs选择会员
			| member_name | member_rank |
			|     tom     |   普通会员  |
			|     tom5    |   普通会员  |

		When jobs批量发优惠券
			"""
			[{
				"modification_method":"给选中的人发优惠券(已取消关注的除外)",
				"coupon_name":"单品券1",
				"count":2
			}]
			"""
		#Then jobs优惠券发放成功

	#校验会员领取优惠券
		When tom访问jobs的webapp
		Then tom能获得webapp优惠券列表
			"""
			[{
				"coupon_id": "coupon1_id_1",
				"money": 10.00,
				"status": "未使用"
			},{
				"coupon_id": "coupon1_id_2",
				"money": 10.00,
				"status": "未使用"
			}]
			"""

		When tom2访问jobs的webapp
		Then tom2能获得webapp优惠券列表
			"""
			[ ]
			"""

		When tom3访问jobs的webapp
		Then tom3能获得webapp优惠券列表
			"""
			[ ]
			"""

		When tom5访问jobs的webapp
		Then tom5能获得webapp优惠券列表
			"""
			[ ]
			"""

		When nokia访问jobs的webapp
		Then nokia能获得webapp优惠券列表
			"""
			[ ]
			"""
	#校验jobs后台发放优惠券的情况
		Given jobs登录系统
		Then jobs能获得优惠券'单品券1'的码库
			"""
			{
				"coupon1_id_1": {
					"money": 10.00,
					"status": "未使用",
					"consumer": "",
					"target": "tom"
				},
				"coupon1_id_2": {
					"money": 10.00,
					"status": "未使用",
					"consumer": "",
					"target": "tom"
				},
				"coupon1_id_3": {
					"money": 10.00,
					"status": "未领取",
					"consumer": "",
					"target": ""
				},
				"coupon1_id_4": {
					"money": 10.00,
					"status": "未领取",
					"consumer": "",
					"target": ""
				},
				"coupon1_id_5": {
					"money": 10.00,
					"status": "未领取",
					"consumer": "",
					"target": ""
				},
				"coupon1_id_6": {
					"money": 10.00,
					"status": "未领取",
					"consumer": "",
					"target": ""
				},
				"coupon1_id_7": {
					"money": 10.00,
					"status": "未领取",
					"consumer": "",
					"target": ""
				},
				"coupon1_id_8": {
					"money": 10.00,
					"status": "未领取",
					"consumer": "",
					"target": ""
				},
				"coupon1_id_9": {
					"money": 10.00,
					"status": "未领取",
					"consumer": "",
					"target": ""
				},
				"coupon1_id_10": {
					"money": 10.00,
					"status": "未领取",
					"consumer": "",
					"target": ""
				}
			}
			"""

@memberList	@promotionCoupon
Scenario:3 给筛选出会员发送优惠券

	Given jobs登录系统

	#给筛选出来的会员发放优惠券
		When jobs设置会员查询条件
			"""
			[{
				"name":"tom",
				"status":"全部"
			}]
			"""
		When jobs选择会员
			| member_name | member_rank |

		When jobs批量发优惠券
			"""
			[{
				"modification_method":"给筛选出来的所有人发优惠券(已取消关注的除外)",
				"coupon_name":"单品券1",
				"count":2
			}]
			"""
		#Then jobs优惠券发放成功

	#校验会员领取优惠券
		When tom访问jobs的webapp
		Then tom能获得webapp优惠券列表
			"""
			[{
				"coupon_id": "coupon1_id_1",
				"money": 10.00,
				"status": "未使用"
			},{
				"coupon_id": "coupon1_id_2",
				"money": 10.00,
				"status": "未使用"
			}]
			"""

		When tom2访问jobs的webapp
		Then tom2能获得webapp优惠券列表
			"""
			[{
				"coupon_id": "coupon1_id_3",
				"money": 10.00,
				"status": "未使用"
			},{
				"coupon_id": "coupon1_id_4",
				"money": 10.00,
				"status": "未使用"
			}]
			"""

		When tom3访问jobs的webapp
		Then tom3能获得webapp优惠券列表
			"""
			[{
				"coupon_id": "coupon1_id_5",
				"money": 10.00,
				"status": "未使用"
			},{
				"coupon_id": "coupon1_id_6",
				"money": 10.00,
				"status": "未使用"
			}]
			"""

		When tom5访问jobs的webapp
		Then tom5能获得webapp优惠券列表
			"""
			[ ]
			"""

		When nokia访问jobs的webapp
		Then nokia能获得webapp优惠券列表
			"""
			[ ]
			"""
	#校验jobs后台发放优惠券的情况
		Given jobs登录系统
		Then jobs能获得优惠券'单品券1'的码库
			"""
			{
				"coupon1_id_1": {
					"money": 10.00,
					"status": "未使用",
					"consumer": "",
					"target": "tom"
				},
				"coupon1_id_2": {
					"money": 10.00,
					"status": "未使用",
					"consumer": "",
					"target": "tom"
				},
				"coupon1_id_3": {
					"money": 10.00,
					"status": "未使用",
					"consumer": "",
					"target": "tom2"
				},
				"coupon1_id_4": {
					"money": 10.00,
					"status": "未使用",
					"consumer": "",
					"target": "tom2"
				},
				"coupon1_id_5": {
					"money": 10.00,
					"status": "未使用",
					"consumer": "",
					"target": "tom3"
				},
				"coupon1_id_6": {
					"money": 10.00,
					"status": "未使用",
					"consumer": "",
					"target": "tom3"
				},
				"coupon1_id_7": {
					"money": 10.00,
					"status": "未领取",
					"consumer": "",
					"target": ""
				},
				"coupon1_id_8": {
					"money": 10.00,
					"status": "未领取",
					"consumer": "",
					"target": ""
				},
				"coupon1_id_9": {
					"money": 10.00,
					"status": "未领取",
					"consumer": "",
					"target": ""
				},
				"coupon1_id_10": {
					"money": 10.00,
					"status": "未领取",
					"consumer": "",
					"target": ""
				}
			}
			"""
