/**
 * @class W.component.wepage.TextNav
 * 
 */
ensureNS('W.component.wepage');
W.component.wepage.NavbarFirstNav = W.component.Component.extend({
	type: 'wepage.navbar_firstnav',
	selectable: 'no',
	propertyViewTitle: '一级菜单',

	properties: [
        {
            group: '属性1',
            groupClass:'xui-propertyView-navbar-firstnav-property',
            groupName: '一级菜单',
            fields: [{
            	name: 'title',
            	type: 'text',
            	displayName: '标题',
                maxLength:5,
                validateIgnoreDefaultValue: true,
                isUserProperty: true,
                placeholder:'标题名',
            	default: '标题名'
            }, {
                name: 'target',
                type: 'select_link',
                displayName: '链接',
                isUserProperty: true,
                triggerButton: '从微站选择',
                default: ''
            }, {
                name: 'second_navs',
                type: 'second_navs',
                displayName: '',
                isUserProperty: true,
                default: ''
            }]
        }
    ],

    propertyChangeHandlers: {
        title: function($node, model, value, $propertyViewNode) {
            value = this.getDisplayValue(value, 'title');
            $node.find('.wa-inner-link').html(value);
        },
        target: function($node, model, value, $propertyViewNode) {
            xwarn(value);
            var $linkSelectFieldNode = $($propertyViewNode.find('.propertyGroup_property_linkSelectField'));
            if (value.length > 0) {
                var linkData = $.parseJSON(value);
                if (linkData.type === 'manualInput') {

                } else {
                    $linkSelectFieldNode.find('.xa-selected-title-box').show();
                    $linkSelectFieldNode.find('.xa-selectLink-url').val(linkData.data).attr('disabled','disabled');
                    $linkSelectFieldNode.find('.xa-selectLink-name').text(linkData.data_path);
                    $linkSelectFieldNode.find('.xa-link-menu').html('修改<span class="glyphicon glyphicon-menu-down"></span>');
                }
            }else{
                $linkSelectFieldNode.find('.xa-selected-title-box').hide();
                $linkSelectFieldNode.find('.xa-selectLink-url').val('').removeAttr('disabled');
                $linkSelectFieldNode.find('.xa-selectLink-name').text('');
                $linkSelectFieldNode.find('.xa-link-menu').html('从微站选择<span class="glyphicon glyphicon-menu-down"></span>');
            }
        },
        second_navs: function($node, model, value, $propertyViewNode) {
            // this.refresh($node, {resize:true});
            model.set('second_navs', $.parseJSON(value), {silent:true});
            var parentComponent = W.component.getComponent(this.pid);
            parentComponent.refresh($node, {resize:true});
        }
    },
    setLimitation: function(args) {
        xwarn('----- set limitation -----');
        xwarn(args);
        console.log(2323, this.name2field);
        this.name2field['title'].maxLength = args.titleMaxLength;
        // alert(this.name2field['title'].maxLength);
    }
});
