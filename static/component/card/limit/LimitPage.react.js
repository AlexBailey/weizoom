/**
 * Copyright(c) 2012-2016 weizoom
 */
"use strict";

var debug = require('debug')('m:card.create_limit:CreateLimitPage');
var React = require('react');
var ReactDOM = require('react-dom');

var Reactman = require('reactman');
var FormInput = Reactman.FormInput;
var FormSelect = Reactman.FormSelect;
var FormRadio = Reactman.FormRadio;
var FormSubmit = Reactman.FormSubmit;
var Dispatcher = Reactman.Dispatcher;
var Resource = Reactman.Resource;
var Shops = require('./Shops.react')
var Restriction = require('./Restriction.react');
var CheckedShops = require('./CheckedShops.react');

var Action = require('./Action');
var Store = require('./Store');
var ShopStore = require('./ShopStore');


var LimitPage = React.createClass({
	getInitialState: function() {
		Store.addListener(this.onChangeStore);
		ShopStore.addListener(this.getShops);
		return Store.getData();
	},
	onChangeStore: function() {
		this.setState(Store.getData());
	},
	getShops: function(){
		this.setState({
			"shops": ShopStore.getShops(),
			"shopsVisible": true
		})
	},

	onChange: function(value, event) {
		var property = event.target.getAttribute('name');
		if (property == "crad_kind"){
			if (value == "3"){
				Action.showShops();
			}else{
				this.setState({
					"shopsVisible": false
				});
			}
		}
		var data = Store.getData();
		data[property] = value;
		Action.addOrdinaryRuleInfo(data);
	},

	onSubmit: function() {
		Action.saveOrdinaryRule(Store.getData());
	},

	render:function(){
		console.log(this.state.shopsVisible,"pppppp")
		return (
		<div className="xui-outlineData-page xui-formPage">
			<form className="form-horizontal mt15">
				<fieldset>
					<div className="pl10 pt10 pb10"><span style={{fontWeight: 'bold'}}>基本信息</span>（<span style={{color: 'red'}}>*</span>表示必填）</div>
					<FormInput label="卡名称:" type="text" name="name" value={this.state.name} placeholder="1-20个字，中英文、数字特殊符合均可" onChange={this.onChange} />
					<FormInput label="卡段号:" type="text" name="weizoom_card_id_prefix" value={this.state.weizoom_card_id_prefix} validate="require-three-number" placeholder="请输入3位数组" onChange={this.onChange} />
					<FormSelect label="卡类型:" name="crad_kind" options={[{"value": "-1", "text": "请选择"},{"value": "2", "text": "条件卡"},{"value": "3", "text": "专属卡"}]} validate="require-select" onChange={this.onChange} />
					<Shops visible={this.state.shopsVisible} shops={this.state.shops} />
					<CheckedShops />
					<Restriction />
					<FormInput label="面值:" type="text" name="money" value={this.state.money} validate="require-price" placeholder="" onChange={this.onChange} />
					<FormInput label="数量:" type="text" name="count" value={this.state.count} validate="require-positive-int" placeholder="" onChange={this.onChange} />
					<FormInput label="备注:" type="text" name="remark" value={this.state.remark} placeholder="" onChange={this.onChange} />
				</fieldset>
				<fieldset>
					<FormSubmit onClick={this.onSubmit} />
				</fieldset>
			</form>
		</div>
		)
	}
})
module.exports = LimitPage;