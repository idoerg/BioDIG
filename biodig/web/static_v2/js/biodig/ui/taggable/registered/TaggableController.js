var deps = [
    'jquery', 'lib/util'
];

define(deps, function($, util) {

    var Helper = {
        setupZoomControls: function() {
            var self = this;
            $(self.zoomable).on('zoom.registered', function() {
                self.drawingBoard.resize();
            });
        },
        setupDialogControls: function() {
            var self = this;
            $.each(DialogControls.setup, function(key, fn) {
                util.scope(self, fn)();
            });
        },
        setupMenuControls: function() {
            var self = this;
            $.each(MenuControls.setup, function(key, fn) {
                util.scope(self, fn)();
            });
        },
        setupDrawingControls: function() {
            var self = this;
            $.each(DrawingControls.setup, function(key, fn) {
                util.scope(self, fn)();
            });
        },
        tearDownZoomableControls: function() {
            $(self.zoomable).off('zoom.registered');
        },
        tearDownDialogControls: function() {
            var self = this;
            $.each(DialogControls.tearDown, function(key, fn) {
                util.scope(self, fn)();
            });
        },
        tearDownMenuControls: function() {
            var self = this;
            $.each(MenuControls.tearDown, function(key, fn) {
                util.scope(self, fn)();
            });
        },
        tearDownDrawingControls: function() {
            var self = this;
            $.each(DrawingControls.tearDown, function(key, fn) {
                util.scope(self, fn)();
            });
        }
    };

    function TaggableController(taggable) {
        this.taggable = taggable;

        this.controllers = {
            'on' : {
                'dialog': util.scope(this.taggable, Helper.setupDialogControls),
                'zoom': util.scope(this.taggable, Helper.setupZoomControls),
                'menu': util.scope(this.taggable, Helper.setupMenuControls),
                'drawing': util.scope(this.taggable, Helper.setupDrawingControls)
            },
            'off' : {
                'dialog': util.scope(this.taggable, Helper.tearDownDialogControls),
                'zoom': util.scope(this.taggable, Helper.tearDownZoomControls),
                'menu': util.scope(this.taggable, Helper.tearDownMenuControls),
                'drawing': util.scope(this.taggable, Helper.tearDownDrawingControls)
            }
        }
    }

    TaggableController.prototype.controls = function(state, type) {
        state = state.toLowerCase() == 'on' ? 'on' : 'off';
        this.controllers[state][type]();
    };

    var MenuControls = {
        setup: {
            tagGroups: function() {
                var self = this;
                // handle the events for clicking to manage tag groups
                this.menu.section('tagGroups').item('add').on('click', function() {
                    self.dialogs.get('AddTagGroup').show();
                });

                this.menu.section('tagGroups').item('edit').on('click', function() {
                    $.when(self.imageDao.tagGroups())
                        .done(function(tagGroups) {
                            self.dialogs.get('EditTagGroup').show({ 'tagGroups' : tagGroups});
                        })
                        .fail(function(e) {
                            console.error(e.detail || e.message);
                        });
                });

                this.menu.section('tagGroups').item('delete').on('click', function() {
                    $.when(self.imageDao.tagGroups())
                        .done(function(tagGroups) {
                            self.dialogs.get('DeleteTagGroup').show(tagGroups);
                        })
                        .fail(function(e) {
                            console.error(e.detail || e.message);
                        });
                });
            },
            organisms: function() {
                var self = this;
                // handle the events for clicking to manage organisms on the image
                this.menu.section('organisms').item('add').on('click', function() {
                    $.when(self.organismDao.organisms())
                        .done(function(organisms) {
                            self.dialogs.get('AddOrganism').show(organisms);
                        })
                        .fail(function(e) {
                            console.error(e.detail || e.message);
                        });
                });

                this.menu.section('organisms').item('delete').on('click', function() {
                    $.when(self.imageDao.organisms())
                        .done(function(organisms) {
                            self.dialogs.get('DeleteOrganism').show(organisms);
                        })
                        .fail(function(e) {
                            console.error(e.detail || e.message);
                        });
                });
            },
            tags: function() {
                var self = this;
                // handle the events for clicking to manage the tags on the page
                this.menu.section('tags').item('add').on('click', function() {
                    // TODO: Access the DrawingMenu and display it
                });

                this.menu.section('tags').item('edit').on('click', function() {
                    if ($.isEmptyObject(self.tagBoard.selected())) {
                        // no tags are selected so we will start with the
                        // tag groups and place the tags in the tag groups for
                        // future menus
                        $.when(self.imageDao.tagGroups())
                            .done(function(tagGroups) {
                                var ids = $.map(tagGroups, function(tagGroup) {
                                    return tagGroup.id;
                                });

                                $.when(self.imageDao.tags(ids))
                                    .done(function(tags) {
                                        // add the tags subsection
                                        $.each(tagGroups, function(id, tagGroup) {
                                            tagGroup.tags = {};
                                        });

                                        $.each(tags, function(id, tag) {
                                            tagGroups[tag.group].tags[tag.id] = tag;
                                        });

                                        // telling it that tag groups are given makes its so
                                        // that the dialog knows to start at the choose tag group
                                        // dialog instead of the choose tag dialog
                                        self.dialogs.get('EditTag').show({
                                            "tagGroups" : tagGroups
                                        });
                                    })
                                    .fail(function(e) {
                                        console.error(e.detail || e.message);
                                    });
                            })
                            .fail(function(e) {
                                console.error(e.detail || e.message);
                            });
                    }
                    else {
                        // if tags are selected then we want to only show those
                        // and proceed directly to the choose tag dialog
                        self.dialogs.get('EditTag').show({
                            "tags" : self.tagBoard.selected()
                        });
                    }
                });

                this.menu.section('tags').item('delete').on('click', function() {
                    if ($.isEmptyObject(self.tagBoard.selected)) {
                        // no tags are selected so we will show all tags
                        $.when(self.imageDao.tags())
                            .done(function(tags) {
                                self.dialogs.get('DeleteTag').show(tags);
                            })
                            .fail(function(e) {
                                console.error(e.detail || e.message);
                            });
                    }
                    else {
                        // if tags are selected then we want to only show those
                        self.dialogs.get('DeleteTag').show(self.tagBoard.selected);
                    }
                });
            },
            geneLinks: function() {
                var self = this;
                this.menu.section('geneLinks').item('add').on('click', function() {
                    if ($.isEmptyObject(self.tagBoard.selected)) {
                        // no tags are selected so we will show all tags
                        $.when(self.imageDao.tags())
                            .done(function(tags) {
                                self.dialogs.get('AddGeneLink').show(tags);
                            })
                            .fail(function(e) {
                                console.error(e.detail || e.message);
                            });
                    }
                    else {
                        // if tags are selected then we want to only show those
                        self.dialogs.get('DeleteTag').show(self.tagBoard.selected);
                    }
                });

                this.menu.section('geneLinks').item('delete').on('click', function() {

                });
            }
        },
        tearDown: {
            tagGroups: function() {

            },
            organisms: function() {

            },
            tags: function() {

            },
            geneLinks: function() {

            }
        }
    };

    var DialogControls = {
        setup: {
            tagGroups: function() {
                var self = this;
                $(this.dialogs.get('EditTagGroup')).on('accept', function(event, $el, data) {
                    $.when(self.imageDao.editTagGroup(data.id, data))
                        .done(function(tagGroup) {
                            console.log("Successful save of tag group: " + tagGroup);
                        })
                        .fail(function(e) {
                            console.error(e.detail || e.message);
                        })
                });
            }
        },
        tearDown: {
            tagGroups: function() {
                $(this.dialogs.get('EditTagGroup')).off('accept');
            }
        }
    };

    var DrawingControls = {
        setup: {

        },
        tearDown: {

        }
    };

    return {
        create: function(taggable) {
            return new TaggableController(taggable);
        }
    }
});
