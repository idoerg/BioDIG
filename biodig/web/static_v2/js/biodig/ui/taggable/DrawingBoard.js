var deps = [
    'jquery', 'underscore', 'lib/util', 'biodig/ui/taggable/util',
    'text!biodig/tmpl/taggable/drawingboard.html'
];

define(deps, function($, _, util, TaggableUtil, DrawingBoardTmpl) {

    var DrawingBoardTemplate = _.template(DrawingBoardTmpl);

    var Helper = {
        drawRect : function(points, refresh) {
            var drawPoints = [points[0], points[1]];
            var otherPoints = TaggableUtil.getOtherRectPoints(drawPoints);
            drawPoints[2] = drawPoints[1];
            drawPoints[1] = otherPoints[0];
            drawPoints[3] = otherPoints[1];
            this.draw(drawPoints, refresh);
        }
    };

    function DrawingBoard(image) {
        this.$image = image;
        this.$board = $(DrawingBoardTemplate(this.$image));
        this.$image.parent().prepend(this.$board);
        this.config = {
            fillStyle : '',
            shape : 'rect',
            n : 0,
            mouseDown : false
        };
        this.points = [];
        this.resize();
    };

    DrawingBoard.prototype.points = function() {
        return this.points;
    };

    DrawingBoard.prototype.resize = function() {
        this.$board.css('left', this.$image.css('left')).css('top', this.$image.css('top'));
        this.$board.height(this.$image.height());
        this.$board.width(this.$image.width());

        this.redraw();
    };

    /*
    --------------------------------------------------------------------------------
                Rectangle Drawing API for starting, finishing and expanding
    --------------------------------------------------------------------------------
    */
    DrawingBoard.prototype.startRect = function(event) {
        var point = TaggableUtil.getCoordinates(event);
        this.points = [];
        this.points[0] = TaggableUtil.convertFromZoomToOriginal(point, this.$image);
        this.config.mouseDown = true;
    };

    DrawingBoard.prototype.finishRect = function(event) {
        var point = TaggableUtil.getCoordinates(event);
        this.points[1] = TaggableUtil.convertFromZoomToOriginal(point, this.$image);
        this.config.mouseDown = false;
    };

    DrawingBoard.prototype.expandRect = function(event) {
        var canvas = this.$board[0];

        // should do nothing if the mouse is not held down
        if (this.config.mouseDown) {
            // converts the events x,y values to create a point that is local to the canvas
            var point = TaggableUtil.getCoordinates(event);

            // since the canvas is most likely zoomed in we must convert back to original points for
            // storing so that they can be properly scaled and stored through ajax later
            point = TaggableUtil.convertFromZoomToOriginal(point, this.$image);
            this.points[1] = point;

            // converts the points array to an array of zoomed points instead
            var drawPoints = [];
            for (var i = 0; i < this.points.length; i++) {
                drawPoints[i] = TaggableUtil.convertFromOriginalToZoom(this.points[i], this.$image);
            }

            // draws the rectangle
            util.scope(this, Helper.drawRect)(drawPoints, true);
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
        this.config.n = 1;
        this.config.mouseDown = true;
    };

    DrawingBoard.prototype.finishPoly = function(event) {
        var point = TaggableUtil.getCoordinates(event);
        this.points.push(TaggableUtil.convertFromZoomToOriginal(point, this.image));
        this.config.mouseDown = false;
    };

    DrawingBoard.prototype.expandPoly = function(event) {
        // should only be called when the mouse is down and should not
        // be called every time because it will produce too many points
        if (this.config.mouseDown && this.config.n % 8 == 1) {
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
            this.draw(drawPoints, true);
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
                util.scope(this, Helper.drawRect)(drawPoints, true);
            }
            else {
                // draws the points
                this.draw(drawPoints, true);
            }
        }
    };

    DrawingBoard.prototype.draw = function(points, refresh) {
        var canvas = this.$board[0];
        // checks to see if the canvas should be refreshed
        if (refresh) {
            canvas.width = canvas.width;
        }
        var context = canvas.getContext("2d");

        // goes through each point and draws the polygon
        context.beginPath();
        context.moveTo(points[0].x, points[0].y);
        for (var i = 1; i < points.length; i++) {
            context.lineTo(points[i].x, points[i].y);
        }
        context.closePath();

        if (this.config.fillStyle != "") {
            context.fillStyle = this.config.fillStyle;
            context.fill();
        }
        context.stroke();
    };

    return {
        create: function(image) {
            return new DrawingBoard(image);
        }
    }
})
