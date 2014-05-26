var deps = [
    'jquery', 'underscore', 'beetledig/clients/OrthologClient',
    'text!beetledig/tmpl/orthologlist.html'
];

define(deps, function($, _, OrthologClient, OrthologListTmpl) {

    var OrthologListTemplate = _.template(OrthologListTmpl);

    function OrthologViewer(selector, TC) {
        this.$container = $(selector);
        this.client = OrthologClient.create();

        var self = this;

        $.when(this.client.get(TC))
            .done(function(ortho_list) {
                var $orthoView = $(OrthologListTemplate({
                    'ortho_list' : ortho_list
                }));
 
                self.$container.append($orthoView);
            })
            .fail(function(e) {
                self.$container.append('ERROR: ' + (e.detail || e.message));
            });
    }

    return {
        create : function(selector, TC) {
            if (!TC) {
                selector = $(selector);
                TC = selector.data('tcId');
            }
            return new OrthologViewer(selector, TC);
        }
    }

});
