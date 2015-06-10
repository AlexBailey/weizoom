ensureNS('W.view.card.overview');
W.view.card.overview.OverviewBoardView = Backbone.View.extend({
    
    getTemplate: function() {
        $('#card-overview-board-view-tmpl-src').template('card-overview-board-view-tmpl');//����srcģ�壬����Ϊtmpl
        return 'card-overview-board-view-tmpl';//����ģ����
    },

    render: function() {
        //var _this = this;
        var html = $.tmpl(this.getTemplate());// tmpl(ģ�壬context)
        this.$el.append(html);//���뵽html
    },

    initialize: function(options) {
        this.$el = $(options.el);
        this.render();
    }


});
