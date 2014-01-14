function MenuSection(text, icon) {
	this.ui = $('<div />', {
		'class' : 'toolbar-section-container'
	});
	
	this.section = $('<div />', {
		'class' : 'toolbar-section'
	});
	
	this.icon = $('<img />', {
		'class' : 'toolbar-section-icon',
		'src'   : icon 
	});
	
	this.text = $('<span />', {
		'class' : 'toolbar-section-text',
		'text'  : text
	});
	
	this.section.append(this.icon);
	this.section.append(this.text);
	this.menu = $('<ul />', {
		'class' : 'toolbar-menu'
	});
	
	this.menuItems = [];
	this.menuDict = {};
	
	this.ui.append(this.section);
	this.ui.append(this.menu);
};

MenuSection.prototype.getMenuItem = function(key) {
	return this.menuDict[key];
};

MenuSection.prototype.addMenuItem = function(name, text, icon, isImage) {
	var menuItem = new MenuItem(text, icon, isImage);
	this.menuItems.push(menuItem);
	this.menuDict[name] = menuItem;
	this.menu.append(menuItem.getUI());
};

MenuSection.prototype.onMouseover = function() {
	this.menu.show();
	this.ui.off('mouseover');
	this.ui.on('mouseout', Util.scopeCallback(this, this.onMouseout));
};

MenuSection.prototype.onMouseout = function() {
	this.menu.hide();
	this.ui.off('mouseout');
	this.ui.on('mouseover', Util.scopeCallback(this, this.onMouseover));
};

MenuSection.prototype.getUI = function() {
	this.menu.menu();
	this.ui.on('mouseover', Util.scopeCallback(this, this.onMouseover));
	return this.ui;
};