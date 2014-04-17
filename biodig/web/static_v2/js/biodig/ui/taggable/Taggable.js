var deps = [
    'jquery', 'underscore', 'biodig/ui/zoomable/Zoomable', 'biodig/ui/taggable/TagBoard',
    'biodig/storage/ImageDao', 'biodig/ui/taggable/ImageMenu', 'biodig/ui/taggable/DialogManager',
    'lib/util', 'text!biodig/tmpl/taggable/structure.html',
    'text!biodig/tmpl/taggable/image-metadata.html',

];

define(deps, function($, _, Zoomable, TagBoard, ImageDao, ImageMenu, DialogManager, util,
    TaggableTmpl, MetadataTmpl) {

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

        // creates a canvas with methods for viewing tags and selecting them
        this.zoomable = Zoomable.create(this.image, $.extend({}, opts, {
            onload: util.scope(this, TaggableImageHelper.loadDrawingModule)
        });

        // create the right side of the taggable interface

        // the title of the right side is determined by the list of organisms
        // on the image
        var self = this;

        $.when(this.imageDao.organisms())
            .done(function(organisms) {
                if (organisms.length > 0) {
                    var organisms_text = []
                    $.each(organisms, function(index, organism) {
                        organisms_text.push(organism.common_name);
                    });
                    self.$right.find('.organism-title').text(", ".join(organisms_text));
                }
                else {
                    self.$right.find('.organism-title').text("No Organisms Added");
                }
            })
            .fail(function(e) {
                console.error(e.detail);
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
        loadDrawingModule: function() {
            this.tagBoard = TagBoard.create(this.$image, opts);

            util.scope(this, TaggableImageHelper.addPublicMenuControls).call();

            util.scope(this, TaggableImageHelper.addPublicDialogControls).call();

            // optionally install the registered features
            if (opts.mode == ACCEPTED_MODES.REGISTERED) {
                // tells the dialog manager that the registered user dialogs
                // are required, so all dialog related functions are loaded here
                $.when(this.dialogs.loadRegistered()).done(function() {
                    // creates a canvas with methods for drawing tags
                    //this.drawingBoard = DrawingBoard.create(this.$image);
                    //this.drawingUI = DrawingUI.create('hidden');

                    //util.scope(this, TaggableImageHelper.addRegisteredControls).call();
                });
            }
        },
        addPublicMenuControls: function() {
            var self = this;

            // toggles the visibility of the tags for the currently selected tag groups
            this.menu.section('tools').item('toggleTags').click(function() {
                $.when(self.imageDao.tagGroups({ visible: true }))
                    .done(function(tagGroups) {
                        var group_ids = $.map(tagGroups, function(tagGroup) {
                            return tagGroup.id;
                        });

                        $.when(self.imageDao.tags({ 'tagGroups' : group_ids }))
                            .done(function(tags) {
                                self.tagBoard.draw(tags);
                            })
                            .fail(function(e) {
                                console.error(e.detail);
                            });
                    })
                    .fail(function(e) {
                        console.error(e.detail);
                    })
            });

            // shows the download dialog for downloading image metadata
            this.menu.section('tools').item('download').click(function() {
                self.dialogs.dialog('DownloadMetadata').show();
            });

            this.menu.section('tools').item('zoomIn').click(function() {
                self.zoomable.zoom(1);
            });

            this.menu.section('tools').item('zoomOut').click(function() {
                self.zoomable.zoom(-1);
            });

            this.menu.section('tagGroups').item('changeVisibleTagGroups').click(function() {
                $.when(self.imageDao.tagGroups())
                    .done(function(tagGroups) {
                        self.dialogs.dialog('ChangeVisibleTagGroups').show({'tagGroups' : tagGroups});
                    })
                    .fail(function(e) {
                        console.error(e.detail);
                    });
            });
        },
        addPublicDialogControls: function() {
            var self = this;
            $(this.dialogs.dialog('ChangeVisibleTagGroups')).on('accept', function(event, ui) {
                // get the selected tag groups from the ui
                var visibleGroups = ui.find('input[type="checkbox"]:checked').map(function() {
                    return $(this).data('tag-group-id');
                }).get();

                // update the tag groups that should be visible and the
                // tag groups that should be invisible
                $.when(self.imageDao.tagGroups())
                    .done(function(tagGroups) {
                        $.each(tagGroups, function(id, tagGroup) {
                            tagGroup.visible = id in visibleGroups;
                        });
                    })
                    .fail(function(e) {
                        console.error(e.detail);
                    });


                // update the tag board with the tags for the newly visible tag groups
                $.when(self.imageDao.tags({ 'tagGroups' : visibleGroups }))
                    .done(function(tags) {
                        self.tagBoard.draw(tags);
                    })
                    .fail(function(e) {
                        console.error(e.detail);
                    });
            });

            $(this.dialogs.dialog('DownloadMetadata')).on('accept', function(event, ui) {
                console.log("Image metadata download started...");
            });
        },
        addRegisteredControls: function() {
            // TODO: implement these features
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
