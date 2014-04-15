var deps = [
    'jquery', 'underscore', 'text!biodig/tmpl/menu-item.html'
];

define(deps, function($, _, MenuItemTmpl) {

    var MenuItemTemplate = _.template(MenuItemTmpl);

    /**
        Constructor of a MenuItem.

        @param text: The text for the MenuItem.
        @param icon: Optional. Either the class for a span which represents an icon
                     or img[src] indicating the icon is an image with the source in
                     the brackets.
    **/
    function MenuItem(text, icon) {
        var iconType;
        icon = $.trim(icon);
        if (icon.substring(0, 3) == "img") {
            iconType = "img"; // icon is an img
            icon = icon.substring(4, icon.length - 1);
        }
        else {
            iconType = "span"; // icon is simply the class of a span
        }

        this.$ui = $(MenuItemTemplate.call({ 'text': text, 'icon': icon, 'iconType': iconType }));
    };

    MenuItem.prototype.click = function(callback) {
        this.$ui.click(callback);
    };

    MenuItem.prototype.ui = function() {
        return this.$ui;
    };

    return {
        create: function(text, icon) {
            return new MenuItem(text, icon);
        }
    }
})
