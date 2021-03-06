ensureNS('W.view.mall');
W.view.mall.ProductsPoolFilterView = Backbone.View.extend({
    getTemplate: function() {
        $('#mall-products-pool-filter-view-tmpl-src').template('mall-products-pool-filter-view-tmpl');
        return 'mall-products-pool-filter-view-tmpl';
    },

    events: {
        'click .xa-search': 'onClickSearchButton',
        'click .xa-reset': 'onClickResetButton',
        'change #firstClassification': 'onChangeEvent',
        'click .xa-selectProductLabel': 'onClickSelectLabels'
    },

    initialize: function(options) {
        this.options = options || {};
        this.$el = $(options.el);
        // this.filter_value = '';
        this.bind('clickStatusBox', this.clickStatusBox);
    },

    render: function() {
        W.resource.mall2.ProductClassification.get({
            scope: this,
            data: {'level': 1},
            success: function(data) {
                var classifications = data.items;
                var html = $.tmpl(this.getTemplate(), {
                    classifications: classifications
                });
                this.$el.append(html);
            },
            error: function() {
                alert('加载失败！请刷新页面重试！');
            }
        })
    },
    clickStatusBox:function(value){
        this.onClickResetButton();
        $('#tabStatus').val(value);
        // 调用搜索事件
        this.onClickSearchButton();
    },
    onClickSelectLabels:function(){
        var productLabelIds = $('#productLabels').val()?$('#productLabels').val().split(','):[];
        W.dialog.showDialog('W.dialog.mall.SelectProductLabelDialog', {
            productLabelIds: productLabelIds,
            success: function(data) {
                console.log(data)
                var spans = [];
                var labelIds = [];
                data['names'].map(function(name){
                    spans.push('<span class="xui-product-label" title="'+ name +'">'+ name +'</span>');
                    labelIds.push()
                })
                var html = spans.join('') + '<a href="javascript:void(0);" class="xui-selectProductLabel xa-selectProductLabel">选择标签</a>'
                $('.xa-labels-box').html(html);
                $('#productLabels').val(data['ids']);
            }
        });
    },
    onClickSearchButton: function(){
        var data = this.getFilterData();
    },

    onClickResetButton: function(){
        $('#productCode').val('');
        $('#name').val('');
        $('#supplier').val('');
        $('#firstClassification').val('-1');
        $('#secondaryClassification').val('-1');
        $('#status').val('-1');
        $('#supplier_type').val('-1');
        $('#tabStatus').val('');

        $('#productLabels').val('');
        $('.xa-labels-box').html('<a href="javascript:void(0);" class="xui-selectProductLabel xa-selectProductLabel">选择标签</a>');
    },

    onChangeEvent: function() {
        var $target = $(event.target);
        var father_id = $target.val();
        W.resource.mall2.ProductClassification.get({
            scope: this,
            data: {'level': 2, 'father_id': father_id},
            success: function(data) {
                console.log(data);
            var option = '<option value="-1">二级分类</option>';
            _.each(data.items,function(data,i){
                option+='<option value='+data.id+'>'+data.name+'</option>';
                });

                $('.xa-secondCategory').html(option);
            },
            error: function() {
                alert('加载失败！请刷新页面重试！');
            }
        })
    },

    // 获取条件数据
    getFilterData: function(){
        //商品编号
        var productCode = $.trim(this.$('#productCode').val());

        //商品名
        var name = $.trim(this.$('#name').val());

        //供货商
        var supplier = $.trim(this.$('#supplier').val());

        //一级分类
        var firstClassification = this.$('#firstClassification').val();
        //二级分类
        var secondaryClassification = this.$('#secondaryClassification').val();

        //状态
        var supplier_type = this.$('#supplier_type').val();
        //商品标签
        var productLabels = this.$('#productLabels').val()?JSON.stringify(this.$('#productLabels').val().split(',')):"";

        var tabStatu = $('#tabStatus').val();
        var data = {
            // product_code: productCode,
            name: name,
            // supplier: supplier,
            first_classification: firstClassification,
            secondary_classification: secondaryClassification,
            // status: status,
            // supplier_type:supplier_type,
            labels:productLabels,
        }
        if(tabStatu == 1){data['is_cps']=1};
        this.trigger('search', data);
    },
});
