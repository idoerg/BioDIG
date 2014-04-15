var deps = [
    'jquery', 'biodig/clients/ImageClient', 'biodig/clients/ImageOrganismClient',
    'biodig/clients/TagGroupClient'
];

define(deps, function($, ImageClient, ImageOrganismClient, TagGroupClient) {

    function ImageDao(image_id) {
        this.image_id = image_id;
        this.imageClient = ImageClient.create();
        this.tagGroupClient = TagGroupClient.create({ 'image_id' : image_id });
        this.imageOrganismClient = ImageOrganismClient.create({ 'image_id' : image_id });

        this.organisms_cache = null;
        this.tagGroups_cache = null;
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
                resolve(self.metadata_cache);
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
                resolve(self.organisms_cache);
            }).promise();
        }
    };

    ImageDao.prototype.tagGroups = function(opts) {
        var self = this;
        if (this.tagGroups_cache == null) {
            return $.Deferred(function(deferred_obj) {
                $.when(self.tagGroupClient.list())
                    .done(function(tagGroups) {
                        // add the tags section into the tag groups
                        // object to be checked later and switch to
                        // a dictionary rather than an array
                        var groups = {};
                        $.each(tagGroups, function(index, tagGroup) {
                            tagGroup['tags'] = null;
                            tagGroup['visible'] = false;
                            groups[tagGroup.id] = tagGroup;
                        });

                        self.tagGroups_cache = groups;
                        if (opts.visible === true) {
                            deferred_object.resolve({});
                        }
                        else {
                            deferred_obj.resolve(groups);
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

                resolve(groups);
            }).promise();
        }
    };

    ImageDao.prototype.tags = function(tagGroup_id) {

    };

    ImageDao.prototype.geneLinks = function(tag_id) {

    };

    return {
        create: function(image_id) {
            return new ImageDao(image_id);
        }
    }
});
