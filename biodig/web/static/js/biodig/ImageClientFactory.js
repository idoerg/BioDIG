define(['jquery'], function($) {

    /**
        Validator for the image client.
    **/
    var ValidatorFactory = {
        getInstance: function() {
            // validator
            return {
                create: function(imageData, description, altText) {
                    if (!imageData) throw { validation_error : 'Image data was empty or null.' }

                    if (!description) throw { validation_error : 'The description of the image was empty.' }

                    if (!altText) throw { validation_error : 'The alternate text for this image is empty' }
                }
            }
        }
    };

    /**
        Image Client constructor that takes in the options
        such as url.

        @param opts: The options to customize this client.
    **/
    function ImageClient(opts) {
        this.url = opts.url;
        if (this.url[this.url.length - 1] != '/') {
            this.url += '/';
        }

        this.validator = ValidatorFactory.getInstance();
    }

    /**
        Creates an image on the server by sending the data over
        to the server when enacted. An error state callback will be
        called on validation error. The error will contain information
        about the validation error.

        @param imageData: The raw data from a FileReader in Base64 encoding
                          for the image to send.
        @param description: The description of the image.
        @param altText: The alternate text for this image.

        @return A deferred object that will enact the correct server action
                to create the image.
    **/
    ImageClient.prototype.createImage = function(imageData, description, altText) {
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
        Gets a list of images that is paginated. Allows for filtering
        by owner and date.

        @param owner: The username of the owner to search.
        @param date: The formatted date string
    **/
    ImageClient.prototype.getImages = function(owner, date) {

    };

    ImageClient.prototype.getImage = function() {

    }

    // default settings for an ImageClient
    var settings = {

    };

    var ImageClientFactory = {
        /**
            Creates an instance of the Image Client.
        **/
        getInstance: function(opts) {
            return new ImageClient($.extend({}, settings, opts));
        }
    }; 

    return ImageClientFactory;
});
