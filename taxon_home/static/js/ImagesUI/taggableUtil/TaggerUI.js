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
		this.title += imageMetadata.organisms[i].commonName;
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
	this.taggingMenu = this.getTaggingMenu(id);
	
	this.parent.prepend(this.menu.getUI());
	this.parent.prepend(this.taggingMenu.getUI());
	
	this.__renderGeneLinksMenu();
	
	var pageBlock = new PageBlock();
	var saveTagDialog = new SaveTagDialog(pageBlock);
	var newTagGroupDialog = new NewTagGroupDialog(pageBlock);
	var newGeneLinkDialog = new NewGeneLinkDialog(pageBlock, this.imageMetadata.organisms, this.siteUrl);
	var changeCurrentTagGroupsDialog = new ChangeCurrentTagGroupsDialog(pageBlock);
	var downloadImageDataDialog = new DownloadImageDataDialog(pageBlock, this.image, this.imagesUrl);
	
	var dialogs = {
		'saveTags' : saveTagDialog,
		'newTagGroup' : newTagGroupDialog,
		'newGeneLink' : newGeneLinkDialog,
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
	
	var drawingBoard = $('<canvas />', {
		id      : id + '-drawing-board',
		'class' : 'drawing-board'
	}).prependTo(this.image.parent());
	
	// creates the drawing API
	this.drawingAPI = new DrawingAPI(drawingBoard, tagBoard, dialogs, this.siteUrl, this.originalData, this.image, this.imageMetadata, this.genomicInfo);
	
	var $tagGroupSelect = this.parent.find('#' + id + '-tag-groups');
	var groups = this.drawingAPI.getTagBoard().getTagGroups();
	for (key in groups) {
		var group = groups[key];
		$tagGroupSelect.append($('<option />', {
			'text' : group.getName(),
			'name' : group.getId()
		}));
	}
	
	var self = this;
	
	// events for clicking the start and stop drawing buttons
	this.menu.getSection('tags').getMenuItem('addNewTag').onClick(function() {
		self.drawingAPI.startTagging();
		self.taggingMenu.show();
	});
	
	this.menu.getSection('tagGroups').getMenuItem('addNewTagGroup').onClick(function() {
		newTagGroupDialog.show();
	});
	
	this.menu.getSection('tagGroups').getMenuItem('changeCurrentGroups').onClick(function() {
		changeCurrentTagGroupsDialog.show();
	});
	
	this.menu.getSection('tools').getMenuItem('toggleTags').onClick(function() {
		self.drawingAPI.getTagBoard().toggleTags();
	});
	
	this.menu.getSection('tools').getMenuItem('download').onClick(function() {
		downloadImageDataDialog.show();
	});
	
	this.menu.getSection('tools').getMenuItem('zoomIn').onClick(function() {
		self.image.zoomable("zoom", 1);
	});
	
	this.menu.getSection('tools').getMenuItem('zoomOut').onClick(function() {
		self.image.zoomable("zoom", -1);
	});
	
	this.menu.getSection('geneLinks').getMenuItem('addNewLink').onClick(function() {
		newGeneLinkDialog.show(self.drawingAPI.getTagBoard());
	});
	
	this.taggingMenu.onCancelClick(function() {
		self.drawingAPI.endTagging();
	});	
	
	// changes the color of the currently drawn tag or just of the paint brush itself
	this.taggingMenu.onColorClick(function() {
		var color = $(this).css('background-color');
		
		var newFillStyle = "";
		if (color != "black") {
			var rgbArr = color.split("(")[1].split(")")[0].split(",");
			if (parseInt($.trim(rgbArr[0])) + parseInt($.trim(rgbArr[1])) + parseInt($.trim(rgbArr[2])) != 0) {
				newFillStyle = "rgba(" + rgbArr[0] + "," + rgbArr[1] + "," + rgbArr[2] + ", 0.5)"; 
			}
		}
		self.drawingAPI.setFillStyle(newFillStyle);
		self.drawingAPI.getDrawingBoard().redraw();
	});
	

	// buttons for switching between drawing in rectangular form and polygonal form
	this.taggingMenu.onRectClick(function() {
		self.drawingAPI.setShape('rect');
		self.drawingAPI.startTagging();
	});
	
	this.taggingMenu.onPolyClick(function() {
		self.drawingAPI.setShape('poly');
		self.drawingAPI.startTagging();
	});
	
	
	// submits the currently drawn tag
	this.taggingMenu.onSubmitClick(function() {
		self.drawingAPI.saveTag();
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
		self.drawingAPI.getDrawingBoard().getBoard().css('left', $(this).css('left')).css('top', $(this).css('top'));
	});
	
	if (this.callback) {
		this.callback();
	}
};

TaggerUI.prototype.resizeCanvas = function() {
	if (this.created) {
		var $canvas = this.drawingAPI.getDrawingBoard().getBoard();
		var $tagBoard = this.drawingAPI.getTagBoard().getBoard();
		var $img = this.image;
		
		// drawing board
		$canvas.css('left', $img.css('left')).css('top', $img.css('top'));
		$canvas[0].height = $img.height();
		$canvas[0].width = $img.width();
		
		// tag board
		$tagBoard.css('left', $img.css('left')).css('top', $img.css('top'));
		$tagBoard.height($img.height());
		$tagBoard.width($img.width());
		
		this.drawingAPI.getTagBoard().redraw();
		this.drawingAPI.getDrawingBoard().redraw();
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
	
	// create organism menu section
	var organisms = new MenuSection('Organisms', this.imagesUrl + 'organismIcon.png');
	organisms.addMenuItem('addOrganism', 'Add Organism', 'ui-icon ui-icon-plusthick', false);
	organisms.addMenuItem('deleteOrganism', 'Delete Organism', 'ui-icon ui-icon-trash', false);
	menu.addNewSection('organisms', organisms);
	
	// create tag groups menu section
	var tagGroups = new MenuSection('Tag Groups', this.imagesUrl + 'tagGroupIcon.png');
	tagGroups.addMenuItem('addNewTagGroup', 'Add New Tag Group', 'ui-icon ui-icon-plusthick', false);
	tagGroups.addMenuItem('changeCurrentGroups', 'Change Current Tag Groups', 'ui-icon ui-icon-pencil', false);
	tagGroups.addMenuItem('editTagGroup', 'Edit Tag Group', 'ui-icon ui-icon-pencil', false);
	tagGroups.addMenuItem('deleteTagGroup', 'Delete Tag Group', 'ui-icon ui-icon-trash', false);
	menu.addNewSection('tagGroups', tagGroups);
	
	// create tag groups menu section
	var tags = new MenuSection('Tags', this.imagesUrl + 'tag.png');
	tags.addMenuItem('addNewTag', 'Add New Tag', 'ui-icon ui-icon-plusthick', false);
	tags.addMenuItem('editTag', 'Edit Tag', 'ui-icon ui-icon-pencil', false);
	tags.addMenuItem('deleteTag', 'Delete Tag', 'ui-icon ui-icon-trash', false);
	menu.addNewSection('tags', tags);
	
	// create gene links menu section
	var geneLinks = new MenuSection('Gene Links', this.imagesUrl + 'geneLinksIcon.png');
	geneLinks.addMenuItem('addNewLink', 'Add New Link To Tag', 'ui-icon ui-icon-plusthick', false);
	geneLinks.addMenuItem('deleteLink', 'Delete Link From Tag', 'ui-icon ui-icon-trash', false);
	menu.addNewSection('geneLinks', geneLinks);
	
	return menu;
};

TaggerUI.prototype.getTaggingMenu = function(id) {
	return new TaggingMenu(id, this.imagesUrl);
}

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