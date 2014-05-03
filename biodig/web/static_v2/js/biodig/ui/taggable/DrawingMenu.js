var deps = [
   'jquery', 'underscore', 'lib/settings', 'text!biodig/tmpl/taggable/drawing-menu.html',
   'colorpicker', 'jquery_ui'
];

define(deps, function($, _, settings, DrawingMenuTmpl) {

    var DrawingMenuTemplate = _.template(DrawingMenuTmpl);

    function DrawingMenu(opts) {
        this.colors = opts.colors;
        this.$el = $(DrawingMenuTemplate({
            'colors' : this.colors,
            'settings' : settings
        }));
        $(opts.parent).prepend(this.$el);

        this.$el.draggable();

        var self = this;

        // sets up custom color picker
        var $colorPicker = this.$el.find('.color-picker');

        $colorPicker.ColorPicker({
            color: '#0000ff',
        	onShow: function (colpkr) {
        		$(colpkr).fadeIn(500);
        		return false;
        	},
        	onHide: function (colpkr) {
        		$(colpkr).fadeOut(500);
        		return false;
        	},
        	onChange: function (hsb, hex, rgb) {
        		$colorPicker.css('background-color', '#' + hex);
                self.color = rgb;
                $(self).trigger('color:change', [self.color]);
        	}
        });

        // setup starting values for the UI
        this.color = this.colors[0];
        this.alpha = 1.0;
        this.style = 'RECT';

        // setup color picker UI
        this.$el.find('button.change-color').on('click', function() {
            self.color = $.parseJSON(unescape($(this).data('color')));
            $(self).trigger('color:change', [self.color]);
        });

        // setup alpha UI
        var $alphaSlider = this.$el.find('.alpha-slider');
        var $alphaText = this.$el.find('.alpha-text');

        $alphaSlider.slider({
            range: 'min',
            min: 0,
            max: 100,
            value: 100
        });

        $alphaSlider.on('slidechange', function(event, ui) {
            $alphaText.val(ui.value + "%");
            self.alpha = ui.value / 100.0;
            $(self).trigger('alpha:change', [self.alpha]);
        });

        // setup style UI
        this.$el.find('.draw-rect').on('click', function() {
            self.style = 'RECT';
            $(self).trigger('style:change', [self.style]);
        });

        this.$el.find('.draw-poly').on('click', function() {
            self.style = 'POLY';
            $(self).trigger('style:change', [self.style]);
        });

        // setup submission and cancellation buttons
        this.$el.find('.submit').on('click', function() {
            $(self).trigger('submit');
        });

        this.$el.find('.cancel').on('click', function() {
            self.hide();
            $(self).trigger('cancel');
        });

        this.$el.find('.close').on('click', function() {
            self.hide();
            $(self).trigger('cancel');
        });
    }

    DrawingMenu.prototype.show = function() {
        this.$el.removeClass('hidden').addClass('show');
    };

    DrawingMenu.prototype.hide = function() {
        this.$el.removeClass('show').addClass('hidden');
    };

    return {
        create: function(opts) {
            var defaults = {
                'colors': [
                    { 'r': 255, 'g': 0, 'b': 0 }, // RED
                    { 'r': 0, 'g': 0, 'b': 255 }, // BLUE
                    { 'r': 0, 'g': 255, 'b': 255 }, // TURQUOISE
                    { 'r': 0, 'g': 98, 'b': 0 }, // DARK GREEN
                    { 'r': 0, 'g': 255, 'b': 0 }, // LIGHT GREEN
                    { 'r': 255, 'g': 255, 'b': 0 }, // YELLOW
                    { 'r': 192, 'g': 192, 'b': 192 } // GREY
                ],
                'parent': 'body'
            };

            $.extend(defaults, opts);

            return new DrawingMenu(defaults);
        },
        RECT: 'RECT',
        POLY: 'POLY'
    };
});
