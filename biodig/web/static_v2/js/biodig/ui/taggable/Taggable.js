var deps = [
    'jquery', 'underscore', 'biodig/ui/zoomable/Zoomable', 'biodig/ui/taggable/TagBoard',
    'biodig/storage/ImageDao', 'biodig/storage/OrganismDao', 'biodig/ui/taggable/ImageMenu',
    'biodig/ui/taggable/DialogManager', 'biodig/ui/taggable/public/TaggableController',
    'biodig/ui/taggable/DrawingBoard', 'biodig/ui/taggable/registered/TaggableController', 'lib/util',
    'text!biodig/tmpl/taggable/structure.html', 'text!biodig/tmpl/taggable/image-metadata.html'
];

define(deps, function($, _, Zoomable, TagBoard, ImageDao, OrganismDao, ImageMenu, DialogManager,
    PublicTaggableController, DrawingBoard, RegisteredTaggableController, util, TaggableTmpl,
    MetadataTmpl) {

    var ACCEPTED_MODES = {
        REGISTERED: 'REGISTERED',
        PUBLIC: 'PUBLIC'
    };

    var TaggableTemplate = _.template(TaggableTmpl);
    var MetadataTemplate = _.template(MetadataTmpl);

    function TaggableImage(selector, opts) {
        // check to see if features were directly requested
        // otherwise use the "mode" to determine the feature set
        this.image = selector;
        this.$image = $(selector);
        this.image_id = this.$image.data('image-id') || opts.image_id;
        if (!this.image_id) {
            throw {
                'detail' : "No image_id given for the TaggableImage interface"
            };
        }

        // sets up the UI for the taggable plugin initially
        this.$container = this.$image.parent();
        this.$contents = $(TaggableTemplate());

        // define the three sections of the UI
        this.$left = this.$contents.children('.taggable-left');
        this.$right = this.$contents.children('.taggable-right');
        this.$toolbar = this.$contents.children('.toolbar-container');


        if (!ACCEPTED_MODES[opts.mode]) opts.mode = ACCEPTED_MODES.REGISTERED;

        this.$container.find('*').not(this.$image).remove();
        this.$container.prepend(this.$contents);
        // relocate the image to the left side
        this.$left.append(this.$image);

        // install the public features

        // creates the correct menu for the given mode
        this.menu = ImageMenu.create(this.$toolbar, opts.mode);

        // create the public dialog boxes
        this.dialogs = DialogManager.create();

        // create the image data manager for storing the current internal
        // state of the image's data
        this.imageDao = ImageDao.create(this.image_id);

        // start the public taggable controller
        this.publicController = PublicTaggableController.create(this);

        var self = this;

        // creates a canvas with methods for viewing tags and selecting them
        this.zoomable = Zoomable.create(this.image, $.extend({}, opts, {
            onload: function() {
                util.scope(self, TaggableImageHelper.loadDrawingModule)(opts);
            }
        }));

        this.publicController.controls('on', 'zoom');

        // create the right side of the taggable interface

        // the title of the right side is determined by the list of organisms
        // on the image

        var createOrganismsView = function(organisms) {
            if (!$.isEmptyObject(organisms)) {
                var organisms_text = []
                $.each(organisms, function(index, organism) {
                    organisms_text.push(organism.common_name);
                });
                self.$right.find('.organism-title').text(organisms_text.join(", "));
            }
            else {
                self.$right.find('.organism-title').text("No Organisms Added");
            }
        };

        $.when(this.imageDao.organisms())
            .done(function(organisms) {
                createOrganismsView(organisms);
            })
            .fail(function(e) {
                console.error(e.detail);
            });

        $(this.imageDao).on('change:organisms', function() {
            $.when(self.imageDao.organisms())
                .done(function(organisms) {
                    createOrganismsView(organisms);
                })
                .fail(function(e) {
                    console.error(e.detail);
                });
        });

        $.when(this.imageDao.metadata())
            .done(function(metadata) {
                self.$right.find('.image-metadata').append($(MetadataTemplate(metadata)));
            })
            .fail(function(e) {
                console.error(e.detail);
            });
    }

    var TaggableImageHelper = {
        loadDrawingModule: function(opts) {
            var self = this;
            this.tagBoard = TagBoard.create(this.$image);

            this.publicController.controls('on', 'dialog');
            this.publicController.controls('on', 'menu');

            // optionally install the registered features
            if (opts.mode == ACCEPTED_MODES.REGISTERED) {
                // tells the dialog manager that the registered user dialogs
                // are required, so all dialog related functions are loaded here
                this.drawingBoard = DrawingBoard.create(this.$image);
                //this.drawingMenu = DrawingMenu.create('hidden');
                this.registeredController = RegisteredTaggableController.create(this);

                this.organismDao = OrganismDao.create();

                // start off by allowing the drawing menu to affect the drawing board
                // and the main menu to control the drawing/tag board
                this.registeredController.controls('on', 'zoom');
                this.registeredController.controls('on', 'drawing');
                this.registeredController.controls('on', 'menu');

                $.when(this.dialogs.loadRegistered()).done(function() {
                    // creates a canvas with methods for drawing tags
                    self.registeredController.controls('on', 'dialog');
                });
            }
        }
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
