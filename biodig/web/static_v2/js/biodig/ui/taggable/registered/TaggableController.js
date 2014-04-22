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
        state = state.lower() == 'on' ? 'on' : 'off';
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
                            self.dialogs.get('EditTagGroup').show(tagGroups);
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
                // handle the events for clicking to manage the tags on the page
                this.menu.section('tags').item('add').on('click', function() {
                    // TODO: Access the DrawingMenu and display it
                });

                this.menu.section('tags').item('edit').on('click', function() {
                    if ($.isEmptyObject(self.tagBoard.selected)) {
                        // no tags are selected so we will show all tags
                        $.when(self.imageDao.tags())
                            .done(function(tags) {
                                self.dialogs.get('EditTag').show(tags);
                            })
                            .fail(function(e) {
                                console.error(e.detail || e.message);
                            });
                    }
                    else {
                        // if tags are selected then we want to only show those
                        self.dialogs.get('EditTag').show(self.tagBoard.selected);
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

    return {
        create: function(taggable) {
            return new TaggableController(taggable);
        }
    }
});