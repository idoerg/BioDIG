var deps = [
    'jquery', 'settings', 'biodig/clients/URLBuilderFactory',
    'lib/util'
];

define(deps, function($, settings, URLBuilderFactory, util) {

    /**
     *  Organism Client constructor that takes in the options
     *  such as url.
     *
     *  @param opts: The options to customize this client.
    **/
    function ChadoClient(opts) {
        this.url = opts.url;
        if (this.url[this.url.length -1] != '/') {
            this.url += '/';
        }

        this.token = opts.token || null;
    }

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
    ChadoClient.prototype.organisms = function(opts) {
        if (!opts) opts = {};
        var urlBuilder = URLBuilderFactory.newBuilder(this.url + 'organisms/');
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

    ChadoClient.prototype.features = function(organism_id) {
        var self = this;

        return $.Deferred(function(deferredObj) {
            $.ajax({
                url: self.url + 'organisms/' + organism_id + '/features/',
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

    ChadoClient.prototype.cvterms = function(cv, opts) {
        var self = this;

        if (!opts) opts = {};
        var urlBuilder = URLBuilderFactory.newBuilder(self.url + 'cv/' + cv + '/terms/');
        $.each(opts, function(key, val) {
            urlBuilder.addQuery(key, val, URLBuilderFactory.NOT_EMPTY);
        });

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
        url: settings.SITE_URL + 'rest/v2/chado/',
        token: null
    };

    return {
        /**
         *  Creates an instance of the Image Client.
        **/
        create: function(opts) {
            return new ChadoClient($.extend({}, defaults, opts));
        }
    };
});
