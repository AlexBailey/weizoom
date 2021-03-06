/*
 Copyright (c) 2011-2012 Weizoom Inc
 */

/**
 * 首页菜单列表
 * @class
 */
W.CommonProblemListView = Backbone.View.extend({
    el: '',

    events: {
        'click #add-menu-btn': 'onAddButton',
        'click #one-menu': 'onShowUpdate',
        'click #delete-menu-btn': 'onDeleteButton'
    },

    getTemplate: function(){
        $('#operation-menu-tmpl-src').template('operation-menu-tmpl');
        return 'operation-menu-tmpl';
    },

    getOneMenuTemplate: function() {
        var name = 'one-menu-tmpl';
        $('#operation-one-menu-tmpl-src').template(name);
        return name;
    },

    /*在拖动时，拖动行的cell（单元格）宽度会发生改变。在这里做了处理就没问题了*/
    storHelper: function(e, ui) {
        ui.children().each(function() {
            $(this).width($(this).width());
        });
        return ui;
    },

    initialize: function(options) {
        this.$el = $(this.el);
        this.$menusContainer = null;
        this.titleId = options.titleId;
        this.titleName = options.titleName;
        this.oneMenu = null;

	    //this.shopName = options.shopName;
	   //this.siteDomain = options.siteDomain;

        this.template = this.getTemplate();
        this.oneMenuTemplate = this.getOneMenuTemplate();

        this.optionsDialog = {
            title: '编辑问题',
            state: 'create',
	        //shopName: this.shopName,
	        //siteDomain: this.siteDomain,
            imageWidthAndHeight: {width: 70, height: 70},
            menu: null
        }

        //创建编辑界面，绑定添加后刷新列表
        this.editEditSiteDialog = W.getEditCommonProblemDialog(this.optionsDialog);
        var _this = this.titleId
        //创建collection对象，绑定其add事件
        this.menus = new W.ProblemLists();
        this.menus.titleId = _this;
        this.menus.bind('add', this.onAdd, this);
        this.menus.bind('change', this.onChange, this);
        this.menus.fetch();
    },

    render: function() {
        this.$el.html($.tmpl(this.template));
        this.$menusContainer = this.$('tbody');

        //拖动排序
        this.$el.find("tbody").css({cursor:'move'});
        this.$el.find("tbody").sortable({
            axis: 'y',
            helper: this.storHelper,
            stop: _.bind(function(options) {
                this.submitForSort();
            }, this)
        }).disableSelection();

        return this;
    },

    refresh: function(){
        this.menus.fetch();
    },

    /**
     * 接收到一条message时的响应函数
     */
    onAdd: function(message) {
        this.$menusContainer.append($.tmpl(this.oneMenuTemplate, message.toJSON()));
    },

    onChange: function(message){
        var $el = this.$('tr[menu_id="'+message.get('id')+'"]');
        $el.replaceWith($.tmpl(this.oneMenuTemplate, message.toJSON()));
    },

    /**
     * 将一条消息从页面上移除
     */
    removeOne: function(li) {
        li.remove();

    },

    submitForSort: function() {
        var sortedCategoryIds = [];
        this.$("tbody tr").each(function() {
            var id = $(this).attr("menu_id");
            sortedCategoryIds.push(id);
        });

        W.getApi().call({
            app: 'operation',
            api: 'problems/display_index/update',
            args: {
                sorted_menu_ids: sortedCategoryIds.join('_')
            },
            success: function(data) {
                this.trigger('finish-submit-message');
                xlog('success');
            },
            error: function(resp) {
                xlog('fail!');
            },
            scope: this
        });
    },

    submitDialog: function(data){
        W.getLoadingView().show();

        var _this = this;
        var id = (this.titleId == null || this.titleId =='' ? '-1' : this.titleId);
        var titleName = (this.titleName == null || this.titleName =='' ? '-1' : this.titleName);
        var task = new W.DelayedTask(function() {
            W.getApi().call({
                app: 'operation',
                api: 'problem/add',
                method: 'post',
                args: {
                    id: id,
                    problem: data.title,
                    answer: data.right_feedback,
                    titleName:titleName
                },
                success: function(data) {
                    _this.trigger('finish-submit-message');
                    _this.refresh();
                    _this.editEditSiteDialog.close();
                    W.getLoadingView().hide();
                },
                error: function() {
                    alert('更新首页菜单失败!');
                    W.getLoadingView().hide();
                },
                scope: this
            });
        });
        task.delay(300);
    },

    onAddButton: function(event){
        event.stopPropagation();
        event.preventDefault();

        var size =this.$el.find('tr').length;
        xlog(size);
        this.oneMenu = null;
        this.optionsDialog.menu = null;
        this.editEditSiteDialog.show(this.optionsDialog);
        this.editEditSiteDialog.unbind("submit");
        this.editEditSiteDialog.bind('submit', function(data) {
            this.submitDialog(data);
        },this);
    },

    /**
     * 点击"删除"链接的响应函数
     */
    onDeleteButton: function(event) {
        var $el = $(event.target);
        var deleteCommentView = W.getItemDeleteView();
        deleteCommentView.bind(deleteCommentView.SUBMIT_EVENT, function(options){
            var $tr = $el.parents('tr');
            var menuId = $tr.attr('menu_id');

            W.getApi().call({
                app: 'conference',
                api: 'delete',
                args: {
                    id: menuId
                },
                success: function(data) {
                    this.trigger('finish-submit-message');
                    this.removeOne($tr);
                    deleteCommentView.hide();
                },
                error: function(resp) {

                },
                scope: this
            });
        }, this);

        deleteCommentView.show({
            $action: $el,
            info: '确定删除吗?'
        });

        event.stopPropagation();
        event.preventDefault();
    },

    onShowUpdate: function(event){
        var $el = $(event.target);
        var id = $el.attr('menu_id');
        var menus = this.menus.getItems();
        var menu = null;
        $.each(menus,function(idx,item){
            if(item.id==id){
                menu = item;
            }
        });

        this.oneMenu = menu;
        this.optionsDialog.menu = menu
        this.editEditSiteDialog.show(this.optionsDialog);
        this.editEditSiteDialog.unbind("submit");
        this.editEditSiteDialog.bind('submit', function(data) {
            this.submitDialog(data);
        },this);

        event.stopPropagation();
        event.preventDefault();
    }
});