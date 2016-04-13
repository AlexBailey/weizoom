/**
 * Copyright(c) 2012-2016 weizoom
 */
"use strict";

var debug = require('debug')('m:outline.datas:CommentDialog');
var React = require('react');
var ReactDOM = require('react-dom');
var Action = require('.././rule_order/Action');
var Reactman = require('reactman');


var ApprovalDialog = Reactman.createDialog({
	getInitialState: function() {
		Action.getLimitAndCommonCard();
		// var product = this.props.data.product;
		return {
			common_status:true,
			limit_status:false
			// comment: product.comment
		}
	},

	onChange: function(value, event) {
		var property = event.target.getAttribute('name');
		var newState = {};
		newState[property] = value;
		this.setState(newState);
	},

	onBeforeCloseDialog: function() {
		if (this.state.comment === 'error') {
			Reactman.PageAction.showHint('error', '不能关闭对话框');
		} else {
			console.log(this.props.data.index,4444444444444444)
			// var product = this.props.data.product;
			// Reactman.Resource.post({
			// 	resource: 'outline.data_comment',
			// 	data: {
			// 		product_id: product.id,
			// 		comment: this.state.comment
			// 	},
			// 	success: function() {
			// 		this.closeDialog();
			// 	},
			// 	error: function() {
			// 		Reactman.PageAction.showHint('error', '评论失败!');
			// 	},
			// 	scope: this
			// })
		}
	},
	tabchange:function(status) {
		if (status=='common_status') {
			var common_status=true;
			var limit_status=false;
		}else{
			var common_status=false;
			var limit_status=true;
		}
		this.setState({
			common_status:common_status,
			limit_status:limit_status 
		});
	},
	render:function(){
		var common_status = this.state.common_status;
		var limit_status = this.state.limit_status;
		return (
		<div className="xui-formPage">
			<form className="form-horizontal mt15">
				<fieldset>
					<a href="javascript:void(0);" style={{cursor:common_status?'default':'pointer'}} onClick={this.tabchange.bind(this,'common_status')}>通用卡</a>&nbsp;&nbsp;
					<a href="javascript:void(0);" style={{cursor:limit_status?'default':'pointer'}} onClick={this.tabchange.bind(this,'limit_status')}>限制卡</a>
					<div style={{display:common_status?'block':'none'}}>1</div>
					<div style={{display:limit_status?'block':'none'}}>2</div>
				</fieldset>
			</form>
		</div>
		)
	}
})
module.exports = ApprovalDialog;