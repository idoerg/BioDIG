/*
 -------------------------------------------------------------------------------------
 						Static utility methods for canvases
 -------------------------------------------------------------------------------------
*/
var TaggableUtil = {};

/**
	Gets the coordinates of a the target of the event with respect to
	the total page
**/
TaggableUtil.getCoordinates = function(event) {
	var posX = 0;
	var posY = 0;
	var $canvas = $(event.target);
	
	// finds the exact position of the canvas on the page
	var imgPos = TaggableUtil.findPosition($canvas[0]);
	if (!event) var event = window.event;
	if (event.pageX || event.pageY) {
		posX = event.pageX;
		posY = event.pageY;
	}
	else if (event.clientX || event.clientY) {
		posX = event.clientX + document.body.scrollLeft
			+ document.documentElement.scrollLeft;
		posY = event.clientY + document.body.scrollTop
			+ document.documentElement.scrollTop;
	}
	// finds the relative position
	posX = posX - imgPos[0];
	posY = posY - imgPos[1];
	return [posX, posY];
};

TaggableUtil.findPosition = function(oElement) {
	if(typeof( oElement.offsetParent ) != "undefined") {
		for(var posX = 0, posY = 0; oElement; oElement = oElement.offsetParent) {
			posX += oElement.offsetLeft;
			posY += oElement.offsetTop;
		}
		return [ posX, posY ];
	}
	
	return [ oElement.x, oElement.y ];
};

/*
---------------------------------------------------------------------------------------
				Methods to convert back and forth between zoom levels
---------------------------------------------------------------------------------------
*/

/**
	Converts a points from the original dimensions to the current zoom level's
	dimensions. Relies heavily on the zoomable plugin
**/
TaggableUtil.convertFromOriginalToZoom = function(point, image) {
	var scale = image.height()/image.data('originalHeight');
	return [point[0]*scale, point[1]*scale];
};

/**
	Converts a points from the current zoom level's dimensions to the original
	dimensions. Relies heavily on the zoomable plugin
**/
TaggableUtil.convertFromZoomToOriginal = function(point, image) {
	var scale = image.data('originalHeight')/image.height();
	return [point[0]*scale, point[1]*scale];
};

/*
-------------------------------------------------------------------------
				Helper methods for the Drawing API 
-------------------------------------------------------------------------
*/
TaggableUtil.getOtherRectPoints = function(points) {
	var pointOne, pointTwo;
	if (points[0][0] < points[1][0] && points[0][1] < points[1][1]) {
		pointOne = [points[0][0], points[1][1]];
		pointTwo = [points[1][0], points[0][1]];
	}
	else if (points[0][0] > points[1][0] && points[0][1] > points[1][1]) {
		pointOne = [points[1][0], points[0][1]];
		pointTwo = [points[0][0], points[1][1]];
	}
	else if (points[0][0] < points[1][0] && points[0][1] > points[1][1]) {
		pointOne = [points[0][0], points[1][1]];
		pointTwo = [points[1][0], points[0][1]];
	}
	else {
		pointOne = [points[1][0], points[0][1]];
		pointTwo = [points[0][0], points[1][1]];
	}
	return [pointOne, pointTwo]; 
};

TaggableUtil.toDate = function(dateTime) {
	var date = dateTime.split(" ");
	var time = date[1];
	date = date[0].split("-");
	time = time.split(":");
	
	var year = parseInt(date[0]);
	var month = parseInt(date[1]);
	var day = parseInt(date[2]);
	
	var hours = parseInt(time[0]);
	var minutes = parseInt(time[1]);
	var seconds = parseInt(time[2]);
	var milliseconds = 0;
	
	return new Date(year, month, day, hours, minutes, seconds, milliseconds);
};