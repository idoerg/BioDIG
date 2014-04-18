var deps = [
    'jquery', 'underscore', 'kinetic', 'lib/util', 'biodig/ui/taggable/util',
    'text!biodig/tmpl/taggable/tagboard.html', 'jquery_ui'
];

define(deps, function($, _, Kinetic, util, taggable_util, TagBoardTmpl, jquery_ui) {

    var TagBoardTemplate = _.template(TagBoardTmpl);

    var TagDrawingUtil = {
        color: function(c) {
            return "rgba(" + c.r + "," + c.g + "," + c.b + ",0.3)";
        },
        poly: function(tag) {
            // converts the tag's points to the current zoom level
            var drawPoints = [];
            for (var i = 0; i < tag.points.length; i++) {
                drawPoints[i] = taggable_util.convertFromOriginalToZoom(tag.points[i], this.$image);
            }

            // checks if the points represent a rectangle and fixes the array to be a four point
            // array in the correct order for drawing
            if (drawPoints.length == 2) {
                var otherPoints = taggable_util.otherRectPoints(drawPoints);
                drawPoints[2] = drawPoints[1];
                drawPoints[1] = otherPoints[0];
                drawPoints[3] = otherPoints[1];
            }

            var fill = this.show ? TagDrawingUtil.color(tag.color) : "";

            // creates a polygon with the points for this tag
            var poly = new Kinetic.Line({
                closed: true,
                points: $.map( drawPoints, function(point){return [point.x, point.y]}),
                fill: fill,
                stroke: "rgba(255,255,255,0)",
                strokeWidth: 1
            });

            // sets the color and description for this polygon
            poly.tag = tag;
            poly.setId(tag.id);

            // toggles the mouseout event for this poly
            // and the mouseover events for all other poly's
            var self = this;
            poly.on('click', function(event) {
                util.scope(self, TagBoardEvents.polyclick)(event, poly);
            });

            return poly;
        }

    };

    var TagBoardEvents = {
        mousemove: function(event) {
            if (!this.locked) {
                var mousePos = this.stage.getPointerPosition(event);

                if (this.shapes.length > 0) {
                    for (var i = 0; i < this.shapes.length; i++) {
                        // draws the shape on mouse over
                        this.shapes[i].attrs.fill =
                            this.show ? TagDrawingUtil.color(this.shapes[i].tag.color) : "";
                        this.shapes[i].attrs.stroke = "rgba(255,255,255,0)";
                    }
                    this.shapes.length = 0;
                }

                this.shapes = this.stage.getAllIntersections(mousePos);

                this.selectedtags = {};

                for (var i = 0; i < this.shapes.length; i++) {
                    // draws the shape on mouse over
                    this.shapes[i].attrs.fill = TagDrawingUtil.color(this.shapes[i].tag.color);
                    this.shapes[i].attrs.stroke = "black";
                    var tag = this.shapes[i].tag;
                    this.selectedtags[tag.id] = tag;
                }

                this.layer.draw();

                $(this).trigger('mousemove');
            }
        },
        polyclick: function(event, poly) {
            this.locked = !this.locked;
            $(this).trigger('poly:click', [poly]);
        }
    }

    function TagBoard(image_el) {
        this.$board = $(TagBoardTemplate({ 'id' : image_el.attr('id') }));
        this.$image = image_el;
        image_el.parent().prepend(this.$board);

        // make the TagBoard draggable
        this.$board.draggable();

        this.stage = new Kinetic.Stage({
            container: this.$board[0],
            width: this.$board.width(),
            height: this.$board.height()
        });

        var self = this;
        this.$board.on('drag', function(event, ui) {
            self.$image.css('left', self.$board.css('left')).css('top', self.$board.css('top'));
            $(self).trigger('drag', [ui]);
        });

        this.locked = false;
        this.shapes = [];
        this.selectedtags = {};
        this.show = true;

        this.resize();
    }

    TagBoard.prototype.resize = function() {
        // change the size and position of the tag board to match the image
        this.locked = true; // lock the TagBoard until it is finsihed resizing
        this.$board.css('left', this.$image.css('left')).css('top', this.$image.css('top'));
        this.$board.height(this.$image.height());
        this.$board.width(this.$image.width());

        this.redraw();
    };

    TagBoard.prototype.redraw = function() {
        var tags = {};
        if (this.layer) {
            $.each(this.layer.children, function(index, shape) {
                tags[shape.tag.id] = shape.tag;
            });
        }
        this.draw(tags);
    };

    TagBoard.prototype.toggleVisibility = function() {
        this.show = !this.show;
        this.redraw();
    };

    TagBoard.prototype.draw = function(tags) {
        this.locked =  false;

        // clear the original stage and resize it
        this.stage.setSize({
            'width': this.$board.width(),
            'height': this.$board.height()
        });

        this.stage.removeChildren();

        this.layer = new Kinetic.Layer();
        var self = this;
        // Draws the tags on the board and sets up mouseover and mouseout events
        $.each(tags, function(id, tag) {
            self.layer.add(util.scope(self, TagDrawingUtil.poly)(tag));
        });

        this.stage.add(this.layer);

        this.$board.on('mousemove', util.scope(this, TagBoardEvents.mousemove));
    };

    TagBoard.prototype.selected = function() {
        return this.selectedtags;
    };

    return {
        create: function(image_el) {
            return new TagBoard(image_el);
        }
    }
});
