/**
 * Creates an API for drawing on the drawing board and then saving the tag onto
 * 
 * 
 * @param drawingBoard
 * @param tagBoard
 * @return
 */
function DrawingAPI(tagBoard, dialogs, siteUrl, originalData, image, imageMetadata) {
	this.tagBoard = new TagBoard(tagBoard, originalData, image, imageMetadata, genomicInfo, siteUrl);
	this.dialogs = dialogs;
	this.dialogs['changeCurrentGroups'].setTagBoard(this.tagBoard);
	this.dialogs['downloadImageData'].setTagBoard(this.tagBoard);
};

DrawingAPI.prototype.getTagBoard = function() {
	return this.tagBoard;
}