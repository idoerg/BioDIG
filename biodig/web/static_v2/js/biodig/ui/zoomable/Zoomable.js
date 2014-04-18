var deps = [
    'jquery', 'underscore', 'lib/util',
    'text!biodig/tmpl/zoomable/structure.html', 'jquery_ui'
];

define(deps, function($, _, util, ZoomableTmpl) {

    var ZoomableUIHelper = {
        createStructure: function(options) {
            this.$image.off('load');
            // renders the zoomable template, structural
            var id = this.$image.attr('id');
            if (!id) {
                id = util.uuid4();
                this.$image.attr('id', id);
            }
            this.$image.parent().append(this.template({ id : id }));

            // this is the container of everything and the image needs to be moved inside of it
            this.$container = this.$image.parent().find('.zoomable-container');
            this.$container.height(options.height);
            this.$container.width(options.width);
            this.$container.append(this.$image);

            // uses the jQueryUI slider plugin to create the controls as a slider
            this.$container.find('.zoomable-slider').slider({
                orientation: 'vertical',
                range: 'min',
                min: 0,
                max: 100,
                value: 0
            });

            // make image fit inside the container
            ZoomableUIHelper.fit(this.$image, this.$container);

            // stores the original height for use later
            this.$image.data('originalHeight', this.$image.height());
            this.$image.data('originalWidth', this.$image.width());
        },
        fit: function($img, $container) {
            // makes the image fit inside of the zoomable container no matter what its
            // aspect ratio is
            var imgRatio = $img.width()/$img.height();
            var containerRatio = $container.width()/$container.height();
            if (imgRatio > containerRatio) {
                $img.css('width', $container.width());
                var topVal = ($container.height() - $img.height())/2;
                $img.css('top', topVal);
            }
            else if (imgRatio < containerRatio) {
                $img.css('height', $container.height());
                var leftVal = ($container.width() - $img.width())/2;
                $img.css('left', leftVal);
            }
        },
        setupControls: function(options) {
            var id = this.$image.attr('id'); // should be set when this is being called
            var self = this;
            // controls are setup for the zooming bar (PLUS)
            this.$container.find('.zoomable-plus > button').on('click', function() {
                var $slider = self.$container.find('.zoomable-slider');
                $slider.slider('value', $slider.slider('value') + 1);
                $(self).trigger('zoom');
            });


            // controls are setup for the zooming bar (MINUS)
            this.$container.find('.zoomable-minus > button').on('click', function() {
                var $slider = self.$container.find('.zoomable-slider');
                $slider.slider('value', $slider.slider('value') - 1);
                $(self).trigger('zoom');
            });

            // sets up the slider to change the zoom level
            $container.find('.zoomable-slider').on('slidechange', function(event, ui) {
                ZoomableUIHelper.changeEvent(event, ui, self.$image);
                $(self).trigger('zoom');
            });

            // sets up the zoomSlider to be hidden by default and appear on mouseover
            $container.children('.zoomable-slider-container').hide();

            $container.on('mouseover', function() {
                $(this).children('.zoomable-slider-container').show();
            });

            $container.on('mouseout', function() {
                $(this).children('.zoomable-slider-container').hide();
            });
        },
        changeEvent: function(event, ui, $img) {
            // gets scale based on the slider value
            var scale = ZoomableUIHelper.levelToZoom(ui.value);

            // figures out the new height and width after scaling
            var newHeight = scale * $img.data('originalHeight');
            var newWidth = scale * $img.data('originalWidth');

            // adjusts left and right to center the zoom
            var curLeft = parseInt($img.css('left').split('px')[0]);
            var curTop = parseInt($img.css('top').split('px')[0]);

            var newLeft = curLeft - (newWidth - $img.width())/2;
            var newTop  = curTop - (newHeight - $img.height())/2;

            // finalizes zoom by applying the properties
            $img.css('height', newHeight);
            $img.css('width', newWidth);

            $img.css('left', newLeft + "px");
            $img.css('top', newTop + "px");
        },
        levelToZoom: function(percent) {
            // convert 1% change = 5% change in zoom level
            return 1 + percent*0.05;
        },
        resetForNewImage: function(actualImage, curImage) {
            curImage.attr('src', actualImage.src);
        }
    }

    function ZoomableUI(image_selector, options) {
        this.image = image_selector;
        this.$image = $(image_selector);

        this.$image.addClass('zoomable-src');
        this.$image.parent().addClass('zoomable-parent');

        this.template = _.template(ZoomableTmpl);

        var self = this;

        var init = function() {
            // creates the structure
            util.scope(self, ZoomableUIHelper.createStructure)(options);
            util.scope(self, ZoomableUIHelper.setupControls)(options);
            self.$image.draggable();

            self.$image.data('zoomable', true);
            if (options.onload) {
                options.onload();
            }
        };

        if (options.alreadyLoaded) {
            init();
        }
        else {
            this.$image.load(init);
        }
    }

    ZoomableUI.prototype.zoom = function() {
        var id = this.$image.attr('id');
        var $slider = this.$container('.zoomable-slider');
        var newVal = $slider.slider("value") + magnitude;
        newVal = newVal < 100 ? newVal : 100;
        newVal = newVal > 0 ? newVal : 0;
        $slider.slider("value", newVal);
        $(self).trigger('zoom');
    };

    ZoomableUI.prototype.withImage = function(src) {
        var self = this;
        var actualImage = new Image();
        actualImage.onload = function() {
            ZoomableUIHelper.resetForNewImage(actualImage, self.$image);
        };
        actualImage.src = src;
    }

    // returns a factory for the Zoomable UI
    return {
        create: function(selector, opts) {
            var settings = {
                height: 500,
                width: 560,
                alreadyLoaded: true
            };

            $.extend(settings, opts);

            var ui = new ZoomableUI(selector, settings);

            if ('actualImageSrc' in settings) {
                ui.withImage(settings.actualImageSrc);
            }

            return ui;
        }
    };

});
