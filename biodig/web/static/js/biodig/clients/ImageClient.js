var deps = [
    'jquery', 'settings', 'lib/util', 'biodig/clients/URLBuilderFactory'
];

define(deps, function($, settings, util, URLBuilderFactory) {

    /**
     *  Validator for the image client.
    **/
    var ValidatorFactory = {
        getInstance: function() {
            // validator
            return {
                create: function(imageData, description, altText) {
                    if (!imageData) throw { detail : 'Image data was empty or null' }

                    if (!description) throw { detail : 'The description of the image was empty' }

                    if (!altText) throw { detail : 'The alternate text for this image is empty' }
                },
                get: function(id) {
                    if (!id || isNaN(id)) throw { detail : 'The id is not a valid positive number' }
                },
                update: function(id, description, altText) {
                    if (!id || isNaN(id)) throw { detail : 'The id is not a valid positive number' }

                    if (!description && !altText) throw { detail : 'No changes have been made to this image' }
                },
                delete: function(id) {
                    if (!id || isNaN(id)) throw { detail : 'The id is not a valid positive number' }
                }
            }
        }
    };

    /**
     *  Image Client constructor that takes in the options
     *  such as url.
     *
     *  @param opts: The options to customize this client.
    **/
    function ImageClient(opts) {
        this.url = opts.url;
        if (this.url[this.url.length - 1] != '/') {
            this.url += '/';
        }

        this.token = opts.token || null;

        this.validator = ValidatorFactory.getInstance();
    }

    /**
     *  Creates an image on the server by sending the data over
     *  to the server when enacted. An error state callback will be
     *  called on validation error. The error will contain information
     *  about the validation error.
     *
     *  @param imageData: The raw data from a FileReader in Base64 encoding
     *                    for the image to send.
     *  @param description: The description of the image.
     *  @param altText: The alternate text for this image.
     *
     *  @return A deferred object that will enact the correct server action
     *          to create the image.
    **/
    ImageClient.prototype.create = function(imageData, description, altText) {
        try {
            this.validator.create(imageData, description, altText);
        }
        catch (e) {
            return $.Deferred(function(deferredObj) {
                deferredObj.reject(e);
            }).promise();
        }

        var self = this;

        return $.Deferred(function(deferredObj) {
            var formData = new FormData();
            formData.append('image', imageData);
            formData.append('description', description);
            formData.append('altText', altText);

            $.ajax({
                url: self.url,
                method: 'POST',
                beforeSend: util.auth(self.token),
                contentType: false,
                processData: false,
                data: formData,
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
     *  Gets a list of images that is paginated. Allows for filtering
     *  by owner and date.
     *
     *  @param opts: The optional query parameters for the list function.
     *               Takes the following properties:
     *
     *               owner: The username of the owner to search.
     *               dateCreated: The formatted date string for the date created.
     *               lastModified: The formatted date string for the date last modified.
     *               limit: The number of entries to retrieve.
     *               offset: The number of entries to skip before listing.
    **/
    ImageClient.prototype.list = function(opts) {
        if (!opts) opts = {};
        var urlBuilder = URLBuilderFactory.newBuilder(this.url);
        $.each(opts, function(key, val) {
            urlBuilder.addQuery(key, val, URLBuilderFactory.NOT_EMPTY);
        });

        // Add the Authorization Header only if the token is set
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
     *  Gets a single image given the id.
     *
     *  @param id: The id of the image.
    **/
    ImageClient.prototype.get = function(id) {
        try {
            this.validator.get(id);
        }
        catch (e) {
            return $.Deferred(function(deferredObj) {
                deferredObj.reject(e);
            });
        }

        var self = this;

        return $.Deferred(function(deferredObj) {
            $.ajax({
                url: self.url + id,
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
     *  Updates the given image with the description and altText, which
     *  are optional.
     *
     *  @param description: The new description of the image.
     *  @param altText: The new altText for the image.
    **/
    ImageClient.prototype.update = function(id, description, altText) {
        try {
            this.validator.update(id, description, altText);
        }
        catch (e) {
            return $.Deferred(function(deferredObj) {
                deferredObj.reject(e);
            }).promise();
        }

        var data = {};
        if (description) data['description'] = description;
        if (altText) data['altText'] = altText;

        var self = this;

        return $.Deferred(function(deferredObj) {
            $.ajax({
                url: self.url + id,
                beforeSend: util.auth(self.token),
                method: 'PUT',
                data: data,
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
    };

    ImageClient.prototype.delete = function(id) {
        try {
            this.validator.delete(id);
        }
        catch (e) {
            return $.Deferred(function(deferredObj) {
                deferredObj.reject(e);
            }).promise();
        }

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

    // default settings for an ImageClient
    var defaults = {
        url: settings.SITE_URL + 'rest/v2/images/',
        token: null
    };

    var ImageClientFactory = {
        /**
         *  Creates an instance of the Image Client.
        **/
        create: function(opts) {
            return new ImageClient($.extend({}, defaults, opts));
        }
    };

    return ImageClientFactory;
});
