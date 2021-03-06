ensureNS('W.view.mall');
W.view.mall.OrderAction = Backbone.View.extend({

    initialize: function (options) {

        var _this = this;
        this.options = options;


        function pageReload(){
            if(_this.options.pageType == 'order_detail'){

                window.location.reload();
            }
            else{
                $('[data-ui-role="advanced-table"]').data('view').reload();
            }
        }

        // 根据mall_type,返回相应的orderId, 母订单还是子订单
        function getOrderId($el) {
            // 从页面中的数据中提取mall_type
            var allData = JSON.parse($('#origin-data').text()|| '{}');
            var mallType = allData.mall_type*1;

            var orderId = $el.parents('.xa-actions').data('order-id');
            if (mallType > 0) {
                orderId = $el.parents('.xa-actions').data('delivery-item-id');
            }
            return orderId;
        }

        // 发货
        $('body').delegate('.xa-order-delivery', 'click', function(event){
            event.stopPropagation();
            event.preventDefault();

            var $el = $(event.currentTarget);
            var orderId = getOrderId($el);

            var expressCompanyValue = $el.data('express-company-name');
            var expressNumber = $el.data('express-number');
            var leaderName = $el.data('leader-name');

            // 点击发货，不是点击修改
            if($el.data('is-update') !== true){
                expressCompanyValue = -1;
                expressNumber = '';
                leaderName = '';
            }
            var mallOrderShipView = W.getMallOrderShipView({
                width: 318,
                title: '发货',
                position:'top',
                isTitle: false,
                privateContainerClass:'xui-shipDropBox xa-shipDropBox'
            });
            mallOrderShipView.show({
                $action: $el,
                orderId: orderId,
                expressCompanyValue: expressCompanyValue,
                expressNumber: expressNumber,
                leaderName: leaderName
            })

        });

        // 取消
        $('body').delegate('.xa-cancelOrder', 'click', function(event) {
            event.stopPropagation();
            event.preventDefault();
            var orderId = $(event.currentTarget).parents('.xa-actions').data('order-id');
            W.requireConfirm({
                $el: $(this),
                viewName: 'order-list-confirm',
                width: 380,
                position: 'top',
                isTitle: false,
                privateContainerClass: 'xui-orderConfirmPop',
                msg: '确定取消订单？',
                confirm: function () {
                    var args = {
                        'order_id': orderId,
                        'action': 'cancel'
                    };
                    W.getApi().call({
                        method: 'post',
                        app: 'mall2',
                        resource: 'order',
                        args: args,
                        success: function (data) {
                            pageReload();
                        },
                        error: function () {
                            W.showHint('error', '订单状态发生改变，不能取消！');
                            pageReload();
                        }
                    })

                }
            })
        })


        //支付
        $('body').delegate('.xa-pay', 'click', function(event){
            event.stopPropagation();
            event.preventDefault();
            var orderId = $(event.currentTarget).parents('.xa-actions').data('order-id');
            W.dialog.showDialog('W.dialog.mall.UpdateOrderDialog', {
                orderId: orderId,
                success: function(data) {
                    var args = {
                        'order_id': orderId,
                        'action' : 'pay'
                    };
                    W.getApi().call({
                        method: 'post',
                        app: 'mall2',
                        resource: 'order',
                        args: args,
                        success: function(data) {
                            pageReload();
                        },
                        error: function() {
                        }
                    })
                }

            });

        });


    	// 修改价格
        $('body').delegate('.xa-update-price', 'click', function(event){
            event.stopPropagation();
		    event.preventDefault();
            var orderId = $(event.currentTarget).parents('.xa-actions').data('order-id');
            W.dialog.showDialog('W.dialog.mall.UpdateOrderDialog', {
                orderId: orderId,
                isUpdatePrice: true,
                success: function(data) {
                    console.log(data);
                    W.getApi().call({
                        app: 'mall2',
                        resource: 'order',
                        method: 'post',
                        args: {
                            order_id: orderId,
                            postage: data.postage,
                            final_price: data.finalPrice
                        },
                        success: function(data) {
                            pageReload();
                        },
                        error: function(resp) {

                        }
                    })
                }
            });

        });


        //标记完成
	    $('body').delegate('.xa-finish', 'click', function(event){
    		event.stopPropagation();
    		event.preventDefault();

            var $el = $(event.currentTarget);
            var orderId = getOrderId($el);

    		W.requireConfirm({
    			$el: $(this),
    			width:445,
    			position:'top',
    			isTitle: false,
    			privateContainerClass:'xui-orderConfirmPop',
    			msg:'确定将该订单标记为完成？',
    			confirm:function(){
    				var args = {
    					'order_id': orderId,
    					'action' : 'finish'
    				}
    				W.getApi().call({
    					method: 'post',
    					app: 'mall2',
    					resource: 'order',
    					args: args,
    					success: function(data) {
    						pageReload();
    					},
    					error: function() {
                        }
    				})

    			}
    		})
    	});


        //申请退款
        $('body').delegate('.xa-refund', 'click', function(event) {
            event.stopPropagation();
            event.preventDefault();

            // modified by Liugenbin
            var $el = $(event.currentTarget);
            var deliveryItemId = $el.parents('.xa-actions').data('delivery-item-id');
            var orderId = $el.parents('.xa-actions').data('order-id');
            var integralPerYuan = $el.parents('.xa-actions').data('integral-per-yuan');

            //
            var allData = JSON.parse($('#origin-data').text() || '{}');
            var mallType = allData.mall_type;

            console.log('申请退款orderID：%o, 商城类型：%o: ', orderId, mallType);

            if (mallType > 0) {
                // 根据商城类型，确定进入申请退款的"确认框"
                W.dialog.showDialog('W.dialog.mall.RefundOrderDialog', {
                    orderId: orderId,
                    deliveryItemId: deliveryItemId,
                    integralPerYuan: integralPerYuan,
                    isUpdatePrice: true,
                    success: function(data) {
                        console.log(data);
                    }
                });
            } else {
                // 申请退款确认框
                W.requireConfirm({
                    $el: $(this),
                    width:380,
                    position:'top',
                    isTitle: false,
                    privateContainerClass:'xui-orderConfirmPop',
                    msg:'确定申请退款？',
                    confirm:function(){
                        var args = {
                            'order_id': orderId,
                            'action' : 'return_pay'
                        }
                        W.getApi().call({
                            method: 'post',
                            app: 'mall2',
                            resource: 'order',
                            args: args,
                            success: function(data) {
                                pageReload();
                            },
                            error: function() {
                                }
                        })
                    }
                })
            }
        });


        //退款成功
        $('body').delegate('.xa-refundSuccess', 'click', function(event) {
            event.stopPropagation();
            event.preventDefault();
            var $el = $(event.currentTarget);
            var href = $el.attr('href');

            var $el = $(event.currentTarget);
            var orderId = $el.parents('.xa-actions').data('order-id');
            var deliveryItemId = $el.parents('.xa-actions').data('delivery-item-id');
            //
            var allData = JSON.parse($('#origin-data').text()||'{}');
            var mallType = allData.mall_type;

            if (mallType > 0) {
                W.requireConfirm({
                    $el: $(this),
                    width:442,
                    position:'top',
                    isTitle: false,
                    privateContainerClass:'xui-orderAuditConfirmPop',
                    msg:'请您与买家私下协商退款且退款成功后，再使用该功能哦!',
                    confirm:function(){
                        var args = {
                            'order_id': orderId,
                            'delivery_item_id': deliveryItemId
                        }
                        W.getApi().call({
                            app: 'mall2',
                            resource: 'refund_successful_sub_order',
                            args: args,
                            method: 'put',
                            success: function(data) {
                                pageReload();
                            },
                            error: function() {
                                }
                        })
                    }
                })
            } else {
                W.requireConfirm({
                    $el: $(this),
                    width:442,
                    position:'top',
                    isTitle: false,
                    privateContainerClass:'xui-orderAuditConfirmPop',
                    msg:'请您与买家私下协商退款且退款成功后，再使用该功能哦!',
                    confirm:function(){
                        var args = {
                            'order_id': orderId,
                            'action' : 'return_success'
                        }
                        W.getApi().call({
                            method: 'post',
                            app: 'mall2',
                            resource: 'order',
                            args: args,
                            success: function(data) {
                                pageReload();
                            },
                            error: function() {}
                        })
                    }
                })

            }
        });


        // 备注
        $('body').delegate('.xa-order-remark', 'click', function(event){
            var $el = $(event.currentTarget);
            var orderId = $el.data('order-id');
            var message = $el.data('order-value');

            var mallOrderRemarkView = W.getMallOrderRemarkView({
                width: 574,
                height: 62,
                title: '备注',
                position:'top',
                isTitle: false,
                privateContainerClass:'xui-remarkDropBox xa-remarkDropBox'

            });
            mallOrderRemarkView.show({
                $action: $el,
                orderId: orderId,
                message: message
            })

        });




    }
});



