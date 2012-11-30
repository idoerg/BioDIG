/*
 -------------------------------------------------------------------------------
 					DrawingBoard object for drawing the tags
 					
 					Dependencies:
 						1. jQuery 1.7.2
 						2. TaggableUtil.js in the taggableUtil package
 -------------------------------------------------------------------------------
*/
/**
 * 
 * @param drawingBoard
 * @param image
 * @return
 */
function DrawingBoard(drawingBoard, image) {
	this.board = drawingBoard;
	this.image = image;
	this.taggingConfig = {
		fillStyle : '',
		shape : 'rect',
		n : 0,
		mouseDown : false
	};
	this.points = [];
};

DrawingBoard.prototype.getBoard = function() {
	return this.board;
};

DrawingBoard.prototype.getCurrentTagPoints = function() {
	return this.points;
};

/* 
--------------------------------------------------------------------------------
			Rectangle Drawing API for starting, finishing and expanding
--------------------------------------------------------------------------------
*/
DrawingBoard.prototype.startRect = function(event) {
	var point = TaggableUtil.getCoordinates(event);
	this.points = [];
	this.points[0] = TaggableUtil.convertFromZoomToOriginal(point, this.image);
	this.taggingConfig.mouseDown = true; 
};

DrawingBoard.prototype.finishRect = function(event) {	
	var point = TaggableUtil.getCoordinates(event);
	this.points[1] = TaggableUtil.convertFromZoomToOriginal(point, this.image);
	this.taggingConfig.mouseDown = false; 
};

DrawingBoard.prototype.expandRect = function(event) {
	var canvas = this.board[0];
	
	// should do nothing if the mouse is not held down
	if (this.taggingConfig.mouseDown) {
		// converts the events x,y values to create a point that is local to the canvas
		var point = TaggableUtil.getCoordinates(event);
		
		// since the canvas is most likely zoomed in we must convert back to original points for
		// storing so that they can be properly scaled and stored through ajax later
		point = TaggableUtil.convertFromZoomToOriginal(point, this.image);
		this.points[1] = point;
		
		// converts the points array to an array of zoomed points instead
		var drawPoints = [];
		for (var i = 0; i < this.points.length; i++) {
			drawPoints[i] = TaggableUtil.convertFromOriginalToZoom(this.points[i], this.image);
		}
		
		// draws the rectangle
		this.__drawRect(drawPoints, true);
	}
};

/* 
---------------------------------------------------------------------------------
			Polygon Drawing API for starting, finishing and expanding
---------------------------------------------------------------------------------
*/
DrawingBoard.prototype.startPoly = function(event) {
	var point = TaggableUtil.getCoordinates(event);
	this.points = [];
	this.points.push(TaggableUtil.convertFromZoomToOriginal(point, this.image));
	this.taggingConfig.n = 1;
	this.taggingConfig.mouseDown = true; 
};

DrawingBoard.prototype.finishPoly = function(event) {	
	var point = TaggableUtil.getCoordinates(event);
	this.points.push(TaggableUtil.convertFromZoomToOriginal(point, this.image));
	this.taggingConfig.mouseDown = false; 
};

DrawingBoard.prototype.expandPoly = function(event) {	
	// should only be called when the mouse is down and should not
	// be called every time because it will produce too many points
	if (this.taggingConfig.mouseDown && this.taggingConfig.n % 8 == 1) {
		// converts the events x,y values to create a point that is local to the canvas
		var point = TaggableUtil.getCoordinates(event);
		
		// since the canvas is most likely zoomed in we must convert back to original points for
		// storing so that they can be properly scaled and stored through ajax later
		point = TaggableUtil.convertFromZoomToOriginal(point, this.image);
		this.points.push(point);
		
		// converts the points array to an array of zoomed points instead
		var drawPoints = [];
		for (var i = 0; i < this.points.length; i++) {
			drawPoints[i] = TaggableUtil.convertFromOriginalToZoom(this.points[i], this.image);
		}
		
		// draws the polygon
		this.__draw(drawPoints, true);
	}
};

DrawingBoard.prototype.redraw = function() {
	if (this.points.length >= 2) {
		// converts the points to be at the correct zoom level
		var drawPoints = [];
		for (var i = 0; i < this.points.length; i++) {
			drawPoints[i] = TaggableUtil.convertFromOriginalToZoom(this.points[i], this.image);
		}
		
		// checks to see if its is a rectangle
		if (drawPoints.length == 2) {
			var otherPoints = TaggableUtil.getOtherRectPoints(drawPoints);
			drawPoints[2] = drawPoints[1];
			drawPoints[1] = otherPoints[0];
			drawPoints[3] = otherPoints[1];
		}
		
		// draws the points
		this.__draw(drawPoints, true);
	}
};

DrawingBoard.prototype.__draw = function(points, refresh) {
	var canvas = this.board[0];
	// checks to see if the canvas should be refreshed
	if (refresh) {
		canvas.width = canvas.width;
	}
	var context = canvas.getContext("2d");
	
	// goes through each point and draws the polygon
	context.beginPath();
	context.moveTo(points[0][0], points[0][1]);
	for (var i = 1; i < points.length; i++) {
		context.lineTo(points[i][0], points[i][1]);    
	}
	context.closePath();
	
	if (this.taggingConfig.fillStyle != "") {
		context.fillStyle = this.taggingConfig.fillStyle;
		context.fill();
	}
	context.stroke(); 
};

DrawingBoard.prototype.__drawRect = function(points, refresh) {
	var drawPoints = [points[0], points[1]];
	var otherPoints = TaggableUtil.getOtherRectPoints(drawPoints);
	drawPoints[2] = drawPoints[1];
	drawPoints[1] = otherPoints[0];
	drawPoints[3] = otherPoints[1];
	this.__draw(drawPoints, refresh);
};