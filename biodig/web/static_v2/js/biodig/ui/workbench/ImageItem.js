var deps = [
    'jquery', 'underscore', 'text!biodig/tmpl/workbench/imageitem.html'
];

define(deps, function($, _, ImageItemTmpl) {
    var ImageItemTemplate = _.template(ImageItemTmpl);

    function ImageItem(image) {
        this.$el = ImageItemTemplate({
            'image': image
        });
        this.image = image;

        var self = this;
        this.$el.on('click', function() {
            $(self).trigger('click');
        });

        this.$el.find('.delete-image-button').on('click', function() {
            $(self).trigger('delete');
        });
    }

    ImageItem.prototype.view = function() {
        return this.$el;
    }

    return {
        create: function(image) {
            return new ImageItem(image);
        }
    };
});
