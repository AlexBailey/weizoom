#_author_:许韦 2015.06.20

Feature: 新建微信专享抽奖活动

Background:
	Given jobs登录系统
	When jobs添加优惠券规则
		"""
		[{
			"name": "优惠券1",
			"money": 100.00,
			"count": 50,
			"limit_counts": 1,
			"start_date": "今天",
			"end_date": "10天后",
			"coupon_id_prefix": "coupon1_id_"
		}, {
			"name": "优惠券2",
			"money": 50.00,
			"count": 50,
			"limit_counts": 1,
			"start_date": "今天",
			"end_date": "5天后",
			"coupon_id_prefix": "coupon2_id_"
		}, {
			"name": "优惠券3",
			"money": 30.00,
			"count": 50,
			"limit_counts": 1,
			"start_date": "今天",
			"end_date": "5天后",
			"using_limit": "满50元可以使用",
			"coupon_id_prefix": "coupon3_id_"
		}]
		"""

@mall2 @apps @apps_lottery @add_exlottery @apps_exlottery_backend
Scenario:1 新建微信专项抽奖
	Given jobs登录系统
	When jobs新建微信专项抽奖活动
		"""
		[{
			"name":"微信专项抽奖活动",
			"desc":"百事专项抽奖活动",
			"start_date":"今天",
			"end_date":"2天后",
			"desc":"抽奖啦抽奖啦",
			"reduce_integral":0,
			"send_integral":1,
			"win_rate":"50%",
			"lottory_code_num":10,
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
	Then jobs获得微信抽奖活动列表
		"""
		[{
			"name":"微信专项抽奖活动",
			"start_date":"今天",
			"end_date":"2天后",
			"status":"进行中",
			"participant_count":0,
			"actions": ["码库","查看结果","链接","关闭","预览"]
		}]
		"""


@mall2 @apps @apps_lottery @add_exlottery @apps_exlottery_backend
Scenario:2 新建微信专项抽奖活动，查看码库
	Given jobs登录系统
	When jobs新建微信抽奖活动
		"""
		[{
			"name":"微信专项抽奖活动",
			"desc":"百事专项抽奖活动",
			"start_date":"明天",
			"end_date":"2天后",
			"reduce_integral":10,
			"send_integral":0,
			"win_rate":"60%",
			"lottory_code_num":5,
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
				"coupon":"优惠券2",
				"pic":"3.jpg"
			},{
				"prize_grade":"三等奖",
				"prize_counts":50,
				"prize_type":"优惠券",
				"coupon":"优惠券3",
				"pic":"4.jpg"
			}]
		}]
		"""
	Then jobs获得码库列表
		"""
		[{
			"lottery_code":"el8s539t18",
			"user":"",
			"use_date":"",
			"prize_grade":"",
			"prize_name":""
		},{
			"lottery_code":"el2f5e754g",
			"user":"",
			"use_date":"",
			"prize_grade":"",
			"prize_name":""
		},{
			"lottery_code":"el58fe24rf",
			"user":"",
			"use_date":"",
			"prize_grade":"",
			"prize_name":""
		},{
			"lottery_code":"elm8v6uj41",
			"user":"",
			"use_date":"",
			"prize_grade":"",
			"prize_name":""
		},{
			"lottery_code":"elmn782f2r",
			"user":"",
			"use_date":"",
			"prize_grade":"",
			"prize_name":""
		}]
		"""