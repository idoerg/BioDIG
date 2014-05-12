var deps = [
    'jquery', 'lib/util', 'settings', 'biodig/clients/URLBuilderFactory'
];

define(deps, function($, util, settings, URLBuilder) {

    /**
     *  Validator for a Tag client.
    **/
    var ValidatorFactory = {
        getInstance: function() {
            // validator
            return {
                create: function(tag_id, organism_id, feature_id) {
                    if (!tag_id || isNaN(tag_id)) {
                        throw { detail : 'The id is not a valid positive number' }
                    }
                    if (!organism_id || isNaN(organism_id)) {
                        throw { detail : 'The id is not a valid positive number' }
                    }
                    if (!feature_id || isNaN(feature_id)) {
                        throw { detail : 'The id is not a valid positive number' }
                    }
                },
                get: function(TagId) {
                    if (!TagId || isNaN(TagId)) throw { detail : 'The id is not a valid positive number' }
                },
                list: function(opts) {
                    if (opts) {
                        if ('owner' in opts && (!opts['owner'] || isNaN(opts['owner']))) {
                            throw { detail : 'The owner is not a valid positive number' }
                        }
                        if ('offset' in opts && (!opts['offset'] || isNaN(opts['offset']))) {
                             throw { detail : 'Offset is not a positive number' }
                        }
                        if ('limit' in opts && (!opts['limit'] || isNaN(opts['limit']))) {
                             throw { detail : 'Limit is not a positive number' }
                        }
                    }
                },
                delete: function(id) {
                    if (!id || isNaN(id)) throw { detail : 'The id is not a valid positive number' }
                }
            }
        }
    };


    /**
     *  GeneLinkClient constructor that takes in the options
     *  such as url.
     *
     *  @param opts: The options to customize this client.
    **/
    function GeneLinkClient(opts) {
        if (! ('image_id' in opts)){
            throw { detail : 'Image ID is necessary for Tag Client use' };
        }
        if (! ('tag_group_id' in opts)){
            throw { detail : 'Tag Group ID is necessary for Tag Client use' };
        }
        if (! ('tag_id' in opts)){
            throw { detail : 'Tag ID is necessary for Tag Client use' };
        }

        this.url = util.format(opts.url, opts.image_id, opts.tag_group_id, opts.tag_id);

        if (this.url[this.url.length -1] != '/') {
                this.url += '/';
        }
        this.validator = ValidatorFactory.getInstance();
        this.token = opts.token || null;
    }

    GeneLinkClient.prototype.create = function(tag_id, organism_id, feature_id) {
        try {
            this.validator.create(tag_id, organism_id, feature_id);
        }
        catch (e) {
            return $.Deferred(function(deferredObj) {
                deferredObj.reject(e);
            }).promise();
        }

        var self = this;

        return $.Deferred(function(deferredObj) {
            $.ajax({
                url : self.url,
                method : 'POST',
                beforeSend : util.auth(self.token),
                dataType : 'json',
                data : {
                    'tag_id': tag_id,
                    'organism_id': organism_id,
                    'feature_id': feature_id
                },
                success : function(data) {
                    deferredObj.resolve(data);
                },
                error : function(jqXHR, textStatus, errorThrown) {
                    var e = $.parseJSON(jqXHR.responseText);
                    deferredObj.reject(e);
                }
            });

        }).promise();
    };

    GeneLinkClient.prototype.get = function(id) {
        try {
            this.validator.get(id);
        }
        catch (e) {
            return $.Deferred(function(deferredObj) {
                deferredObj.reject(e);
            }).promise();
        }
        var self = this;

        return $.Deferred(function(deferredObj) {
            $.ajax({
                url : self.url + id,
                method : 'GET',
                beforeSend : util.auth(self.token),
                dataType : 'json',
                success : function(data) {
                    deferredObj.resolve(data);
                },
                error : function(jqXHR, textStatus, errorThrown) {
                    var e = $.parseJSON(jqXHR.responseText);
                    deferredObj.reject(e);
                }
            });

        }).promise();
    };

    GeneLinkClient.prototype.list = function(opts) {
        try {
            if (!opts) opts = {};
            this.validator.list(opts);
        }
        catch (e) {
            return $.Deferred(function(deferredObj) {
                deferredObj.reject(e);
            }).promise();
        }

        var urlBuilder = URLBuilder.newBuilder(this.url);
        $.each(opts, function(key, val) {
            urlBuilder.addQuery(key, val, URLBuilder.NOT_EMPTY);
        });

        var self = this;


        return $.Deferred(function(deferredObj) {
            $.ajax({
                url: urlBuilder.complete(),
                method: 'GET',
                beforeSend : util.auth(self.token),
                success: function(data, textStatus, jqXHR) {
                    deferredObj.resolve(data);
                },
                error: function(jqXHR, textStatus, errorThrown) {
                    var e = $.parseJSON(jqXHR.responseText);
                    deferredObj.reject(e);
                }
           });

        }).promise();
    };

    GeneLinkClient.prototype.delete = function(id) {
        try {
            this.validator.delete(id);
        }
        catch (e) {
            return $.Deferred(function(deferredObj) {
                deferredObj.reject(e);
            }).promise();
        }

        var self = this;

        return $.Deferred(function(deferredObj) {
            $.ajax({
                url: self.url + id,
                beforeSend: util.auth(self.token),
                method: 'DELETE',
                success: function(data) {
                    deferredObj.resolve(data);
                },
                error: function(jqXHR, textStatus, errorThrown) {
                    try {
                        var e = $.parseJSON(jqXHR.responseText);
                        deferredObj.reject(e);
                    }
                    catch (e) {
                        deferredObj.reject({ detail: 'An unidentified error occurred with the server.'});
                    }
                }
            });
        }).promise();
    }



    var defaults = {
        url : settings.SITE_URL + 'rest/v2/images/{0}/tagGroups/{1}/tags/{2}/geneLinks/'
    };

    var GeneLinkClientFactory = {
        create: function(opts) {
            return new GeneLinkClient($.extend({}, defaults, opts));
        }
    };

    return GeneLinkClientFactory;
});
