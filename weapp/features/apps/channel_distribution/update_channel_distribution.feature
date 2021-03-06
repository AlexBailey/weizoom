#author: 江秋丽 2016-08-03
Feature:渠道分销-修改分销二维码
Background:
	Given jobs登录系统

	When jobs添加优惠券规则
		"""
		[{
			"name": "优惠券1",
			"money": 100.00,
			"count": 5,
			"limit_counts": 1,
			"using_limit": "满50元可以使用",
			"start_date": "今天",
			"end_date": "1天后",
			"coupon_id_prefix": "coupon1_id_"
		}]
		"""
	And jobs添加会员分组
		"""
		{
			"tag_id_1": "分组1",
			"tag_id_2": "分组2"
		}
		"""
	And jobs已添加多图文
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
	And bigs关注jobs的公众号于'2015-10-01'
	And bill关注jobs的公众号于'2015-10-01 10:00:00'
	And tom关注jobs的公众号于'2015-10-02'
	Given jobs登录系统
	When jobs新建渠道分销二维码
		"""
		[{
			"code_name": "渠道分销二维码",
			"relation_member": "bigs",
			"distribution_prize_type": "无",
			"commission_return_rate":"10",
			"minimum_cash_discount":"80",
			"commission_return_standard":500.00,
			"settlement_time":0,
			"tags": "未分组",
			"prize_type": "无",
			"reply_type": "文字",
			"scan_code_reply": "扫码后回复文本",
			"create_time": "2015-10-10 10:20:30"
		}]
		"""

		Then jobs获得渠道分销二维码列表
			"""
			[{
				"code_name": "渠道分销二维码",
				"relation_member": "bigs",
				"attention_number": "0",
				"total_transaction_money": 0.00,
				"cash_back_amount":0.00,
				"prize": "无奖励",
				"distribution_prize":"无",
				"create_time": "2015-10-10 10:20:30"
			}]
			"""
@mall2 @apps @senior @update_distribution
Scenario:1 修改渠道分销二维码
	#修改：会员头衔、扫码设置
	Given jobs登录系统
	When jobs更新渠道分销二维码'渠道分销二维码'
		"""
		{
			"code_name": "渠道分销二维码2",
			"relation_member": "bigs",
			"distribution_prize_type": "无",
			"commission_return_rate":"10",
			"minimum_cash_discount":"80",
			"commission_return_standard":500.00,
			"setlement_time":7,
			"tags": "分组2",
			"prize_type": "优惠券",
			"coupon":"优惠券1",
			"reply_type": "图文",
			"scan_code_reply": "图文1",
			"create_time": "2015-10-12 10:20:30"
		}
		"""

	Then jobs获得渠道分销二维码列表
			"""
			[{
				"code_name": "渠道分销二维码2",
				"relation_member": "bigs",
				"attention_number": "0",
				"total_transaction_money": 0.00,
				"cash_back_amount":0.00,
				"prize": "优惠券",
				"distribution_prize":"无",
				"create_time": "2015-10-10 10:20:30"
			}]
			"""