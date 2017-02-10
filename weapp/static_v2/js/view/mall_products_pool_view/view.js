/*
Copyright (c) 2011-2012 Weizoom Inc
*/

/**
 * 运费模板编辑器
 * @constructor
 */
ensureNS('W.view.mall');
W.view.mall.ProductsPoolView = Backbone.View.extend({
    getModelInfoTemplate: function() {
        $('#mall-product-pool-view-model-info-tmpl-src').template('mall-product-pool-view-model-info-tmpl');
        return 'mall-product-pool-view-model-info-tmpl';
    },

    initialize: function(options) {
        this.$el = $(this.el);
        this.options = options || {};
        this.modelInfoTemplate = this.getModelInfoTemplate();
        this.table = this.$('[data-ui-role="pool-advanced-table"]').data('view');
    },

    events: {
        'click .xa-checkOffshelf': 'onClickCheckOffShelf',
        'click .xa-batchOffshelf': 'onClickBatchAddOffShelf',
        'click .xa-tab' : 'onClickTab',
        'click .xa-update': 'onClickUpdateBtn',
        'click .xa-offshelf': 'onClickCreateProductOffShelf',
        'click .xa-selectAll':'onClickSelectAll',
        'click .xa-showAllModels': 'onClickShowAllModelsButton'
    },

    render: function() {
        this.filterView = new W.view.mall.ProductsPoolFilterView({
            el: '.xa-productFilterView'
        });
        this.filterView.on('search', _.bind(this.onSearch, this));
        this.filterView.render();
    },
    /**
     * onClickCheckOffShelf: 单个‘未选择’商品放入待售
     */
    onClickCheckOffShelf: function(){
        W.dialog.showDialog('W.dialog.mall.OffShelfProductsListDialog', {
            success: function(data) {}
            });
    },
    /**
     * onClickTab: 选择“所有商品”或“cps商品”
     */
     onClickTab: function(event){
        this.filterView.onClickResetButton();
        var $el = $(event.currentTarget);
        var status = $el.data('cps-value');
        var tabStatus = $('#tabStatus').val();
        this.filterView.trigger('clickStatusBox', status);
        $('.xa-tab').removeClass('active');
        $('[data-cps-value="'+tabStatus+'"]').addClass('active');
        //alert('[data-cps-value="'+tabStatus+'"]')
     },
    /**
     * onClickBatchAddOffShelf: 批量‘未选择’商品放入待售
     */
     onClickBatchAddOffShelf: function(event){
        var product_ids = this.table.getAllSelectedDataIds();
        product_ids = product_ids.filter(function(currentValue, index, arr) {
            if (currentValue) {
                return currentValue;
            }
        });
        var $el = $(event.currentTarget);
        var _this = this;
        if(product_ids.length !== 0){
            var msg = "是否确认批量保存" + product_ids.length + "个商品至</br>在售商品管理？";
            W.requireConfirm({
                $el: $el,
                width:260,
                position:'top',
                isTitle: false,
                templateAlign:"vertical",
                privateContainerClass:'xui-updatePop',
                msg:msg,
                confirm:function(){
                    W.resource.mall2.ProductPool.put({
                        data: {'product_ids': JSON.stringify(product_ids)},
                        success: function(data){
                            _this.table.reload();
                            _this.$('.xa-selectAll').prop('checked', false);
                        },
                        error: function(data){}
                    })
                }
            })

        }
     },
    /**
     * onSearch: 响应filter view抛出的search事件
     */
    onSearch: function(data) {
        this.table.reload(data, {
            emptyDataHint: '没有符合条件的商品'
        });
    },
    onClickCreateProductOffShelf: function(event) {
        var _this = this;
        var product_ids = [];
        var $el = $(event.currentTarget);
        var product_id = $el.parent().parent().data('id');
        product_ids.push(product_id);
        W.resource.mall2.ProductPool.put({
            data: {'product_ids': JSON.stringify(product_ids)},
            success: function(data){
                _this.table.reload();
                _this.$('.xa-selectAll').prop('checked', false);
            },
            error: function(data){}
        })
    },
    /**
     * onClickSelectAll: 点击全选选择框时的响应函数
     */
    onClickSelectAll: function(event) {
        var $checkbox = $(event.currentTarget);
        var isChecked = $checkbox.is(':checked');
        this.$('tbody .xa-select').prop('checked', isChecked);
        this.$('.xa-selectAll').prop('checked', isChecked);
    },
    onClickUpdateBtn: function(event){
        var $el = $(event.currentTarget);
        var productId = $el.parents('tr').data('id');
        var hasActivity = $el.parents('tr').data('product-has-promotion');
        var hasGroup = $el.parents('tr').data('product-has-group');
        if(hasGroup && hasGroup == true){
            W.showHint('error', '该商品正在进行团购活动!');
            return false;
        }

        var _this = this,
            width,
            templateAlign,
            msg;
        if(hasActivity && hasActivity == 1){
            width = 300;
            templateAlign = "vertical";
            msg = "该商品正在参加活动，更新后活动将结束，</br>是否确认更新该商品？";
        }else{
            width = 400;
            templateAlign = "";
            msg = "是否确认上架该商品？";
        }
        W.requireConfirm({
            $el: $el,
            width:width,
            position:'top',
            isTitle: false,
            templateAlign:templateAlign,
            privateContainerClass:'xui-updatePop',
            msg:msg
            ,
            confirm:function(){
                W.resource.mall2.ProductPool.post({
                    data: {'product_id': productId},
                    success: function(data){
                        _this.table.reload();
                    },
                    error: function(data){
                        W.showHint('error', '该商品正在进行团购活动!');
                    }
                })
            }
        })
    },
    /**
     * onClickShowAllModelsButton: 鼠标点击“查看规格”区域的响应函数
     */
    onClickShowAllModelsButton: function(event) {
        var $target = $(event.currentTarget);
        var $tr = $target.parents('tr');
        var id = $tr.data('id');
        var product = this.table.getDataItem(id);
        var models = product.get('models');
        var $tbody = $target.parents('tbody');
        var settlementType = $tbody.attr('data-settlement');
        console.log(settlementType)
        var properties = _.pluck(models[0].property_values, 'propertyName');
        var $node = $.tmpl(this.modelInfoTemplate, {properties: properties, models: models, settlementType: settlementType});
        W.popup({
            $el: $target,
            position:'top',
            isTitle: false,
            msg: $node
        });
    },
});
W.view.mall.ProductsPoolTable = W.view.common.AdvancedTable.extend({
    afterload:function(){
        $('.xa-selectTr').each(function(index, el) {
            if($(this).data('product-status') !== 2){
                $(this).find('.xa-select').attr('disabled', 'disabled').removeClass('xa-select');
            }
        });
    }
});
W.registerUIRole('div[data-ui-role="pool-advanced-table"]', function() {
    var $div = $(this);
    var template = $div.data('template-id');
    var app = $div.data('app')
    var api = $div.attr('data-api');
    var itemCountPerPage = $div.data('item-count-per-page');
    var enablePaginator = $div.data('enable-paginator');
    var enableSort = $div.data('enable-sort');
    var enableSelect = $div.data('selectable');
    var disableHeaderSelect = $div.data('disable-header-select');
    var outerSelecter = $div.data('outer-selecter');
    var advancedTable = new W.view.mall.ProductsPoolTable({
        el: $div[0],
        template: template,
        app: app,
        api: api,
        itemCountPerPage: itemCountPerPage,
        enablePaginator: enablePaginator,
        enableSort: enableSort,
        enableSelect: enableSelect,
        outerSelecter:outerSelecter,
        disableHeaderSelect: disableHeaderSelect,
        autoLoad: true
    });
    advancedTable.render();
    advancedTable.afterload();

    $div.data('view', advancedTable);
});