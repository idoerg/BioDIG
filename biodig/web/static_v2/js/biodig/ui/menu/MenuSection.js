var deps = [
    'jquery', 'biodig/ui/menu/MenuItem', 'lib/util',
    'text!biodig/tmpl/menu-section.html', 'jquery_ui'
];

define(deps, function($, MenuItem, MenuSectionTmpl) {

    var MenuSectionTemplate = _.template(MenuSectionTmpl);

    /**
        Constructor of a MenuSection.

        @param text: The text for the MenuSection.
        @param icon: Optional. Either the class for a span which represents an icon
                     or img[src] indicating the icon is an image with the source in
                     the brackets.
    **/
    function MenuSection(text, icon) {
        this.menuItems = [];
        this.menuDict = {};

        var iconType;
        icon = $.trim(icon);
        if (icon.substring(0, 3) == "img") {
            iconType = "img"; // icon is an img
            icon = icon.substring(4, icon.length - 1);
        }
        else {
            iconType = "span"; // icon is simply the class of a span
        }

        this.$ui = $(MenuSectionTemplate.call({ text: text, icon: icon, iconType: iconType }));

        this.$menu = this.$ui.find('.toolbar-menu');
    };

    MenuSection.prototype.item = function(key, text, icon) {
        if (!this.menuDict[key] && text) {
            this.addItem(key, MenuItem.create(text, icon));
        }
        return this.menuDict[key];
    };

    MenuSection.prototype.addItem = function(key, item) {
        this.menuItems.push(item);
        this.menuDict[key] = item;
        this.$menu.append(item.ui());
    };

    MenuSection.prototype.mouseover = function() {
        this.$menu.show();
        this.$ui.off('mouseover');
        this.$ui.on('mouseout', util.scope(this, this.mouseout));
    };

    MenuSection.prototype.mouseout = function() {
        this.$menu.hide();
        this.$ui.off('mouseout');
        this.$ui.on('mouseover', util.scope(this, this.mouseover));
    };

    MenuSection.prototype.ui = function() {
        this.$menu.menu();
        this.$ui.on('mouseover', util.scope(this, this.mouseover));
        return this.$ui;
    };

    return {
        create: function(text, icon) {
            return new MenuSection(text, icon);
        }
    }
});
