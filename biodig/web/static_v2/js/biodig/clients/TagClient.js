var deps = [
    'jquery', 'lib/util', 'lib/settings', 'biodig/clients/URLBuilderFactory'
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
        var self=this;
        // Add the Authorization Header only if the token is set
        var addAuthToken = this.token ?
            function (xhr) {
                xhr.setRequestHeader('Authorization', 'Token ' + self.token) ;
            } :
            function(xhr) {};

        return $.Deferred(function(deferredObj) {
            $.ajax({
                url : self.url,
                method : 'POST',
                beforeSend : addAuthToken,
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
        var self=this;
        var addAuthToken = this.token ?
            function (xhr) {
                xhr.setRequestHeader('Authorization', 'Token ' + self.token) ;
            } :
            function(xhr) {};
        return $.Deferred(function(deferredObj) {
            $.ajax({
                url : self.url + id,
                method : 'GET',
                beforeSend : addAuthToken,
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
        var addAuthToken = this.token ?
            function (xhr) {
                xhr.setRequestHeader('Authorization', 'Token ' + self.token) ;
            } :
            function(xhr) {};


      return $.Deferred(function(deferredObj) {
            $.ajax({
                url: urlBuilder.complete(),
                method: 'GET',
                beforeSend : addAuthToken,
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

   TagClient.prototype.update = function(TagId) {
        try {
            this.validator.update(TagId);
        }
        catch (e) {
            return $.Deferred(function(deferredObj) {
                deferredObj.reject(e);
            }).promise();
        }
        var self = this;
        var addAuthToken = this.token ?
            function (xhr) {
                xhr.setRequestHeader('Authorization', 'Token ' + self.token) ;
            } :
            function(xhr) {};
        var data = {
            name : name
        };

        return $.Deferred(function(deferredObj) {
            $.ajax({
                url: self.url + TagId,
                method: 'PUT',
                beforeSend : addAuthToken,
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
