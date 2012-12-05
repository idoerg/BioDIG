/**
 * Object that represents a grouping of image tags
 * 
 * @param group
 * @param imageKey
 * @param siteUrl
 * @return
 */
function TagGroup(group, imageKey, siteUrl) {
	this.tags = [];
	this.lastModified = TaggableUtil.toDate(group.lastModified);
	this.dateCreated = TaggableUtil.toDate(group.dateCreated);
	this.name = group.name;
	this.key = group.pk;
	
	for (var i = 0; i < group.tags.length; i++) {
		var tag = group.tags[i];
		var colorArr = tag.color;
		var tagPoints = tag.points;
		var description = tag.description;
		var geneLinks = tag.geneLinks;
		var id = tag.id;
		this.tags.push(new Tag(id, colorArr, tagPoints, description, geneLinks, imageKey, siteUrl, this));
	}
};

TagGroup.prototype.getName = function() {
	return this.name;
};

TagGroup.prototype.getKey = function() {
	return this.key;
};

TagGroup.prototype.getTags = function() {
	return this.tags;
};

TagGroup.prototype.addTag = function(tag) {
	this.tags.push(tag);
};