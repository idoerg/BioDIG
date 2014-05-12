var deps = [
    'jquery', 'underscore', 'lib/util', 'biodig/clients/PublicationRequestClient',
    'biodig/clients/UserClient', 'biodig/clients/ImageClient', 'biodig/ui/dialogs/DynamicDialog',
    'text!biodig/tmpl/taggable/publication/request-preview.html',
    'text!biodig/tmpl/dashboard/publication-request-container.html',
    'text!biodig/tmpl/dashboard/publication-request.html'
];

define(deps, function($, _, util, PublicationRequestClient, UserClient, ImageClient, DynamicDialog,
    PublicationRequestPreviewTmpl, PublicationRequestContainerTmpl, PublicationRequestTmpl) {

    var PublicationRequestContainerTemplate = _.template(PublicationRequestContainerTmpl);
    var PublicationRequestTemplate = _.template(PublicationRequestTmpl);
    var PublicationRequestPreviewTemplate = _.template(PublicationRequestPreviewTmpl);

    function PublicationRequestDashboard(selector) {
        this.$container = $(selector);
        this.$el = $(PublicationRequestContainerTemplate());
        this.$container.append(this.$el);

        this.preview = DynamicDialog.create('PublicationRequestPreview', 'Publication Request Preview',
            PublicationRequestPreviewTemplate);

        this.client = PublicationRequestClient.create();
        this.userClient = UserClient.create();
        this.imageClient = ImageClient.create();

        this.publicationRequests = {};

        var self = this;
        $.when(this.client.list())
            .done(function(publicationRequests) {
                if (publicationRequests.length == 0) {
                    this.$el.append('<div class="panel-body">There are no Publication Requests at this time</div>');
                }

                $.each(publicationRequests, function(id, publicationReq) {
                    $.when(self.userClient.get(publicationReq.owner))
                        .done(function(user) {
                            $.when(self.imageClient.get(publicationReq.target))
                                .done(function(image) {
                                    publicationReq.user = user;
                                    publicationReq.image = image;
                                    publicationReq.dateCreated = util.prettyDate(publicationReq.dateCreated);
                                    var $req = $(PublicationRequestTemplate(publicationReq));
                                    self.$el.append($req);
                                    publicationReq.$el = $req;
                                    self.publicationRequests[publicationReq.id] = publicationReq;

                                    $req.find('button[name="preview"]').on('click', function() {
                                        $.when(self.client.previewRequest(publicationReq.id))
                                            .done(function(preview) {
                                                self.preview.show(preview);
                                            })
                                            .fail(function(e) {
                                                console.error(e.detail || e.message);
                                            });
                                    });

                                    $req.find('button[name="publish"]').on('click', function() {
                                        $.when(self.client.approve(publicationReq.id))
                                            .done(function() {
                                                self.publicationRequests[publicationReq.id].$el.remove();
                                                delete self.publicationRequests[publicationReq.id];
                                            })
                                            .fail(function(e) {
                                                console.error(e.detail || e.message);
                                            });
                                    });

                                    $req.find('button[name="deny"]').on('click', function() {
                                        $.when(self.client.delete(publicationReq.id))
                                            .done(function() {
                                                self.publicationRequests[publicationReq.id].$el.remove();
                                                delete self.publicationRequests[publicationReq.id];
                                            })
                                            .fail(function(e) {
                                                console.error(e.detail || e.message);
                                            });
                                    });
                                })
                                .fail(function(e) {
                                    console.error(e.detail || e.message);
                                });
                        })
                        .fail(function(e) {
                            console.error(e.detail || e.message);
                        })
                });
            })
            .fail(function(e) {
                console.error(e.detail || e.message);
            });
    }




    return {
        create: function(selector) {
            return new PublicationRequestDashboard(selector);
        }
    };
});
