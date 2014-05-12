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
                            self.dialogs.get('EditTagGroup').show({ 'tagGroups' : tagGroups });
                        })
                        .fail(function(e) {
                            console.error(e.detail || e.message);
                        });
                });

                this.menu.section('tagGroups').item('delete').on('click', function() {
                    $.when(self.imageDao.tagGroups())
                        .done(function(tagGroups) {
                            self.dialogs.get('DeleteTagGroup').show({ 'tagGroups' : tagGroups });
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
                    $.when(self.chadoDao.organisms())
                        .done(function(organisms) {
                            self.dialogs.get('AddOrganism').show({ 'organisms' : organisms });
                        })
                        .fail(function(e) {
                            console.error(e.detail || e.message);
                        });
                });

                this.menu.section('organisms').item('delete').on('click', function() {
                    $.when(self.imageDao.organisms())
                        .done(function(organisms) {
                            self.dialogs.get('DeleteOrganism').show({ 'organisms' : organisms });
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
                    self.drawingMenu.show();
                    self.drawingBoard.begin();
                });

                this.menu.section('tags').item('edit').on('click', function() {
                    if ($.isEmptyObject(self.tagBoard.selected())) {
                        self.loading.show();
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
                                        self.loading.hide();
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
                                        self.loading.hide();
                                        console.error(e.detail || e.message);
                                    });
                            })
                            .fail(function(e) {
                                self.loading.hide();
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
                    if ($.isEmptyObject(self.tagBoard.selected())) {
                        self.loading.show();
                        $.when(self.imageDao.tagGroups())
                            .done(function(tagGroups) {
                                var ids = $.map(tagGroups, function(tagGroup) {
                                    return tagGroup.id;
                                });
                                // no tags are selected so we will show all tags
                                $.when(self.imageDao.tags(ids))
                                    .done(function(tags) {
                                        self.loading.hide();
                                        self.dialogs.get('DeleteTag').show({ 'tags' : tags });
                                    })
                                    .fail(function(e) {
                                        self.loading.hide();
                                        console.error(e.detail || e.message);
                                    });
                            })
                            .fail(function(e) {
                                self.loading.hide();
                                console.error(e.detail || e.message);
                            });
                    }
                    else {
                        // if tags are selected then we want to only show those
                        self.dialogs.get('DeleteTag').show({
                            'tags': self.tagBoard.selected()
                        });
                    }
                });
            },
            geneLinks: function() {
                var self = this;
                this.menu.section('geneLinks').item('add').on('click', function() {
                    var data = {};
                    var errors = [];
                    var promises = [];

                    self.loading.show();

                    if ($.isEmptyObject(self.tagBoard.selected())) {
                        // get the tag groups and group the tags into the tag groups
                        promises.push($.Deferred(function(deferred_object) {
                            self.imageDao.tagGroups()
                                .done(function(tagGroups) {
                                    var ids = $.map(tagGroups, function(tagGroup) {
                                        tagGroup.tags = {};
                                        return tagGroup.id;
                                    });

                                    $.when(self.imageDao.tags(ids))
                                        .done(function(tags) {
                                            $.each(tags, function(id, tag) {
                                                tagGroups[tag.group].tags[id] = tag;
                                            });

                                            data['tagGroups'] = tagGroups;

                                            deferred_object.resolve();
                                        })
                                        .fail(function(e) {
                                            errors.push(e);
                                            deferred_object.reject();
                                        });
                                })
                                .fail(function(e) {
                                    errors.push(e);
                                    deferred_object.reject();
                                })
                            }).promise()
                        );
                    }
                    else {
                        // if tags are selected then we want to only show those
                        data['tags'] = self.tagBoard.selected();
                    }

                    // get the organisms on this image and lookup
                    // the features associated with those organisms
                    promises.push($.Deferred(function(deferred_object) {
                        $.when(self.imageDao.organisms())
                            .done(function(organisms) {
                                $.when(self.chadoDao.features(organisms))
                                    .done(function(features) {
                                        data['features'] = features;
                                        data['organisms'] = organisms;
                                        deferred_object.resolve();
                                    })
                                    .fail(function(e) {
                                        errors.push(e);
                                        deferred_object.reject();
                                    });
                            })
                            .fail(function(e) {
                                errors.push(e);
                                deferred_object.reject();
                            });
                        }).promise()
                    );

                    // get the types of features
                    promises.push($.Deferred(function(deferred_object) {
                        $.when(self.chadoDao.types())
                            .done(function(types) {
                                data['types'] = types;
                                deferred_object.resolve();
                            })
                            .fail(function(e) {
                                deferred_object.reject();
                            });
                        }).promise()
                    );

                    $.when.apply($, promises).always(function() {
                        self.loading.hide();
                        if (errors.length > 0) {
                            $.each(errors, function(index, error) {
                                self.messager.add(self.messager.ERROR, error.detail || error.message);
                            });
                        }
                        else {
                            self.dialogs.get('AddGeneLink').show(data);
                        }
                    });
                });

                this.menu.section('geneLinks').item('delete').on('click', function() {

                });
            }
        },
        tearDown: {
            tagGroups: function() {
                this.menu.section('tagGroups').item('add').off('click');
                this.menu.section('tagGroups').item('edit').off('click');
                this.menu.section('tagGroups').item('delete').off('click');
            },
            organisms: function() {
                this.menu.section('organisms').item('add').off('click');
                this.menu.section('organisms').item('delete').off('click');
            },
            tags: function() {
                this.menu.section('tags').item('add').off('click');
                this.menu.section('tags').item('edit').off('click')
            },
            geneLinks: function() {
                this.menu.section('geneLinks').item('add').off('click');
                this.menu.section('geneLinks').item('delete').off('click');
            }
        }
    };

    var DialogControls = {
        setup: {
            tagGroups: function() {
                var self = this;

                $(this.dialogs.get('AddTagGroup')).on('accept', function(event, $el) {
                    var data = {
                        'name' : $el.find('input[name="name"]').val()
                    };

                    $.when(self.imageDao.addTagGroup(data))
                        .done(function(tagGroup) {
                            self.messager.add(self.messager.SUCCESS, 'Added tag group "' +
                                data.name + '"');
                        })
                        .fail(function(e) {
                            console.error(e.detail || e.message);
                        })
                });

                $(this.dialogs.get('EditTagGroup')).on('accept', function(event, $el, data) {
                    $.when(self.imageDao.editTagGroup(data.id, data))
                        .done(function(tagGroup) {
                            console.log("Successful save of tag group: " + tagGroup);
                        })
                        .fail(function(e) {
                            console.error(e.detail || e.message);
                        })
                });

                $(this.dialogs.get('DeleteTagGroup')).on('accept', function(event, $el) {
                    var data = $.parseJSON(
                        unescape($el.find('.modal-body').find('.select-tag-group option:selected').data('tagGroup'))
                    );

                    $.when(self.imageDao.deleteTagGroup(data.id))
                        .done(function(tagGroup) {
                            console.log("Successful deletion of tag group: " + tagGroup);
                        })
                        .fail(function(e) {
                            console.error(e.detail || e.message);
                        })
                });
            },
            organisms: function() {
                var self = this;
                $(this.dialogs.get('AddOrganism')).on('accept', function(event, $el) {
                    var data = $.parseJSON(
                        unescape($el.find('.modal-body').find('.select-organism option:selected').data('organism'))
                    );

                    $.when(self.imageDao.addOrganism(data.id))
                        .done(function() {
                            console.log("Successfully added organism: " + data);
                        })
                        .fail(function(e) {
                            console.error(e.detail || e.message);
                        })
                });

                $(this.dialogs.get('DeleteOrganism')).on('accept', function(event, $el) {
                    var data = $.parseJSON(
                        unescape($el.find('.modal-body').find('.select-organism option:selected').data('organism'))
                    );

                    $.when(self.imageDao.deleteOrganism(data.id))
                        .done(function() {
                            console.log("Successfully deleted organism: " + data);
                        })
                        .fail(function(e) {
                            console.error(e.detail || e.message);
                        })
                });
            },
            tags: function() {
                var self = this;
                $(this.dialogs.get('AddTag')).on('accept', function(event, $el, data) {
                    $.when(self.imageDao.addTag(data))
                        .done(function(tag) {
                            self.messager.add(self.messager.SUCCESS, 'Added tag "' + tag.name + '"');
                            self.drawingBoard.hide();
                            self.drawingMenu.hide();
                        })
                        .fail(function(e) {
                            console.error(e.detail || e.message);
                        })
                });

                $(this.dialogs.get('AddTag')).on('cancel', function() {
                    self.drawingBoard.end();
                    self.drawingBoard.hide();
                    self.drawingMenu.hide();
                });

                $(this.dialogs.get('EditTag')).on('accept', function(event, $el, data) {
                    $.when(self.imageDao.editTag(data.id, data))
                        .done(function(tag) {
                            console.log("Successful save of tag group: " + tag);
                        })
                        .fail(function(e) {
                            console.error(e.detail || e.message);
                        })
                });

                $(this.dialogs.get('DeleteTag')).on('accept', function(event, $el) {
                    var data = $.parseJSON(
                        unescape($el.find('.modal-body').find('.select-tag option:selected').data('tag'))
                    );

                    $.when(self.imageDao.deleteTag(data.id))
                        .done(function(tag) {
                            console.log("Successful deletion of tag: " + tag);
                        })
                        .fail(function(e) {
                            console.error(e.detail || e.message);
                        })
                });
            },
            geneLinks: function() {
                $(this.dialogs.get('AddGeneLink')).on('accept', function(event, $el, data) {
                    $.when(self.imageDao.addGeneLink(data))
                        .done(function(geneLink) {
                            self.messager.add(self.messager.SUCCESS, 'Added gene link "' + geneLink.feature.name + '"');
                        })
                        .fail(function(e) {
                            console.error(e.detail || e.message);
                        })
                });
            }
        },
        tearDown: {
            tagGroups: function() {
                $(this.dialogs.get('AddTagGroup')).off('accept');
                $(this.dialogs.get('EditTagGroup')).off('accept');
                $(this.dialogs.get('DeleteTagGroup')).off('accept');
            },
            organisms: function() {
                $(this.dialogs.get('AddOrganism')).off('accept');
                $(this.dialogs.get('DeleteOrganism')).off('accept');
            },
            tags: function() {
                $(this.dialogs.get('EditTag')).off('accept');
            },
            geneLinks: function() {

            }
        }
    };

    var DrawingControls = {
        setup: {
            follow: function() {
                var self = this;
                $(this.tagBoard).on('drag.drawing', function(event, ui) {
                    self.drawingBoard.$board.css('left', ui.position.left).css('top', ui.position.top);
                });
            },
            menu: function() {
                var self = this;
                $(this.drawingMenu).on('submit', function() {
                    self.imageDao.tagGroups()
                        .done(function(tagGroups) {
                            self.drawingBoard.end();

                            var data = {
                                'color': $.extend({}, self.drawingMenu.color, {'a':self.drawingMenu.alpha}),
                                'points': self.drawingBoard.points,
                                'tagGroups': tagGroups
                            };
                            self.dialogs.get('AddTag').show(data);
                        })
                        .fail(function(e) {
                            console.error(e.detail || e.message);
                        });
                });

                $(this.drawingMenu).on('cancel', function() {
                    self.drawingBoard.end();
                });

                $(this.drawingMenu).on('style:change', function() {
                    self.drawingBoard.config('shape', self.drawingMenu.style);
                });

                $(this.drawingMenu).on('color:change alpha:change', function() {
                    var rgb = self.drawingMenu.color;
                    var alpha = self.drawingMenu.alpha;
                    var color = 'rgba(' + rgb.r + ',' + rgb.g + ',' + rgb.b + ',' + alpha + ')';
                    self.drawingBoard.config('fillStyle', color);
                    self.drawingBoard.redraw();
                });
            }
        },
        tearDown: {
            follow: function() {
                $(this.tagBoard).off('drag.drawing');
            },
            menu: function() {
                $(this.drawingMenu).off('submit');
                $(this.drawingMenu).off('style:change');
                $(this.drawingMenu).off('color:change alpha:change');
            }
        }
    };

    return {
        create: function(taggable) {
            return new TaggableController(taggable);
        }
    }
});
