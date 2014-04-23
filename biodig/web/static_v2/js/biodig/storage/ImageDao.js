var deps = [
    'jquery', 'biodig/clients/ImageClient', 'biodig/clients/ImageOrganismClient',
    'biodig/clients/TagGroupClient', 'biodig/clients/TagClient'
];

define(deps, function($, ImageClient, ImageOrganismClient, TagGroupClient, TagClient) {

    function ImageDao(image_id) {
        this.image_id = image_id;
        this.imageClient = ImageClient.create();
        this.tagGroupClient = TagGroupClient.create({ 'image_id' : image_id });
        this.imageOrganismClient = ImageOrganismClient.create({ 'image_id' : image_id });

        this.organisms_cache = null;
        this.tagGroups_cache = null;
        this.tags_cache = null;
        this.geneLinks_cache = null;
        this.metadata_cache = null;
    }

    ImageDao.prototype.metadata = function() {
        var self = this;
        if (this.metadata_cache == null) {
            return $.Deferred(function(deferred_obj) {
                $.when(self.imageClient.get(self.image_id))
                    .done(function(metadata) {
                        self.metadata_cache = metadata;
                        deferred_obj.resolve(metadata);
                    })
                    .fail(function(e) {
                        deferred_obj.reject(e);
                    });
            }).promise();
        }
        else {
            return $.Deferred(function(deferred_obj) {
                deferred_obj.resolve(self.metadata_cache);
            }).promise();
        }
    };

    ImageDao.prototype.organisms = function() {
        var self = this;
        if (this.organisms_cache == null) {
            return $.Deferred(function(deferred_obj) {
                $.when(self.imageOrganismClient.list())
                    .done(function(organisms) {
                        self.organisms_cache = organisms;
                        deferred_obj.resolve(organisms);
                    })
                    .fail(function(e) {
                        deferred_obj.reject(e);
                    });
            }).promise();
        }
        else {
            return $.Deferred(function(deferred_obj) {
                deferred_obj.resolve(self.organisms_cache);
            }).promise();
        }
    };

    ImageDao.prototype.tagGroups = function(opts) {
        if (!opts) opts = {};
        var self = this;
        if (this.tagGroups_cache == null) {
            return $.Deferred(function(deferred_obj) {
                $.when(self.tagGroupClient.list())
                    .done(function(tagGroups) {
                        // add the tags section into the tag groups
                        // object to be checked later and switch to
                        // a dictionary rather than an array
                        self.tags_cache = {};
                        self.tagGroups_cache = {};
                        $.each(tagGroups, function(index, tagGroup) {
                            // setup the new clients for each tag group to
                            // fetch the tags in the tag cache
                            self.tags_cache[tagGroup.id] = {
                                client: TagClient.create({
                                    'image_id' : self.image_id,
                                    'tag_group_id' : tagGroup.id
                                }),
                                tags: null
                            };
                            tagGroup['visible'] = false;
                            self.tagGroups_cache[tagGroup.id] = tagGroup;
                        });

                        if (opts.visible === true) {
                            deferred_object.resolve({});
                        }
                        else {
                            deferred_obj.resolve(self.tagGroups_cache);
                        }
                    })
                    .fail(function(e) {
                        deferred_obj.reject(e);
                    });
            }).promise();
        }
        else {
            return $.Deferred(function(deferred_obj) {
                var groups = self.tagGroups_cache;
                if (opts.visible === true || opts.visible === false) {
                    var filter = {};
                    $.each(groups, function(id, group) {
                        if (group.visible === opts.visible) {
                            filter[id] = group;
                        }
                    });
                    groups = filter;
                }

                deferred_obj.resolve(groups);
            }).promise();
        }
    };

    ImageDao.prototype.editTagGroup = function(id, opts) {
        var self = this;
        return $.Deferred(function(deferred_obj) {
            $.when(self.tagGroupClient.update(id, opts.name))
                .done(function(tagGroup) {
                    self.tagGroups_cache[tagGroup.id] = tagGroup;
                    deferred_obj.resolve(tagGroup);
                })
                .fail(function(e) {
                    deferred_obj.reject(e);
                });
        });
    };

    ImageDao.prototype.tags = function(tagGroup_ids, opts) {
        if (!opts) opts = {};
        if (!$.isArray(tagGroup_ids)) tagGroup_ids = [tagGroup_ids];

        var self = this;
        var tags = {};
        var promises = [];
        $.each(tagGroup_ids, function(index, tagGroupId) {
            if (self.tags_cache[tagGroupId].tags == null) {
                if (!self.tags_cache[tagGroupId].client) {
                    self.tags_cache[tagGroupId].client = TagClient.create({
                        'image_id': self.image_id,
                        'tag_group_id': tagGroupId
                    });
                }

                promises.push($.Deferred(function(deferred_obj) {
                    $.when(self.tags_cache[tagGroupId].client.list())
                        .done(function(tag_results) {
                            if (self.tags_cache[tagGroupId].tags == null) {
                                self.tags_cache[tagGroupId].tags = {};
                            }

                            $.each(tag_results, function(index, tag) {
                                self.tags_cache[tagGroupId].tags[tag.id] = tag;
                                tags[tag.id] = tag;
                            });

                            deferred_obj.resolve();
                        })
                        .fail(function(e) {
                            deferred_obj.reject(e);
                        });
                }).promise());
            }
            else {
                promises.push($.Deferred(function(deferred_obj) {
                    $.extend(tags, self.tags_cache[tagGroupId].tags);
                    deferred_obj.resolve();
                }).promise());
            }
        });

        return $.Deferred(function(deferred_obj) {
            $.when.apply($, promises)
                .done(function() {
                    deferred_obj.resolve(tags);
                })
                .fail(function(e) {
                    deferred_obj.reject(e.detail);
                });
        }).promise();
    };

    ImageDao.prototype.geneLinks = function(tag_id) {

    };

    return {
        create: function(image_id) {
            return new ImageDao(image_id);
        }
    }
});
