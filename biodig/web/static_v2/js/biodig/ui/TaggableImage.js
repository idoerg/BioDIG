var deps = ['jquery', 'underscore', 'text!biodig/tmpl/taggable.html'];

define(deps, function($, _, TaggableTmpl) {

    var ACCEPTED_MODES = {
        REGISTERED: 'REGISTERED',
        PUBLIC: 'PUBLIC'
    };

    function TaggableImage(selector, opts) {
        // check to see if features were directly requested
        // otherwise use the "mode" to determine the feature set
        this.image = selector;
        this.$image = $(selector);
        this.$image_id = this.$image.data('image-id') || opts.image_id;
        if (!this.$image_id) {
            throw {
                'detail' : "No image_id given for the TaggableImage interface"
            };
        }

        // sets up the UI for the taggable plugin initially
        this.$container = this.$image.parent();
        this.$contents = $(_.template(TaggableTmpl)());

        // define the three sections of the UI
        this.$left = this.$contents.find('.taggable-left');
        this.$right = this.$contents.find('.taggable-right');
        this.$toolbar = this.$contents.find('.toolbar-container');

        this.features = [];

        if (opts.features) {
            throw {
                detail: "TaggableImage: Individual features not implemented at this time."
            };
        }
        else {
            if (!ACCEPTED_MODES[opts.mode]) opts.mode = ACCEPTED_MODES.REGISTERED;
        }

        this.$container.find('*').not(this.$image).remove();
        this.$container.prepend(this.$contents);
        // relocate the image to the left side
        this.$left.append(this.$image);
    }

    return {
        create: function(selector, opts) {
            var defaults = {
                'mode': 'registered' // registered or public
            };

            $.extend(defaults, opts);

            return new TaggableImage(selector, defaults);
        },
        MODES: ACCEPTED_MODES
    }
});
