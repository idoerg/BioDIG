var deps = [
    'jquery', 'underscore', 'biodig/ui/workbench/MyImages', //'biodig/ui/workbench/RecentlyViewedImages',
    'text!biodig/tmpl/workbench/toolbar.html'
];

define(deps, function($, _, MyImages, ToolbarTmpl) {

    var ToolbarTemplate = _.template(ToolbarTmpl);

    function Toolbar(selector, user) {
        this.$container = $(selector);
        this.$el = $(ToolbarTemplate());

        this.$container.append(this.$el);
        this.menus = {};

        this.add(MyImages.create(user));
        //this.add(RecentlyViewedImages.create());
    }

    Toolbar.prototype.add = function(menu) {
        this.$el.append(menu.view());
        this.menus[menu.name()] = menu;
    };

    Toolbar.prototype.get = function(name) {
        return this.menus[name];
    };

    return {
        create: function(selector, user) {
            return new Toolbar(selector, user);
        }
    }
});
