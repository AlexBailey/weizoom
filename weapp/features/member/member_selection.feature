#author: 王丽
#editor: 张三香 2015.10.16
#editor: 冯雪静 2016.03.30
#editor: 田丰敏 2016.05.31

Feature: 筛选会员列表
	"""
		jobs能管理会员列表
		1、默认展示两行筛选条件，点击展开后显示所有，当点击收起后展示为默认状态
			筛选条件顺序如下
			会员名称、会员状态、关注时间
			会员等级、会员分组、会员来源
			消费总额、购买次数、最后购买时间
			积分范围、最后对话时间
		2、筛选规则
		（1）【会员名称】：模糊匹配
		（2）【会员状态】：下拉选择（已关注、全部、取消关注）；默认"已关注"
		（3）【关注时间】：开始和结束时间，过滤会员的关注时间；
						开始时间必须小于结束时间，不能清空；
						开始时间为空，提示"请输入关注开始时间"；
						结束时间为空，提示"请输入关注结束时间"；
		（4）【会员等级】：下拉选择（全部、会员等级列表按照创建的顺序）；默认"全部"
		（5）【会员分组】：下拉选择（全部、会员分组列表按照创建的顺序）；默认"全部"
		（6）【会员来源】：下拉选择（全部、直接关注、推广扫码、会员分享）；默认"全部"
		（7）【消费总额】：会员提交支付的所有订单的实付金额总和
					=∑ 订单.实付金额[(订单.买家=当前会员) and (订单.状态 in {待发货、已发货、已完成、退款中、退款成功})]
					可以输入任何数字，不管前后输入框输入什么数字，均查询最小数至最大数之间的结果
		（8）【购买次数】：会员提交支付的所有订单的总和
					=∑ 订单.个数[(订单.买家=当前会员) and (订单.状态 in {待发货、已发货、已完成、退款中、退款成功})]
					可以输入任何数字，不管前后输入框输入什么数字，均查询最小数至最大数之间的结果
		（9）【最后购买时间】：会员最后一个提交有效订单（已完成）的【付款时间】
		（10）【积分范围】：会员目前拥有的积分
				可以输入任何数字，不管前后输入框输入什么数字，均查询最小数至最大数之间的结果
		（11）【最后对话时间】：会员发送给公众账号的最后一条消息的时间

		# __author__ : "王丽"
		2015-9新增需求
		1、会员分组默认有个分组："未分组"，不能修改（没有修改框）、不能删除（没有删除按钮）
		2、新增会员和调整没有分组的会员，默认进入"未分组"
	"""

Background:

	Given jobs登录系统
	And 开启手动清除cookie模式
	And jobs设定会员积分策略
		"""
		{
			"be_member_increase_count":0,
			"click_shared_url_increase_count_before_buy":0,
			"click_shared_url_increase_count_after_buy":0,
			"buy_via_shared_url_increase_count_for_author":0,
			"buy_increase_count_for_father":0,
			"buy_via_offline_increase_count_for_author":0,
			"click_shared_url_increase_count":0,
			"buy_award_count_for_buyer":0
		}
		"""
	#添加相关基础数据
		When jobs已添加商品
			"""
			[{
				"name": "商品1",
				"postage":10.00,
				"price":100.00
			}, {
				"name": "商品2",
				"postage":15.00,
				"price":100.00
			}]
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
				"type": "支付宝",
				"is_active": "启用"
			}]
			"""
		And jobs添加会员等级
			"""
			[{
				"name": "银牌会员",
				"upgrade": "手动升级",
				"shop_discount": "10"
			},{
				"name": "金牌会员",
				"upgrade": "手动升级",
				"shop_discount": "9"
			}]
			"""

		When jobs添加会员分组
			"""
			{
				"tag_id_1": "分组1",
				"tag_id_2": "分组2",
				"tag_id_3": "分组3"
			}
			"""

	#批量获取微信用户关注
		When jobs批量获取微信用户关注
			| member_name   | attention_time 	   | member_source |   grade  |    tags     |
			| tom1 			| 2014-08-04 23:59:59  | 直接关注      | 银牌会员 | 分组1       |
			| tom2 			| 2014-08-05 00:00:00  | 推广扫码      | 普通会员 | 分组1       |
			| tom3	 	    | 2014-08-05 08:00:00  | 会员分享      | 银牌会员 | 分组1,分组3 |
			| tom4 			| 2014-08-05 23:59:59  | 会员分享      | 金牌会员 | 分组3       |
			| tom5 			| 2014-08-06 00:00:00  | 会员分享      | 金牌会员 | 分组3       |
			| tom6          | 2014-10-01 08:00:00  | 推广扫码      | 普通会员 |             |
			| tom7          | 2014-10-01 08:00:00  | 直接关注      | 金牌会员 |             |

		And tom2取消关注jobs的公众号
		And tom4取消关注jobs的公众号

	#好友
		#bill和tom1建立好友关系
			When tom1访问jobs的webapp
			When tom1把jobs的微站链接分享到朋友圈
			When tom1获得db中在jobs公众号中的mt为'mt_{tom1_jobs}'

			When 清空浏览器
			When bill点击tom1分享链接
			Then bill在jobs公众号中有uuid对应的webapp_user
			Then 浏览器cookie包含"[fmt, uuid]"
			Then 浏览器cookie等于
				"""
				{"fmt":"mt_{tom1_jobs}"}
				"""
			When bill关注jobs的公众号
			When bill访问jobs的webapp

		#bill2和tom1建立好友关系
			When 清空浏览器
			When bill2关注jobs的公众号
			When bill2访问jobs的webapp
			When bill2点击tom1分享链接

		#bill3和tom3建立好友关系
			When 清空浏览器
			When tom3访问jobs的webapp
			When tom3把jobs的微站链接分享到朋友圈
			When tom3获得db中在jobs公众号中的mt为'mt_{tom3_jobs}'

			When 清空浏览器
			When bill3点击tom3分享链接
			Then bill3在jobs公众号中有uuid对应的webapp_user
			Then 浏览器cookie包含"[fmt, uuid]"
			Then 浏览器cookie等于
				"""
				{"fmt":"mt_{tom3_jobs}"}
				"""
			When bill3关注jobs的公众号
			When bill3访问jobs的webapp


	#获取会员积分
		When 清空浏览器
		When tom2访问jobs的webapp
		When tom2获得jobs的50会员积分
		Then tom2在jobs的webapp中拥有50会员积分

		When tom3访问jobs的webapp
		When tom3获得jobs的100会员积分
		Then tom3在jobs的webapp中拥有100会员积分

		When tom4访问jobs的webapp
		When tom4获得jobs的20会员积分
		Then tom4在jobs的webapp中拥有20会员积分

	#微信用户批量下订单
		When 微信用户批量消费jobs的商品
			| order_id | date         | payment_time | consumer |   product | payment | pay_type | postage*| price* | paid_amount*| alipay*| wechat*| cash* |     action    | order_status*|
			|   0001   | 2015-01-01   |   2015-01-01 | tom1     | 商品1,1   | 支付    | 支付宝   | 10.00   | 100.00 | 110.00      | 110.00 | 0.00   | 0.00  |               | 待发货       |
			|   0002   | 2015-01-02   |              | tom1     | 商品2,2   |         | 支付宝   | 15.00   | 100.00 | 0.00        | 0.00   | 0.00   | 0.00  | jobs,取消     | 已取消       |
			|   0003   | 2015-02-01   |   2015-02-01 | tom2     | 商品2,2   | 支付    | 支付宝   | 15.00   | 100.00 | 215.00      | 215.00 | 0.00   | 0.00  | jobs,发货     | 已发货       |
			|   0004   | 2015-02-02   |   2015-04-02 | tom2     | 商品1,1   | 支付    | 微信支付 | 10.00   | 100.00 | 110.00      | 0.00   | 110.00 | 0.00  | jobs,完成     | 已完成       |
			|   0005   | 2015-02-04   |              | tom2     | 商品1,1   |         | 微信支付 | 10.00   | 100.00 | 0.00        | 0.00   | 0.00   | 0.00  |               | 待支付       |
			|   0006   | 2015-03-02   |   2015-03-02 | tom3     | 商品1,1   | 支付    | 货到付款 | 10.00   | 100.00 | 110.00      | 0.00   | 0.00   | 110.00| jobs,完成     | 已完成       |
			|   0007   | 2015-03-04   |   2015-05-02 | tom3     | 商品2,1   | 支付    | 微信支付 | 15.00   | 100.00 | 115.00      | 0.00   | 115.00 | 0.00  | jobs,退款     | 退款中       |
			|   0008   | 2015-03-05   |   2015-03-05 | tom3     | 商品1,1   | 支付    | 支付宝   | 10.00   | 100.00 | 110.00      | 110.00 | 0.00   | 0.00  | jobs,完成退款 | 退款完成     |

@mall2 @member @memberList @tesss
Scenario:1 默认条件和空条件查询

	Given jobs登录系统

	#首次进入，默认条件查询
		When jobs访问会员列表
		Then jobs获得会员列表默认查询条件
			"""
			[{
				"status":"已关注"
			}]
			"""
		Then jobs获得刷选结果人数
			"""
			[{
				"result_quantity":8
			}]
			"""
		Then jobs可以获得会员列表
			| name  | member_rank |  fans_count | integral | pay_money | unit_price | pay_times |   attention_time  |  source  |    tags     |
			| bill3 |   普通会员  |       0      |     0    |   0.00    |    0.00    |      0    |        今天       | 会员分享 | 未分组      |
			| bill2 |   普通会员  |       0      |     0    |   0.00    |    0.00    |      0    |        今天       | 直接关注 | 未分组      |
			| bill  |   普通会员  |       0      |     0    |   0.00    |    0.00    |      0    |        今天       | 会员分享 | 未分组      |
			| tom7  |   金牌会员  |       0      |     0    |   0.00    |    0.00    |      0    |      2014-10-01   | 直接关注 | 未分组      |
			| tom6  |   普通会员  |       0      |     0    |   0.00    |    0.00    |      0    |      2014-10-01   | 推广扫码 | 未分组      |
			| tom5  |   金牌会员  |       0      |     0    |   0.00    |    0.00    |      0    |      2014-08-06   | 会员分享 | 分组3       |
			| tom3  |   银牌会员  |       1      |    100   |   110.00  |    110.00  |      1    |      2014-08-05   | 会员分享 | 分组1,分组3 |
			| tom1  |   银牌会员  |       1      |     0    |   0.00    |    0.00    |      0    |      2014-08-04   | 直接关注 | 分组1       |

	#空调条件查询，“重置”查询条件，空调间查询所有数据
		When jobs设置会员查询条件
			"""
			[{
				"status":"全部"
			}]
			"""
		Then jobs获得刷选结果人数
			"""
			[{
				"result_quantity":10
			}]
			"""
		Then jobs可以获得会员列表
			| name  | member_rank |  fans_count | integral | pay_money | unit_price | pay_times | attention_time | source   |    tags     |
			| bill3 | 普通会员    |       0      |     0    |   0.00    |    0.00    |    0      |       今天     | 会员分享 | 未分组      |
			| bill2 | 普通会员    |       0      |     0    |   0.00    |    0.00    |    0      |       今天     | 直接关注 | 未分组      |
			| bill  | 普通会员    |       0      |     0    |   0.00    |    0.00    |    0      |       今天     | 会员分享 | 未分组      |
			| tom7  | 金牌会员    |       0      |     0    |   0.00    |    0.00    |    0      |     2014-10-01 | 直接关注 | 未分组      |
			| tom6  | 普通会员    |       0      |     0    |   0.00    |    0.00    |    0      |     2014-10-01 | 推广扫码 | 未分组      |
			| tom5  | 金牌会员    |       0      |     0    |   0.00    |    0.00    |    0      |     2014-08-06 | 会员分享 | 分组3       |
			| tom4  | 金牌会员    |       0      |     20   |   0.00    |    0.00    |    0      |     2014-08-05 | 会员分享 | 分组3       |
			| tom3  | 银牌会员    |       1      |    100   |   110.00  |    110.00  |    1      |     2014-08-05 | 会员分享 | 分组1,分组3 |
			| tom2  | 普通会员    |       0      |     50   |   110.00  |    110.00  |    1      |     2014-08-05 | 推广扫码 | 分组1       |
			| tom1  | 银牌会员    |       1      |     0    |   0.00    |    0.00    |    0      |     2014-08-04 | 直接关注 | 分组1       |

@mall2 @member @memberList
Scenario:2 过滤条件"会员名称"

	#会员名称部分匹配查询
		When jobs设置会员查询条件
			"""
			[{
				"name":"bill",
				"status":"全部"
			}]
			"""
		Then jobs获得刷选结果人数
			"""
			[{
				"result_quantity":3
			}]
			"""
		Then jobs可以获得会员列表
			"""
			[{
				"name":"bill3"
			},{
				"name":"bill2"
			},{
				"name":"bill"
			}]
			"""

	#会员名称完全匹配查询
		When jobs设置会员查询条件
			"""
			[{
				"name":"tom5",
				"status":"全部"
			}]
			"""
		Then jobs获得刷选结果人数
			"""
			[{
				"result_quantity":1
			}]
			"""
		Then jobs可以获得会员列表
			"""
			[{
				"name":"tom5"
			}]
			"""

	#无查询结果
		When jobs设置会员查询条件
			"""
			[{
				"name":"marry",
				"status":"全部"
			}]
			"""
		Then jobs获得刷选结果人数
			"""
			[{
				"result_quantity":0
			}]
			"""
		Then jobs可以获得会员列表
			"""
			[]
			"""

@mall2 @member @memberList
Scenario:3 过滤条件"会员状态"

	#会员状态匹配
		When jobs设置会员查询条件
			"""
			[{
				"status":"取消关注"
			}]
			"""
		Then jobs获得刷选结果人数
			"""
			[{
				"result_quantity":2
			}]
			"""
		Then jobs可以获得会员列表
			"""
			[{
				"name":"tom4",
				"member_rank":"金牌会员"
			},{
				"name":"tom2",
				"member_rank":"普通会员"
			}]
			"""

@mall2 @member @memberList
Scenario:4 过滤条件"关注时间"

	#区间时间边界值查询，不包含结束时间
		When jobs设置会员查询条件
			"""
			[{
				"status":"全部",
				"attention_start_time":"2014-08-05 00:00",
				"attention_end_time":"2014-08-06 00:00"
			}]
			"""
		Then jobs获得刷选结果人数
			"""
			[{
				"result_quantity":4
			}]
			"""
		Then jobs可以获得会员列表
			"""
			[{
				"name":"tom5",
				"attention_time":"2014-08-06"
			},{
				"name":"tom4",
				"attention_time":"2014-08-05"
			},{
				"name":"tom3",
				"attention_time":"2014-08-05"
			},{
				"name":"tom2",
				"attention_time":"2014-08-05"
			}]
			"""

	#开始结束时间相同查询
		When jobs设置会员查询条件
			"""
			[{
				"status":"全部",
				"attention_start_time":"2014-10-01 08:00",
				"attention_end_time":"2014-10-01 08:00"
			}]
			"""
		Then jobs获得刷选结果人数
			"""
			[{
				"result_quantity":2
			}]
			"""
		Then jobs可以获得会员列表
			"""
			[{
				"name":"tom7",
				"attention_time":"2014-10-01"
			},{
				"name":"tom6",
				"attention_time":"2014-10-01"
			}]
			"""

	#无查询结果
		When jobs设置会员查询条件
			"""
			[{
				"status":"全部",
				"attention_start_time":"2015-8-10 00:00",
				"attention_end_time":"2015-8-11 00:00"
			}]
			"""
		Then jobs获得刷选结果人数
			"""
			[{
				"result_quantity":0
			}]
			"""
		Then jobs可以获得会员列表
			"""
			[]
			"""

@mall2 @member @memberList
Scenario:5 过滤条件"会员等级"

	#单等级匹配
		When jobs设置会员查询条件
			"""
			[{
				"status":"全部",
				"member_rank":"金牌会员"
			}]
			"""
		Then jobs获得刷选结果人数
			"""
			[{
				"result_quantity":3
			}]
			"""
		Then jobs可以获得会员列表
			"""
			[{
				"name":"tom7",
				"member_rank":"金牌会员"
			},{
				"name":"tom5",
				"member_rank":"金牌会员"
			},{
				"name":"tom4",
				"member_rank":"金牌会员"
			}]
			"""

@mall2 @member @memberList
Scenario:6 过滤条件"会员分组"

	#单会员分组匹配
		When jobs设置会员查询条件
			"""
			[{
				"status":"全部",
				"tags":"分组1"
			}]
			"""
		Then jobs获得刷选结果人数
			"""
			[{
				"result_quantity":3
			}]
			"""
		Then jobs可以获得会员列表
			| name  | member_rank |    tags     |
			| tom3  | 银牌会员    | 分组1,分组3 |
			| tom2  | 普通会员    | 分组1       |
			| tom1  | 银牌会员    | 分组1       |

		When jobs设置会员查询条件
			"""
			[{
				"status":"全部",
				"tags":"分组3"
			}]
			"""
		Then jobs获得刷选结果人数
			"""
			[{
				"result_quantity":3
			}]
			"""
		Then jobs可以获得会员列表
			| name  | member_rank |    tags     |
			| tom5  | 金牌会员    | 分组3       |
			| tom4  | 金牌会员    | 分组3       |
			| tom3  | 银牌会员    | 分组1,分组3 |

	#无查询结果
		When jobs设置会员查询条件
			"""
			[{
				"name":"marry",
				"status":"全部",
				"tags":"分组2"
			}]
			"""
		Then jobs获得刷选结果人数
			"""
			[{
				"result_quantity":0
			}]
			"""
		Then jobs可以获得会员列表
		"""
		[]
		"""

@mall2 @member @memberList
Scenario:7 过滤条件"会员来源"

	#单会员来源匹配

		#直接关注
			When jobs设置会员查询条件
				"""
				[{
					"status":"全部",
					"source":"直接关注"
				}]
				"""
			Then jobs获得刷选结果人数
				"""
				[{
					"result_quantity":3
				}]
				"""
			Then jobs可以获得会员列表
				| name  | member_rank | source   |
				| bill2 | 普通会员    | 直接关注 |
				| tom7  | 金牌会员    | 直接关注 |
				| tom1  | 银牌会员    | 直接关注 |

		#直接关注
			When jobs设置会员查询条件
				"""
				[{
					"status":"全部",
					"source":"推广扫码"
				}]
				"""
			Then jobs获得刷选结果人数
				"""
				[{
					"result_quantity":2
				}]
				"""
			Then jobs可以获得会员列表
				| name  | member_rank | source   |
				| tom6  | 普通会员    | 推广扫码 |
				| tom2  | 普通会员    | 推广扫码 |

		#会员分享
			When jobs设置会员查询条件
				"""
				[{
					"status":"全部",
					"source":"会员分享"
				}]
				"""
			Then jobs获得刷选结果人数
				"""
				[{
					"result_quantity":5
				}]
				"""
			Then jobs可以获得会员列表
				| name  | member_rank | source   |
				| bill3 | 普通会员    | 会员分享 |
				| bill  | 普通会员    | 会员分享 |
				| tom5  | 金牌会员    | 会员分享 |
				| tom4  | 金牌会员    | 会员分享 |
				| tom3  | 银牌会员    | 会员分享 |

@mall2 @member @memberList
Scenario:8 过滤条件"消费总额"

	#区间查询，包含开始和结束数值，开始数值小于结束数值
		When jobs设置会员查询条件
			"""
			[{
				"status":"全部",
				"pay_money_start":"1.00",
				"pay_money_end":"200.00"
			}]
			"""
		Then jobs获得刷选结果人数
			"""
			[{
				"result_quantity":2
			}]
			"""
		Then jobs可以获得会员列表
			| name  | member_rank | pay_money | unit_price | pay_times |
			| tom3  | 银牌会员    |   110.00  |   110.00   |     1     |
			| tom2  | 普通会员    |   110.00  |   110.00   |     1     |

	#区间查询，包含开始和结束数值，开始数值大于结束数值
		When jobs设置会员查询条件
			"""
			[{
				"status":"全部",
				"pay_money_start":"110.123456",
				"pay_money_end":"109.2356"
			}]
			"""
		Then jobs获得刷选结果人数
			"""
			[{
				"result_quantity":2
			}]
			"""
		Then jobs可以获得会员列表
			| name  | member_rank | pay_money | unit_price | pay_times |
			| tom3  | 银牌会员    |   110.00  |   110.00   |     1     |
			| tom2  | 普通会员    |   110.00  |   110.00   |     1     |

	#开始结束数值相同
		When jobs设置会员查询条件
			"""
			[{
				"status":"全部",
				"pay_money_start":"110.00",
				"pay_money_end":"110.00"
			}]
			"""
		Then jobs获得刷选结果人数
			"""
			[{
				"result_quantity":2
			}]
			"""
		Then jobs可以获得会员列表
			| name  | member_rank | pay_money | unit_price | pay_times |
			| tom3  | 银牌会员    |   110.00  |   110.00   |     1     |
			| tom2  | 普通会员    |   110.00  |   110.00   |     1     |

	#特殊数据查询
		When jobs设置会员查询条件
			"""
			[{
				"status":"全部",
				"pay_money_start":"-10.00",
				"pay_money_end":"10.00"
			}]
			"""
		Then jobs获得刷选结果人数
			"""
			[{
				"result_quantity":8
			}]
			"""
		Then jobs可以获得会员列表
			| name  | member_rank | pay_money | unit_price | pay_times |
			| bill3 | 普通会员    |   0.00    |    0.00    |     0     |
			| bill2 | 普通会员    |   0.00    |    0.00    |     0     |
			| bill  | 普通会员    |   0.00    |    0.00    |     0     |
			| tom7  | 金牌会员    |   0.00    |    0.00    |     0     |
			| tom6  | 普通会员    |   0.00    |    0.00    |     0     |
			| tom5  | 金牌会员    |   0.00    |    0.00    |     0     |
			| tom4  | 金牌会员    |   0.00    |    0.00    |     0     |
			| tom1  | 银牌会员    |   0.00    |    0.00    |     0     |

	#无查询结果
		When jobs设置会员查询条件
			"""
			[{
				"status":"全部",
				"pay_money_start":"-10.00",
				"pay_money_end":"-1.00"
			}]
			"""
		Then jobs获得刷选结果人数
			"""
			[{
				"result_quantity":0
			}]
			"""
		Then jobs可以获得会员列表
		"""
		[]
		"""

@mall2 @member @memberList
Scenario:9 过滤条件"购买次数"

	#区间查询，包含开始和结束数值, 开始至小于结束值
		When jobs设置会员查询条件
			"""
			[{
				"status":"全部",
				"pay_times_start":"1",
				"pay_times_end":"3"
			}]
			"""
		Then jobs获得刷选结果人数
			"""
			[{
				"result_quantity":2
			}]
			"""
		Then jobs可以获得会员列表
			| name  | member_rank | pay_times |
			| tom3  | 银牌会员    |     1     |
			| tom2  | 普通会员    |     1     |

	#区间查询，包含开始和结束数值, 开始至大于结束值
		When jobs设置会员查询条件
			"""
			[{
				"status":"全部",
				"pay_times_start":"3.123",
				"pay_times_end":"0.123"
			}]
			"""
		Then jobs获得刷选结果人数
			"""
			[{
				"result_quantity":2
			}]
			"""
		Then jobs可以获得会员列表
			| name  | member_rank | pay_times |
			| tom3  | 银牌会员    |     1     |
			| tom2  | 普通会员    |     1     |

	#开始结束数值相同
		When jobs设置会员查询条件
			"""
			[{
				"status":"全部",
				"pay_times_start":"2",
				"pay_times_end":"2"
			}]
			"""
		Then jobs获得刷选结果人数
			"""
			[{
				"result_quantity":0
			}]
			"""
		Then jobs可以获得会员列表
			"""
			[]
			"""

	#特殊数据查询
		When jobs设置会员查询条件
			"""
			[{
				"status":"全部",
				"pay_times_start":"-2.2",
				"pay_times_end":"2.3"
			}]
			"""
		Then jobs获得刷选结果人数
			"""
			[{
				"result_quantity":10
			}]
			"""
		Then jobs可以获得会员列表
			| name  | member_rank | pay_times |
			| bill3 | 普通会员    |    0      |
			| bill2 | 普通会员    |    0      |
			| bill  | 普通会员    |    0      |
			| tom7  | 金牌会员    |    0      |
			| tom6  | 普通会员    |    0      |
			| tom5  | 金牌会员    |    0      |
			| tom4  | 金牌会员    |    0      |
			| tom3  | 银牌会员    |    1      |
			| tom2  | 普通会员    |    1      |
			| tom1  | 银牌会员    |    0      |

	#无查询结果
		When jobs设置会员查询条件
			"""
			[{
				"status":"全部",
				"pay_times_start":"4",
				"pay_times_end":"10.6"
			}]
			"""
		Then jobs获得刷选结果人数
			"""
			[{
				"result_quantity":0
			}]
			"""
		Then jobs可以获得会员列表
			"""
			[]
			"""

@mall2 @member @memberList
Scenario:10 过滤条件"最后购买时间"

	#区间时间边界值查询，包含结束时间
		When jobs设置会员查询条件
			"""
			[{
				"status":"全部",
				"last_buy_start_time":"2015-04-02 00:00",
				"last_buy_end_time":"2015-05-02 00:00"
			}]
			"""
		Then jobs获得刷选结果人数
			"""
			[{
				"result_quantity":2
			}]
			"""
		Then jobs可以获得会员列表
			| name  | member_rank | pay_money | unit_price | pay_times |
			| tom3  | 银牌会员    |   110.00  |   110.00   |     1     |
			| tom2  | 普通会员    |   110.00  |   110.00   |     1     |

	#无查询结果
		When jobs设置会员查询条件
			"""
			[{
				"status":"全部",
				"last_buy_start_time":"2015-08-11 00:00",
				"last_buy_end_time":"2015-08-12 00:00"
			}]
			"""
		Then jobs获得刷选结果人数
			"""
			[{
				"result_quantity":0
			}]
			"""
		Then jobs可以获得会员列表
			"""
			[]
			"""

@mall2 @member @memberList
Scenario:11 过滤条件"积分范围"

	#区间查询，包含开始和结束数值，开始至小于结束值
		When jobs设置会员查询条件
			"""
			[{
				"status":"全部",
				"integral_start":"20",
				"integral_end":"100"
			}]
			"""
		Then jobs获得刷选结果人数
			"""
			[{
				"result_quantity":3
			}]
			"""
		Then jobs可以获得会员列表
			| name  | member_rank | integral |
			| tom4  | 金牌会员    |     20   |
			| tom3  | 银牌会员    |    100   |
			| tom2  | 普通会员    |     50   |

	#区间查询，包含开始和结束数值，开始至大于结束值
		When jobs设置会员查询条件
			"""
			[{
				"status":"全部",
				"integral_start":"100.123",
				"integral_end":"15.456"
			}]
			"""
		Then jobs获得刷选结果人数
			"""
			[{
				"result_quantity":3
			}]
			"""
		Then jobs可以获得会员列表
			| name  | member_rank | integral |
			| tom4  | 金牌会员    |     20   |
			| tom3  | 银牌会员    |    100   |
			| tom2  | 普通会员    |     50   |

	#开始结束数值相同
		When jobs设置会员查询条件
			"""
			[{
				"status":"全部",
				"integral_start":"0",
				"integral_end":"0"
			}]
			"""
		Then jobs获得刷选结果人数
			"""
			[{
				"result_quantity":7
			}]
			"""
		Then jobs可以获得会员列表
			| name  | member_rank | integral |
			| bill3 | 普通会员    |     0    |
			| bill2 | 普通会员    |     0    |
			| bill  | 普通会员    |     0    |
			| tom7  | 金牌会员    |     0    |
			| tom6  | 普通会员    |     0    |
			| tom5  | 金牌会员    |     0    |
			| tom1  | 银牌会员    |     0    |

	#无查询结果
		When jobs设置会员查询条件
			"""
			[{
				"status":"全部",
				"integral_start":"150",
				"integral_end":"300"
			}]
			"""
		Then jobs获得刷选结果人数
			"""
			[{
				"result_quantity":0
			}]
			"""
		Then jobs可以获得会员列表
			"""
			[]
			"""

@mall2 @member @memberList
Scenario:12 过滤条件"条件组合查询"

	#空调条件查询，“重置”查询条件，空调间查询所有数据
		When jobs设置会员查询条件
			"""
			[{
				"name":"tom",
				"status":"取消关注",
				"attention_start_time":"2014-08-03 00:00",
				"attention_end_time":"今天",
				"member_rank":"普通会员",
				"tags":"分组1",
				"source":"推广扫码",
				"pay_money_start":"100.00",
				"pay_money_end":"325.00",
				"pay_times_start":"0",
				"pay_times_end":"2",
				"last_buy_start_time":"2015-01-01",
				"last_buy_end_time":"2025-02-02",
				"integral_start":"0",
				"integral_end":"50",
				"message_start_time":"",
				"message_end_time":""
			}]
			"""
		Then jobs获得刷选结果人数
			"""
			[{
				"result_quantity":1
			}]
			"""
		Then jobs可以获得会员列表
			| name  | member_rank |  fans_count | integral | pay_money | unit_price | pay_times | attention_time | source   |  tags   |
			| tom2  | 普通会员    |       0      |     50   |   110.00  |   110.00   |     1     |   2014-08-05   | 推广扫码 | 分组1   |

@mall2 @member @memberList
Scenario:13 会员列表分页

	Given jobs登录系统

	And jobs设置分页查询参数
		"""
		{
			"count_per_page":3
		}
		"""

		When jobs访问会员列表
		When jobs访问会员列表第1页
		Then jobs可以获得会员列表
			| name  | member_rank |  fans_count | integral | pay_money | unit_price | pay_times |   attention_time  |  source  |    tags     |
			| bill3 |   普通会员  |       0      |     0    |   0.00    |    0.00    |      0    |        今天       | 会员分享 | 未分组      |
			| bill2 |   普通会员  |       0      |     0    |   0.00    |    0.00    |      0    |        今天       | 直接关注 | 未分组      |
			| bill  |   普通会员  |       0      |     0    |   0.00    |    0.00    |      0    |        今天       | 会员分享 | 未分组      |

		When jobs访问会员列表第2页
		Then jobs可以获得会员列表
			| name  | member_rank |  fans_count | integral | pay_money | unit_price | pay_times | attention_time | source   |    tags     |
			| tom7  | 金牌会员    |       0      |     0    |   0.00    |    0.00    |    0      |   2014-10-01   | 直接关注 | 未分组      |
			| tom6  | 普通会员    |       0      |     0    |   0.00    |    0.00    |    0      |   2014-10-01   | 推广扫码 | 未分组      |
			| tom5  | 金牌会员    |       0      |     0    |   0.00    |    0.00    |    0      |   2014-08-06   | 会员分享 | 分组3       |

		When jobs访问会员列表第3页
		Then jobs可以获得会员列表
			| name  | member_rank |  fans_count | integral | pay_money | unit_price | pay_times | attention_time | source   |    tags     |
			| tom3  | 银牌会员    |       1      |    100   |   110.00  |    110.00  |    1      |   2014-08-05   | 会员分享 | 分组1,分组3 |
			| tom1  | 银牌会员    |       1      |     0    |    0.00   |     0.00   |    0      |   2014-08-04   | 直接关注 | 分组1       |

		When jobs访问会员列表第2页
		Then jobs可以获得会员列表
			| name  | member_rank |  fans_count | integral | pay_money | unit_price | pay_times | attention_time | source   |    tags     |
			| tom7  | 金牌会员    |       0      |     0    |   0.00    |    0.00    |    0      |   2014-10-01   | 直接关注 | 未分组      |
			| tom6  | 普通会员    |       0      |     0    |   0.00    |    0.00    |    0      |   2014-10-01   | 推广扫码 | 未分组      |
			| tom5  | 金牌会员    |       0      |     0    |   0.00    |    0.00    |    0      |   2014-08-06   | 会员分享 | 分组3       |
