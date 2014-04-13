define(['jquery', 'underscore', 'text!biodig/tmpl/zoomable.html'], function($, _, ZoomableTmpl) {

    var ZoomableUIHelper = {
        uuid4: function() {
            return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
                var r = Math.random()*16|0, v = c == 'x' ? r : (r&0x3|0x8);
                return v.toString(16);
            });
        },
        createStructure: function($img, template, options) {
            $img.off('load');
            // renders the zoomable template, structural
            var id = $img.attr('id');
            if (!id) {
                id = ZoomableUIHelper.uuid4();
                $img.attr('id', id);
            }
            $img.parent().append(template(id));

            // uses the jQueryUI slider plugin to create the controls as a slider
            $('#' + id + '-zoomable-slider').slider({
                orientation: 'vertical',
                range: 'min',
                min: 0,
                max: 100,
                value: 0
            });

            // this is the container of everything and the image needs to be moved inside of it
            var $zoomableContainer = $('#' + id + '-zoomable-container');
            $zoomableContainer.height(options.height);
            $zoomableContainer.width(options.width);
            $zoomableContainer.append($img);

            // make image fit inside the container
            ZoomableUIHelper.fit($img, $zoomableContainer);

            // stores the original height for use later
            $img.data('originalHeight', $img.height());
            $img.data('originalWidth', $img.width());
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
        setupControls: function($img, options) {
            var id = $img.attr('id'); // should be set when this is being called
            // controls are setup for the zooming bar (PLUS)
            $('#' + id + '-zoomable-plus').on('click', function() {
                $('#' + id + '-zoomable-slider').slider('value', $('#' + id + '-zoomable-slider').slider('value') + 1);
                if (options.zoom_callback) {
                    if (options.zoom_callback_args) {
                        options.zoom_callback.apply(this, options.zoom_callback_args);
                    }
                    else {
                        options.zoom_callback();
                    }
                }
            });


            // controls are setup for the zooming bar (MINUS)
            $('#' + id + '-zoomable-minus').on('click', function() {
                $('#' + id + '-zoomable-slider').slider('value', $('#' + id + '-zoomable-slider').slider('value') - 1);
                if (options.zoom_callback) {
                    if (options.zoom_callback_args) {
                        options.zoom_callback.apply(this, options.zoom_callback_args);
                    }
                    else {
                        options.zoom_callback();
                    }
                }
            });

            // sets up the slider to change the zoom level
            $('#' + id + '-zoomable-slider').on('slidechange', function(event, ui) {
                ZoomableUIHelper.changeEvent(event, ui, $img);
                if (options.zoom_callback) {
                    if (options.zoom_callback_args) {
                        options.zoom_callback.apply(this, options.zoom_callback_args);
                    }
                    else {
                        options.zoom_callback();
                    }
                }
            });

            var $zoomableContainer = $('#' + id + '-zoomable-container');

            // sets up the zoomSlider to be hidden by default and appear on mouseover
            $zoomableContainer.children('.zoomable-slider-container').hide();

            $zoomableContainer.on('mouseover', function() {
                $(this).children('.zoomable-slider-container').show();
            });

            $zoomableContainer.on('mouseout', function() {
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

        this.template = _template($(ZoomableTmpl).html());

        var self = this;

        var init = function() {
            // creates the structure
            ZoomableUIHelper.createStructure(self.$image, self.template, options);
            ZoomableUIHelper.setupControls(self.$image, options);
            self.$image.draggable();

            self.$image.data('zoomable', true);
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
        var zoomSlider = $('#' + id + '-zoomable-slider');
        var newVal = zoomSlider.slider("value") + magnitude;
        newVal = newVal < 100 ? newVal : 100;
        newVal = newVal > 0 ? newVal : 0;
        zoomSlider.slider("value", newVal);
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
                width: 500,
                alreadyLoaded: false
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
