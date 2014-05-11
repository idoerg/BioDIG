function MenuItem(text, icon, isImage) {
    this.ui = $('<li />', {
        'class' : 'toolbar-menu-item'
    });
    
    this.text = $('<span />', {
        'class' : 'toolbar-menu-text',
        'text'   : text
    });
    
    if (icon) {
        if (isImage) {
            this.icon = $('<img />', {
                'class' : 'toolbar-menu-icon',
                'src'   : icon
            });
        }
        else {
            this.icon = $('<span />', {
                'class' : 'toolbar-menu-icon ' + icon,
            });
        }
        
        this.ui.append(this.icon);
    }
    
    this.ui.append(this.text);
};

MenuItem.prototype.onClick = function(callback) {
    $(this.ui).click(callback);
};

MenuItem.prototype.getUI = function() {
    return this.ui;
};