function NewGeneLinkDialog(pageBlock, organisms, siteUrl) {
	this.block = pageBlock;
	this.submitUrl = siteUrl + 'api/geneLinks';
	
	this.dialog = $('<div />', {
		'class' : 'tagging-dialog',
	});
	
	this.block = pageBlock;
	
	this.title = $('<div />', {
		'class' : 'tagging-dialog-title',
		'text' : 'Add New Gene Link'
	});
	
	this.closeButton = $('<span />', {
		'class' : 'ui-icon ui-icon-circle-close close-button'
	});
	
	this.title.append(this.closeButton);
	
	this.contents = $('<div />', {
		'class' : 'tagging-dialog-contents'
	});
	
	this.table = $('<table />', {
		'class' : 'dialog-table'
	});
	
	this.contents.append(this.table);
	
	var geneNameContainer = $('<div />');
	
	this.geneName = $('<input />', {
		'type' : 'text'
	});
	
	var nameLabel = $('<span />', {
		'text' : 'Gene or Locus Tag',
		'style' : 'margin-right: 10px'
	});
	
	var geneUniqueNameContainer = $('<div />');
	
	this.geneUniqueName = $('<input />', {
		'type' : 'text'
	});
	
	var uniqueNameLabel = $('<span />', {
		'text' : 'Uniquename (optional)',
		'style' : 'margin-right: 10px'
	});
	
	geneNameContainer.append(nameLabel);
	geneNameContainer.append(this.geneName);
	this.contents.append(geneNameContainer);
	
	geneUniqueNameContainer.append(uniqueNameLabel);
	geneUniqueNameContainer.append(this.geneUniqueName);
	this.contents.append(geneUniqueNameContainer);
	
	var organismContainer = $('<div />');
	
	this.organism = $('<select />', {
		'type' : 'text'
	});
	
	var self = this;
	
	$.each(organisms, function(index, organism) {
		var option = $('<option />', {
			'text' : organism.commonName,
			'value' : organism.id
		});
		self.organism.append(option);
	});
	
	var organismLabel = $('<span />', {
		'text' : 'Organism',
		'style' : 'margin-right: 10px'
	});
	
	organismContainer.append(organismLabel);
	organismContainer.append(this.organism);
	this.contents.append(organismContainer);
	
	this.finalizeUI = $('<div />', {
		'class' : 'tagging-dialog-contents'
	});
	
	this.finalizeBody = $('<div />');
	
	this.submitGeneLinkButton = $('<button />', {
		'class' : 'tagging-button',
		'text': 'Add'
	});
	
	this.cancelButton = $('<button />', {
		'class' : 'tagging-button',
		'text': 'Cancel',
		'style' : 'margin-left: 10px'
	});
	
	this.finalizeBody.append(this.submitGeneLinkButton);
	this.finalizeBody.append(this.cancelButton);
	this.finalizeBody.css('border-top', '1px solid #CCC');
	this.finalizeBody.css('padding-top', '5px');
	
	this.finalizeUI.append(this.finalizeBody);
	
	this.dialog.append(this.title);
	this.dialog.append(this.contents);
	this.dialog.append(this.finalizeUI);
	
	this.submitCallback = null;
	
	this.submitGeneLinkButton.on('click', Util.scopeCallback(this, this.onSubmit));
	this.cancelButton.on('click', Util.scopeCallback(this, this.onCancel));
	this.closeButton.on('click', Util.scopeCallback(this, this.onCancel));
	
	$('body').append(this.dialog);
};

NewGeneLinkDialog.prototype.onSubmit = function() {
	var geneName = $.trim(this.geneName.val());
	var uniqueName = $.trim(this.geneUniqueName.val());
	var organismId = this.organism.val();
	var tagId = this.table.find('input:radio[name=tag]:checked').val();
	if (geneName && organismId && tagId) {
		var self = this;
		
		$.ajax({
			url : this.submitUrl,
			type : 'POST',
			data : {
				name : geneName,
				organismId : organismId,
				tagId: tagId,
				uniqueName: uniqueName
			},
			dataType : 'json',
			success : function(data, textStatus, jqXHR) {
				data.feature.organismId = organismId;
				this.tags[tagId].addGeneLink(data.id, data.feature);
				this.hide();
			},
			error : function(jqXHR, textStatus, errorThrown) {
				var errorMessage = $.parseJSON(jqXHR.responseText).message;
				alert(errorMessage);
			}
		});
	}
};

NewGeneLinkDialog.prototype.onCancel = function() {
	this.hide();
};

NewGeneLinkDialog.prototype.hide = function() {
	this.block.hide();
	this.dialog.hide();
};

NewGeneLinkDialog.prototype.show = function(tagBoard) {
	var tags = tagBoard.getSelectedTags();
	if ($.isEmptyObject(tags)) {
		var currentTagGroups = tagBoard.getCurrentTagGroups();
		if ($.isEmptyObject(currentTagGroups)) {
			alert("Please select tags by clicking on them or a current tag group.");
		}
		else {
			tags = {};
			$.each(currentTagGroups, function(key, group) {
				$.extend(tags, group.getTags());
			});
		}
	}
	
	if (!$.isEmptyObject(tags)) {
		this.table.empty();
		var tbody = $('<tbody />');
		
		var index = 0;
		$.each(tags, function(id, tag) {
			var newRow = $('<tr />');
			var text = '';
			if (index == 0) {
				text = 'Select a Tag:';
			}
			
			var labelCell = $('<td />', {
				'text' : text
			});
			
			var tagCell = $('<td />');
			
			tagCell.append($('<input />', {
				'value' : tag.getId(),
				'type' : 'radio',
				'name' : 'tag',
				'checked' : index == 0
			}));
			
			tagCell.append($('<span />', {
				'text' : tag.getDescription()
			}));
			
			newRow.append(labelCell);
			newRow.append(tagCell);
			tbody.append(newRow);
			index++;
		});
	}
	
	this.tags = tags;
	
	this.table.append(tbody);
	this.block.show();
	this.dialog.show();
};