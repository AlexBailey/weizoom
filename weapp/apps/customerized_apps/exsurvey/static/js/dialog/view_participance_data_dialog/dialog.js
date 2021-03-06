/*
Copyright (c) 2011-2012 Weizoom Inc
*/

/**
 * 对话框
 */
ensureNS('W.dialog.app.exsurvey');
W.dialog.app.exsurvey.ViewParticipanceDataDialog = W.dialog.Dialog.extend({
	events: _.extend({
	}, W.dialog.Dialog.prototype.events),
	
	templates: {
		dialogTmpl: '#app-exsurvey-viewParticipanceDataDialog-dialog-tmpl',
		resultTmpl: '#app-exsurvey-viewParticipanceResultDialog-dialog-tmpl'
	},

	onInitialize: function(options) {
	},
	
	beforeShow: function(options) {
	},
	
	onShow: function(options) {
		this.activityId = options.activityId;
	},
	
	afterShow: function(options) {
		var that = this;
		if (this.activityId) {
			W.getApi().call({
				app: 'apps/exsurvey',
				resource: 'exsurvey_participance',
				scope: this,
				args: {
					id: this.activityId
				},
				success: function(data) {
					this.$dialog.find('.modal-body').text(data);
					var template = Handlebars.compile($(that.templates['resultTmpl']).html());
					$('.xui-app_survey-Dialog .modal-body').html(template(data));

					var click_count = 1;
					$('img.xa-uploadimg').click(function(){
						if(click_count ===1){
							var curr_hight = $(document).scrollTop();
							$('.xa-uploadimg_box').css('top',curr_hight+'px');

							click_count = click_count+1;
							var that = this;
							var img_len = $(that).parent().find('img').length;
							var img_arr = $(that).parent().find('img').clone(true);
							var img_id_index = parseInt($(that).attr('id').split('-')[1]);

							$(this).parents().find('.xa-uploadimg_box').append("<div class='xa-uploadimg_div'></div><div><img class='xa-close_btn' src='/static_v2/img/close_btn.png'></div><div class='xa-arr xa-arr_left'></div><div class='xa-arr xa-arr_right'></div>").fadeIn('fast');
							$('.xa-uploadimg_div').append($(that).clone(true));
							if(img_len==1){
								$('.xa-arr').css('display','none');
							}
							
							$('.xa-close_btn').click(function(){
									$('.xa-uploadimg_box').fadeOut('fast');
									$('.xa-uploadimg_box').empty();
									click_count = 1;
								});
							$('.xa-arr_left').click(function(){
								img_id_index = img_id_index - 1;
								if (img_id_index < 0){
									img_id_index = img_len - 1;
								}
								$('.xa-uploadimg_div').empty().append(img_arr[img_id_index]);
							});
							$('.xa-arr_right').click(function () {
								img_id_index = img_id_index + 1;
								if (img_id_index > img_len-1){
									img_id_index = 0;
								}
								$('.xa-uploadimg_div').empty().append(img_arr[img_id_index]);
							});
						}
					});

				},
				error: function(resp) {
				}
			})
		}
	},
	
	/**
	 * onGetData: 获取数据
	 */
	onGetData: function(event) {
		return {};
	}
});
