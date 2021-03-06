
# __author__ : "冯雪静"

Feature: 商品管理-批量添加到分组
	"""
	在售商品列表批量添加分组
		页面验证：
			1.在售商品列表显示-“添加分组”
			2.不选择商品点击-添加分组，提示错误信息-“请先选择商品！”
			3.选择商品点击-添加分组，显示所有商品分组且都可以勾选，以添加分组的正序显示
			4.选择商品点击-添加分组，不选择分组，提示错误信息-“请至少选择一个分组”
			5.已参加团购活动的商品在待售列表没有复选框，所以团购商品不支持批量添加分组
		功能：
			6.选择商品可以添加一个分组或多个分组
			7.如商品已存在分组里面，也可以选择此分组添加
			8.如商品第一次选择分组2，然后再选择分组1，2，3，这个商品分组的排序2，1，3，会记录之前添加分组的顺序
	"""

Background:
    Given jobs登录系统
    When jobs添加商品分类
        """
        [{
            "name": "分类1"
        }, {
            "name": "分类2"
        }, {
            "name": "分类3"
        }, {
            "name": "分类4"
        }, {
            "name": "分类5"
        }, {
            "name": "分类6"
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
    And jobs已添加商品
        """
        [{
            "name": "商品1",
            "categories": "分类1,分类2"
        }, {
            "name": "商品2",
            "categories": "分类2,分类3"
        }, {
            "name": "商品3",
            "categories": ""
        }, {
            "name": "商品4",
            "categories": ""
        }]
        """

@mall2  @product @group @ProductList  @mall @mall.product_category @djs
Scenario:1 给未添加商品分组的商品批量添加一个分组

    Given jobs登录系统
    Then jobs能够获得'在售'商品列表
        """
        [{
            "name": "商品1",
            "categories": ["分类1", "分类2"]
        },{
            "name": "商品2",
            "categories": ["分类2", "分类3"]
        },{
            "name": "商品3",
            "categories": []
        },{
            "name": "商品4",
            "categories": []
        }]
        """
    When jobs选择商品
        """
        [{
            "name": "商品3"
        },{
            "name": "商品4"
        }]
        """
    When jobs批量添加商品分组
        """
        ["分类4"]
        """
    Then jobs能够获得'在售'商品列表
        """
        [{
            "name": "商品1",
            "categories": ["分类1", "分类2"]
        }, {
            "name": "商品2",
            "categories": ["分类2", "分类3"]
        }, {
            "name": "商品3",
            "categories": ["分类4"]
        }, {
            "name": "商品4",
            "categories": ["分类4"]
        }]
        """

@mall2  @product @group @ProductList  @mall @mall.product_category @djs
Scenario:2 给未添加商品分组的商品批量添加多个分组

    Given jobs登录系统
    When jobs选择商品
        """
        [{
            "name": "商品3"
        }, {
            "name": "商品4"
        }]
        """
    When jobs批量添加商品分组
        """
        ["分类4", "分类5", "分类6"]
        """
    Then jobs能够获得'在售'商品列表
        """
        [{
            "name": "商品1",
            "categories": ["分类1", "分类2"]
        }, {
            "name": "商品2",
            "categories": ["分类2", "分类3"]
        }, {
            "name": "商品3",
            "categories": ["分类4", "分类5", "分类6"]
        }, {
            "name": "商品4",
            "categories": ["分类4", "分类5", "分类6"]
        }]
        """

@mall2  @product @group @ProductList  @mall @mall.product_category @djs
Scenario:3 给已添加商品分组的商品批量添加多个分组

    Given jobs登录系统
    When jobs选择商品
        """
        [{
            "name": "商品1"
        }, {
            "name": "商品2"
        }]
        """
    When jobs批量添加商品分组
        """
        ["分类4", "分类5", "分类6"]
        """
    Then jobs能够获得'在售'商品列表
        """
        [{
            "name": "商品1",
            "categories": ["分类1", "分类2", "分类4", "分类5", "分类6"]
        }, {
            "name": "商品2",
            "categories": ["分类2", "分类3", "分类4", "分类5", "分类6"]
        }, {
            "name": "商品3",
            "categories": []
        }, {
            "name": "商品4",
            "categories": []
        }]
        """

@mall2  @product @group @ProductList  @mall @mall.product_category @djs
Scenario:4 给全部商品批量添加多个分组

    Given jobs登录系统
    When jobs选择商品
        """
        [{
            "name": "商品1"
        }, {
            "name": "商品2"
        }, {
            "name": "商品3"
        }, {
            "name": "商品4"
        }]
        """
    When jobs批量添加商品分组
        """
        ["分类1", "分类2", "分类3"]
        """
    Then jobs能够获得'在售'商品列表
        """
        [{
            "name": "商品1",
            "categories": ["分类1", "分类2", "分类3"]
        }, {
            "name": "商品2",
            "categories": [ "分类2", "分类3","分类1"]
        }, {
            "name": "商品3",
            "categories": ["分类1", "分类2", "分类3"]
        }, {
            "name": "商品4",
            "categories": ["分类1", "分类2", "分类3"]
        }]
        """