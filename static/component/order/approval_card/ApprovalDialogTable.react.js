/**
 * Copyright(c) 2012-2016 weizoom
 */
"use strict";

var debug = require('debug')('m:outline.datas:CommentDialog');
var React = require('react');
var ReactDOM = require('react-dom');
var Action = require('.././rule_order/Action');
var Reactman = require('reactman');



var CardTable = React.createClass({
	handleChoice:function(event) {
		var newState = {};
		newState['id'] = event.target.getAttribute('data-cardrule-id');
		newState['name'] = event.target.getAttribute('data-cardrule-name');
		newState['countlimit'] = event.target.getAttribute('data-cardrule-countlimit');
		var is_cancel = event.target.getAttribute('data-cancel')
		if (is_cancel) {
			this.setState({id:''});
		} else {
			this.setState(newState);
		}
		
	},
	onClickShops: function(event){
		var ruleId = parseInt(event.target.getAttribute('data-rule-id'));
		var shop_limit_list = this.refs.table.getData(ruleId).shop_limit_list;
		var node_strings = '';
		for (var i in shop_limit_list){
			node_strings +='<div class="fl">'+shop_limit_list[i]+'</div>'
		}

		Reactman.PageAction.showPopover({
			target: event.target,
			content: node_strings
		});
	},
	rowFormatter: function(field, value, data) {
		if (field=='action') {
			if (this.state!=null) {
				if (this.state.id==data.id) {
					return (
					<a className="btn btn-link btn-xs mt5" onClick={this.handleChoice} data-cardrule-id={data.id} data-cancel='true'>已选择</a>
					)
				} else {
					return (
					<a className="btn btn-link btn-xs mt5" onClick={this.handleChoice} data-cardrule-id={data.id} data-cardrule-name={data.name} data-cardrule-countlimit={data.storage_count} >选择</a>
					)
				}
			} else {
				return (
				<a className="btn btn-link btn-xs mt5" onClick={this.handleChoice} data-cardrule-id={data.id} data-cardrule-name={data.name} data-cardrule-countlimit={data.storage_count}>选择</a>
				)
			}
			
		} else if (field=='shop_limit_list') {
			if (value.length >0){
				return (
					<a className="btn btn-success" href='javascript:void(0);' onClick={this.onClickShops} data-rule-id={data.id}>查看专属商家</a>
				)
			}
		}else {
			return value;
		}
	},
	render: function() {
		var cardruletype = this.props.cardruletype;
		var cardrulesResource= {
			resource: 'order.approval_card',
			data: {
				cardruletype:cardruletype,
				count_per_page:6,
				page:1
			}
		};
		return (
			<Reactman.TablePanel>
				<Reactman.TableActionBar></Reactman.TableActionBar>
				<Reactman.Table resource={cardrulesResource} formatter={this.rowFormatter} pagination={true} countPerPage={6} ref="table">
					<Reactman.TableColumn name="卡名称" field="name" width="120px" />
					<Reactman.TableColumn name="面值" field="money" />
					<Reactman.TableColumn name="库存" field="storage_count" width="120px"/>
					<Reactman.TableColumn name="卡类型" field="card_kind" width="80px" />
					<Reactman.TableColumn name="使用限制" field="valid_restrictions" width="80px" />
					<Reactman.TableColumn name="专属商家" field="shop_limit_list" width="80px" />
					<Reactman.TableColumn name="卡号区间" field="card_range" />
					<Reactman.TableColumn name="操作" field="action" width="80px" />
				</Reactman.Table>
			</Reactman.TablePanel>
		);
	}
});

module.exports = CardTable;