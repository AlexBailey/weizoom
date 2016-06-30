#_author_:江秋丽 2016.06.30

Feature:微信用户使用抽奖码

Background:
	Given jobs登录系统
	And jobs设定会员积分策略
		"""
		{
			"be_member_increase_count":20
		}
		"""
	When jobs添加优惠券规则
		"""
		[{
			"name": "优惠券1",
			"money": 100.00,
			"count": 50,
			"limit_counts": "无限",
			"start_date": "今天",
			"end_date": "10天后",
			"coupon_id_prefix": "coupon1_id_"
		}, {
			"name": "优惠券2",
			"money": 50.00,
			"count": 50,
			"limit_counts": "无限",
			"start_date": "今天",
			"end_date": "5天后",
			"coupon_id_prefix": "coupon2_id_"
		}]
		"""
	When jobs添加单图文
		"""
		[{
			"title":"百事抽奖活动单图文",
			"cover": [{
				"url": "6.jpg"
			}],
			"cover_in_the_text":"true",
			"summary":"百事抽奖",
			"content":"百事抽奖",
			"jump_url":"新建百事抽奖活动"
		}]
		"""
	When jobs添加关键词自动回复规则
		"""
		[{
			"rules_name":"抽奖规则",
			"keyword":
				[{
					"keyword": "百事抽奖",
					"type": "equal"
				}],
			"keyword_reply":
				[{
					"reply_content":"百事抽奖活动单图文",
					"reply_type":"text_picture"
				}]
		}]
		"""

@mall2 @apps @apps_exlottery @participate_exlottery_addition 
Scenario:1 微信用户进入专项抽奖活动首页，未输入验证码
	Given jobs登录系统
	When jobs新建专项抽奖活动
		"""
		[{
			"name":"专项抽奖活动01",
			"share_intro":"百事专项抽奖活动",
			"rule":"活动规则",
			"home_page_pic":"1.jpg",
			"lottory_pic":"2.jpg",
			"lottory_color":"red",
			"start_date":"今天",
			"end_date":"2天后",
			"reduce_integral":0,
			"send_integral":0,
			"win_rate":"50%",
			"lottory_code_num":1,
			"is_repeat_win":"否",
			"prize_settings":[{
				"prize_grade":"一等奖",
				"prize_counts":10,
				"prize_type":"积分",
				"integral":1000,
				"pic":"2.jpg"
			},{
				"prize_grade":"二等奖",
				"prize_counts":30,
				"prize_type":"优惠券",
				"coupon":"优惠券1",
				"pic":"3.jpg"
			},{
				"prize_grade":"三等奖",
				"prize_counts":50,
				"prize_type":"优惠券",
				"coupon":"优惠券2",
				"pic":"4.jpg"
			}]
		}]
		"""
	Then jobs生成'专项抽奖'码库
	"""
		["el8s539t18"]
	"""
	Then jobs生成'专项抽奖'验证码
	"""
		tudf
	"""
	
	Given bill关注jobs的公众号
	When bill访问jobs的webapp
	When bill获得jobs的20会员积分
	Then bill在jobs的webapp中拥有20会员积分
	When bill在微信中向jobs的公众号发送消息'百事抽奖'
	Then bill收到自动回复'百事抽奖活动单图文'
	When bill点击图文'百事抽奖活动单图文'进入'专项抽奖'活动页面
	When bill在'专项抽奖'活动首页中输入验证码""

	Then bill获得页面提示的消息
	"""
		请输入验证码
	"""

@mall2 @apps @apps_exlottery @participate_exlottery_addition 
Scenario:2 微信用户进入专项抽奖活动首页，输入验证码错误
	Given jobs登录系统
	When jobs新建专项抽奖活动
		"""
		[{
			"name":"专项抽奖",
			"share_intro":"百事专项抽奖活动",
			"rule":"活动规则",
			"home_page_pic":"1.jpg",
			"lottory_pic":"2.jpg",
			"lottory_color":"red",
			"start_date":"今天",
			"end_date":"5天后",
			"reduce_integral":5,
			"send_integral":0,
			"win_rate":"60%",
			"lottory_code_num":1,
			"is_repeat_win":"否",
			"prize_settings":[{
				"prize_grade":"一等奖",
				"prize_counts":10,
				"prize_type":"积分",
				"integral":1000,
				"pic":"2.jpg"
			},{
				"prize_grade":"二等奖",
				"prize_counts":30,
				"prize_type":"优惠券",
				"coupon":"优惠券1",
				"pic":"3.jpg"
			},{
				"prize_grade":"三等奖",
				"prize_counts":50,
				"prize_type":"优惠券",
				"coupon":"优惠券2",
				"pic":"4.jpg"
			}]
		}]
		"""
	Then jobs生成'专项抽奖'码库
	"""
		["el8s539t18"]
	"""
	Then jobs生成'专项抽奖'验证码
	"""
		tudf
	"""
	Given bill关注jobs的公众号
	When bill访问jobs的webapp
	When bill获得jobs的20会员积分
	Then bill在jobs的webapp中拥有20会员积分
	When bill在微信中向jobs的公众号发送消息'百事抽奖'
	Then bill收到自动回复'百事抽奖活动单图文'
	When bill点击图文'百事抽奖活动单图文'进入'专项抽奖'活动页面
	When bill在'专项抽奖'活动首页中输入验证码"sdfg"

	Then bill获得页面提示的消息
	"""
		验证码输入有误
	"""

@mall2 @apps @apps_exlottery @participate_exlottery_addition 
Scenario:3
微信用户进入专项抽奖活动首页，验证码正确，活动未开始
	Given jobs登录系统
	When jobs新建专项抽奖活动
	"""
		[{
			"name":"专项抽奖",
			"share_intro":"百事专项抽奖活动",
			"rule":"活动规则",
			"home_page_pic":"1.jpg",
			"lottory_pic":"2.jpg",
			"lottory_color":"red",
			"start_date":"2天后",
			"end_date":"5天后",
			"reduce_integral":5,
			"send_integral":0,
			"win_rate":"60%",
			"lottory_code_num":1,
			"is_repeat_win":"否",
			"prize_settings":[{
				"prize_grade":"一等奖",
				"prize_counts":10,
				"prize_type":"积分",
				"integral":1000,
				"pic":"2.jpg"
			},{
				"prize_grade":"二等奖",
				"prize_counts":30,
				"prize_type":"优惠券",
				"coupon":"优惠券1",
				"pic":"3.jpg"
			},{
				"prize_grade":"三等奖",
				"prize_counts":50,
				"prize_type":"优惠券",
				"coupon":"优惠券2",
				"pic":"4.jpg"
			}]
		}]
		"""
	Then jobs生成'专项抽奖'码库
	"""
		["el8s539t18"]
	"""
	Then jobs生成'专项抽奖'验证码
	"""
		tudf
	"""
	Given bill关注jobs的公众号
	When bill访问jobs的webapp
	When bill获得jobs的20会员积分
	Then bill在jobs的webapp中拥有20会员积分
	When bill在微信中向jobs的公众号发送消息'百事抽奖'
	Then bill收到自动回复'百事抽奖活动单图文'
	When bill点击图文'百事抽奖活动单图文'进入'专项抽奖'活动页面
	When bill在'专项抽奖'活动首页中输入验证码"tudf"
	When bill在'专项抽奖'活动首页中输入抽奖码'el8s539t18'
	Then bill获得页面提示的消息
	"""
		该抽奖码尚未生效
	"""
	
@mall2 @apps @apps_exlottery @participate_exlottery_addition
Scenario:4 微信用户进入专项抽奖活动首页，验证码正确，抽奖码正确且未使用
	Given jobs登录系统
	When jobs新建专项抽奖活动
		"""
		[{
			"name":"专项抽奖",
			"share_intro":"百事专项抽奖活动",
			"rule":"活动规则",
			"home_page_pic":"1.jpg",
			"lottory_pic":"2.jpg",
			"lottory_color":"red",
			"start_date":"今天",
			"end_date":"5天后",
			"reduce_integral":5,
			"send_integral":0,
			"win_rate":"60%",
			"lottory_code_num":1,
			"is_repeat_win":"否",
			"prize_settings":[{
				"prize_grade":"一等奖",
				"prize_counts":10,
				"prize_type":"积分",
				"integral":1000,
				"pic":"2.jpg"
			},{
				"prize_grade":"二等奖",
				"prize_counts":30,
				"prize_type":"优惠券",
				"coupon":"优惠券1",
				"pic":"3.jpg"
			},{
				"prize_grade":"三等奖",
				"prize_counts":50,
				"prize_type":"优惠券",
				"coupon":"优惠券2",
				"pic":"4.jpg"
			}]
		}]
		"""
	Then jobs生成'专项抽奖'码库
	"""
		["el8s539t18"]
	"""
	Then jobs生成'专项抽奖'验证码
	"""
		tudf
	"""
	Given bill关注jobs的公众号
	When bill访问jobs的webapp
	When bill获得jobs的20会员积分
	Then bill在jobs的webapp中拥有20会员积分
	When bill在微信中向jobs的公众号发送消息'百事抽奖'
	Then bill收到自动回复'百事抽奖活动单图文'
	When bill点击图文'百事抽奖活动单图文'进入'专项抽奖'活动页面
	When bill在专项抽奖活动首页中输入验证码"tudf"
	When bill在专项抽奖活动首页中输入抽奖码'el8s539t18'
	When bill点击'立即抽奖'进入'专项抽奖'活动内容页
	When bill参加专项抽奖活动'专项抽奖'
	Then bill获得专项抽奖结果
	"""
		{
			"prize_grade":"二等奖",
			"prize_name":"优惠券1"
		}
	"""
	

@mall2 @apps @apps_exlottery @participate_exlottery_addition
Scenario:5 微信用户进入专项抽奖活动首页，验证码正确，活动已结束并且抽奖码已使用

	Given jobs登录系统
	When jobs新建专项抽奖活动
		"""
		[{
			"name":"专项抽奖",
			"share_intro":"百事专项抽奖活动",
			"rule":"活动规则",
			"home_page_pic":"1.jpg",
			"lottory_pic":"2.jpg",
			"lottory_color":"red",
			"start_date":"今天",
			"end_date":"明天",
			"reduce_integral":5,
			"send_integral":0,
			"win_rate":"60%",
			"lottory_code_num":1,
			"is_repeat_win":"否",
			"prize_settings":[{
				"prize_grade":"一等奖",
				"prize_counts":10,
				"prize_type":"积分",
				"integral":1000,
				"pic":"2.jpg"
			},{
				"prize_grade":"二等奖",
				"prize_counts":30,
				"prize_type":"优惠券",
				"coupon":"优惠券1",
				"pic":"3.jpg"
			},{
				"prize_grade":"三等奖",
				"prize_counts":50,
				"prize_type":"优惠券",
				"coupon":"优惠券2",
				"pic":"4.jpg"
			}]
		}]
		"""
	Then jobs生成'专项抽奖'码库
	"""
		["el8s539t18"]
	"""
	Then jobs生成'专项抽奖'验证码
	"""
		tudf
	"""
	Given bill关注jobs的公众号
	When bill访问jobs的webapp
	When bill获得jobs的20会员积分
	Then bill在jobs的webapp中拥有20会员积分
	When bill在微信中向jobs的公众号发送消息'百事抽奖'
	Then bill收到自动回复'百事抽奖活动单图文'
	When bill点击图文'百事抽奖活动单图文'进入'专项抽奖'活动页面
	
	When bill在'专项抽奖'活动首页中输入验证码"tudf"
	When bill在'专项抽奖'活动首页中输入抽奖码'el8s539t18'
	When bill点击'立即抽奖'进入'专项抽奖'活动内容页
	When bill参加专项抽奖活动'专项抽奖'
	Then bill获得专项抽奖结果
	"""
		{
			"prize_grade":"二等奖",
			"prize_name":"优惠券1"
		}
	"""
	When bill在'专项抽奖'活动首页中输入抽奖码'el8s539t18'
	Then bill页面提示的消息
	"""
		该抽奖码已使用
	"""


@mall2 @apps @apps_exlottery @participate_exlottery_addition
Scenario:6 微信用户进入专项抽奖活动首页，验证码正确，活动进行中，抽奖码已使用
	Given jobs登录系统
	When jobs新建专项抽奖活动
		"""
		[{
			"name":"专项抽奖",
			"share_intro":"百事专项抽奖活动",
			"rule":"活动规则",
			"home_page_pic":"1.jpg",
			"lottory_pic":"2.jpg",
			"lottory_color":"red",
			"start_date":"今天",
			"end_date":"5天后",
			"reduce_integral":5,
			"send_integral":0,
			"win_rate":"60%",
			"lottory_code_num":1,
			"is_repeat_win":"否",
			"prize_settings":[{
				"prize_grade":"一等奖",
				"prize_counts":10,
				"prize_type":"积分",
				"integral":1000,
				"pic":"2.jpg"
			},{
				"prize_grade":"二等奖",
				"prize_counts":30,
				"prize_type":"优惠券",
				"coupon":"优惠券1",
				"pic":"3.jpg"
			},{
				"prize_grade":"三等奖",
				"prize_counts":50,
				"prize_type":"优惠券",
				"coupon":"优惠券2",
				"pic":"4.jpg"
			}]
		}]
		"""
	Then jobs生成'专项抽奖'码库
	"""
		["el8s539t18"]
	"""
	Then jobs生成'专项抽奖'验证码
	"""
		tudf
	"""
	Given bill关注jobs的公众号
	When bill访问jobs的webapp
	When bill获得jobs的20会员积分
	Then bill在jobs的webapp中拥有20会员积分
	When bill在微信中向jobs的公众号发送消息'百事抽奖'
	Then bill收到自动回复'百事抽奖活动单图文'
	When bill点击图文'百事抽奖活动单图文'进入'专项抽奖'活动页面
	
	When bill在'专项抽奖'活动首页中输入验证码"tudf"
	When bill在'专项抽奖'活动首页中输入抽奖码'el8s539t18'
	When bill点击'立即抽奖'进入'专项抽奖'活动内容页
	When bill参加专项抽奖活动'专项抽奖'
	Then bill获得专项抽奖结果
	"""
		{
			"prize_grade":"一等奖",
			"prize_name":"1000积分"
		}
	"""
	When bill在'专项抽奖'活动首页中输入抽奖码'el8s539t18'
	Then bill获得页面提示的消息
	"""
		该抽奖码已使用
	"""


	
@mall2 @apps @apps_exlottery @participate_exlottery_addition
Scenario:7 微信用户进入专项抽奖活动首页，验证码正确，活动已结束并且抽奖码未使用

	Given jobs登录系统
	When jobs新建专项抽奖活动
		"""
		[{
			"name":"专项抽奖",
			"share_intro":"百事专项抽奖活动",
			"rule":"活动规则",
			"home_page_pic":"1.jpg",
			"lottory_pic":"2.jpg",
			"lottory_color":"red",
			"start_date":"2天前",
			"end_date":"1天前",
			"reduce_integral":5,
			"send_integral":0,
			"win_rate":"60%",
			"lottory_code_num":1,
			"is_repeat_win":"否",
			"prize_settings":[{
				"prize_grade":"一等奖",
				"prize_counts":10,
				"prize_type":"积分",
				"integral":1000,
				"pic":"2.jpg"
			},{
				"prize_grade":"二等奖",
				"prize_counts":30,
				"prize_type":"优惠券",
				"coupon":"优惠券1",
				"pic":"3.jpg"
			},{
				"prize_grade":"三等奖",
				"prize_counts":50,
				"prize_type":"优惠券",
				"coupon":"优惠券2",
				"pic":"4.jpg"
			}]
		}]
		"""
	Then jobs生成'专项抽奖'码库
	"""
		["el8s539t18"]
	"""
	Then jobs生成'专项抽奖'验证码
	"""
		tudf
	"""
	Given bill关注jobs的公众号
	When bill访问jobs的webapp
	When bill获得jobs的20会员积分
	Then bill在jobs的webapp中拥有20会员积分
	When bill在微信中向jobs的公众号发送消息'百事抽奖'
	Then bill收到自动回复'百事抽奖活动单图文'
	When bill点击图文'百事抽奖活动单图文'进入'专项抽奖'活动页面
	When bill在'专项抽奖'活动首页中输入验证码"tudf"
	When bill在'专项抽奖'活动首页中输入抽奖码'el8s539t18'
	Then bill获得页面提示的消息
	"""
		该抽奖码已过期
	"""

@mall2 @apps @apps_exlottery @participate_exlottery_addition 
Scenario:8 微信用户进入专项抽奖活动首页，验证码正确，抽奖码不正确
	Given jobs登录系统
	When jobs新建专项抽奖活动
		"""
		[{
			"name":"专项抽奖",
			"share_intro":"百事专项抽奖活动",
			"rule":"活动规则",
			"home_page_pic":"1.jpg",
			"lottory_pic":"2.jpg",
			"lottory_color":"red",
			"start_date":"2天前",
			"end_date":"1天前",
			"reduce_integral":5,
			"send_integral":0,
			"win_rate":"60%",
			"lottory_code_num":1,
			"is_repeat_win":"否",
			"prize_settings":[{
				"prize_grade":"一等奖",
				"prize_counts":10,
				"prize_type":"积分",
				"integral":1000,
				"pic":"2.jpg"
			},{
				"prize_grade":"二等奖",
				"prize_counts":30,
				"prize_type":"优惠券",
				"coupon":"优惠券1",
				"pic":"3.jpg"
			},{
				"prize_grade":"三等奖",
				"prize_counts":50,
				"prize_type":"优惠券",
				"coupon":"优惠券2",
				"pic":"4.jpg"
			}]
		}]
		"""
	Then jobs生成'专项抽奖'码库
	"""
		["el8s539t18"]
	"""
	Then jobs生成'专项抽奖'验证码
	"""
		tudf
	"""
	Given bill关注jobs的公众号
	When bill访问jobs的webapp
	When bill获得jobs的20会员积分
	Then bill在jobs的webapp中拥有20会员积分
	When bill在微信中向jobs的公众号发送消息'百事抽奖'
	Then bill收到自动回复'百事抽奖活动单图文'
	When bill点击图文'百事抽奖活动单图文'进入'专项抽奖'活动页面
	When bill在'专项抽奖'活动首页中输入验证码"tudf"
	When bill在'专项抽奖'活动首页中输入抽奖码'el12345678'
	Then bill获得页面提示的消息
	"""
		请输入正确的抽奖码
	"""