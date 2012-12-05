function ChangeCurrentTagGroupsDialog(pageBlock) {
	this.block = pageBlock;
	this.dialog = $('<div />', {
		'class' : 'tagging-dialog',
	});
	
	this.block = pageBlock;
	
	this.title = $('<div />', {
		'class' : 'tagging-dialog-title',
		'text' : 'Change Current Tag Groups'
	});
	
	this.closeButton = $('<span />', {
		'class' : 'ui-icon ui-icon-circle-close close-button'
	});
	
	this.title.append(this.closeButton);
	
	this.contents = $('<div />', {
		'class' : 'tagging-dialog-contents'
	});
	
	this.contentTable = $('<table cellspacing="0" />');
	
	this.contents.append(this.contentTable);
	
	this.entry = $('<td />');
	
	this.entry.append($('<input />', {
		'type' : 'checkbox',
		'class' : 'current-tag-group-checkbox'
	}));
	
	this.entry.append($('<span />', {
		'text' : '',
		'class' : 'current-tag-group-text'
	}));
	
	this.finalizeUI = $('<div />', {
		'class' : 'tagging-dialog-contents'
	});
	
	this.finalizeBody = $('<div />');
	
	this.submitTagGroupButton = $('<button />', {
		'class' : 'tagging-menu-button',
		'text': 'Accept'
	});
	
	this.cancelButton = $('<button />', {
		'class' : 'tagging-menu-button',
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

ChangeCurrentTagGroupsDialog.prototype.setTagBoard = function(tagBoard) {
	this.tagBoard = tagBoard;
};

ChangeCurrentTagGroupsDialog.prototype.addSubmitCallback = function(callback) {
	this.submitCallback = callback;
};

ChangeCurrentTagGroupsDialog.prototype.onSubmit = function() {
	if (this.tagBoard) {
		var self = this;
		
		this.tagBoard.emptyCurrentTagGroups();
		
		var values = this.contentTable.find('input:checkbox:checked').map(function() {
			return this.value;
		}).get(); 
		
		var tagGroups = this.tagBoard.getTagGroups();
		
		var isLast;
		for (var i = 0; i < values.length; i++) {
			isLast = i == values.length - 1;
			this.tagBoard.addToCurrentTagGroups(tagGroups[values[i]], isLast);
		}
	}
	
	this.hide();
};

ChangeCurrentTagGroupsDialog.prototype.onCancel = function() {
	this.hide();
};

ChangeCurrentTagGroupsDialog.prototype.hide = function() {
	this.block.hide();
	this.dialog.hide();
};

ChangeCurrentTagGroupsDialog.prototype.show = function() {
	var tagGroups = this.tagBoard.getTagGroups();
	var currentTagGroups = this.tagBoard.getCurrentTagGroups();
	this.contentTable.empty();
	if (this.tagBoard && tagGroups.length > 0) {
		var contentRow = null;
		for (var i = 0; i < tagGroups.length; i++) {
			var tagGroup = tagGroups[i];
			var entryClone = this.entry.clone();
			
			var checkbox = entryClone.children('.current-tag-group-checkbox');
			var text = entryClone.children('.current-tag-group-text');
			checkbox.val(i);
			
			if (currentTagGroups[tagGroup.getKey()]) {
				checkbox.attr("checked", "checked");
			}
			
			text.text(tagGroup.getName());
			
			if (i % 2 == 0) {
				contentRow = $('<tr />');
				this.contentTable.append(contentRow);
			}
			
			contentRow.append(entryClone);
		}
		
		
		this.block.show();
		var self = this;
		$(window).on('resize', function() {
			self.center($(this).width(), $(this).height());
		});
		this.center($(window).width(), $(window).height());
		this.dialog.show();
	}
	else {
		alert("No tag groups");
	}
};

ChangeCurrentTagGroupsDialog.prototype.center = function(width, height) {
	if (height > this.dialog.height()) {
		this.dialog.css('top', (height - this.dialog.height())/2 + 'px');
	}
	else {
		this.dialog.css('top', '0px');
	}
	
	this.dialog.css('left', (width - this.dialog.width())/2 + 'px');
};