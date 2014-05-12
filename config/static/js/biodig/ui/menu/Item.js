var deps = [
    'jquery', 'underscore', 'text!biodig/tmpl/menu/item.html'
];

define(deps, function($, _, ItemTmpl) {

    var ItemTemplate = _.template(ItemTmpl);

    /**
        Constructor of a Item.

        @param text: The text for the Item.
        @param icon: Optional. Either the class for a span which represents an icon
                     or img[src] indicating the icon is an image with the source in
                     the brackets.
    **/
    function Item(text, icon) {
        var iconType;
        icon = $.trim(icon);
        if (icon.substring(0, 3) == "img") {
            iconType = "img"; // icon is an img
            icon = icon.substring(4, icon.length - 1);
        }
        else {
            iconType = "span"; // icon is simply the class of a span
        }

        this.$ui = $(ItemTemplate({ 'text': text, 'icon': icon, 'iconType': iconType }));
    };

    Item.prototype.on = function(event, callback) {
        this.$ui.on(event, callback);
    };

    Item.prototype.off = function(event) {
        this.$ui.off(event);
    };

    Item.prototype.ui = function() {
        return this.$ui;
    };

    return {
        create: function(text, icon) {
            return new Item(text, icon);
        }
    }
})
