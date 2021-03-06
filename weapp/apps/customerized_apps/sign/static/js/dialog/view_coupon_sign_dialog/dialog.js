
ensureNS('W.dialog.app.sign');
W.dialog.app.sign.MemberDetailSignCouponsDialog = W.dialog.Dialog.extend({
    events: _.extend({
    }, W.dialog.Dialog.prototype.events),

    getTemplate: function() {
        $('#member-detail-sign-coupons-dialog-tmpl-src').template('member-detail-sign-coupons-dialog-tmpl');
        return "member-detail-sign-coupons-dialog-tmpl";
    },

    onInitialize: function(options) {
        this.getTemplate();
        this.table = this.$dialog.find('[data-ui-role="advanced-table"]').data('view');
        options = options || {};
        this.memberId = options.memberId;
    },

    onShow: function(options) {
        this.memberId = options.memberId;

        var _this = this;
        if (!_this.table) {
            _this.table = this.$dialog.find('[data-ui-role="advanced-table"]').data('view');
        }
        if (options.isReload == true && _this.table) {
            _this.table.curPage = 1;
        }
        $('#member-detail-sign-coupons-dialog-tmpl-src').html('');
        _this.table.reload({id:this.memberId});
    }
});

