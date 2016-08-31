# __author__ : "田丰敏"

Feature: 添加限定区域配置
	"""
		普通
		1、商家未配置任何限定区域，在“添加新商品”或“更新商品”的限定区域的区域模板处，只显示“添加新模板”
		2、商家在“限定区域”页面可添加限定区域配置，在“添加新商品”或“更新商品”页面可在区域模板处选择已配置的模板
		3、限定区域列表如果直接勾选了省份，在市一列展示为“已全选”

		自营平台：
		商品详情页面的限定区域，只能查看不可做任何修改，限定区域数据是由商品管理系统配置
	"""

Scenario:1 添加限定区域配置
	Jobs添加"限定区域配置"
	1. jobs能获得限定区域配置列表

	Given jobs登录系统
	Then jobs能获取限定区域列表
		"""
		[]
		"""
	When jobs添加限定区域配置
		"""
		{
			"name": "禁售地区",
			"limit_area": [{
				"area": "其他",
				"city": ["香港"]
			}]
		}
		"""
	When jobs添加限定区域配置
		"""
		{
			"name": "仅售地区",
			"limit_area": [{
				"area": "直辖市",
				"city": ["北京市","天津市","上海市","重庆市"]
			}]
		}
		"""
	When jobs添加限定区域配置
		"""
		{
			"name": "仅售地区",
			"limit_area": [{
				"area": "直辖市",
				"city": ["北京市","天津市"]
			},{
				"area": "华北-东北",
				"province": "河北省",
				"city": ["石家庄","唐山","沧州"]
			},{
				"area": "西北-西南",
				"province": "陕西省",
				"city": ["西安市"]
			},{
				"area": "华北-东北",
				"province": "山西省",
				"city": ["太原市","大同市","阳泉市","长治市","晋城市","朔州市","晋中市","运城市","忻州市","临汾市","吕梁市"]
			}]
		}
		"""
	Then jobs能获取限定区域列表
		"""
		[{
			"name": "仅售地区",
			"limit_area": [{
				"area": "直辖市",
				"city": ["北京市","天津市"]
			},{
				"area": "华北-东北",
				"province": "河北省",
				"city": ["石家庄","唐山","沧州"]
			},{
				"area": "西北-西南",
				"province": "陕西省",
				"city": ["西安市"]
			},{
				"area": "华北-东北",
				"province": "山西省",
				"city": "已全选"
			}],
			"actions": ["修改","删除"]
		},{
			"name": "仅售地区",
			"limit_area": [{
				"area": "直辖市",
				"city": "已全选"
			}],
			"actions": ["修改","删除"]
		},{
			"name": "禁售地区",
			"limit_area": [{
				"area": "其他",
				"city": ["香港"]
			}],
			"actions": ["修改","删除"]
		}]
		"""
