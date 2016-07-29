/**
 * wepage异步组件加载
 * author：liupeiyu
 */
(function() {
/**
 * AsyncComponentLoadView: 异步组件加载View
 */
var AsyncComponentLoadView = BackboneLite.View.extend({
    events: {
    },

    initialize: function(options) {
        var _this = this;
        this.$el = $(this.el);
        this.componentType = options.componentType;
        this.componentModel = options.componentModel;
        this.component = {
            component: {
                model: options.componentModel,
                type: options.componentType
            }
        };
        console.log('>>>>>>>>>> options: ', options, this.component);
        this.handlebarTmpl = $("#componentTemplates").html();
        this.template = Handlebars.compile(this.handlebarTmpl);
        _this.sendApi();
    },

    sendApi: function() {
        var _this = this;
        var product_ids = this.componentModel['items'];
        console.log('要加载的商品列表：', product_ids);
        // 尝试慢的问题
        var new_ids = [];
        if (product_ids.length > 10) {
            for (var i=0; i<10; i++) {
                new_ids.push(product_ids[i]);
            }
        }
        product_ids = new_ids;
        console.log('新的商品列表：', product_ids);
        /////////////////
        // 第一次渲染
        var orgHtml = _this.renderComponent(_this.component);
        _this.$el.html(orgHtml);
        W.getApi().call({
            app: 'webapp',
            api: 'project_api/call',
            method: 'get',
            args: {
                woid: W.webappOwnerId,
                module: 'mall',
                target_api: 'page_products/get',
                product_ids: product_ids
            },
            success: function(data) {
                // 根据商品数量填补component对象
                _this.component['component']['valid_product_count'] = data['products'].length;
                _this.component['component']['components'] = {};
                var $eleUl = _this.$el.find('ul');
                _this.renderSub($eleUl, data);
            },
            error: function(data) {

            }
        });
    },

    // 渲染
    renderComponent: function (component) {
        var html = this.template(component);
        return html;
    },

    // 渲染子标签
    renderSub: function($el, data) {
        var _this = this;
        console.log('>>>>>>>>> 异步接口: ', data);
        var product_ids = this.componentModel['items'];
        var products = data['products'];
        var sub_component_htmls = [];
        product_ids.forEach(function(product_id, idx) {
            var product = _.find(products, function(item){return item.id === product_id});
            // TODO: 将该html加入到sub_component中的html属性中
            var sub_component_html = _this.addSubComponetRender(product, idx);
            sub_component_htmls.push(sub_component_html);
        });

        // TODO: 使用handlebar-template 渲染 
        $el.html(sub_component_htmls.join(''));

    },

    addSubComponetRender: function(product, idx) {
        // TODO: 使用handlebar-template 渲染 
        var _this = this;
        var itemComponent = {
            component: {
                type: 'wepage.item',
                runtime_data: {product: product},
                model: { index: idx },
                parent_component: _this.component.component
            },
            product: product
        };
        var html = this.renderComponent(itemComponent);
        return html;
    }
});



$(function() {
    $('div[data-ui-role="async-component"]').each(function() {
        var $div = $(this);
        var componentType = $div.attr('data-type');
        var componentModel = $.parseJSON($div.attr('data-model') || '{}');
        var asyncComponent = new AsyncComponentLoadView({
            el: $div[0],
            componentType: componentType,
            componentModel: componentModel,
        });

        $div.data('view', asyncComponent);
    });
})

})(W);

