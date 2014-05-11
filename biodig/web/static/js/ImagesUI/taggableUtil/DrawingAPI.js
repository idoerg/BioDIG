/**
 * Creates an API for drawing on the drawing board and then saving the tag onto
 * 
 * 
 * @param drawingBoard
 * @param tagBoard
 * @return
 */
function DrawingAPI(drawingBoard, tagBoard, dialogs, siteUrl, originalData, image, imageMetadata, genomicInfo) {
    this.tagBoard = new TagBoard(tagBoard, originalData, image, imageMetadata, genomicInfo, siteUrl);
    this.drawingBoard = new DrawingBoard(drawingBoard, image);
    this.imageMetadata = imageMetadata;
    this.image = image;
    this.dialogs = dialogs;
    this.dialogs['newTagGroup'].setTagBoard(this.tagBoard);
    this.dialogs['changeCurrentGroups'].setTagBoard(this.tagBoard);
    this.dialogs['downloadImageData'].setTagBoard(this.tagBoard);
};

/*
 ---------------------------------------------------------------
         Tagging Config Methods for setting and getting
 ---------------------------------------------------------------
*/
DrawingAPI.prototype.setFillStyle = function(newFillStyle) {
    this.drawingBoard.taggingConfig.fillStyle = newFillStyle;
};

DrawingAPI.prototype.setN = function(newN) {
    this.drawingBoard.taggingConfig.n = newN;
};

DrawingAPI.prototype.setMouseDown = function(newMouseDown) {
    this.drawingBoard.taggingConfig.mouseDown = newMouseDown;
};

DrawingAPI.prototype.setShape = function(newShape) {
    if (newShape != 'rect') {
        this.drawingBoard.taggingConfig.shape = 'poly';
    }
    else {
        this.drawingBoard.taggingConfig.shape = 'rect';
    }
};

DrawingAPI.prototype.getFillStyle = function() {
    return this.drawingBoard.taggingConfig.fillStyle;
};

DrawingAPI.prototype.getN = function() {
    return this.drawingBoard.taggingConfig.n;
};

DrawingAPI.prototype.getMouseDown = function() {
    return this.drawingBoard.taggingConfig.mouseDown;
};

DrawingAPI.prototype.getShape = function(newShape) {
    return this.drawingBoard.taggingConfig.shape;
};

/*
 ------------------------------------------------------------
             Getters and Setters for other properties
 ------------------------------------------------------------
*/
DrawingAPI.prototype.getTagBoard = function() {
    return this.tagBoard;
};

DrawingAPI.prototype.getDrawingBoard = function() {
    return this.drawingBoard;
};

/**
 * 
**/
DrawingAPI.prototype.startTagging = function() {
    var canvas = this.drawingBoard.board;
    
    canvas.css('z-index', 500);
    
    canvas.off('mousedown');
    canvas.off('mouseup');
    canvas.off('mousemove');
    
    if (this.getShape() == 'rect') {
        canvas.on('mousedown', Util.scopeCallback(this.drawingBoard, this.drawingBoard.startRect));
        canvas.on('mouseup', Util.scopeCallback(this.drawingBoard, this.drawingBoard.finishRect));
        canvas.on('mousemove', Util.scopeCallback(this.drawingBoard, this.drawingBoard.expandRect));
    }
    else {
        canvas.on('mousedown', Util.scopeCallback(this.drawingBoard, this.drawingBoard.startPoly));
        canvas.on('mouseup', Util.scopeCallback(this.drawingBoard, this.drawingBoard.finishPoly));
        canvas.on('mousemove', Util.scopeCallback(this.drawingBoard, this.drawingBoard.expandPoly));
    }
};

/**
 * 
**/
DrawingAPI.prototype.endTagging = function() {
    var canvas = this.drawingBoard.board;
    
    canvas.css('z-index', 0);
    canvas.off('mousedown');
    canvas.off('mouseup');
    canvas.off('mousemove');
};

DrawingAPI.prototype.saveTag = function() {
    var $canvas = this.drawingBoard.getBoard();
    var tagPoints = this.drawingBoard.getCurrentTagPoints();
    var id = this.image.attr('id');
    
    // gets the 3 color values RGB
    var fillStyle = this.getFillStyle();
    var colorArr = fillStyle.split('(')[1].split(')')[0].split(',');
    colorArr.pop();
    for (var i = 0; i < colorArr.length; i++) {
        colorArr[i] = $.trim(colorArr[i])
    }
    
    this.dialogs['saveTags'].show(this.tagBoard, colorArr, tagPoints, this.dialogs['newTagGroup']);
};