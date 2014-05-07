var deps = [
    'jquery', 'underscore', 'kinetic', 'lib/util', 'biodig/ui/taggable/util',
    'text!biodig/tmpl/taggable/drawingboard.html'
];

define(deps, function($, _, Kinetic, util, TaggableUtil, DrawingBoardTmpl) {

    var DrawingBoardTemplate = _.template(DrawingBoardTmpl);

    var Helper = {
        drawRect : function(points, refresh) {
            var drawPoints = [points[0], points[1]];
            var otherPoints = TaggableUtil.otherRectPoints(drawPoints);
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

        this.stage = new Kinetic.Stage({
            container: this.$board[0],
            width: this.$board.width(),
            height: this.$board.height()
        });

        this.dconfig = {
            fillStyle : '',
            shape : 'RECT',
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

        // clear the original stage and resize it
        this.stage.setSize({
            'width': this.$board.width(),
            'height': this.$board.height()
        });

        this.redraw();
    };

    DrawingBoard.prototype.config = function(key, value) {
        this.dconfig[key] = value;
    };

    DrawingBoard.prototype.begin = function() {
        this.$board.removeClass('hidden').addClass('show');
        this.$board.css('z-index', 500);

        this.$board.off('mousedown');
        this.$board.off('mouseup');
        this.$board.off('mousemove');

        this.$board.on('mousedown', util.scope(this, function(e) {
            if (this.dconfig.shape == 'RECT') {
                this.startRect(e);
            }
            else {
                this.startPoly(e);
            }
        }));

        this.$board.on('mouseup', util.scope(this, function(e) {
            if (this.dconfig.shape == 'RECT') {
                this.finishRect(e);
            }
            else {
                this.finishPoly(e);
            }
        }));

        this.$board.on('mousemove', util.scope(this, function(e) {
            if (this.dconfig.shape == 'RECT') {
                this.expandRect(e);
            }
            else {
                this.expandPoly(e);
            }
        }));
    };

    DrawingBoard.prototype.end = function() {
        this.$board.removeClass('show').addClass('hidden');

        this.$board.off('mousedown');
        this.$board.off('mouseup');
        this.$board.off('mousemove');
    };

    /*
    --------------------------------------------------------------------------------
                Rectangle Drawing API for starting, finishing and expanding
    --------------------------------------------------------------------------------
    */
    DrawingBoard.prototype.startRect = function(event) {
        var mousePos = this.stage.getPointerPosition(event);
        this.points = [];
        this.points[0] = TaggableUtil.convertFromZoomToOriginal(mousePos, this.$image);
        this.dconfig.mouseDown = true;
    };

    DrawingBoard.prototype.finishRect = function(event) {
        var mousePos = this.stage.getPointerPosition(event);
        this.points[1] = TaggableUtil.convertFromZoomToOriginal(mousePos, this.$image);
        this.dconfig.mouseDown = false;
    };

    DrawingBoard.prototype.expandRect = function(event) {
        var canvas = this.$board[0];

        // should do nothing if the mouse is not held down
        if (this.dconfig.mouseDown) {
            // converts the events x,y values to create a point that is local to the canvas
            var mousePos = this.stage.getPointerPosition(event);

            // since the canvas is most likely zoomed in we must convert back to original points for
            // storing so that they can be properly scaled and stored through ajax later
            this.points[1] = TaggableUtil.convertFromZoomToOriginal(mousePos, this.$image);

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
        var mousePos = this.stage.getPointerPosition(event);
        this.points = [];
        this.points.push(TaggableUtil.convertFromZoomToOriginal(mousePos, this.$image));
        this.dconfig.n = 1;
        this.dconfig.mouseDown = true;
    };

    DrawingBoard.prototype.finishPoly = function(event) {
        var mousePos = this.stage.getPointerPosition(event);
        this.points.push(TaggableUtil.convertFromZoomToOriginal(mousePos, this.$image));
        this.dconfig.mouseDown = false;
    };

    DrawingBoard.prototype.expandPoly = function(event) {
        // should only be called when the mouse is down and should not
        // be called every time because it will produce too many points
        if (this.dconfig.mouseDown && this.dconfig.n % 8 == 1) {
            // converts the events x,y values to create a point that is local to the canvas
            var mousePos = this.stage.getPointerPosition(event);

            // since the canvas is most likely zoomed in we must convert back to original points for
            // storing so that they can be properly scaled and stored through ajax later
            point = TaggableUtil.convertFromZoomToOriginal(mousePos, this.$image);
            this.points.push(point);

            // converts the points array to an array of zoomed points instead
            var drawPoints = [];
            for (var i = 0; i < this.points.length; i++) {
                drawPoints[i] = TaggableUtil.convertFromOriginalToZoom(this.points[i], this.$image);
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
                drawPoints[i] = TaggableUtil.convertFromOriginalToZoom(this.points[i], this.$image);
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
        // creates a polygon with the points
        var poly = new Kinetic.Line({
            closed: true,
            points: $.map( drawPoints, function(point){return [point.x, point.y]}),
            fill: this.dconfig.fillStyle,
            stroke: "rgba(255,255,255,0)",
            strokeWidth: 1
        });

        // clear the original stage and resize it
        this.stage.setSize({
            'width': this.$board.width(),
            'height': this.$board.height()
        });

        this.stage.removeChildren();

        var layer = new Kinetic.Layer();
        layer.add(poly);

        this.stage.add(layer);
    };

    return {
        create: function(image) {
            return new DrawingBoard(image);
        }
    }
})
