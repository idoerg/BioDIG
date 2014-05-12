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
                create: function(name) {
                    if (!name) throw { detail : 'Not a valid name' }
                },
                get: function(TagId) {
                    if (!TagId || isNaN(TagId)) throw { detail : 'The id is not a valid positive number' }
                },
                list: function(opts) {
                    if (opts) {
                        if ('owner' in opts && (!opts['owner'] || isNaN(opts['owner']))) {
                            throw { detail : 'The owner is not a valid positive number' }
                        }
                        if ('name' in opts && !opts['name']) {
                            throw { detail : 'Not a valid name' }
                        }
                        if ('offset' in opts && (!opts['offset'] || isNaN(opts['offset']))) {
                             throw { detail : 'Offset is not a positive number' }
                        }
                        if ('limit' in opts && (!opts['limit'] || isNaN(opts['limit']))) {
                             throw { detail : 'Limit is not a positive number' }
                        }
                    }
                },
                update: function(tag_id) {
                    if (!tag_id || isNaN(tag_id)) throw { detail : 'The id is not a valid positive number' }
                },
                delete: function(id) {
                    if (!id || isNaN(id)) throw { detail : 'The id is not a valid positive number' }
                }
            }
        }
    };


    /**
     *  TagClient constructor that takes in the options
     *  such as url.
     *
     *  @param opts: The options to customize this client.
    **/
    function TagClient(opts) {
        if (! ('image_id' in opts)){
            throw { detail : 'Image ID is necessary for Tag Client use' };
        }
        if (! ('tag_group_id' in opts)){
            throw { detail : 'Tag Group ID is necessary for Tag Client use' };
        }
        this.url = util.format(opts.url, opts.image_id, opts.tag_group_id);

        if (this.url[this.url.length -1] != '/') {
                this.url += '/';
        }
        this.validator = ValidatorFactory.getInstance();
        this.token = opts.token || null;
    }

    TagClient.prototype.create = function(name,points,color) {
        try {
            this.validator.create(name);
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
                    name: name,
                    points: JSON.stringify(points,null,2),
                    color: JSON.stringify(color,null,2)
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

    TagClient.prototype.get = function(id) {
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

    TagClient.prototype.list = function(opts) {
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

   TagClient.prototype.update = function(id, name, points, color) {
        try {
            this.validator.update(id, name, points, color);
        }
        catch (e) {
            return $.Deferred(function(deferredObj) {
                deferredObj.reject(e);
            }).promise();
        }

        var self = this;

        var data = {};
        if (name) data['name'] = name;
        if (points) data['points'] = JSON.stringify(points,null,2);
        if (color) data['color'] = JSON.stringify(color,null,2);

        return $.Deferred(function(deferredObj) {
            $.ajax({
                url: self.url + id,
                method: 'PUT',
                beforeSend : util.auth(self.token),
                data: data,
                success: function(data) {
                    deferredObj.resolve(data);
                },
                error: function(jqXHR, textStatus, errorThrown) {
                    var e = $.parseJSON(jqXHR.responseText);
                    deferredObj.reject(e);
                }
            });
        }).promise();
    };

    TagClient.prototype.delete = function(id) {
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
        url : settings.SITE_URL + 'rest/v2/images/{0}/tagGroups/{1}/tags/'
    };

    var TagClientFactory = {
        create: function(opts) {
            return new TagClient($.extend({}, defaults, opts));
        }
    };

    return TagClientFactory;
});
