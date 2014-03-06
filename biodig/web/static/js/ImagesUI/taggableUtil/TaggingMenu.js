function TaggingMenu(id, imagesUrl) {
	this.colors = [
      	{ colorRGB : 'rgb(255, 0, 0)'},
   		{ colorRGB : 'rgb(0, 0, 255)'},
   		{ colorRGB : 'rgb(0, 255, 255)'},
   		{ colorRGB : 'rgb(0, 98, 0)'},
   		{ colorRGB : 'rgb(0, 255, 0)'},
   		{ colorRGB : 'rgb(255, 255, 0)'},
   		{ colorRGB : 'rgb(192, 192, 192)'},
   		{ colorRGB : 'rgb(0, 0, 0)'}
   	];
	
	this.ui = $('<div />', {
		'class': 'tagging-menu-box'
	});
	
	this.title = $('<div />', {
		'class' : 'tagging-menu-box-title',
		'text' : 'Tagging Tools'
	});
	
	this.colorsUI = $('<div />', {
		'class' : 'tagging-menu-box-section'
	});
	
	this.colorsUI.append($('<div />', {
		'class' : 'tagging-menu-box-section-title',
		'text' : 'Colors'
	}));
	
	this.colorBody = $('<div />', {
		'class' : 'tagging-menu-box-section-body'
	});
	
	this.colorsUI.append(this.colorBody);
	
	var currentParent = null;
	this.colorButtons = [];
	
	for (var i = 0; i < this.colors.length; i++) {
		if (i % 4 == 0) {
			currentParent = $('<div />', {
				'class' : 'tagging-menu-color-container'
			});
			this.colorBody.append(currentParent);
		}
		var color = this.colors[i];
		var colorButton = $('<button />', {
			'class' : "change-color toolbar-item",
			'style' : 'background-color: ' + color.colorRGB
		});
		currentParent.append(colorButton);
		this.colorButtons.push(colorButton);
	}
	
	this.drawStyleUI = $('<div />', {
		'class' : 'tagging-menu-box-section'
	});
	
	this.drawStyleUI.append($('<div />', {
		'class' : 'tagging-menu-box-section-title',
		'text' : 'Draw Style'
	}));
	
	this.drawStyleBody = $('<div />', {
		'class' : 'tagging-menu-box-section-body'
	});
	
	this.drawRectButton = $('<button />', {
		'id' : id + '-draw-rect',
		'class' : 'draw-rect tagging-button toolbar-item'
	});
	
	this.drawRectButton.append($('<img />', {
		'height' : '20px',
		'src' : imagesUrl + 'rectButtonIcon.png'
	}));
	
	this.drawPolyButton = $('<button />', {
		'id' : id + '-draw-poly',
		'class' : 'draw-poly tagging-button toolbar-item',
		'style' : 'margin-left: 30px'
	});
	
	this.drawPolyButton.append($('<img />', {
		'height' : '20px',
		'src' : imagesUrl + 'polygonButtonIcon.png'
	}));
	
	this.drawStyleBody.append(this.drawRectButton);
	this.drawStyleBody.append(this.drawPolyButton);
	
	this.drawStyleUI.append(this.drawStyleBody);
	
	this.finalizeUI = $('<div />', {
		'class' : 'tagging-menu-box-section'
	});
	
	this.finalizeBody = $('<div />', {
		'class' : 'tagging-menu-box-section-body'
	});
	
	this.submitTagButton = $('<button />', {
		'class' : 'tagging-button',
		'text': 'Submit'
	});
	
	this.cancelButton = $('<button />', {
		'class' : 'tagging-button .tagging-button-last',
		'text': 'Cancel',
		'style' : 'margin-left: 10px'
	});
	
	this.finalizeBody.append(this.submitTagButton);
	this.finalizeBody.append(this.cancelButton);
	this.finalizeBody.css('border-top', '1px solid #CCC');
	this.finalizeBody.css('padding-top', '5px');
	
	this.finalizeUI.append(this.finalizeBody);
	
	this.ui.append(this.title);
	this.ui.append(this.colorsUI);
	this.ui.append(this.drawStyleUI);
	this.ui.append(this.finalizeUI);
	
	this.ui.draggable();
};

TaggingMenu.prototype.show = function() {
	this.ui.show();
};

TaggingMenu.prototype.hide = function() {
	this.ui.hide();
};

TaggingMenu.prototype.onColorClick = function(callback) {
	this.colorBody.find('.change-color').on('click', callback);
};

TaggingMenu.prototype.onCancelClick = function(callback) {
	var self = this;
	this.cancelButton.on('click', function() {
		callback();
		self.hide();
	});
};

TaggingMenu.prototype.onRectClick = function(callback) {
	this.drawRectButton.on('click', callback);
};

TaggingMenu.prototype.onPolyClick = function(callback) {
	this.drawPolyButton.on('click', callback);
};

TaggingMenu.prototype.onSubmitClick = function(callback) {
	this.submitTagButton.on('click', callback);
};

TaggingMenu.prototype.getUI = function() {
	return this.ui;
};

