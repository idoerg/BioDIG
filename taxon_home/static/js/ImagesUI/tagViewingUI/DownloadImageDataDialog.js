function DownloadImageDataDialog(pageBlock, image, imagesUrl) {
	this.block = pageBlock;
	this.image = image;
	this.imageKey = image.attr('id');
	this.downloadUrl = this.siteUrl + 'images/getImageMetadata';
	this.imagesUrl = imagesUrl;
	imagesUrl = imagesUrl.substring(0, imagesUrl.length - 1);
	this.staticUrl = imagesUrl.substring(0, imagesUrl.lastIndexOf('/') + 1);
	this.dialog = $('<div />', {
		'class' : 'tagging-dialog',
	});
	
	this.block = pageBlock;
	
	this.title = $('<div />', {
		'class' : 'tagging-dialog-title',
		'text' : 'Download Image Data'
	});
	
	this.closeButton = $('<span />', {
		'class' : 'ui-icon ui-icon-circle-close close-button'
	});
	
	this.title.append(this.closeButton);
	
	this.contents = $('<div />', {
		'class' : 'tagging-dialog-contents'
	});
	
	this.dataStoreContent = this.createDataStoreContent();
	this.includedDataContent = this.createIncludedDataContent();
	this.fileTypeContent = this.createFileTypeContent();
	
	this.contents.append(this.dataStoreContent);
	this.contents.append(this.includedDataContent);
	this.contents.append(this.fileTypeContent);
	
	this.finalizeUI = $('<div />', {
		'class' : 'tagging-dialog-contents'
	});
	
	this.finalizeBody = $('<div />');
	
	this.submitButton = $('<span />', {
		'class' : 'tagging-menu-button',
		'style' : 'display: inline-block',
		'text': 'Download'
	});
	
	this.cancelButton = $('<button />', {
		'class' : 'tagging-button',
		'text': 'Cancel',
		'style' : 'margin-left: 10px'
	});
	
	this.finalizeBody.append(this.submitButton);
	this.finalizeBody.append(this.cancelButton);
	this.finalizeBody.css('border-top', '1px solid #CCC');
	this.finalizeBody.css('padding-top', '5px');
	
	this.finalizeUI.append(this.finalizeBody);
	
	
	this.dialog.append(this.title);
	this.dialog.append(this.contents);
	this.dialog.append(this.finalizeUI)
	
	var self = this;
	
	this.cancelButton.on('click', Util.scopeCallback(this, this.onCancel));
	this.closeButton.on('click', Util.scopeCallback(this, this.onCancel));
	
	$('body').append(this.dialog);
	this.downloadified = false;
};

DownloadImageDataDialog.prototype.setTagBoard = function(tagBoard) {
	this.tagBoard = tagBoard;
};

DownloadImageDataDialog.prototype.onSubmit = function() {
	if (this.tagBoard) {
		var dataStore = $('input[type=radio]:checked', this.dataStoreContent).val();
		var fileType = $('input[type=radio]:checked', this.fileTypeContent).val();
		var includedData = {};
		$('input[type=checkbox]:checked', this.includedDataContent).each(function(index) {
			includedData[$(this).val()] = true;
		});
		
		var urlOfImage = includedData.hasOwnProperty('urlOfImage');
		var imageFile = includedData.hasOwnProperty('imageFile');
		var uploadDateUser = includedData.hasOwnProperty('uploadDateUser');
		var tagGroups = includedData.hasOwnProperty('tagGroups');
		var imageTags = includedData.hasOwnProperty('imageTags');
		var geneLinks = includedData.hasOwnProperty('geneLinks');
		var organisms = includedData.hasOwnProperty('organisms');
		var file = this.tagBoard.createFile(
			urlOfImage, imageFile, organisms, uploadDateUser, tagGroups, imageTags, 
			geneLinks, fileType == "xml", dataStore == "cached"
		);
		
		return file.getFile();
	}
	else {
		return '';
	}
};

DownloadImageDataDialog.prototype.onCancel = function() {
	this.hide();
};

DownloadImageDataDialog.prototype.hide = function() {
	this.block.hide();
	$(window).off('resize');
	this.dialog.hide();
};

DownloadImageDataDialog.prototype.show = function() {
	this.block.show();
	var self = this;
	$(window).on('resize', function() {
		self.center($(this).width(), $(this).height());
	});
	this.center($(window).width(), $(window).height());
	if (!this.downloadified) {
		Downloadify.create(this.submitButton[0], {
			filename: function() {
				return 'imageData.zip';
			},
			data: function(){ 
			    return self.onSubmit();
			},
			onComplete: function(){ 
			    alert('Your File Has Been Saved!'); 
			},
			onError: function(){ 
			    alert('Nothing to save. Please select some options in the dialog provided.'); 
			},
			dataType: 'base64',
			swf: this.staticUrl + 'js/downloadify/downloadify.swf', 
			downloadImage: this.imagesUrl + 'downloadButton.png',
			width: 95,
			height: 21,
			transparent: true,
			append: false
		});
		this.downloadified = true;
	}
	this.dialog.show();
};

DownloadImageDataDialog.prototype.createDataStoreContent = function() {
	var dataStore = $('<div />', {
		
	});
	
	var dataStoreTitle = $('<div />', {
		'text' : 'Data Store',
		'class' : 'download-image-data-dialog-content-section-title'
	});
	
	var dataStoreTableContainer = $('<div />', {
		'class' : 'download-image-data-dialog-content-section'
	});
	
	var dataStoreTable = $('<table cellspacing="0" />');
	
	var dataStoreRow = $('<tr />');
	
	dataStoreTable.append(dataStoreRow);
	dataStoreTableContainer.append(dataStoreTable);
	dataStore.append(dataStoreTitle);
	dataStore.append(dataStoreTableContainer);
	
	var cached = $('<td />');
	
	cached.append($('<input />', {
		'type' : 'radio',
		'name' : 'dataStore',
		'checked' : true,
		'value' : 'cached'
	}));
	
	cached.append($('<span />', {
		'text' : 'Cached (Includes Unsaved Data)',
		'class' : ''
	}));
	
	var fresh = $('<td />');
	
	fresh.append($('<input />', {
		'type' : 'radio',
		'name' : 'dataStore',
		'class' : '',
		'value' : 'fresh'
	}));
	
	fresh.append($('<span />', {
		'text' : 'Fresh Data (Saved in Database)',
		'class' : ''
	}));
	
	dataStoreRow.append(cached);
	dataStoreRow.append(fresh);
	
	return dataStore;
};

DownloadImageDataDialog.prototype.createIncludedDataContent = function() {
	var includedData = $('<div />', {
		
	});
	
	var includedDataTitle = $('<div />', {
		'text' : 'Include what type of data in the download?',
		'class' : 'download-image-data-dialog-content-section-title'
	});
	
	var includedDataTableContainer = $('<div />', {
		'class' : 'download-image-data-dialog-content-section'
	});
	
	var includedDataTable = $('<table cellspacing="0" />');
	
	var includedDataRowOne = $('<tr />');
	var includedDataRowTwo = $('<tr />');
	var includedDataRowThree = $('<tr />');
	var includedDataRowFour = $('<tr />');
	
	includedDataTable.append(includedDataRowOne);
	includedDataTable.append(includedDataRowTwo);
	includedDataTable.append(includedDataRowThree);
	includedDataTable.append(includedDataRowFour);
	includedDataTableContainer.append(includedDataTable);
	includedData.append(includedDataTitle);
	includedData.append(includedDataTableContainer);
	
	// First row of the table
	
	var urlOfImage = $('<td />');
	
	urlOfImage.append($('<input />', {
		'type' : 'checkbox',
		'value' : 'urlOfImage',
		'checked' : 'checked'
	}));
	
	urlOfImage.append($('<span />', {
		'text' : 'URL of Image',
		'class' : ''
	}));
	
	var imageFile = $('<td />');
	
	imageFile.append($('<input />', {
		'type' : 'checkbox',
		'value' : 'imageFile',
		'class' : '',
		'checked' : 'checked'
	}));
	
	imageFile.append($('<span />', {
		'text' : 'Image File',
		'class' : ''
	}));
	
	includedDataRowOne.append(urlOfImage);
	includedDataRowOne.append(imageFile);
	
	// Second row of the table
	
	var uploadDateUser = $('<td />');
	
	uploadDateUser.append($('<input />', {
		'type' : 'checkbox',
		'value' : 'uploadDateUser',
		'checked' : 'checked'
	}));
	
	uploadDateUser.append($('<span />', {
		'text' : 'Upload Date/User',
		'class' : ''
	}));
	
	var tagGroups = $('<td />');
	
	tagGroups.append($('<input />', {
		'type' : 'checkbox',
		'value' : 'tagGroups',
		'checked' : 'checked'
	}));
	
	tagGroups.append($('<span />', {
		'text' : 'Tag Groups'
	}));
	
	includedDataRowTwo.append(uploadDateUser);
	includedDataRowTwo.append(tagGroups);
	
	// Third row of the table
	
	var imageTags = $('<td />');
	
	imageTags.append($('<input />', {
		'type' : 'checkbox',
		'value' : 'imageTags',
		'checked' : 'checked'
	}));
	
	imageTags.append($('<span />', {
		'text' : 'Image Tags'
	}));
	
	var geneLinks = $('<td />');
	
	geneLinks.append($('<input />', {
		'type' : 'checkbox',
		'value' : 'geneLinks',
		'checked' : 'checked'
	}));
	
	geneLinks.append($('<span />', {
		'text' : 'Gene Links'
	}));
	
	includedDataRowThree.append(imageTags);
	includedDataRowThree.append(geneLinks);
	
	// Fourth row of the table
	
	var organisms = $('<td />');
	
	organisms.append($('<input />', {
		'type' : 'checkbox',
		'value' : 'organisms',
		'checked' : 'checked'
	}));
	
	organisms.append($('<span />', {
		'text' : 'Associated Organisms'
	}));
	
	includedDataRowFour.append(organisms);
	
	tagGroups.children('input').click(function() {   
	    if (!this.checked) {
	    	imageTags.children('input').attr("checked", false);
	        geneLinks.children('input').attr("checked", false);
	    }
	});
	
	imageTags.children('input').click(function() {   
	    if (this.checked) {
	        tagGroups.children('input').attr("checked", true);
	    }
	    else {
	    	geneLinks.children('input').attr("checked", false);
	    }
	});
	
	geneLinks.children('input').click(function() {   
	    if (this.checked) {
	        tagGroups.children('input').attr("checked", true);
	        imageTags.children('input').attr("checked", true);
	    }
	});
	
	return includedData;
};

DownloadImageDataDialog.prototype.createFileTypeContent = function() {
	var fileType = $('<div />', {
		
	});
	
	var fileTypeTitle = $('<div />', {
		'text' : 'Metadata File Type',
		'class' : 'download-image-data-dialog-content-section-title'
	});
	
	var fileTypeTableContainer = $('<div />', {
		'class' : 'download-image-data-dialog-content-section'
	});
	
	var fileTypeTable = $('<table cellspacing="0" />');
	
	var fileTypeRow = $('<tr />');
	
	fileTypeTable.append(fileTypeRow);
	fileTypeTableContainer.append(fileTypeTable);
	fileType.append(fileTypeTitle);
	fileType.append(fileTypeTableContainer);
	
	var json = $('<td />');
	
	json.append($('<input />', {
		'type' : 'radio',
		'name' : 'fileType',
		'checked' : true,
		'value' : 'json'
	}));
	
	json.append($('<span />', {
		'text' : 'Json',
		'class' : ''
	}));
	
	var xml = $('<td />');
	
	xml.append($('<input />', {
		'type' : 'radio',
		'name' : 'fileType',
		'class' : '',
		'value' : 'xml'
	}));
	
	xml.append($('<span />', {
		'text' : 'XML',
		'class' : ''
	}));
	
	fileTypeRow.append(json);
	fileTypeRow.append(xml);
	
	return fileType;
};

DownloadImageDataDialog.prototype.center = function(width, height) {
	if (height > this.dialog.height()) {
		this.dialog.css('top', (height - this.dialog.height())/2 + 'px');
	}
	else {
		this.dialog.css('top', '0px');
	}
	
	this.dialog.css('left', (width - this.dialog.width())/2 + 'px');
};