define(['biodig/ui/menu/MenuSection'], function(MenuSection) {
    function Menu(toolbar) {
        this.menuBar = toolbar;
        this.sections = {};
    }

    Menu.prototype.section = function(key, text, icon) {
        if (!this.sections[key] && text) {
            this.addSection(key, MenuSection.create(text, icon));
        }
        return this.sections[key];
    };

    Menu.prototype.addSection = function(key, section) {
        this.sections[key] = section;
        this.menuBar.append(section.ui());
    };

    return {
        create: function(toolbar) {
            return new Menu(toolbar);
        }
    }
});
