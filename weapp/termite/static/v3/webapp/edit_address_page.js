
/**
 * Backbone View in Mobile
 */
W.page.EditAddressPage = W.page.InputablePage.extend({
    events: _.extend({
        'click .xa-submit': 'onClickSubmitButton',
        'click .xa-delete':'onClickDeleteButton'
    }, W.page.InputablePage.prototype.events),

    /**
     * onClickSubmitButton: 点击“提交”按钮的响应函数
     */
    onClickSubmitButton: function(event) {
        var $form = $('form');
        if (W.validate($form)) {
            $('.xa-submit').attr('disabled','disabled');

            var args = $form.serializeObject();
            var ship_info = deepCopyJSON(args);
            var banned_address = ["海淀科技大厦12层","海淀科技大厦1201", "海淀科技大厦12层微众", "海淀科技大厦7层", "海淀科技大厦1202",
                "海淀科技大厦1203", "海淀科技大厦1204", "海淀科技大厦1205", "海淀科技大厦1206", "海淀科技大厦1207", "海淀科技大厦1208",
                "海淀科技大厦1209", "海淀科技大厦1210", "泰兴大厦301", "泰兴大厦三层301", "泰兴大厦三层微众", "泰兴大厦3层301", "海淀科技大厦十二层", "海淀科技大厦七层"];
            for (var i=0,len=banned_address.length;i<len;i++){
                if(ship_info.ship_address.indexOf(banned_address[i])>=0){
                    $('.xa-submit').removeAttr('disabled');
                    $('body').alert({
                            isShow: true,
                            isSlide: true,
                            info: '该收货地址不可用',
                            speed: 2000
                    });
                    return;
                }
            }
            ship_info['area_str'] = $('.xa-openSelect').text();

            W.getApi().call({
                app: 'webapp',
                api: 'project_api/call',
                method: 'post',
                args: _.extend(args, {
                    woid: W.webappOwnerId,
                    module: 'mall',
                    target_api: 'address/save'
                }),
                success: function(data) {
                    var ship_id = data['ship_id'];
                    ship_info['ship_id'] = ship_id;
                    ship_info['is_selected'] = true;
                    var ship_infos;
                    if(sessionStorage.ship_infos){
                        ship_infos = JSON.parse(sessionStorage.ship_infos);

                    }
                    else{
                        ship_infos = JSON.constructor();
                    }

                    for(var i in ship_infos){
                        if(i!=ship_id){
                            ship_infos[i].is_selected = false;

                        }
                    }
                    ship_infos[ship_id] = ship_info;

                    sessionStorage.ship_infos = JSON.stringify(ship_infos);


                    if (data['msg'] != null) {
                        $('body').alert({
                            isShow: true,
                            speed: 2000,
                            isSlide: true,
                            info: data['msg']
                        })
                    } else {
                        var mallShipfromUrl = sessionStorage.mallShipfromUrl;
                        sessionStorage.removeItem('mallShipfromUrl');
                        if(mallShipfromUrl){
                            // 返回订单
                            window.location.href = mallShipfromUrl;
                        }else{
                            // 返回地址列表
                            window.location.href = document.referrer;
                        }
                    }
                },
                error: function(resp) {
                    $('.xa-submit').removeAttr('disabled');
                    var errMsg = '保存失败';
                    if (resp.errMsg) {
                        errMsg = resp.errMsg;
                    } else if (resp.data && resp.data['msg']) {
                        errMsg = resp.data['msg']
                    }

                    $('body').alert({
                        isShow: true,
                        isSlide: true,
                        info: errMsg,
                        speed: 2000
                    });
                }
            });
        } else {
            
        }
    },


    /**
     * onClickDeleteButton: 点击“删除”按钮的响应函数
     */
    onClickDeleteButton: function(event){
        var ship_id = getParam('id');
        W.getApi().call({
                app: 'webapp',
                api: 'project_api/call',
                method: 'post',
                args: {
                    woid: W.webappOwnerId,
                    module: 'mall',
                    target_api: 'address/delete',
                    id: ship_id
                },
                success: function(data) {
                    var selected_id=data.selected_id;

                    var ship_infos = JSON.parse(sessionStorage.ship_infos);
                    delete ship_infos[ship_id];
                    if(selected_id){
                        ship_infos[selected_id]['is_selected'] = true;
                    }
                    sessionStorage.ship_infos = JSON.stringify(ship_infos);
                    window.location.href = './?woid=' + getWoid()+ '&module=mall&model=address&action=list' + addFmt();

                },
                error: function(resp) {
                    var errMsg = '删除失败';
                    if (resp.errMsg) {
                        errMsg = resp.errMsg;
                    } else if (resp.data && resp.data['msg']) {
                        errMsg = resp.data['msg']
                    }

                    $('body').alert({
                        isShow: true,
                        isSlide: true,
                        info: errMsg,
                        speed: 2000
                    });
                }
            });



    }
});
