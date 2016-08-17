#author: 邓成龙 2016-08-03

Feature:分销会员前台分销推广页
"""
		【已提取】:达到返现提取金额,申请返现的所有金额
		【收入】:所有佣金
		【返现标准】:达到该返现金额才能申请返现
		【已获得奖励】:从上次体现截止到这一次提现的时间范围内，所获得的佣金
		【差额】:还差多少金额才能申请返现
		1.没有订单完成,没有佣金
		2.有订单完成,未达到返现提取标准
		3.有订单完成,达到提取返现提取标准
		4.已返现
"""

Background:
	Given jobs登录系统
	When jobs已添加多图文
		"""
		[{
			"title":"图文1",
			"cover": [{
				"url": "/standard_static/test_resource_img/hangzhou1.jpg"
				}],
			"cover_in_the_text":"true",
			"content":"单条图文1文本内容"
		}]
		"""
	When bigs关注jobs的公众号于'2015-10-01'
	Given jobs登录系统
	When jobs新建渠道分销二维码
		"""
		[{
			"code_name": "分销二维码1",
			"relation_member": "bigs",
			"distribution_prize_type": "佣金",
			"commission_return_rate":"10",
			"minimum_cash_discount":"80",
			"commission_return_standard":50.00,
			"settlement_time":"0",
			"tags": "未分组",
			"prize_type": "无",
			"reply_type": "文字",
			"scan_code_reply": "扫码后回复文本",
			"create_time": "2015-10-10 10:20:30"
		}]
		"""
	And jobs已添加支付方式
		"""
		[{
			"type":"货到付款"
		},{
			"type":"微信支付"
		},{
			"type":"支付宝"
		}]
		"""

	And jobs已添加商品
		"""
		[{
			"name": "商品1",
			"price": 100.00,
			"count":"10"
		},{
			"name": "商品2",
			"price": 100.00,
			"count":"10"
		}]
		"""

	#扫码关注成为会员
		When 清空浏览器
		And jack扫描渠道二维码"分销二维码1"于2015-08-10 10:00:00
		And jack访问jobs的webapp

	#会员购买
		When jack购买jobs的商品::apiserver
			"""
			{
				"order_id": "002",
				"pay_type": "货到付款",
				"products":[{
					"name":"商品2",
					"count":1 
				}]
			}
			"""
		When jack购买jobs的商品::apiserver
			"""
			{
				"order_id": "003",
				"pay_type": "货到付款",
				"products":[{
					"name":"商品2",
					"count":1 
				}]
			}
			"""
		When jack购买jobs的商品::apiserver
			"""
			{
				"order_id": "004",
				"pay_type": "货到付款",
				"products":[{
					"name":"商品2",
					"count":1 
				}]
			}
			"""
		When jack购买jobs的商品::apiserver
			"""
			{
				"order_id": "005",
				"pay_type": "货到付款",
				"products":[{
					"name":"商品2",
					"count":1 
				}]
			}
			"""
		When jack购买jobs的商品::apiserver
			"""
			{
				"order_id": "006",
				"pay_type": "货到付款",
				"products":[{
					"name":"商品2",
					"count":1 
				}]
			}
			"""
		When jack购买jobs的商品::apiserver
			"""
			{
				"order_id": "007",
				"pay_type": "货到付款",
				"products":[{
					"name":"商品2",
					"count":1 
				}]
			}
			"""
		
@mall2 @apps @senior @user_order_commission @user_order_commission_1
Scenario:1 没有订单,没有佣金
	
		When bigs访问jobs的webapp
		
		Then bigs获得推广分销详情
			"""
			[{
				"already_extracted": 0,
				"income":0,
				"commission_return_standard":50.00,
				"already_reward":0,
				"difference_value":50.00
			}]
			"""

@mall2 @apps @senior @user_order_commission @user_order_commission_2
Scenario:2 有订单完成,佣金收入
	Given jobs登录系统
	When jobs完成订单"002"
	When 后台执行channel_distribution_update
		When bigs访问jobs的webapp
		
		Then bigs获得推广分销详情
			"""
			[{
				"already_extracted":0.0,
				"income":10.00,
				"commission_return_standard":50.00,
				"already_reward":10.0,
				"difference_value":40.00
			}]
			"""
@mall2 @apps @senior @user_order_commission @user_order_commission_3
Scenario:3 达到提取金额
		Given jobs登录系统
		When jobs完成订单"002"
		When jobs完成订单"003"
		When jobs完成订单"004"
		When jobs完成订单"005"
		When jobs完成订单"006"
		When 后台执行channel_distribution_update
		When bigs申请返现于2015-08-12 10:00:00
		When jobs已返现给bigs金额"50.00"
		When bigs访问jobs的webapp
		
		Then bigs获得推广分销详情
			"""
			[{
				"already_extracted": 50.00,
				"income":50.00,
				"commission_return_standard":50.00,
				"already_reward":0.00,
				"difference_value":50.00
			}]
			"""

@mall2 @apps @senior @user_order_commission @user_order_commission_4
Scenario:4 已返现
		Given jobs登录系统
		When jobs完成订单"002"
		When jobs完成订单"003"
		When jobs完成订单"004"
		When jobs完成订单"005"
		When jobs完成订单"006"
		When jobs完成订单"007"
		When 后台执行channel_distribution_update
		When bigs申请返现于2015-08-12 10:00:00
		When jobs已返现给bigs金额"50.00"
		When bigs访问jobs的webapp
		Then bigs获得推广分销详情
			"""
			[{
				"already_extracted": 60.00,
				"income":60.00,
				"commission_return_standard":50.00,
				"already_reward":0.00,
				"difference_value":50.00
			}]
			"""

@mall2 @apps @senior @user_order_commission @user_order_commission_5
Scenario:5 返现一次，完成订单
		Given jobs登录系统
		When jobs完成订单"002"
		When jobs完成订单"003"
		When jobs完成订单"004"
		When jobs完成订单"005"
		When jobs完成订单"006"
		When 后台执行channel_distribution_update
		When bigs申请返现于2015-08-12 10:00:00
		When jobs已返现给bigs金额"50.00"
		When bigs访问jobs的webapp
		Then bigs获得推广分销详情
			"""
			[{
				"already_extracted": 50.00,
				"income":50.00,
				"commission_return_standard":50.00,
				"already_reward":0.00,
				"difference_value":50.00
			}]
			"""

		When jobs完成订单"007"
		When 后台执行channel_distribution_update
		When bigs访问jobs的webapp
		Then bigs获得推广分销详情
			"""
			[{
				"already_extracted": 50.00,
				"income":60.00,
				"commission_return_standard":50.00,
				"already_reward":10.00,
				"difference_value":40.00
			}]
			"""