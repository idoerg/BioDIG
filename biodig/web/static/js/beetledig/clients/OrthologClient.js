var deps = [
    'jquery', 'settings', 'lib/util'
];

define(deps, function($, settings, util) {

    /**
     *  Validator for the User client.
    **/
    var ValidatorFactory = {
        getInstance: function() {
            // validator
            return {
                get: function(TC_id) {
                    if (!TC_id ||TC_id.length<=3 ||TC_id.substring(0,3)!="TC_") throw { detail : 'The id is not a valid TC Number' }
                }
            };
	}
    };

    /**
     *  Ortholog Client constructor that takes in the options
     *  such as url.
     *
     *  @param opts: The options to customize this client.
    **/
    function OrthologClient(opts) {
        this.url = opts.url;
        if (this.url[this.url.length - 1] != '/') {
            this.url += '/';
        }

        this.token = opts.token || null;

        this.validator = ValidatorFactory.getInstance();
    }


    /**
     *  Gets a single User given the id.
     *
     *  @param id: The id of the User.
    **/
    OrthologClient.prototype.get = function(TC_id) {
        try {
            this.validator.get(TC_id);
        }
        catch (e) {
            return $.Deferred(function(deferredObj) {
                deferredObj.reject(e);
            });
        }

        var self = this;

        return $.Deferred(function(deferredObj) {
            $.ajax({
                url: self.url + TC_id,
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


    OrthologClient.prototype.list = function() {
        var self = this;

        return $.Deferred(function(deferredObj) {
            $.ajax({
                url: self.url ,
                method: 'GET',
                beforeSend: util.auth(self.token),
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

    // default settings for an UserClient
    var defaults = {
        url: settings.SITE_URL + 'rest/beetles/orthologs/',
        token: null
    };

    var OrthologClientFactory = {
        /**
         *  Creates an instance of the User Client.
        **/
        create: function(opts) {
            return new OrthologClient($.extend({}, defaults, opts));
        }
    };

    return OrthologClientFactory;
});
