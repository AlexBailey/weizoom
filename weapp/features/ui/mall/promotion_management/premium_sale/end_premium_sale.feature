#_author_:张三香

Feature:结束买赠活动
	jobs能结束状态为"未开始"和"进行中"的买赠活动

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
			"name":"商品1",
			"price":100.00,
			"shelve_type": "上架"
		},{
			"name":"赠品1",
			"price":100.00,
			"shelve_type": "上架"
		},{
			"name": "商品2",
			"shelve_type": "上架",
			"is_enable_model": "启用规格",
			"model": {
				"models":{
					"M": {
						"price": 100.00,
						"stock_type": "无限"
					},
					"S": {
						"price": 200.00,
						"stock_type": "无限"
					}
				}
			}
		},{
			"name":"商品3",
			"price":100.00,
			"shelve_type": "上架",
			"is_member_product": "on"
		}]
		"""
	When jobs添加会员等级
		"""
		[{
			"name": "铜牌会员",
			"upgrade": "手动升级",
			"discount": "9"
		}, {
			"name": "银牌会员",
			"upgrade": "手动升级",
			"discount": "8"
		}, {
			"name": "金牌会员",
			"upgrade": "手动升级",
			"discount": "7"
		}]
		"""
	Then jobs能获取会员等级列表
		"""
		[{
			"name": "普通会员",
			"discount": "10.0"
		}, {
			"name": "铜牌会员",
			"upgrade": "手动升级",
			"discount": "9.0"
		}, {
			"name": "银牌会员",
			"upgrade": "手动升级",
			"discount": "8.0"
		}, {
			"name": "金牌会员",
			"upgrade": "手动升级",
			"discount": "7.0"
		}]
		"""
	When jobs创建买赠活动
		"""
			[{
				"name": "活动名称:商品3买赠",
				"product_name": "商品3",
				"product_price":100.00,
				"status":"已结束",
				"start_date": "2天前",
				"end_date": "1天前",
				"actions": ["详情","删除"],
				"premium_products": [{
					"name": "赠品1"
				}]
			},{
				"name": "活动名称:商品2买赠",
				"product_name": "商品2",
				"product_price":"100.00~200.00",
				"status":"进行中",
				"start_date": "今天",
				"end_date": "3天后",
				"actions": ["详情","结束"],
				"premium_products": [{
					"name": "赠品1"
				}]
			},{
				"name":"活动名称:商品1买赠",
				"product_name": "商品1",
				"product_price":100.00,
				"status":"未开始",
				"start_date": "明天",
				"end_date": "3天后",
				"actions": ["详情","结束"],
				"premium_products": [{
					"name": "赠品1"
				}]
			}]
		"""

@promotion @promotionPremium
Scenario: 1 结束状态为'未开始'的买赠活动
	Given jobs登录系统
	When jobs"结束"促销活动"活动名称:商品1买赠"
	Then jobs获取买赠活动列表
		"""
			[{
				"name": "活动名称:商品1买赠",
				"product_name": "商品1",
				"product_price":100.00,
				"status":"已结束",
				"start_date": "明天",
				"end_date": "3天后",
				"actions": ["详情","删除"]
			},{
				"name": "活动名称:商品2买赠",
				"product_name": "商品2",
				"product_price":"100.0 ~ 200.0",
				"status":"进行中",
				"start_date": "今天",
				"end_date": "3天后",
				"actions": ["详情","结束"]
			},{
				"name": "活动名称:商品3买赠",
				"product_name": "商品3",
				"product_price":100.00,
				"status":"已结束",
				"start_date": "2天前",
				"end_date": "1天前",
				"actions": ["详情","删除"]
			}]
		"""

@promotion @promotionPremium
Scenario: 2 结束状态为'进行中'的买赠活动
	Given jobs登录系统
	When jobs"结束"促销活动"活动名称:商品2买赠"
	Then jobs获取买赠活动列表
		"""
			[{
				"name": "活动名称:商品1买赠",
				"product_name": "商品1",
				"product_price":100.00,
				"status":"未开始",
				"start_date": "明天",
				"end_date": "3天后",
				"actions": ["详情","结束"]
			},{
				"name": "活动名称:商品2买赠",
				"product_name": "商品2",
				"product_price":"100.0 ~ 200.0",
				"status":"已结束",
				"start_date": "今天",
				"end_date": "3天后",
				"actions": ["详情","删除"]
			},{
				"name": "活动名称:商品3买赠",
				"product_name": "商品3",
				"product_price":100.00,
				"status":"已结束",
				"start_date": "2天前",
				"end_date": "1天前",
				"actions": ["详情","删除"]
			}]
		"""

@promotion @promotionPremium
Scenario: 3 批量结束买赠活动（不包括已结束状态的）
	Given jobs登录系统
	When jobs批量'结束'促销活动
		"""
			[{
				"name": "活动名称:商品1买赠",
				"product_name": "商品1",
				"product_price":100.00,
				"status":"未开始",
				"start_date": "明天",
				"end_date": "3天后",
				"actions": ["详情","删除"]
			},{
				"name": "活动名称:商品2买赠",
				"product_name": "商品2",
				"product_price":"100.0 ~ 200.0",
				"status":"进行中",
				"start_date": "今天",
				"end_date": "3天后",
				"actions": ["详情","删除"]
			}]
		"""
	Then jobs获取买赠活动列表
		"""
			[{
				"name": "活动名称:商品1买赠",
				"product_name": "商品1",
				"product_price":100.00,
				"status":"已结束",
				"start_date": "明天",
				"end_date": "3天后",
				"actions": ["详情","删除"]
			},{
				"name": "活动名称:商品2买赠",
				"product_name": "商品2",
				"product_price":"100.0 ~ 200.0",
				"status":"已结束",
				"start_date": "今天",
				"end_date": "3天后",
				"actions": ["详情","删除"]
			},{
				"name": "活动名称:商品3买赠",
				"product_name": "商品3",
				"product_price":100.00,
				"status":"已结束",
				"start_date": "2天前",
				"end_date": "1天前",
				"actions": ["详情","删除"]
			}]
		"""

@ui @promotion @promotionPremium
Scenario: 4 批量结束买赠活动（包括已结束状态的）
	Given jobs登录系统
	When jobs批量'结束'促销活动
		"""
			[{
				"name": "活动名称:商品1买赠",
				"product_name": "商品1",
				"product_price":100.00,
				"status":"未开始",
				"start_date": "明天",
				"end_date": "3天后",
				"actions": ["详情","结束"]
			},{
				"name": "活动名称:商品2买赠",
				"product_name": "商品2",
				"product_price":"100.0 ~ 200.0",
				"status":"进行中",
				"start_date": "今天",
				"end_date": "3天后",
				"actions": ["详情","结束"]
			},{
				"name": "活动名称:商品3买赠",
				"product_name": "商品3",
				"product_price":100.00,
				"status":"已结束",
				"start_date": "2天前",
				"end_date": "1天前",
				"actions": ["详情","删除"]
			}]
		"""
	Then jobs获得系统提示'不能同时进行删除和结束操作'

@promotion @promotionPremium
Scenario: 5 商品下架导致买赠活动结束
	Given jobs登录系统
	When jobs批量下架商品
		"""
		["商品1", "商品2"]
		"""
	Then jobs能获得'在售'商品列表
		"""
		[{
			"name":"商品3",
			"price":100.00,
			"is_member_product": "on"
		}, {
			"name":"赠品1",
			"price":100.00
		}]
		"""
	And jobs获取买赠活动列表
		"""
			[{
				"name": "活动名称:商品1买赠",
				"product_name": "商品1",
				"product_price":100.00,
				"status":"已结束",
				"start_date": "明天",
				"end_date": "3天后",
				"actions": ["详情","删除"]
			},{
				"name": "活动名称:商品2买赠",
				"product_name": "商品2",
				"product_price":"100.0 ~ 200.0",
				"status":"已结束",
				"start_date": "今天",
				"end_date": "3天后",
				"actions": ["详情","删除"]
			},{
				"name": "活动名称:商品3买赠",
				"product_name": "商品3",
				"product_price":100.00,
				"status":"已结束",
				"start_date": "2天前",
				"end_date": "1天前",
				"actions": ["详情","删除"]
			}]
		"""