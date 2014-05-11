var deps = [
    'jquery', 'biodig/clients/OrganismClient'
];

define(deps, function($, OrganismClient) {

    function OrganismDao() {
        this.organismClient = OrganismClient.create();
        this.organisms_cache = null;
    }

    OrganismDao.prototype.organisms = function() {
        var self = this;
        if (this.organisms_cache == null) {
            return $.Deferred(function(deferred_obj) {
                $.when(self.organismClient.list())
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

    return {
        create: function() {
            return new OrganismDao();
        }
    }
});
