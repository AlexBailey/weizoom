#_author_：张三香
#editor:雪静 2015.10.15
Feature:删除积分应用活动
	Jobs能删除状态为'已结束'的积分应用活动

Background:
	Given jobs登录系统
	And jobs已添加商品
		"""
		[{
			"name": "商品1",
			"price": 100.00,
			"bar_code":"123456"
		}, {
			"name": "商品2",
			"price": 100.00
		}, {
			"name": "商品3",
			"price": 100.00
		}, {
			"name": "商品4",
			"price": 100.00
		}]
		"""
	Given jobs设定会员积分策略
		"""
		{
			"integral_each_yuan": 2
		}
		"""
	When jobs创建积分应用活动
		"""
		[{
			"name": "商品1积分应用",
			"start_date": "2015-07-11",
			"end_date": "2015-08-10",
			"status":"已结束",
			"product_name": "商品1",
			"is_permanant_active": false,
			"rules": [{
				"member_grade": "全部会员",
				"discount": 50,
				"discount_money": 50.00
			}]
		}, {
			"name": "商品2积分应用",
			"start_date": "",
			"end_date": "",
			"status":"进行中",
			"product_name": "商品2",
			"is_permanant_active": true,
			"rules": [{
				"member_grade": "全部会员",
				"discount": 50,
				"discount_money": 50.00
			}]
		}, {
			"name": "商品3积分应用",
			"start_date": "今天",
			"end_date": "2天后",
			"status":"进行中",
			"product_name": "商品3",
			"is_permanant_active": false,
			"rules": [{
				"member_grade": "全部会员",
				"discount": 50,
				"discount_money": 50.00
			}]
		}, {
			"name": "商品4积分应用",
			"start_date": "明天",
			"end_date": "3天后",
			"status":"未开始",
			"product_name": "商品4",
			"is_permanant_active": false,
			"rules": [{
				"member_grade": "全部会员",
				"discount": 50,
				"discount_money": 50.00
			}]
		}]
		"""

@mall2 @promotion @promotionIntegral @integral
Scenario: 1 删除状态为'已结束'的积分应用活动
		Given jobs登录系统
		When jobs'删除'促销活动'商品1积分应用'
		Then jobs获取积分应用活动列表
			"""
			[{
				"name": "商品4积分应用",
				"status":"未开始"
			}, {
				"name": "商品3积分应用",
				"status":"进行中"
			}, {
				"name": "商品2积分应用",
				"status":"进行中",
				"is_permanant_active": true
			}]
			"""

@mall2 @promotion @promotionIntegral @integral
Scenario: 2 批量删除积分应用活动（不包含未结束状态的活动）
	Given jobs登录系统
	When jobs批量'删除'促销活动
		"""
		[{
			"name": "商品2积分应用"
		}, {
			"name": "商品1积分应用"
		}]
		"""
	Then jobs获取积分应用活动列表
		"""
		[{
			"name": "商品4积分应用"
		}, {
			"name": "商品3积分应用"
		}]
		"""

# __author__ : "王丽" 补充在查询结果中删除活动
@mall2 @promotion @promotionIntegral @integral
Scenario: 3 在按"商品名称"查询的查询结果下删除积分活动

	Given jobs登录系统
	When jobs设置查询条件
		"""
		{
			"product_name":"商品1"
		}
		"""
	Then jobs获取积分应用活动列表
		"""
		[{
			"name": "商品1积分应用"
		}]
		"""
	When jobs'删除'促销活动'商品1积分应用'
	Then jobs获取积分应用活动列表
		"""
		[]
		"""

@mall2 @promotion @promotionIntegral @integral
Scenario: 4 在按"商品条码"查询的查询结果下删除积分活动

	Given jobs登录系统
	When jobs设置查询条件
		"""
		{
			"bar_code":"123456"
		}
		"""
	Then jobs获取积分应用活动列表
		"""
		[{
			"name": "商品1积分应用"
		}]
		"""
	When jobs'删除'促销活动'商品1积分应用'
	Then jobs获取积分应用活动列表
		"""
		[]
		"""

@mall2 @promotion @promotionIntegral @integral
Scenario: 5 在按"促销状态"查询的查询结果下删除积分活动

	Given jobs登录系统
	When jobs设置查询条件
		"""
		{
			"status":"已结束"
		}
		"""
	Then jobs获取积分应用活动列表
		"""
		[{
			"name": "商品1积分应用",
			"status":"已结束"
		}]
		"""
	When jobs'删除'促销活动'商品1积分应用'
	Then jobs获取积分应用活动列表
		"""
		[]
		"""

@mall2 @promotion @promotionIntegral @integral
Scenario: 6 在按"活动时间"查询的查询结果下删除积分活动

	Given jobs登录系统
	When jobs设置查询条件
		"""
		{
			"start_date":"2015-07-11",
			"end_date":"2015-08-10"
		}
		"""
	Then jobs获取积分应用活动列表
		"""
		[{
			"name": "商品1积分应用",
			"start_date": "2015-07-11",
			"end_date": "2015-08-10"
		}]
		"""
	When jobs'删除'促销活动'商品1积分应用'
	Then jobs获取积分应用活动列表
		"""
		[]
		"""
