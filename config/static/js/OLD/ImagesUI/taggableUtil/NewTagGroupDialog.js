function NewTagGroupDialog(pageBlock) {
	this.block = pageBlock;
	this.dialog = $('<div />', {
		'class' : 'tagging-dialog',
	});
	
	this.block = pageBlock;
	
	this.title = $('<div />', {
		'class' : 'tagging-dialog-title',
		'text' : 'Add New Tag Group'
	});
	
	this.closeButton = $('<span />', {
		'class' : 'ui-icon ui-icon-circle-close close-button'
	});
	
	this.title.append(this.closeButton);
	
	this.contents = $('<div />', {
		'class' : 'tagging-dialog-contents'
	});
	
	this.name = $('<input />', {
		'type' : 'text'
	});
	
	var nameLabel = $('<span />', {
		'text' : 'Name',
		'style' : 'margin-right: 10px'
	});
	
	this.contents.append(nameLabel);
	this.contents.append(this.name);
	
	this.finalizeUI = $('<div />', {
		'class' : 'tagging-dialog-contents'
	});
	
	this.finalizeBody = $('<div />');
	
	this.submitTagGroupButton = $('<button />', {
		'class' : 'tagging-button',
		'text': 'Add'
	});
	
	this.cancelButton = $('<button />', {
		'class' : 'tagging-button',
		'text': 'Cancel',
		'style' : 'margin-left: 10px'
	});
	
	this.finalizeBody.append(this.submitTagGroupButton);
	this.finalizeBody.append(this.cancelButton);
	this.finalizeBody.css('border-top', '1px solid #CCC');
	this.finalizeBody.css('padding-top', '5px');
	
	this.finalizeUI.append(this.finalizeBody);
	
	
	this.dialog.append(this.title);
	this.dialog.append(this.contents);
	this.dialog.append(this.finalizeUI);
	
	this.submitCallback = null;
	
	this.submitTagGroupButton.on('click', Util.scopeCallback(this, this.onSubmit));
	this.cancelButton.on('click', Util.scopeCallback(this, this.onCancel));
	this.closeButton.on('click', Util.scopeCallback(this, this.onCancel));
	
	$('body').append(this.dialog);
};

NewTagGroupDialog.prototype.setTagBoard = function(tagBoard) {
	this.tagBoard = tagBoard;
};

NewTagGroupDialog.prototype.addSubmitCallback = function(callback) {
	this.submitCallback = callback;
};

NewTagGroupDialog.prototype.onSubmit = function() {
	var name = $.trim(this.name.val());
	if (name && this.tagBoard) {
		var self = this;
		this.tagBoard.addNewTagGroup(name, 
			function() {
				self.hide();
				if (self.submitCallback != null) {
					self.submitCallback(self.tagBoard);
					self.submitCallback = null;
				}
			},
			function(errorMessage) {
				self.hide();
				alert(errorMessage);
			});
	}
};

NewTagGroupDialog.prototype.onCancel = function() {
	this.hide();
};

NewTagGroupDialog.prototype.hide = function() {
	this.block.hide();
	this.dialog.hide();
};

NewTagGroupDialog.prototype.show = function() {
	this.block.show();
	this.dialog.show();
};