function Tag(id, colorArr, tagPoints, description, geneLinks, imageKey, siteUrl, tagGroup) {
	this.id = id;
	this.color = colorArr;
	this.tagGroup = tagGroup;
	this.points = tagPoints;
	this.description = description;
	this.imageKey = imageKey;
	this.siteUrl = siteUrl;
	this.saveUrl = siteUrl + 'api/tags';
	this.geneLinks = this.__convertToGeneLinks(geneLinks);
};

Tag.prototype.setTagGroup = function(tagGroup) {
	this.tagGroup = tagGroup;
};

Tag.prototype.addGeneLink = function(id, feature) {
	this.geneLinks.push(new GeneLink(id, feature));
};

Tag.prototype.setId = function(id) {
	this.id = id;
};

Tag.prototype.getId = function() {
	return this.id;
};

Tag.prototype.getColor = function() {
	return this.color;
};

Tag.prototype.getPoints = function() {
	return this.points;
};

Tag.prototype.getDescription = function() {
	return this.description;
};

Tag.prototype.getGeneLinks = function() {
	return this.geneLinks;
};

Tag.prototype.getFormattedColor = function() {
	if (this.color[0] + this.color[1] + this.color[2] != 0) {
		return 'rgba(' + this.color.join() + ',0.3)';
	}
	else {
		return '';
	}
};

/**
 * Saves this tag into the database using an ajax call
 * 
 * @param callback: function to run when the saving of the tag has been confirmed.
 */
Tag.prototype.save = function(callback, errorCallback) {
	$.ajax({
		url : this.saveUrl,
		type : 'POST',
		data : {
			color : JSON.stringify(this.color),
			points : JSON.stringify(this.points),
			name : this.description,
			tagGroupId : this.tagGroup.getId()
		},
		dataType : 'json',
		success : function(data, textStatus, jqXHR) {
			callback(data);
		},
		error : function(jqXHR, textStatus, errorThrown) {
			var errorMessage = $.parseJSON(jqXHR.responseText).message;
			errorCallback(errorMessage);
		}
	});
};

Tag.prototype.copy = function() {
	return new Tag(this.getId(), this.getColor(), this.getPoints(), 
		this.description, this.getGeneLinks(), this.imageKey, this.siteUrl, this.tagGroup);
};

Tag.prototype.__convertToGeneLinks = function(geneLinksObj) {
	var geneLinks = [];
	
	$.each(geneLinksObj, function(index, geneLink) {
		geneLinks.push(new GeneLink(geneLink.id, geneLink.feature));
	});
	
	return geneLinks;
};