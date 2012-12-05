/**
	Creates a tagging application that links to the database using ajax
	
	Dependencies:
		1. All of the dependencies taggable.js 
**/
function TaggerUI(image, parent, originalData, imageMetadata, genomicInfo, imagesUrl, siteUrl, alreadyLoaded, callback) {
	this.image = image;
	this.parent = parent;
	this.originalData = originalData;
	this.genomicInfo = genomicInfo;
	this.imagesUrl = imagesUrl;
	this.siteUrl = siteUrl;
	this.imageMetadata = imageMetadata;
	this.title = "";
	this.callback = callback;
	this.alreadyLoaded = alreadyLoaded;
	this.created = false;
	
	for (var i = 0; i < imageMetadata.organisms.length; i++) {
		this.title += imageMetadata.organisms[i].common_name;
		if (i < imageMetadata.organisms.length - 1) {
			this.title += ", ";
		}
	}
	
	$(this.image).zoomable({
		callback: Util.scopeCallback(this, this.createStructure),
		zoom_callback: Util.scopeCallback(this, this.resizeCanvas),
		zoom_callback_args: [$(this.image).attr('id')],
		alreadyLoaded: this.alreadyLoaded
	});
};

TaggerUI.prototype.createStructure = function() {	
	// create the toolbar
	var id = this.image.attr('id');
	
	this.menu = this.getToolbar(id);
	
	this.parent.prepend(this.menu.getUI());
	
	this.__renderGeneLinksMenu();
	
	var pageBlock = new PageBlock();
	var changeCurrentTagGroupsDialog = new ChangeCurrentTagGroupsDialog(pageBlock);
	var downloadImageDataDialog = new DownloadImageDataDialog(pageBlock, this.image, this.imagesUrl);
	
	var dialogs = {
		'changeCurrentGroups' : changeCurrentTagGroupsDialog,
		'downloadImageData' : downloadImageDataDialog
	};
	
	if ($('#taggable-tooltip').length == 0) {
		this.parent.parent().append('<div id="taggable-tooltip"></div>');
	}
	
	// creates the tag board and the drawing board
	var tagBoard = $('<div />', {
		id      : id + '-tag-board',
		'class' : 'tag-board'
	}).prependTo(this.image.parent());
	
	tagBoard.draggable();
	
	// creates the drawing API
	this.drawingAPI = new DrawingAPI(tagBoard, dialogs, this.siteUrl, this.originalData, this.image, this.imageMetadata, this.genomicInfo);
	
	var $tagGroupSelect = this.parent.find('#' + id + '-tag-groups');
	var groups = this.drawingAPI.getTagBoard().getTagGroups();
	for (key in groups) {
		var group = groups[key];
		$tagGroupSelect.append($('<option />', {
			'text' : group.getName(),
			'name' : group.getKey()
		}));
	}
	
	var self = this;
	
	// events for clicking the start and stop drawing buttons
	
	this.menu.getSection('tools').getMenuItem('toggleTags').onClick(function() {
		self.drawingAPI.getTagBoard().toggleTags();
	});
	
	this.menu.getSection('tools').getMenuItem('zoomIn').onClick(function() {
		self.image.zoomable("zoom", 1);
	});
	
	this.menu.getSection('tools').getMenuItem('zoomOut').onClick(function() {
		self.image.zoomable("zoom", -1);
	});
	
	this.menu.getSection('tools').getMenuItem('download').onClick(function() {
		downloadImageDataDialog.show();
	});
	
	this.menu.getSection('tagGroups').getMenuItem('changeCurrentGroups').onClick(function() {
		changeCurrentTagGroupsDialog.show();
	});
	
	var left = parseInt(this.image.css('left').split('px')[0]);
	var top = parseInt(this.image.css('top').split('px')[0]);
	
	// sizes everything correctly based on the image specifics
	// also draws the original tags if they exist
	this.created = true;
	this.resizeCanvas();
	
	// since the tagBoard has to be above the image we must make it drag the image with it
	this.drawingAPI.getTagBoard().getBoard().bind('drag', function(event, ui) {
		self.image.css('left', $(this).css('left')).css('top', $(this).css('top'));
	});
	
	if (this.callback) {
		this.callback();
	}
};

TaggerUI.prototype.resizeCanvas = function() {
	if (this.created) {
		var $tagBoard = this.drawingAPI.getTagBoard().getBoard();
		var $img = this.image;
		
		// tag board
		$tagBoard.css('left', $img.css('left')).css('top', $img.css('top'));
		$tagBoard.height($img.height());
		$tagBoard.width($img.width());
		
		this.drawingAPI.getTagBoard().redraw();
	}
};

TaggerUI.prototype.getToolbar = function(id) {
	var menu = new Menu();
	
	// create tools menu section
	var tools = new MenuSection('Tools', this.imagesUrl + 'tools.png');
	tools.addMenuItem('download', 'Download Image Data', 'ui-icon ui-icon-disk', false);
	tools.addMenuItem('zoomIn', 'Zoom In', 'ui-icon ui-icon-zoomin', false);
	tools.addMenuItem('zoomOut', 'Zoom Out', 'ui-icon ui-icon-zoomout', false);
	tools.addMenuItem('toggleTags', 'Toggle All Tag Visibility', this.imagesUrl + 'eye.png', true);
	menu.addNewSection('tools', tools);
	
	// create tag groups menu section
	var tagGroups = new MenuSection('Tag Groups', this.imagesUrl + 'tag.png');
	tagGroups.addMenuItem('changeCurrentGroups', 'Change Current Tag Groups', 'ui-icon ui-icon-pencil', false);
	menu.addNewSection('tagGroups', tagGroups);
	
	return menu;
};

/**
 * Renders the Gene Links Menu UI which is in charge of adding new links 
 * to the current tag
**/
TaggerUI.prototype.__renderGeneLinksMenu = function() {
	var id = this.image.attr('id');
	
	// adds the title to the Gene Links Menu
	var genomicInfoTitle = $('<div />', {
		'class' : 'organismTitle',
		text : this.title
	});
	
	this.genomicInfo.html(genomicInfoTitle);
	
	var info = $('<div />', {
		'class' : 'imageInfo'
	});
	
	var speciesInfo = $('<div />', {
		'class' : 'speciesInfo'
	});
	
	speciesInfo.append(this.__renderSpeciesInfo());
	info.append(speciesInfo);
	
	// adds the geneLinks menu
	var geneLinksInfo = $('<div />', {
		'class' : 'geneLinksInfo'
	});
	
	var geneLinksTitle = $('<div />', {
		'class' : 'geneLinksInfoTitle',
		'text' : 'Gene Links'
	});
	
	var geneLinksContainer = $('<div />', {
		'class' : 'tagInfoContainer'
	});
	
	geneLinksInfo.append(geneLinksTitle);
	geneLinksInfo.append(geneLinksContainer);
	
	info.append(geneLinksInfo);
	
	this.genomicInfo.append(info);
	this.genomicInfo.attr('id', id + 'GeneLinkContainer');
};

/**
 * Renders the species info portion of the gene links menu,
 * which will be shown when no tag is moused over or clicked
 */
TaggerUI.prototype.__renderSpeciesInfo = function() {
	var speciesInfo = $('<table cellspacing="0" />', {
		
	});
	
	// description of image
	var descriptionRow = $('<tr />');
	var descriptionLabel = $('<td />', {
		'text' : 'Description:'
	});
	var description = $('<td />', {
		'text' : this.imageMetadata.description
	});
	
	descriptionRow.append(descriptionLabel);
	descriptionRow.append(description);
	
	speciesInfo.append(descriptionRow);

	// upload date data
	var uploadDateRow = $('<tr />', {
		'class' : 'even'
	});
	var uploadDateLabel = $('<td />', {
		'text' : 'Uploaded on:'
	});
	var uploadDate = $('<td />', {
		'text' : this.imageMetadata.uploadDate
	});
	
	uploadDateRow.append(uploadDateLabel);
	uploadDateRow.append(uploadDate);
	
	speciesInfo.append(uploadDateRow);
	
	// uploader data
	var uploaderRow = $('<tr />');
	var uploaderLabel = $('<td />', {
		'text' : 'Uploaded by:'
	});
	var uploader = $('<td />', {
		'text' : this.imageMetadata.uploadedBy
	});
	
	uploaderRow.append(uploaderLabel);
	uploaderRow.append(uploader);
	
	speciesInfo.append(uploaderRow);
	return speciesInfo;
};