#_author_:王丽

Feature: 经营报告-经营概况——流量

	说明：1）统计整个店铺的订单包含‘本店’和‘商城’的两部分
	2）有效订单：订单状态为 待发货、已发货、已完成的订单

	一、查询条件
		1、刷选日期
			1）开始日期和结束日期都为空；选择开始结束日期，精确到日期
			2）开始日期或者结束日期，只有一个为空，给出系统提示“请填写XX日期”
			3）默认为‘最近7天’，筛选日期：‘七天前’到‘今天’
			4）包含筛选日期的开始和结束的边界值
			5）手工设置筛选日期，点击查询后，‘快速查询’的所有项都处于‘未选中状态’，时间和选项匹配的，选项处于选中状态
		2、快速查看
		    1）今天：查询的当前日期，例如，今天是2015-6-16，筛选日期是：2015-6-16到2015-6-16
		    2）昨天：查询的前一天，例如，今天是2015-6-16，筛选日期是：2015-6-15到2015-6-15
			3）最近7天；包含今天，向前7天；例如，今天是2015-6-16，筛选日期是：2015-6-10到2015-6-16
			4）最近30天；包含今天，向前30天；例如，今天是2015-6-16，筛选日期是：2015-5-19到2015-6-16
			5）最近90天；包含今天，向前90天；例如，今天是2015-6-16，筛选日期：2015-3-19到2015-6-16
			6）全部：筛选日期更新到：2013.1.1到今天
			7）打印：
	
	二、经营概况——流量 

		##同微商城的首页中的’页面访问‘

		1、【PV】：在查询区间的不同日期点的“店铺流量”的分布曲线

			例如：筛选日期：2015-5-1到2015-5-22
					2015-5-10的【PV】=∑商品.浏览次数[(2015-5-10 00:00 <= 商品.访问时间 < 2015-5-11 00:00)]
					其他日期点的【PV】依次类推

		2、【UV】：在查询区间的不同日期点的”店铺的访问量“的分布曲线

			例如：筛选日期：2015-5-1到2015-5-22
					2015-5-10的【UV】=∑商品.访问人数[(2015-5-10 00:00 <= 商品.访问时间 < 2015-5-11 00:00)]
					其他日期点的【UV】依次类推

	三、经营概况——销量

		##同微商城的首页中的’购买趋势‘

		1、【订单量】：在查询区间的不同日期点的“店铺的订单量”的分布曲线

			例如：筛选日期：2015-5-1到2015-5-22
						2015-5-10的【订单量】=∑订单.个数[(2015-5-10 00:00 <= 订单.下单时间 < 2015-5-11 00:00) 
															and (订单.订单状态 in {待发货、已发货、已完成})]
						其他日期点的【订单量】依次类推

		2、【销售额】：在查询区间的不同日期点的“店铺的销售额”的分布曲线

			例如：筛选日期：2015-5-1到2015-5-22
						2015-5-10的【销售额】=∑订单.实付金额[(2015-5-10 00:00 <= 订单.下单时间 < 2015-5-11 00:00) 
															and (订单.订单状态 in {待发货、已发货、已完成})]
						其他日期点的【销售额】依次类推

Background:
	Given jobs登录系统

	When jobs已添加商品
		"""
		[{
			"name": "商品1",
			"model": {
				"models": {
					"standard": {
						"price": 100.00,
						"freight":"10",
						"weight": 5.0,
						"stock_type": "无限"
					}
				}
			},
			"synchronized_mall":"是"
		},{
			"name": "商品2",
			"model": {
				"models": {
					"standard": {
						"price": 100.00,
						"freight":"15",
						"weight": 5.0,
						"stock_type": "无限"
					}
				}
			},
			"synchronized_mall":"是"
		}]
		"""

	And jobs设置未付款订单过期时间
		"""
		{
			"no_payment_order_expire_day":"1天"
		}
		"""

	And jobs已添加支付方式
		"""
		[{
			"type": "货到付款",
			"is_active": "启用"
		},{
			"type": "微信支付",
			"is_active": "启用"
		},{
			"type": "支付宝支付",
			"is_active": "启用"
		}]
		"""

	And jobs已添加微众支付
		"""
		[{
			"is_weizoom_pay":"是"
		}]
		"""

	And jobs设定会员积分策略
		"""
		[{ 
			"integral_each_yuan": 10
		}]
		"""

	And jobs已添加积分应用活动
		"""
		[{
			"name": "商品1积分应用",
			"start_date": "2014-8-1",
			"end_date": "10天后",
			"products": ["商品1"],
			"is_permanant_active": false,
			"rules": [{
				"member_grade_name": "全部会员",
				"discount": 70,
				"discount_money": 70.0
			}]
		}]
		"""

	And toms已添加了优惠券规则
		"""
		[{
			"name": "商品2优惠券",
			"money": 10,
			"start_date": "今天",
			"end_date": "10天后",
			"coupon_id_prefix": "coupon1_id_"
		}]
		"""

	Given bill关注jobs的公众账号于'2015-05-01'
	Given tom关注jobs的公众账号于'2015-05-02'
	Given mary关注jobs的公众账号于'2015-05-02'
	Given bill3关注jobs的公众账号于'2015-05-03'

Scenario: 1  经营概况：流量（PV和UV）

	#用户名前加’-‘标示非会员	
	When 微信用户批量浏览访问jobs的商品
		|    member   |     access_time    |   browse_object  |
		|    bill     |  2015-5-5 10:30:59 |       商品1      |
		|    bill     |  2015-5-5 15:30:59 |       商品1      |
		|    bill     |  2015-5-5 16:30:59 |       商品2      |
		|    -bill1   |  2015-5-5 11:30:20 |       商品2      |
		|    tom      |  2015-5-5 10:30:59 |       商品1      |
		|    Mary     |  2015-5-5 15:30:59 |       商品2      |
		|    -bill2   |  2015-5-6 00:00:00 |       商品2      |
		|    bill3    |  2015-5-6 10:02:00 |       商品1      |

	When jobs设置筛选日期
		"""
		[{
			"begin_date":"2015-5-5",
			"end_date":"2015-5-6"
		}]
		"""

	Then jobs获得PV和UV
		|     date    |    PV   |  UV  |
		|   2015-5-5  |    6    |  4   |
		|   2015-5-6  |    2    |  2   |

Scenario: 2  经营概况：销量
	
	When 微信用户批量消费jobs的商品
		|       date    	| consumer |businessman|      product     | payment | payment_method | freight |   price  | product_integral | coupon | paid_amount | weizoom_card | alipay | wechat | cash |      action         |  order_status   |
		| 2015-4-4  10:20  	| mary     | jobs      | 商品1,1          | 支付    |   微信支付     | 10      | 100      | 10       | 0      | 100         | 0            | 0      |   100  | 0    |   jobs发货，完成    |    已完成       |
		| 2015-5-2  8:00  	| bill     | jobs      | 商品1,1          |         |   支付宝       | 10      | 100      |  0       | 0      |  0          | 0            | 0      |    0   | 0    |   系统化自动取消    |    已取消       |
		| 2015-5-3  10:00  	| tom      | jobs      | 商品2,1          | 支付    |   微信支付     | 15      | 100      |  0       | 0      | 115         | 0            | 0      |    115 | 0    |   jobs发货，完成    |    已完成       |
		| 2015-5-5  9:00  	| bill     | jobs      | 商品1,1          | 支付    |   货到付款     | 10      | 100      |  0       | 30     | 80          | 0            | 0      |    0   | 80   |                     |    待发货       |
		| 2015-5-6  9:00  	| tom      | jobs      | 商品1,1          | 支付    |   货到付款     | 10      | 100      |  20      | 0      | 90          | 0            | 0      |    0   | 90   |   jobs发货          |    已发货       |
		| 2015-5-6  10:00  	| bill     | jobs      | 商品1,1          | 支付    |   支付宝       | 10      | 100      |  0       | 0      | 110         | 0            | 110    |    0   | 0    |   jobs发货，退款    |    退款中       |
		| 2015-5-8  10:00  	| bill     | jobs      | 商品2,1          | 支付    |   微信支付     | 15      | 100      |  0       | 0      | 115         | 0            | 0      |   115  | 0    |   jobs发货，退款成功|    退款成功     |
		| 2015-5-10  23:59  | mary     | jobs      | 商品2,2          | 支付    |   支付宝       | 15      | 100      |  0       | 20     | 195         | 0            | 195    |    0   | 0    |   jobs发货          |    已发货       |
		| 2015-5-10  00:00  | tom      | jobs      | 商品2,2          | 支付    |   支付宝       | 15      | 100      |  0       | 20     | 195         | 0            | 195    |    0   | 0    |   jobs发货          |    已发货       |
		| 今天  23:59       | mary     | jobs      | 商品2,2          |         |   支付宝       | 15      | 100      |  0       | 20     | 0           | 0            | 195    |    0   | 0    |                     |    待支付       |

	When jobs设置筛选日期
		"""
		[{
			"begin_date":"2015-5-1",
			"end_date":"2015-5-10"
		}]
		"""

	Then jobs获得销量
		|   date    | order_quantity  |  Sales  |
		| 2015-5-1  |       0         |    0    |
		| 2015-5-2  |       0         |    0    |
		| 2015-5-3  |       1         |   115   |
		| 2015-5-4  |       0         |    0    |
		| 2015-5-5  |       1         |   80    |
		| 2015-5-6  |       1         |   90    |
		| 2015-5-7  |       0         |    0    |
		| 2015-5-8  |       0         |    0    |
		| 2015-5-9  |       0         |    0    |
		| 2015-5-10 |       2         |   390   |
		