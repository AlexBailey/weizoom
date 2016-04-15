#_author_:宋温馨
Feature:商品列表页搜索和分页功能

Background:
	Given jobs登录系统
	And jobs已添加微页面
		"""
		[{
			"name": "微页面1"
		},{
			"name": "微页面2"
		},{
			"name": "微页面3"
		},{
			"name": "微页面4"
		},{
			"name": "微页面5"
		},{
			"name": "微页面6"
		},{
			"name": "微页面7"
		},{
			"name": "微页面8"
		},{
			"name": "微页面9"
		},{
			"name": "微页面10"
		},{
			"name": "微页面11"
		},{
			"name": "微页面12"
		},{
			"name": "微页面13"
		},{
			"name": "微页面14"
		},{
			"name": "微页面15"
		},{
			"name": "微页面16"
		},{
			"name": "微页面17"
		},{
			"name": "微页面18"
		},{
			"name": "微页面19"
		}]
		"""

@mall2 @termite2
Scenario:1微页面列表搜索功能（按微页面名称进行查询）
	#模糊匹配搜索
	When jobs按微页面名称搜索
		"""
		[{
			"search":"5"
		}]
		"""
	Then jobs能获取微页面列表
		"""
		[{
			"name":"微页面15"
		},{
			"name":"微页面5"
		}]
		"""	
	#精准匹配搜索
	When jobs按微页面名称搜索
		"""
		[{
			"search":"微页面11"
		}]
		"""
	Then jobs能获取微页面列表
		"""
		[{
			"name":"微页面11"
		}]
		"""	
	#空搜索
	When jobs按微页面名称搜索
		"""
		[{
			"search":""
		}]
		"""
	Then jobs能获取微页面列表
		"""
		[{
			"name": "空白页面"
		},{
			"name": "微页面19"
		},{
			"name": "微页面18"
		},{
			"name": "微页面17"
		},{
			"name": "微页面16"
		},{
			"name": "微页面15"
		},{
			"name": "微页面14"
		},{
			"name": "微页面13"
		},{
			"name": "微页面12"
		},{
			"name": "微页面11"
		},{
			"name": "微页面10"
		},{
			"name": "微页面9"
		},{
			"name": "微页面8"
		},{
			"name": "微页面7"
		},{
			"name": "微页面6"
		},{
			"name": "微页面5"
		},{
			"name": "微页面4"
		},{
			"name": "微页面3"
		},{
			"name": "微页面2"
		},{
			"name": "微页面1"
		}]
		"""

@mall2 @termite2
Scenario:2 微页面分页显示
    #微页面每页20个
	When jobs创建微页面
		"""
		[{
			"title":{
				"name": "微页面标题"
			}
		}]
		"""	
	When jobs给微页面设置分页条数
		"""
		{
			"count_per_page":20
		}
		"""
	Then jobs能获取微页面列表
		"""
		[{
			"name": "空白页面"
		},{
			"name": "微页面标题"
		},{
			"name": "微页面19"
		},{
			"name": "微页面18"
		},{
			"name": "微页面17"
		},{
			"name": "微页面16"
		},{
			"name": "微页面15"
		},{
			"name": "微页面14"
		},{
			"name": "微页面13"
		},{
			"name": "微页面12"
		},{
			"name": "微页面11"
		},{
			"name": "微页面10"
		},{
			"name": "微页面9"
		},{
			"name": "微页面8"
		},{
			"name": "微页面7"
		},{
			"name": "微页面6"
		},{
			"name": "微页面5"
		},{
			"name": "微页面4"
		},{
			"name": "微页面3"
		},{
			"name": "微页面2"
		}]
		"""
	Then jobs能获取微页面显示共'2'页
	When jobs访问微页面列表第'1'页
	Then jobs能获取微页面列表
		"""
		[{
			"name": "空白页面"
		},{
			"name": "微页面标题"
		},{
			"name": "微页面19"
		},{
			"name": "微页面18"
		},{
			"name": "微页面17"
		},{
			"name": "微页面16"
		},{
			"name": "微页面15"
		},{
			"name": "微页面14"
		},{
			"name": "微页面13"
		},{
			"name": "微页面12"
		},{
			"name": "微页面11"
		},{
			"name": "微页面10"
		},{
			"name": "微页面9"
		},{
			"name": "微页面8"
		},{
			"name": "微页面7"
		},{
			"name": "微页面6"
		},{
			"name": "微页面5"
		},{
			"name": "微页面4"
		},{
			"name": "微页面3"
		},{
			"name": "微页面2"
		}]
		"""
	When jobs浏览微页面列表'下一页'
	Then jobs能获取微页面列表
		"""
		[{
			"name": "微页面1"
		}]
		"""
	When jobs浏览浏览微页面列表'上一页'
    Then jobs能获取微页面列表
		"""
		[{
			"name": "空白页面"
		},{
			"name": "微页面标题"
		},{
			"name": "微页面19"
		},{
			"name": "微页面18"
		},{
			"name": "微页面17"
		},{
			"name": "微页面16"
		},{
			"name": "微页面15"
		},{
			"name": "微页面14"
		},{
			"name": "微页面13"
		},{
			"name": "微页面12"
		},{
			"name": "微页面11"
		},{
			"name": "微页面10"
		},{
			"name": "微页面9"
		},{
			"name": "微页面8"
		},{
			"name": "微页面7"
		},{
			"name": "微页面6"
		},{
			"name": "微页面5"
		},{
			"name": "微页面4"
		},{
			"name": "微页面3"
		},{
			"name": "微页面2"
		}]
		"""