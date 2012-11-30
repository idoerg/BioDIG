function GeneLink(feature) {
	this.name = feature.name;
	this.uniqueName = feature.uniquename;
	this.organismId = feature.organismId;
};

GeneLink.prototype.getUniqueName = function() {
	return this.uniqueName;
};

GeneLink.prototype.getName = function() {
	return this.name;
};

GeneLink.prototype.getOrganismId = function() {
	return this.organismId;
};