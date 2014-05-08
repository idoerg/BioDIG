var deps = [
    'jquery', 'lib/util'
];

define(deps, function($, util) {

    var Helper = {
        setupZoomControls: function() {
            var self = this;
            $(self.zoomable).on('zoom.public', function() {
                self.tagBoard.resize();
            });
        },
        setupDialogControls: function() {
            var self = this;
            $(this.dialogs.get('ChangeVisibleTagGroups')).on('accept', function(event, ui) {
                // get the selected tag groups from the ui
                var visibleGroups = ui.find('input[type="checkbox"]:checked').map(function() {
                    return $(this).data('tagGroupId');
                }).get();

                // update the tag groups that should be visible and the
                // tag groups that should be invisible
                var visibleGroupsSet = {};
                $.each(visibleGroups, function(index, group_id) {
                    visibleGroupsSet[group_id] = true;
                });

                $.when(self.imageDao.tagGroups())
                    .done(function(tagGroups) {
                        $.each(tagGroups, function(id, tagGroup) {
                            tagGroup.visible = tagGroup.id in visibleGroupsSet;
                        });
                    })
                    .fail(function(e) {
                        console.error(e.detail);
                    });


                // update the tag board with the tags for the newly visible tag groups
                $.when(self.imageDao.tags(visibleGroups))
                    .done(function(tags) {
                        self.tagBoard.draw(tags);
                    })
                    .fail(function(e) {
                        console.error(e.detail);
                    });
            });

            $(this.dialogs.get('DownloadMetadata')).on('accept', function(event, ui) {
                console.log("Image metadata download started...");
            });
        },
        setupMenuControls: function() {
            var self = this;
            // toggles the visibility of the tags for the currently selected tag groups
            this.menu.section('tools').item('toggleTags').on('click', function() {
                self.tagBoard.toggleVisibility();
            });

            // shows the download dialog for downloading image metadata
            this.menu.section('tools').item('download').on('click', function() {
                self.dialogs.get('DownloadMetadata').show();
            });

            this.menu.section('tools').item('zoomIn').on('click', function() {
                self.zoomable.zoom(1);
            });

            this.menu.section('tools').item('zoomOut').on('click', function() {
                self.zoomable.zoom(-1);
            });

            this.menu.section('tagGroups').item('changeVisibleTagGroups').on('click', function() {
                $.when(self.imageDao.tagGroups())
                    .done(function(tagGroups) {
                        self.dialogs.get('ChangeVisibleTagGroups').show({'tagGroups' : tagGroups});
                    })
                    .fail(function(e) {
                        console.error(e.detail);
                    });
            });
        },
        setupTagBoardControls: function() {
            var self = this;
            $(this.imageDao).on('tagGroups:change tags:change', function() {
                $.when(self.imageDao.tagGroups({'visible' : true}))
                    .done(function(tagGroups) {
                        var ids = $.map(tagGroups, function(tagGroup) {
                            return tagGroup.id;
                        });

                        $.when(self.imageDao.tags(ids))
                            .done(function(tags) {
                                self.tagBoard.draw(tags);
                            })
                            .fail(function(e) {
                                console.error(e.detail || e.message);
                            });
                    })
                    .fail(function() {
                        console.error(e.detail || e.message);
                    });
            });

            $(this.tagBoard).on('mousemove', function(e) {
                $.when(self.imageDao.tagGroups())
                    .done(function(tagGroups) {
                        var tags = self.tagBoard.selected();
                        var display = {};
                        $.each(tags, function(id, tag) {
                            display[id] = $.extend({}, poly.tag, { 'group': tagGroups[tag.group].name });
                            display[id].geneLinks = {};
                        });

                        self.tagInfo.update(display);
                    })
                    .fail(function(e) {
                        console.error(e.detail || e.message);
                    });
            })

        },
        tearDownZoomableControls: function() {
            $(self.zoomable).off('zoom.public');
        },
        tearDownDialogControls: function() {
            $(this.dialogs.get('ChangeVisibleTagGroups')).off('accept');
            $(this.dialogs.get('DownloadMetadata')).off('accept');
        },
        tearDownMenuControls: function() {
            this.menu.section('tools').item('toggleTags').off('click');

            this.menu.section('tools').item('download').off('click');

            this.menu.section('tools').item('zoomIn').off('click');

            this.menu.section('tools').item('zoomOut').off('click');

            this.menu.section('tagGroups').item('changeVisibleTagGroups').off('click');
        },
        tearDownTagBoardControls: function() {
            $(this.imageDao).off('tagGroups:change tags:change');
        }
    };

    function TaggableController(taggable) {
        this.taggable = taggable;

        this.controllers = {
            'on' : {
                'dialog': util.scope(this.taggable, Helper.setupDialogControls),
                'zoom': util.scope(this.taggable, Helper.setupZoomControls),
                'menu': util.scope(this.taggable, Helper.setupMenuControls),
                'tagboard': util.scope(this.taggable, Helper.setupTagBoardControls)
            },
            'off' : {
                'dialog': util.scope(this.taggable, Helper.tearDownDialogControls),
                'zoom': util.scope(this.taggable, Helper.tearDownZoomControls),
                'menu': util.scope(this.taggable, Helper.tearDownMenuControls),
                'tagboard': util.scope(this.taggable, Helper.tearDownTagBoardControls)
            }
        }
    }

    TaggableController.prototype.controls = function(state, type) {
        state = state.toLowerCase() == 'on' ? 'on' : 'off';
        this.controllers[state][type]();
    };

    return {
        create: function(taggable) {
            return new TaggableController(taggable);
        }
    }
});
