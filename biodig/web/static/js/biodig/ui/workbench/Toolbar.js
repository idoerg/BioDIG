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

        //this.add(RecentlyViewedImages.create());
        var myImages = MyImages.create(user);
        this.add(myImages);
        $(myImages).on('render', function() {
            myImages.view().find('.scaled-image').on('load', function() {
                var $img = $(this);
                var $container = $(this).parent();
                var imgRatio = $img.width()/$img.height();
                var containerRatio = $container.width()/$container.height();
                if (imgRatio > containerRatio) {
                    $img.css('width', $container.width());
                    var topVal = ($container.height() - $img.height())/2;
                    $img.css('top', topVal);
                }
                else if (imgRatio < containerRatio) {
                    $img.css('height', $container.height());
                    var leftVal = ($container.width() - $img.width())/2;
                    $img.css('left', leftVal);
                }
            });
        });
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
