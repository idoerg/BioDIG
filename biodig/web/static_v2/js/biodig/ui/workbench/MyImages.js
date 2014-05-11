var deps = [
    'jquery', 'underscore', 'biodig/clients/ImageClient', 'biodig/ui/workbench/ImageItem',
    'text!biodig/tmpl/workbench/toolbar-menu.html'
];

define(deps, function($, _, ImageClient, ImageItem, ToolbarMenuTmpl) {

    var ToolbarMenuTemplate = _.template(ToolbarMenuTmpl);

    function MyImages(user) {
        this.$el = $(ToolbarMenuTemplate());
        this.$body = this.$el.find('.toolbar-body');
        this.client = ImageClient.create();

        var self = this;
        $.when(this.client.list({ 'owner' : user }))
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
            })
            .fail(function(e) {
                self.$body.text("Unable to retrieve images");
            });
    }

    MyImages.prototype.view = function() {
        return this.$el;
    };

    MyImages.prototype.name = function() {
        return "MyImages";
    }

    return {
        create: function(user) {
            return new MyImages(user);
        }
    }

});
