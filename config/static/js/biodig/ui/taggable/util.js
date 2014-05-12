define(['jquery'], function($) {

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
        return {x : posX, y : posY};
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
        var scale = image.height()/image[0].naturalHeight;
        return { x : point.x*scale, y : point.y*scale };
    };

    /**
        Converts a points from the current zoom level's dimensions to the original
        dimensions. Relies heavily on the zoomable plugin
    **/
    TaggableUtil.convertFromZoomToOriginal = function(point, image) {
        var scale = image[0].naturalHeight/image.height();
        return { x : point.x*scale, y : point.y*scale };
    };

    /*
    -------------------------------------------------------------------------
                    Helper methods for the Drawing API
    -------------------------------------------------------------------------
    */
    TaggableUtil.otherRectPoints = function(points) {
        var pointOne, pointTwo;
        if (points[0].x < points[1].x && points[0].y < points[1].y) {
            pointOne = { x : points[0].x, y : points[1].y };
            pointTwo = { x : points[1].x, y : points[0].y };
        }
        else if (points[0].x > points[1].x && points[0].y > points[1].y) {
            pointOne = { x : points[1].x, y : points[0].y };
            pointTwo = { x : points[0].x, y : points[1].y };
        }
        else if (points[0].x < points[1].x && points[0].y > points[1].y) {
            pointOne = { x : points[0].x, y : points[1].y };
            pointTwo = { x : points[1].x, y : points[0].y };
        }
        else {
            pointOne = { x : points[1].x, y : points[0].y };
            pointTwo = { x : points[0].x, y : points[1].y };
        }
        return [pointOne, pointTwo];
    };

    TaggableUtil.toDate = function(dateTime) {
        var date = dateTime.split(" ");
        var time = date[1];
        date = date[0].split("-");
        time = time.split(":");

        var year = parseInt(date[0], 10);
        var month = parseInt(date[1], 10);
        var day = parseInt(date[2], 10);

        var hours = parseInt(time[0], 10);
        var minutes = parseInt(time[1], 10);
        var seconds = parseInt(time[2], 10);
        var milliseconds = 0;

        return new Date(year, month - 1, day, hours, minutes, seconds, milliseconds);
    };

    TaggableUtil.formatDate = function(date) {
        // example: 2012-10-11 09:34:28
        var dateTime = date.getFullYear();

        var month = date.getMonth() + 1;
        if (month < 10) {
            month = "0" + month;
        }

        var day = date.getDate();
        if (day < 10) {
            day = "0" + day;
        }

        var hour = date.getHours();
        if (hour < 10) {
            hour = "0" + hour;
        }

        var minute = date.getMinutes();
        if (minute < 10) {
            minute = "0" + minute;
        }

        var second = date.getSeconds();
        if (second < 10) {
            second = "0" + second;
        }

        dateTime += "-" + month;
        dateTime += "-" + day;
        dateTime += " " + hour;
        dateTime += ":" + minute;
        dateTime += ":" + second;

        return dateTime;
    };

    return TaggableUtil;

});
