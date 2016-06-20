#_author_:许韦 2016.06.20

Feature:更新微信专项抽奖活动
	"""
	1、未开始状态的微信抽奖可以进行编辑并保存，进行中和已结束状态的不能进行更改；
	2、不同状态的微信抽奖，对应的操作列按钮不同:
		未开始:【码库】【查看结果】【链接】【删除】【预览】
		进行中:【码库】【查看结果】【链接】【关闭】【预览】
		已结束:【码库】【查看结果】【链接】【删除】【预览】
	3、进行中的微信抽奖可以进行'关闭'操作，关闭后结束时间会随之更改为关闭时的时间，状态变为'已结束'
	4、未开始和已结束状态的微信抽奖，可以进行'删除'操作
	"""

Background:
	Given jobs登录系统
	When jobs添加优惠券规则
		"""
		[{
			"name": "优惠券1",
			"money": 100.00,
			"count": 500,
			"limit_counts": 1,
			"using_limit": "满50元可以使用",
			"start_date": "今天",
			"end_date": "1天后",
			"coupon_id_prefix": "coupon1_id_"
		}]
		"""
	When jobs新建微信专项抽奖活动
		"""
		[{
			"name":"专项抽奖01",
			"desc":"抽奖啦抽奖啦",
			"start_date":"明天",
			"end_date":"2天后",
			"reduce_integral":0,
			"send_integral":1,
			"win_rate":"50%",
			"lottory_code_num":5,
			"reply":"感谢关注！",
			"link_reply":"立即抽奖",
			"is_repeat_win":"是",
			"prize_settings":[{
				"prize_grade":"一等奖",
				"prize_counts":10,
				"prize_type":"积分",
				"integral":100,
				"pic":""
			},{
				"prize_grade":"二等奖",
				"prize_counts":30,
				"prize_type":"优惠券",
				"coupon":"优惠券1",
				"pic":""
			},{
				"prize_grade":"三等奖",
				"prize_counts":50,
				"prize_type":"实物",
				"gift":"精美礼品",
				"pic":"1.jpg"
			}]
		},{
			"name":"微信抽奖02",
			"desc":"抽奖啦抽奖啦",
			"start_date":"今天",
			"end_date":"2天后",
			"reduce_integral":100,
			"send_integral":0,
			"win_rate":"50%",
			"lottory_code_num":5,
			"reply":"感谢关注！",
			"link_reply":"立即抽奖",
			"is_repeat_win":"否",
			"prize_settings":[{
				"prize_grade":"一等奖",
				"prize_counts":10,
				"prize_type":"积分",
				"integral":100,
				"pic":""
			},{
				"prize_grade":"二等奖",
				"prize_counts":30,
				"prize_type":"优惠券",
				"coupon":"优惠券1",
				"pic":""
			},{
				"prize_grade":"三等奖",
				"prize_counts":50,
				"prize_type":"实物",
				"gift":"精美礼品",
				"pic":"1.jpg"
			}]
		},{
			"name":"微信抽奖03",
			"desc":"抽奖啦抽奖啦",
			"start_date":"3天前",
			"end_date":"昨天",
			"reduce_integral":0,
			"send_integral":0,
			"win_rate":"50%",
			"lottory_code_num":5,
			"reply":"感谢关注！",
			"link_reply":"立即抽奖",
			"is_repeat_win":"是",
			"prize_settings":[{
				"prize_grade":"一等奖",
				"prize_counts":10,
				"prize_type":"积分",
				"integral":100,
				"pic":""
			},{
				"prize_grade":"二等奖",
				"prize_counts":30,
				"prize_type":"优惠券",
				"coupon":"优惠券1",
				"pic":""
			},{
				"prize_grade":"三等奖",
				"prize_counts":50,
				"prize_type":"实物",
				"gift":"精美礼品",
				"pic":"1.jpg"
			}]
		}]
		"""

@mall2 @apps @apps_exlottery @update_exlottery
Scenario:1 编辑'未开始'状态的微信专项抽奖活动
	Given jobs登录系统
	Then jobs获得微信专项抽奖活动列表
		"""
		[{
			"name":"微信抽奖03",
			"status":"已结束"
		},{
			"name":"微信抽奖02",
			"status":"进行中"
		},{
			"name":"微信抽奖01",
			"status":"未开始"
		}]
		"""
	Then jobs获得'微信抽奖01'码库列表
		"""
		[{
			"lottery_code":"el8s539t18"
		},{
			"lottery_code":"el2f5e754g"
		},{
			"lottery_code":"el58fe24rf"
		},{
			"lottery_code":"elm8v6uj41"
		},{
			"lottery_code":"elmn782f2r"
		}]
		"""
	#修改名称、时间、自动回复语、中奖规则、码库数量及奖项设置
	When jobs编辑微信专项抽奖活动'微信抽奖01'
		"""
		[{
			"name":"微信抽奖001",
			"desc":"抽奖啦抽奖啦",
			"start_date":"今天",
			"end_date":"2天后",
			"reduce_integral":0,
			"send_integral":1,
			"win_rate":"80%",
			"lottory_code_num":2,
			"reply":"欢迎来到奇妙世界！",
			"link_reply":"叮一下试试看",
			"is_repeat_win":"否",
			"prize_settings":[{
				"prize_grade":"一等奖",
				"prize_counts":10,
				"prize_type":"优惠券",
				"coupon":"优惠券1",
				"pic":""
			},{
				"prize_grade":"二等奖",
				"prize_counts":20,
				"prize_type":"积分",
				"integral":100,
				"pic":""
			},{
				"prize_grade":"三等奖",
				"prize_counts":30,
				"prize_type":"积分",
				"integral":30,
				"pic":"1.jpg"
			}]
		}]
		"""
	Then jobs获得微信专项抽奖活动列表
		"""
		[{
			"name":"微信抽奖03",
			"status":"已结束"
		},{
			"name":"微信抽奖02",
			"status":"进行中"
		},{
			"name":"微信抽奖001",
			"status":"进行中"
		}]
		"""
	And jobs获得微信抽奖活动'微信抽奖001'
		"""
		[{
			"name":"微信抽奖001",
			"start_date":"今天",
			"end_date":"2天后",
			"desc":"抽奖啦抽奖啦",
			"reduce_integral":0,
			"send_integral":1,
			"win_rate":"80%",
			"lottory_code_num":2,
			"reply":"欢迎来到奇妙世界！",
			"link_reply":"叮一下试试看",
			"is_repeat_win":"否",
			"prize_settings":[{
				"prize_grade":"一等奖",
				"prize_counts":10,
				"prize_type":"优惠券",
				"coupon":"优惠券1",
				"pic":""
			},{
				"prize_grade":"二等奖",
				"prize_counts":20,
				"prize_type":"积分",
				"integral":100,
				"pic":""
			},{
				"prize_grade":"三等奖",
				"prize_counts":30,
				"prize_type":"积分",
				"integral":30,
				"pic":"1.jpg"
			}]
		}]
		"""
	And jobs获得'微信抽奖01'码库列表
		"""
		[{
			"lottery_code":"el3h5uj74u"
		},{
			"lottery_code":"elf8t1t5ha"
		}]
		"""

@mall2 @apps @apps_exlottery @update_exlottery
Scenario:2 关闭'进行中'状态的微信专项抽奖活动
	Given jobs登录系统
	Then jobs获得微信专项抽奖活动列表
		"""
		[{
			"name":"微信抽奖03",
			"status":"已结束"
		},{
			"name":"微信抽奖02",
			"start_date":"今天",
			"end_date":"2天后",
			"status":"进行中"
		},{
			"name":"微信抽奖01",
			"status":"未开始"
		}]
		"""
	When jobs关闭微信专项抽奖活动'微信抽奖02'
	Then jobs获得微信专项抽奖活动列表
		"""
		[{
			"name":"微信抽奖03",
			"status":"已结束"
		},{
			"name":"微信抽奖02",
			"start_date":"今天",
			"end_date":"今天",
			"status":"已结束"
		},{
			"name":"微信抽奖01",
			"status":"未开始"
		}]
		"""

@mall2 @apps @apps_exlottery @update_exlottery
Scenario:3 删除'未开始'和'已结束'状态的微信专项抽奖活动
	Given jobs登录系统
	Then jobs获得微信专项抽奖活动列表
		"""
		[{
			"name":"微信抽奖03",
			"status":"已结束",
			"actions": ["码库","查看结果","链接","删除","预览"]
		},{
			"name":"微信抽奖02",
			"status":"进行中",
			"actions": ["码库","查看结果","链接","关闭","预览"]
		},{
			"name":"微信抽奖01",
			"status":"未开始",
			"actions": ["码库","查看结果","链接","删除","预览"]
		}]
		"""
	#删除'未开始'状态的微信抽奖01
	When jobs删除微信专项抽奖活动'微信抽奖01'
	Then jobs获得微信专项抽奖活动列表
		"""
		[{
			"name":"微信抽奖03",
			"status":"已结束",
			"actions": ["码库","查看结果","链接","删除","预览"]
		},{
			"name":"微信抽奖02",
			"status":"进行中",
			"actions": ["码库","查看结果","链接","关闭","预览"]
		}]
		"""

	#删除'已结束'状态的微信抽奖03
	When jobs删除微信专项抽奖活动'微信抽奖03'
	Then jobs获得微信专项抽奖活动列表
		"""
		[{
			"name":"微信抽奖02",
			"status":"进行中",
			"actions": ["码库","查看结果","链接","关闭","预览"]
		}]
		"""

@mall2 @apps @apps_exlottery @update_exlottery
Scenario:4 编辑'进行中'状态的微信专项抽奖活动
	Given jobs登录系统
	Then jobs获得微信专项抽奖活动列表
		"""
		[{
			"name":"微信抽奖03",
			"status":"已结束"
		},{
			"name":"微信抽奖02",
			"status":"进行中"
		},{
			"name":"微信抽奖01",
			"status":"未开始"
		}]
		"""
	#修改奖品数量设置
	When jobs编辑微信专项抽奖活动'微信抽奖02'
		"""
		[{
			"name":"微信抽奖02",
			"start_date":"今天",
			"end_date":"2天后",
			"desc":"抽奖啦抽奖啦",
			"reduce_integral":100,
			"send_integral":0,
			"win_rate":"50%",
			"lottory_code_num":5,
			"reply":"感谢关注！",
			"link_reply":"立即抽奖",
			"is_repeat_win":"否",
			"prize_settings":[{
				"prize_grade":"一等奖",
				"prize_counts":15,
				"prize_type":"积分",
				"integral":100,
				"pic":""
			},{
				"prize_grade":"二等奖",
				"prize_counts":40,
				"prize_type":"优惠券",
				"coupon":"优惠券1",
				"pic":""
			},{
				"prize_grade":"三等奖",
				"prize_counts":60,
				"prize_type":"实物",
				"gift":"精美礼品",
				"pic":"1.jpg"
			}]
		}]
		"""
	Then jobs获得微信专项抽奖活动列表
		"""
		[{
			"name":"微信抽奖03",
			"status":"已结束"
		},{
			"name":"微信抽奖02",
			"status":"进行中"
		},{
			"name":"微信抽奖01",
			"status":"未开始"
		}]
		"""
	And jobs获得微信专项抽奖活动'微信抽奖02'
		"""
		[{
			"name":"微信抽奖02",
			"start_date":"今天",
			"end_date":"2天后",
			"desc":"抽奖啦抽奖啦",
			"reduce_integral":100,
			"send_integral":0,
			"win_rate":"50%",
			"lottory_code_num":5,
			"reply":"感谢关注！",
			"link_reply":"立即抽奖",
			"is_repeat_win":"否",
			"prize_settings":[{
				"prize_grade":"一等奖",
				"prize_counts":15,
				"prize_type":"积分",
				"integral":100,
				"pic":""
			},{
				"prize_grade":"二等奖",
				"prize_counts":40,
				"prize_type":"优惠券",
				"coupon":"优惠券1",
				"pic":""
			},{
				"prize_grade":"三等奖",
				"prize_counts":60,
				"prize_type":"实物",
				"gift":"精美礼品",
				"pic":"1.jpg"
			}]
		}]
		"""