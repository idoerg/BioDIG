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
        this.tags_cache = {
            'all': {}
        };
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

    ImageDao.prototype.addOrganism = function(id) {
        var self = this;
        return $.Deferred(function(deferred_obj) {
            $.when(self.imageOrganismClient.create(id))
                .done(function(imageOrg) {
                    self.organisms_cache[id] = imageOrg;
                    $(self).trigger('change:organisms');
                    deferred_obj.resolve(imageOrg);
                })
                .fail(function(e) {
                    deferred_obj.reject(e);
                });
        });
    };

    ImageDao.prototype.deleteOrganism = function(id) {
        var self = this;
        return $.Deferred(function(deferred_obj) {
            $.when(self.imageOrganismClient.delete(id))
                .done(function(imageOrg) {
                    delete self.organisms_cache[id];
                    $(self).trigger('change:organisms');
                    deferred_obj.resolve(imageOrg);
                })
                .fail(function(e) {
                    deferred_obj.reject(e);
                });
        });
    };

    ImageDao.prototype.organisms = function() {
        var self = this;
        if (this.organisms_cache == null) {
            return $.Deferred(function(deferred_obj) {
                $.when(self.imageOrganismClient.list())
                    .done(function(organisms) {
                        self.organisms_cache = {};
                        $.each(organisms, function(id, organism) {
                            self.organisms_cache[organism.id] = organism;
                        });

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

    ImageDao.prototype.addTagGroup = function(opts) {
        var self = this;
        return $.Deferred(function(deferred_obj) {
            $.when(self.tagGroupClient.create(opts.name))
                .done(function(tagGroup) {
                    tagGroup.visible = false;
                    self.tagGroups_cache[tagGroup.id] = tagGroup;
                    self.tags_cache[tagGroup.id] = {
                        client: TagClient.create({
                            'image_id' : self.image_id,
                            'tag_group_id' : tagGroup.id
                        }),
                        tags: null
                    };
                    deferred_obj.resolve(tagGroup);
                })
                .fail(function(e) {
                    deferred_obj.reject(e);
                });
        });
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

    ImageDao.prototype.deleteTagGroup = function(id) {
        var self = this;
        return $.Deferred(function(deferred_obj) {
            $.when(self.tagGroupClient.delete(id))
                .done(function(tagGroup) {
                    // update the imageDao to delete all of the tag group's
                    // information including tags and gene links
                    // TODO: Delete gene links
                    delete self.tagGroups_cache[tagGroup.id];
                    $.each(self.tags_cache, function(tagGroupId, group) {
                        if (group.tags) {
                            $.each(group.tags, function(tagId, tag) {
                                if (tag.group == tagGroup.id) {
                                    delete self.tags_cache[tagGroupId][tagId];
                                    delete self.tags_cache.all[tagId];
                                }
                            })
                        }
                    });
                    deferred_obj.resolve(tagGroup);
                })
                .fail(function(e) {
                    deferred_obj.reject(e);
                });
        });
    };

    ImageDao.prototype.tags = function(tagGroup_ids, opts) {
        if (!tagGroup_ids) throw { 'detail' : 'Please provide a list of TagGroup ids' }
        if (!opts) opts = {};
        if (!$.isArray(tagGroup_ids)) tagGroup_ids = [tagGroup_ids];

        var self = this;
        var tags = {};
        var promises = [];
        $.each(tagGroup_ids, function(index, tagGroupId) {
            if (!self.tags_cache[tagGroupId]) {
                throw { 'detail' : "Please retrieve the tag group information first for group: " + tagGroupId }
            }
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
                                self.tags_cache.all[tag.id] = tag;
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

    ImageDao.prototype.addTag = function(opts) {
        var self = this;
        return $.Deferred(function(deferred_obj) {
            // find the correct tag client
            var client = self.tags_cache[opts.group].client;

            $.when(client.create(opts.name, opts.points, opts.color))
                .done(function(tag) {
                    self.tags_cache[tag.id] = tag;
                    self.tags_cache.all[tag.id] = tag;
                    deferred_obj.resolve(tag);
                })
                .fail(function(e) {
                    deferred_obj.reject(e);
                });
        });
    };

    ImageDao.prototype.editTag = function(id, opts) {
        var self = this;
        return $.Deferred(function(deferred_obj) {
            // find the correct tag client
            var client = self.tags_cache[self.tags_cache.all[id].group].client;

            $.when(client.update(id, opts.name))
                .done(function(tag) {
                    self.tags_cache[tag.id] = tag;
                    self.tags_cache.all[tag.id] = tag;
                    deferred_obj.resolve(tag);
                })
                .fail(function(e) {
                    deferred_obj.reject(e);
                });
        });
    };

    ImageDao.prototype.deleteTag = function(id) {
        var self = this;
        return $.Deferred(function(deferred_obj) {
            // find the correct tag client
            var client = self.tags_cache[self.tags_cache.all[id].group].client;

            $.when(client.delete(id))
                .done(function(tag) {
                    // update the imageDao to delete all of the tag's
                    // information including tags and gene links
                    // TODO: Delete gene links
                    delete self.tags_cache[tag.group].tags[id];
                    delete self.tags_cache.all[id];
                    deferred_obj.resolve(tag);
                })
                .fail(function(e) {
                    deferred_obj.reject(e);
                });
        });
    };

    ImageDao.prototype.geneLinks = function(tag_id) {

    };

    return {
        create: function(image_id) {
            return new ImageDao(image_id);
        }
    }
});
