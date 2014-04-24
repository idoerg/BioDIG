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
     *  Organism Client constructor that takes in the options
     *  such as url.
     *
     *  @param opts: The options to customize this client.
    **/
    function OrganismClient(opts) {
        if (! ('image_id' in opts)){
            throw { detail : 'Image ID is necessary for Organism Client use' };
        }

        this.url = util.format(opts.url, opts.image_id);
        if (this.url[this.url.length -1] != '/') {
            this.url += '/';
        }

        this.token = opts.token || null;
        this.validator = ValidatorFactory.getInstance();
    }

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
    OrganismClient.prototype.list = function(opts) {
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

    // default settings for an ImageClient
    var defaults = {
        url: settings.SITE_URL + 'rest/v2/organisms/',
        token: null
    };

    return {
        /**
         *  Creates an instance of the Image Client.
        **/
        create: function(opts) {
            return new OrganismClient($.extend({}, defaults, opts));
        }
    };
});
