define(['jquery', 'URLBuilder'], function($, URLBuilder) {

    /**
     *  Validator for the image client.
    **/
    var ValidatorFactory = {
        getInstance: function() {
            // validator
            return {
                create: function(imageData, description, altText) {
                    if (!imageData) throw { validation_error : 'Image data was empty or null' }

                    if (!description) throw { validation_error : 'The description of the image was empty' }

                    if (!altText) throw { validation_error : 'The alternate text for this image is empty' }
                },
                get: function(id) {
                    if (!id || isNan(id)) throw { validation_error : 'The id is not a valid positive number' }
                },
                update: function(id, description, altText) {
                    if (!id || isNan(id)) throw { validation_error : 'The id is not a valid positive number' }
                    
                    if (!description && !altText) throw { validation_error : 'No changes have been made to this image' }
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

        return $.Deferred(function(deferredObj) {
            $.ajax({
                url: this.url,
                method: 'POST',
                data: {
                    image: imageData,
                    description: description,
                    altText: altText
                },
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
        var urlBuilder = URLBuilderFactory.newBuilder(this.url);
        $.each(opts, function(key, val) {
            urlBuilder.addQuery(key, val, URLBuilderFactory.NOT_EMPTY);
        });
        
        return $.Deferred(function(deferredObj) {
            $.ajax({
                url: urlBuilder.complete(),
                method: 'GET',
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
        
        return $.Deferred(function(deferredObj) {
            $.ajax({
                url: this.url + id,
                method: 'GET',
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
        
        return $.Deferred(function(deferredObj) {
            $.ajax({
                url: this.url + id,
                method: 'PUT',
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

    // default settings for an ImageClient
    var settings = {
        url: '/rest/v2/images/'
    };

    var ImageClientFactory = {
        /**
         *  Creates an instance of the Image Client.
        **/
        getInstance: function(opts) {
            return new ImageClient($.extend({}, settings, opts));
        }
    }; 

    return ImageClientFactory;
});
