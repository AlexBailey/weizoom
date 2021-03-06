# watcher: zhangsanxiang@weizoom.com,benchi@weizoom.com
#_author_：张三香 2015.12.14

Feature:个人中心（我的优惠券、微众卡余额查询）

Background:
	Given jobs登录系统
	And jobs已添加商品
		"""
		[{
			"name": "商品1",
			"price": 200.00
		}]
		"""
	And jobs已添加了优惠券规则
		"""
		[{
			"name": "单品券1",
			"money": 10.00,
			"limit_counts": 1,
			"start_date": "今天",
			"end_date": "1天后",
			"coupon_id_prefix": "coupon1_id_",
			"coupon_product": "商品1"
		}, {
			"name": "全体券2",
			"money": 100.00,
			"limit_counts": 1,
			"start_date": "今天",
			"end_date": "2天后",
			"using_limit": "满50元可以使用",
			"coupon_id_prefix": "coupon2_id_"
		}, {
			"name": "未开始3",
			"money": 100.00,
			"start_date": "明天",
			"end_date": "2天后",
			"using_limit": "满50元可以使用",
			"coupon_id_prefix": "coupon3_id_"
		}]
		"""
	And jobs已有微众卡支付权限
	And jobs已添加支付方式
		"""
		[{
			"type": "微众卡支付"
		}, {
			"type": "货到付款"
		}, {
			"type": "微信支付"
		}]
		"""
	Given bill关注jobs的公众号
	Given tom关注jobs的公众号

@personCenter @balance @wip.victor13
Scenario:2 个人中心-微众卡余额查询
	Given jobs登录系统
	And jobs设定会员积分策略
		"""
		{
			"integral_each_yuan": 2
		}
		"""
	And jobs已创建微众卡
		"""
		{
			"cards":[{
				"id":"0000001",
				"password":"1234567",
				"status":"未使用",
				"price":100.00
			},{
				"id":"0000002",
				"password":"1234567",
				"status":"已使用",
				"price":50.00
			},{
				"id":"0000003",
				"password":"1231231",
				"status":"已用完",
				"price":0.00
			},{
				"id":"0000004",
				"password":"1231231",
				"status":"未激活",
				"price":30.00
			},{
				"id":"0000005",
				"password":"1231231",
				"status":"已过期",
				"price":30.00
			}]
		}
		"""
	When bill访问jobs的webapp
	#查询'未使用'或'已使用'的微众卡
	When bill进行微众卡余额查询
		"""
		{
			"id":"0000001",
			"password":"1234567"
		}
		"""
	Then bill获得微众卡余额查询结果
		"""
		{
			"card_remaining":100.00
		}
		"""
		#	"can_exchange_integral":200
	#您的微众卡余额"：100.00元
	#您可以兑换：200积分
	#【返回】按钮

	#查询'已用完'的微众卡
	When bill进行微众卡余额查询
		"""
		{
			"id":"0000003",
			"password":"1231231"
		}
		"""
	Then bill获得微众卡余额查询结果
		"""
		{
			"card_remaining": 0.00
		}
		"""
		#	"can_exchange_integral":0,
		#您的微众卡余额"：0.00元
		#您可以兑换：0积分
		#您的微众卡余额不足！（红色字体显示）
		#【确认】【取消】按钮

	#查询'已过期'的微众卡
	When bill进行微众卡余额查询
		"""
		{
			"id":"0000005",
			"password":"1231231"
		}
		"""
	Then bill获得错误信息'微众卡已过期'

	#查询'未激活'的微众卡
	When bill进行微众卡余额查询
		"""
		{
			"id":"0000004",
			"password":"1231231"
		}
		"""
	Then bill获得错误信息'微众卡未激活'

	#输入错误的卡号或密码
	When bill进行微众卡余额查询
		"""
		{
			"id":"0000011",
			"password":"1234567"
		}
		"""
	Then bill获得错误信息'卡号或密码错误'

	When bill进行微众卡余额查询
		"""
		{
			"id":"0000001",
			"password":"1234568"
		}
		"""
	Then bill获得错误信息'卡号或密码错误'
