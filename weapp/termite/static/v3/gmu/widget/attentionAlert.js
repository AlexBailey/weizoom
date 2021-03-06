/*
Copyright (c) 2011-2012 Weizoom Inc
*/

/**
 * weizoom.AttentionAlert widget
 */
 (function($, undefined) {
	// component definition
	gmu.define('AttentionAlert', {
        setting: {
            isShowButton: function(_this) {
                return W.isSubscribedMember == false;
            },
            isShowCover: function(_this) {
                return _this.$el.data('is-show-cover') ? true : false;
            },
            getDataId: function(_this) {
                var id = _this.$el.data('id');
                return id;
            },
            getQrcodeImage: function(_this) {
                var qrcode_image = _this.$el.data('qrcode-image');
                return qrcode_image;
            }
        },
		_create : function() {
            this.getIsSubscribed();
        },

        initView: function () {
            // 微众商城未关注会员点击黄条显示看购专属二维码
            if(W.webappOwnerId == 216){
                this.qrcode_image = '/static_v2/img/kangouQrcodeImg.jpg'
            }else{
                this.qrcode_image = this.setting.getQrcodeImage(this);
            }
            var height = window.screen.height;
            if('True' === this.$el.data('varnish')){
                this.$el.data('view', this);
            }else if(this.setting.isShowButton(this)) {
                this.render();
            }
        },

        getIsSubscribed: function () {            
            var _this = this;
            W.getApi().call({
                app: 'webapp',
                api: 'project_api/call',
                method: 'get',
                args: {
                    woid: W.webappOwnerId,
                    module: 'mall',
                    target_api: 'member_subscribed_status/get',
                    need_project: false
                },
                success: function(data) {
                    var is_subscribed = data.is_subscribed;
                    // 设置全局变量
                    W.isSubscribedMember = is_subscribed;
                    _this.initView();
                },
                error: function(data) {

                }
            });
        },

        render: function() {
            this.$button = $('<a class="wa-guideAttention">关注我们可查看账户积分、红包、优惠券等！</a>');
            this.$el.html(this.$button);
            if($('.xa-page')){
                $('.xa-page').css('padding-top','40px');
            }
            if($('.wa-page')){
                $('.wa-page').css('padding-top','40px');
            }
            //编辑订单页的布局因为配合iscroll滚动所以使用了绝对定位脱离了page，因而单独处理
            if($('xa-editOrderPage')){
                $('#wrapper').css('top','40px');
            }
            //订单列表页，非会员
            if($('.xui-orderListPage')){
                $('.wui-swiper-tabs').css('top','40px');
            }
            var height = this.setting.isShowCover(this) ? '100%' : '40px';
            this.$el.css('height', height);
            $('body').append('<div data-ui-role="swipemask" class="xa-qrcodeMask" data-background="rgba(0,0,0,.5)"><div class="wui-attentionBox"><img class="wui-twoDimensionImg" src="'+this.qrcode_image+'"/></div></div>');
            
            var _this = this;
            $('.xa-qrcodeMask').swipeMask().bind('click', function(event) {
                _this.clickMask();
            });
        },

        clickGuideAttention :function() {
            $('.xa-qrcodeMask').swipeMask('show');
        },
        clickMask: function(){
            $('.xa-qrcodeMask').swipeMask('hide');
        },
		_bind : function() {
		},

		_unbind : function() {
		},

		destroy : function() {
			// Unbind any events that were bound at _create
			this._unbind();

			this.options = null;
		}
	});

	// taking into account of the component when creating the window
	// or at the create event
	$(function() {
    	$('[data-ui-role="attentionAlert"]').each(function() {
    		$(this).attentionAlert();
    	});
        $('.wui-attentionAlert').click(function(){
            $(this).attentionAlert('clickGuideAttention');
        });
	})
})(Zepto);