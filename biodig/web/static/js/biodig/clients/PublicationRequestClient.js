var deps = [
    'jquery', 'settings', 'biodig/clients/URLBuilderFactory',
    'lib/util'
];

define(deps, function($, settings, URLBuilderFactory, util) {

    /**
     *  Validator for the image client.
    **/
    var ValidatorFactory = {
        getInstance: function() {
            // validator
            return {
                create: function(organism_id) {
                    if (!organism_id || isNaN(organism_id)) throw { detail : 'The organism_id is not a valid positive number' }
                },
                delete: function(organism_id) {
                    if (!organism_id || isNaN(organism_id)) throw { detail : 'The organism_id is not a valid positive number' }
                }
            }
        }
    };

    /**
     *  PublicationRequestClient Client constructor that takes in the options
     *  such as url.
     *
     *  @param opts: The options to customize this client.
    **/
    function PublicationRequestClient(opts) {

        this.url = opts.url
        if (this.url[this.url.length -1] != '/') {
            this.url += '/';
        }

        this.token = opts.token || null;
        this.validator = ValidatorFactory.getInstance();
    }

    PublicationRequestClient.prototype.create = function(image_id) {
        try {
            this.validator.create(image_id);
        }
        catch (e) {
            return $.Deferred(function(deferredObj) {
                deferredObj.reject(e);
            }).promise();
        }

        var self = this;

        return $.Deferred(function(deferredObj) {
            $.ajax({
                url: self.url,
                method: 'POST',
                beforeSend: util.auth(self.token),
                dataType: 'json',
                data: {
                    'image_id' : image_id
                },
                success: function(data, textStatus, jqXHR) {
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
    };

    PublicationRequestClient.prototype.preview = function(image_id) {
        try {
            this.validator.create(image_id);
        }
        catch (e) {
            return $.Deferred(function(deferredObj) {
                deferredObj.reject(e);
            }).promise();
        }

        var self = this;

        return $.Deferred(function(deferredObj) {
            $.ajax({
                url: self.url,
                method: 'POST',
                beforeSend: util.auth(self.token),
                dataType: 'json',
                data: {
                    'image_id' : image_id,
                    'preview': true
                },
                success: function(data, textStatus, jqXHR) {
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
    };

    PublicationRequestClient.prototype.previewRequest = function(publication_request_id) {
        try {
            this.validator.create(publication_request_id);
        }
        catch (e) {
            return $.Deferred(function(deferredObj) {
                deferredObj.reject(e);
            }).promise();
        }

        var self = this;

        return $.Deferred(function(deferredObj) {
            $.ajax({
                url: self.url + publication_request_id + '/preview/',
                method: 'GET',
                beforeSend: util.auth(self.token),
                dataType: 'json',
                success: function(data, textStatus, jqXHR) {
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
    };

    PublicationRequestClient.prototype.list = function(opts) {
        if (!opts) opts = {};
        var urlBuilder = URLBuilderFactory.newBuilder(this.url);
        $.each(opts, function(key, val) {
            urlBuilder.addQuery(key, val, URLBuilderFactory.NOT_EMPTY);
        });

        var self = this;

        return $.Deferred(function(deferredObj) {
            $.ajax({
                url: urlBuilder.complete(),
                beforeSend: util.auth(self.token),
                method: 'GET',
                success: function(data, textStatus, jqXHR) {
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
    };

    /**
     *  Deletes the given organism from image with the description and altText, which
     *  are optional.
     *
     *  @param description: The new description of the image.
    **/
    PublicationRequestClient.prototype.delete = function(id) {
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

    PublicationRequestClient.prototype.approve = function(id) {
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
                method: 'PUT',
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

    // default settings for a PublicatoinRequestClient
    var defaults = {
        url: settings.SITE_URL + 'rest/v2/publicationRequests/',
        token: null
    };

    return {
        /**
         *  Creates an instance of the Image Client.
        **/
        create: function(opts) {
            return new PublicationRequestClient($.extend({}, defaults, opts));
        }
    };
});
