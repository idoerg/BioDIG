var deps = [
    'jquery', 'lib/settings', 'biodig/clients/URLBuilderFactory',
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
                    if (!organism_id || isNan(organism_id)) throw { detail : 'The organism_id is not a valid positive number' }
                },
                delete: function(organism_id) {
                    if (!organism_id || isNan(organism_id)) throw { detail : 'The organism_id is not a valid positive number' }
                }
            }
        }
    };

    /**
     *  ImageOrganism Client constructor that takes in the options
     *  such as url.
     *
     *  @param opts: The options to customize this client.
    **/
    function ImageOrganismClient(opts) {
        if (! ('image_id' in opts)){
            throw { detail : 'Image ID is necessary for ImageOrganism Client use' };
        }

        this.url = util.format(opts.url, opts.image_id);
        if (this.url[this.url.length -1] != '/') {
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
    ImageOrganismClient.prototype.create = function(organism_id) {
        try {
            this.validator.create(organism_id);
        }
        catch (e) {
            return $.Deferred(function(deferredObj) {
                deferredObj.reject(e);
            }).promise();
        }

        var self = this;
        // Add the Authorization Header only if the token is set
        var addAuthToken = this.token ?
            function (xhr) {
                xhr.setRequestHeader('Authorization', 'Token ' + self.token) ;
            } :
            function(xhr) {};

        return $.Deferred(function(deferredObj) {
            $.ajax({
                url: self.url,
                method: 'POST',
                beforeSend: addAuthToken,
                dataType: 'json',
                data: {
                    'organism_id' : organism_id
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

    /**
     *  Gets a list of images that is paginated. Allows for filtering
     *  by owner and date.
     *
     *  @param opts: The optional query parameters for the list function.
     *               Takes the following properties:
     *
     *  		     owner: The username of the owner to search.
     *  			 dateCreated: The formatted date string for the date created.
     *  			 lastModified: The formatted date string for the date last modified.
     *  			 limit: The number of entries to retrieve.
     *               offset: The number of entries to skip before listing.
    **/
    ImageOrganismClient.prototype.list = function(opts) {
    	var urlBuilder = URLBuilderFactory.newBuilder(this.url);
    	$.each(opts, function(key, val) {
    		urlBuilder.addQuery(key, val, URLBuilderFactory.NOT_EMPTY);
    	});

        // Add the Authorization Header only if the token is set
        var self = this;
        var addAuthToken = this.token ?
            function (xhr) {
                xhr.setRequestHeader('Authorization', 'Token ' + self.token) ;
            } :
            function(xhr) {};

    	return $.Deferred(function(deferredObj) {
    		$.ajax({
    			url: urlBuilder.complete(),
                beforeSend: addAuthToken,
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
    ImageOrganismClient.prototype.delete = function(organism_id) {
        try {
            this.validator.delete(id);
        }
        catch (e) {
            return $.Deferred(function(deferredObj) {
                deferredObj.reject(e);
            }).promise();
        }

        var addAuthToken = this.token ?
            function (xhr) {
                xhr.setRequestHeader('Authorization', 'Token ' + self.token) ;
            } :
            function(xhr) {};

        return $.Deferred(function(deferredObj) {
            $.ajax({
                url: self.url + organism_id,
                beforeSend: addAuthToken,
                method: 'DELETE',
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
    }

    // default settings for an ImageClient
    var defaults = {
        url: settings.SITE_URL + 'rest/v2/images/{0}/organisms/',
        token: null
    };

    return {
        /**
         *  Creates an instance of the Image Client.
        **/
        create: function(opts) {
            return new ImageOrganismClient($.extend({}, defaults, opts));
        }
    };
});
