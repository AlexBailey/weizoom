$(document).ready(function() {
    W.sharePageTitle = {% if share_page_title %}"{{ share_page_title }}"{% else %}"{{ page_title }}"{% endif %};
    W.sharePageDesc = {% if share_page_desc %}"{{ share_page_desc }}"{% else %}"{{ page_title }}"{% endif %};
    W.sharePageImg = {% if share_img_url %}"{{ share_img_url }}"{% else %}"{{ request.share_img_url }}"{% endif %};

    if(W.sharePageImg.substr(0,7)!="http://" && W.sharePageImg.substr(0,8)!="https://")
    W.sharePageImg = "http://"+window.location.host+W.sharePageImg;

    var link = window.location.href;
    if (link.indexOf('fmt') === -1){
        if (link.indexOf('&') === -1){
            link = link +"?fmt="+W.curRequestMemberToken;
        } else {
            link = link +"&fmt="+W.curRequestMemberToken;
        }
    }
    alert(link)
    $('a').highlight();
    FastClick.attach(document.body);
    var hm = document.createElement("script");
    hm.src = "/weixin/js/config/?path="+encodeURIComponent(location.href);
    var s = document.getElementsByTagName("script")[0]; 
    s.parentNode.insertBefore(hm, s);
    /*
     * 微信分享按钮事件
     * 注意：
     * 1. 所有的JS接口只能在公众号绑定的域名下调用，公众号开发者需要先登录微信公众平台进入“公众号设置”的“功能设置”里填写“JS接口安全域名”。
     * 2. 如果发现在 Android 不能分享自定义内容，请到官网下载最新的包覆盖安装，Android 自定义分享接口需升级至 6.0.2.58 版本及以上。
     * 3. 完整 JS-SDK 文档地址：http://mp.weixin.qq.com/wiki/7/aaa137b55fb2e0456bf8dd9148dd613f.html
     *
     * 功能说明
     * 1、分享给微信好友
     * 2、分享到微信朋友圈
     * 3、分享到腾讯微博
     */
    W.wxShareData = {
        "imgUrl" : W.sharePageImg,
        "link" : link,
        "desc" : W.sharePageDesc,
        "title" : W.sharePageTitle,
        // 点击分享按钮
        trigger: function (res) {
           //alert('用户点击分享按钮'+res);
        },
        // 分享成功
        success : function(res) {
           //alert('success'+res);
            W.getApi().call({
                app: 'webapp',
                api: 'project_api/call',
                method: 'post',
                args: _.extend({
                    woid: W.webappOwnerId,
                    project_id: W.projectId,
                    module: 'user_center',
                    target_api: 'shared_url/record',
                    link: link,
                    title:W.sharePageTitle
                }),
                success: function(data) {
                    alert("分享链接成功")
                },
                error: function(data){
                    alert("分享链接失败")
                }
            });
        }
    };
    wx.ready(function () {
      alert('-----------in weapp jssdk')
      // 1 判断当前版本是否支持指定 JS 接口，支持批量判断
      wx.checkJsApi({
        jsApiList: [
          'onMenuShareAppMessage',
          'onMenuShareTimeline',
          'onMenuShareQQ',
          'previewImage',
          'hideOptionMenu',
          'showOptionMenu',
          'previewImage'
        ],
        success: function (res) {
          if(!W.wxShareData)
            return;
          res = res.checkResult;
          if(res.onMenuShareAppMessage)
            wx.onMenuShareAppMessage(W.wxShareData);
          if(res.onMenuShareTimeline)
            wx.onMenuShareTimeline(W.wxShareData);
          if(res.onMenuShareQQ)
            wx.onMenuShareQQ(W.wxShareData);
          if(res.previewImage)
            W.ImagePreview(wx);
          if(res.hideOptionMenu && isHideWeixinOptionMenu)
            wx.hideOptionMenu();
          if(res.showOptionMenu && !isHideWeixinOptionMenu)
            wx.showOptionMenu()
        }
      });

      wx.previewImage({
        current: 'http://img5.douban.com/view/photo/photo/public/p1353993776.jpg',
        urls: [
          'http://img3.douban.com/view/photo/photo/public/p2152117150.jpg',
          'http://img5.douban.com/view/photo/photo/public/p1353993776.jpg',
          'http://img3.douban.com/view/photo/photo/public/p2152134700.jpg'
        ]});
    });

 })