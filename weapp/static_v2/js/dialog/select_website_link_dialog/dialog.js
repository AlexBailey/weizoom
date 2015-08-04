/*
Copyright (c) 2011-2012 Weizoom Inc
*/


/**
 * 选择链接dialog
 */
ensureNS('W.dialog.weixin');
W.dialog.weixin.SelectWebSiteLinkDialog = W.dialog.Dialog.extend({
    events: _.extend({
        'click .xa-selectPage': 'onSelectPage',
        'click .xa-search': 'onSearch',
        'keypress .xa-query': 'onPressKey',
        'click .xa-titleNav': 'onClickTitle'
    }, W.dialog.Dialog.prototype.events),

    getTemplate: function() {
        $('#weixin-select-link-page-dialog-tmpl-src').template('weixin-select-link-page-dialog-tmpl');
        return "weixin-select-link-page-dialog-tmpl";
    },

    onInitialize: function(options) {
        this.table = this.$('[data-ui-role="advanced-table"]').data('view');
        this.getLinkTargetJsonFun = options.getLinkTargetJsonFun;

        this.titles = options.title;
        this.menuType = options.menuType;
        this.menuItem = options.menuItem; 
        this.menuName = this.menuItem.name;
        this.selectedLinkTarget = options.selectedLinkTarget;

        this.setItemType(this.titles);
        this.setAddBtuHtml();
    },

    beforeShow: function() {
        this.table.reset();
    },

    onShow: function(options) {
        this.titles = options.title;
        this.menuType = options.menuType;
        this.menuItem = options.menuItem;
        this.menuName = this.menuItem.name;
        this.selectedLinkTarget = options.selectedLinkTarget;

        this.setItemType(this.titles);
        this.setAddBtuHtml();
        this.setAddBox();
        if(this.table.paginationView && this.menuType.indexOf('shengjing')>=0){
            this.table.paginationView.hide();
            // this.table.paginationView = false;
        }
    },

    afterShow: function(options) {
        this.onSearch();
    },

    onPressKey: function(event) {
        var keyCode = event.keyCode;
        if (keyCode == 13) {
            this.onSearch(event);
        }
    },

    setAddBtuHtml: function(){
        var $addBtn = this.$('.xa-add-item');
        $addBtn.html('<span class="xui-add-btn-icon">+</span>' + this.selectedItem.add_btn_title);
        $addBtn.attr('href', this.selectedItem.add_link);
    },

    setAddBox: function(){
        if (this.menuType == 'shengjingCustom') {
            this.$el.find('.xa-add-box').hide();
        }else{
            this.$el.find('.xa-add-box').show();
        }
    },

    onSearch: function(event) {
        var query = $.trim($('.xa-query').val());
        var link = (this.selectedLinkTarget || "").replace(/\&/g, "%26");
        this.table.reload({
            menu_type: this.menuType,
            selected_link_target: link,
            type: this.itemType,
            query: query
        })
    },

    setItemType: function(title, index){
        if (index) {
            this.selectedItem = title[index];
            this.itemType = this.selectedItem.type;
            this.titleName = this.selectedItem.name;
        }else{
            this.selectedItem = title[0];
            this.itemType = this.selectedItem.type;
            this.titleName = this.selectedItem.name;
        }
    },

    onClickTitle: function(event){
        var $el = $(event.currentTarget);
        this.itemType = $el.attr('data-nav');
        this.titleName = $el.text();
        this.$('.xa-query').val();

        this.selectedItem = this.getItemByType(this.itemType);
        this.setAddBtuHtml();

        this.onSearch();
    },

    getItemByType: function(type){
        return _.filter(this.titles, function(item) {
            return item.type == type;
        }, this)[0];
    },

    onSelectPage: function(event) {
        var $checkbox = $(event.currentTarget);
        if (!this.enableMultiSelection) {
            var $label = this.$('label.checked');
            $label.find('input').prop('checked', false);
            $label.removeClass('checked');
            if($checkbox.parent().hasClass('checked')){
                $checkbox.parent('.checked').find('span').text('已选择');
            }else{
                $checkbox.parents('tr').siblings().find('label span').text('选取');
            }
        }
        if ($checkbox.is(':checked')) {
            $checkbox.parent().addClass('checked');
            $checkbox.parent('.checked').find('span').text('已选择');
        } else {
            $checkbox.parent().removeClass('checked');
            $checkbox.parent().find('span').text('选取');
        }
    },

    /**
     * onClickSubmitButton: 点击“确定”按钮后的响应函数
     */
    onGetData: function(event) {
        var dataId = null;
        var _this = this;

        this.$('tbody tr').each(function() {
            var $tr = $(this);
            if ($tr.find('.xa-selectPage').is(':checked')) {
                dataId = $tr.data('id');
            }
        })

        var originalData = this.table.getDataItem(dataId).toJSON()
        var data = this.getLinkTargetJsonFun(
            originalData.id,
            this.menuName,
            this.titleName,
            originalData.name,
            this.titleName+'-'+originalData.name,
            originalData.link 
        );

        return data;
    }
});