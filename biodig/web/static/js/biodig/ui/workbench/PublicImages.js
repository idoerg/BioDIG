var deps = [
    'jquery', 'underscore', 'settings', 'biodig/clients/ImageClient', 'biodig/ui/workbench/ImageItem',
    'text!biodig/tmpl/workbench/toolbar-menu.html'
];

define(deps, function($, _, settings, ImageClient, ImageItem, ToolbarMenuTmpl) {

    var ToolbarMenuTemplate = _.template(ToolbarMenuTmpl);

    function PublicImages() {
        this.$el = $(ToolbarMenuTemplate({
            'settings': settings,
            'title': 'Public Images'
        }));
        this.$body = this.$el.find('.toolbar-body');
        this.client = ImageClient.create();

        var self = this;
        $.when(this.client.list())
            .done(function(images) {
                $.each(images, function(id, image) {
                    var item = ImageItem.create(image);
                    self.$body.append(item.view());

                    $(item).on('click', function(e) {
                        $(self).trigger('image:click', [item.image]);
                    });

                    $(item).on('delete', function(e) {
                        $.when(self.client.delete(item.image.id))
                            .done(function(image) {
                                item.view().remove();
                            })
                            .fail(function(e) {
                                console.error(e.detail || e.message);
                            });
                    });
                });

                $(self).trigger('render');
            })
            .fail(function(e) {
                self.$body.text("Unable to retrieve images");
            });
    }

    PublicImages.prototype.view = function() {
        return this.$el;
    };

    PublicImages.prototype.name = function() {
        return "PublicImages";
    }

    return {
        create: function() {
            return new PublicImages();
        }
    }

});
