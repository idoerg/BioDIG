function SaveTagDialog(pageBlock) {
	this.dialog = $('<div />', {
		'class' : 'tagging-dialog',
	});
	
	this.block = pageBlock;
	
	this.title = $('<div />', {
		'class' : 'tagging-dialog-title',
		'text' : 'Submit Tag'
	});
	
	this.closeButton = $('<span />', {
		'class' : 'ui-icon ui-icon-circle-close close-button'
	});
	
	this.title.append(this.closeButton);
	
	this.contents = $('<div />', {
		'class' : 'tagging-dialog-contents'
	});
	
	this.table = $('<table />', {
		'class' : 'submit-tag-group-table'
	});
	
	this.nameUI = $('<div />');
	
	this.nameUI.append($('<span />', {
		'text' : 'Tag Name',
		'style' : 'margin-right: 10px; padding-left: 4px;'
	}));
	
	this.name = $('<input />', {
		'type' : 'text'
	});
	
	this.nameUI.append(this.name);
	
	this.contents.append(this.table);
	this.contents.append(this.nameUI);
	
	this.finalizeUI = $('<div />', {
		'class' : 'tagging-dialog-contents'
	});
	
	this.finalizeBody = $('<div />');
	
	this.submitTagButton = $('<button />', {
		'class' : 'tagging-menu-button',
		'text': 'Submit'
	});
	
	this.cancelButton = $('<button />', {
		'class' : 'tagging-menu-button',
		'text': 'Cancel',
		'style' : 'margin-left: 10px'
	});
	
	this.finalizeBody.append(this.submitTagButton);
	this.finalizeBody.append(this.cancelButton);
	this.finalizeBody.css('border-top', '1px solid #CCC');
	this.finalizeBody.css('padding-top', '5px');
	
	this.finalizeUI.append(this.finalizeBody);
	
	
	this.dialog.append(this.title);
	this.dialog.append(this.contents);
	this.dialog.append(this.finalizeUI);
	
	this.submitTagButton.on('click', Util.scopeCallback(this, this.onSubmit));
	this.cancelButton.on('click', Util.scopeCallback(this, this.hide));
	this.closeButton.on('click', Util.scopeCallback(this, this.hide));
	
	$('body').append(this.dialog);
};

SaveTagDialog.prototype.onSuccess = function() {
	alert("Success");
	this.hide();
};

SaveTagDialog.prototype.onError = function(errorMessage) {
	alert("Error: " + errorMessage);
	this.hide();
};

SaveTagDialog.prototype.onSubmit = function() {
	var description = $.trim(this.name.val());
	
	if (description) {		
		// adds the current drawn tag to the local tags object
		this.tagBoard.addTag(this.colorArr, this.tagPoints, description, 
			Util.scopeCallback(this, this.onSuccess), Util.scopeCallback(this, this.onError));
		// updates the tag board
		this.tagBoard.redraw();
	}
};

SaveTagDialog.prototype.hide = function() {
	this.dialog.hide();
	this.block.hide();
	this.name.val("");
};

SaveTagDialog.prototype.show = function(tagBoard, colorArr, tagPoints, newTagGroupDialog) {
	this.colorArr = colorArr;
	this.tagPoints = tagPoints;
	if (tagBoard.getTagGroups().length == 0) {
		var self = this;
		newTagGroupDialog.addSubmitCallback(function(newTagBoard) {
			self.showHelper(newTagBoard);
		});
		newTagGroupDialog.show();
	}
	else {
		this.showHelper(tagBoard);
	}
};

SaveTagDialog.prototype.showHelper = function(tagBoard) {
	this.block.show();
	this.table.empty();
	var tbody = $('<tbody />');
	var i = 0;
	var currentTagGroups = tagBoard.getCurrentTagGroups();
	for (key in currentTagGroups) {
		if (currentTagGroups.hasOwnProperty(key)) {
			var group = currentTagGroups[key];
			var newRow = $('<tr />');
			var text = ' ';
			if (i == 0) {
				text = 'Tag Groups:';
			}
			newRow.append($('<td />', {
				'text' : text
			}));
			newRow.append($('<td />', {
				'text' : group.getName(),
				'class' : 'tag-group-cell',
			}));
			tbody.append(newRow);
			i++;
		}
	}
	this.table.append(tbody);
	this.currentTagGroups = currentTagGroups;
	this.dialog.show();
	this.tagBoard = tagBoard;
};