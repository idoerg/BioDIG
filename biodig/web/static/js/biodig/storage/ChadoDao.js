var deps = [
    'jquery', 'biodig/clients/ChadoClient'
];

define(deps, function($, ChadoClient) {

    function ChadoDao() {
        this.chadoClient = ChadoClient.create();
        this.organisms_cache = null;
        this.features_cache = {};
        this.types_cache = [];
    }

    ChadoDao.prototype.organisms = function() {
        var self = this;
        if (this.organisms_cache == null) {
            return $.Deferred(function(deferred_obj) {
                $.when(self.chadoClient.organisms())
                    .done(function(organisms) {
                        self.organisms_cache = organisms;
                        deferred_obj.resolve(organisms);
                    })
                    .fail(function(e) {
                        deferred_obj.reject(e);
                    });
            }).promise();
        }
        else {
            return $.Deferred(function(deferred_obj) {
                deferred_obj.resolve(self.organisms_cache);
            }).promise();
        }
    };

    ChadoDao.prototype.features = function(organisms) {
        var promises = [];
        var errors = [];
        var data = {};
        var self = this;

        $.each(organisms, function(id, organism) {
            promises.push($.Deferred(function(deferred_obj) {
                if (self.features_cache[id]) {
                    $.extend(data, self.features_cache[id]);
                    deferred_obj.resolve();
                }
                else {
                    $.when(self.chadoClient.features(id))
                        .done(function(features) {
                            self.features_cache[id] = {};
                            $.each(features, function(fid, feature) {
                                feature.organism = id;
                                self.features_cache[id][fid] = feature;
                            });
                            $.extend(data, self.features_cache[id]);
                            deferred_obj.resolve();
                        })
                        .fail(function(e) {
                            errors.push(e);
                            deferred_obj.reject();
                        });
                }
            }).promise());
        });

        return $.Deferred(function(deferred_obj) {
            $.when.apply($, promises).always(function() {
                if (errors) {
                    var e = { 'detail' : '' };
                    $.each(errors, function(index, error) {
                        e.detail += error.detail || error.message + "<br />";
                    });
                    deferred_obj.reject(e);
                }
                else {
                    deferred_obj.resolve(data);
                }
            });
        });
    };

    ChadoDao.prototype.types = function() {
        var self = this;
        if (self.types_cache.length == 0) {
            return $.Deferred(function(deferred_obj) {
                $.when(self.chadoClient.types())
                    .done(function(types) {
                        self.types_cache = types;
                        deferred_obj.resolve(types);
                    })
                    .fail(function(e) {
                        deferred_obj.reject(e);
                    });
            });
        }
        else {
            return $.Deferred(function(deferred_obj) {
                deferred_obj.resolve(self.types_cache);
            });
        }
    };

    return {
        create: function() {
            return new ChadoDao();
        }
    }
});
