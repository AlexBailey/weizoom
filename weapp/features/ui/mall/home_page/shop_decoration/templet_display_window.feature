#_author_:师帅

Feature:自定义模块——【基础模块】橱窗-页面

@ui
Scenario:(1)橱窗，编辑、删除、字数和控制校验
	#编辑橱窗
		#橱窗的空值校验 jobs设置橱窗标题'空',显示方式'默认',内容标题'空',内容说明'空'
		When jobs添加橱窗
		"""
			[{
				"display_window_title":"",
				"content_title":"",
				"content_explain":""
			}]
		"""
		Then jobs展示区显示默认添加的图片，以'默认'方式展示
		And jobs展示区标题'空',内容标题'空',内容说明'空'

	#橱窗的字数校验  标题'大于15',显示方式'默认',内容标题'大于15',内容说明'大于50'
		When jobs修改橱窗
		"""
			[{
				"display_window_title":"橱窗标题名大于15",
				"display_mode":"默认",
				"content_title":"内容标题大于15",
				"content_explain":"内容说明大于50"

			}]
		"""
		Then jobs展示区'橱窗标题''居左''自动折行'显示
		And jobs展示区'内容标题''居左''自动折行'显示
		And jobs展示区'内容说明''居左''自动折行'显示
		And jobs编辑区提示错误信息'橱窗标题名不能多于15字'
		And jobs编辑区提示错误信息'内容标题不能多于15字'
		And jobs编辑区提示错误信息'内容说明不能多于50字'

	#编辑橱窗 jobs修改橱窗标题'小于15',显示方式'默认',内容标题'小于15',内容说明'小于50',图片，无链接
		When jobs修改橱窗
		"""
		[{
			"display_window_title":"橱窗标题名小于15",
			"display_mode":"默认",
			"content_title":"内容标题小于15",
			"content_explain":"内容说明小于50"
		}]
		"""

		Then jobs展示区'橱窗标题''居左''自动折行'显示
		And jobs展示区'内容标题''居左''自动折行'显示
		And jobs展示区'内容说明''居左''自动折行'显示
		And jobs展示区'图片''默认样式''默认图片'显示

	#编辑橱窗 jobs修改橱窗标题'小于15',显示方式'默认',内容标题'小于15',内容说明'小于50',图片,有链接
		When jobs修改橱窗
		"""
		[{
			"display_window_title":"橱窗标题名小于15",
			"display_mode":"默认",
			"content_title":"内容标题小于15",
			"content_explain":"内容说明小于50"
			"pictrue_link_modle":[{
				"pictrue_link1":"图片链接1"
				}]
		}]
		"""

		Then jobs展示区'橱窗标题''居左''自动折行'显示
		And jobs展示区'内容标题''居左''自动折行'显示
		And jobs展示区'内容说明''居左''自动折行'显示
		And jobs展示区'图片''默认样式''默认图片'显示

	#编辑橱窗 jobs修改橱窗标题'小于15',显示方式'默认',内容标题'小于15',内容说明'小于50',图片,链接
		When jobs修改橱窗
		"""
		[{
			"display_window_title":"橱窗标题名小于15",
			"display_mode":"3列",
			"content_title":"内容标题小于15",
			"content_explain":"内容说明小于50",
			"value":[{
				"pictrue1":"图片1",
				"pictrue_link1":"图片链接1"
			},{
				"pictrue2":"图片2",
				"pictrue_link2":"图片链接2"
			},{
				"pictrue2":"图片3",
				"pictrue_link2":"图片链接3"
				}]
		}]
		"""

		Then jobs展示区'橱窗标题''居左''自动折行'显示
		And jobs展示区'内容标题''居左''自动折行'显示
		And jobs展示区'内容说明''居左''自动折行'显示
		And jobs展示区'图片''3列''设置图片'显示

	#删除橱窗模块,弹出删除确认提示窗体
		When jobs删除橱窗模块
		Then jobs展示区橱窗模块删除
		And  jobs编辑区对应的编辑窗体关闭