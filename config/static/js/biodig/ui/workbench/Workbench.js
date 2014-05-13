var deps = [
    'jquery', 'underscore', 'settings', 'biodig/ui/workbench/Toolbar',
    'biodig/ui/taggable/Taggable', 'text!biodig/tmpl/workbench/structure.html'
];

define(deps, function($, _, settings, Toolbar, Taggable, StructureTmpl) {

    var StructureTemplate = _.template(StructureTmpl);

    function Workbench(selector, user) {
        this.$container = $(selector);
        this.$el = $(StructureTemplate({ 'settings' : settings }));
        this.$container.append(this.$el);

        this.toolbar = Toolbar.create(this.$el.find('.workbench-toolbar-outside'), user);
        this.$workArea = this.$el.find('.work-area');

        var self = this;

        var imageFn = function(e, image) {
            // clear out the old taggable plugin
            self.$workArea.empty();

            // make the img tag for the Taggable plugin from the image data
            var $image = $('<img />').width(560).attr('src', image.url).data('imageId', image.id);
            self.$workArea.append($image);

            Taggable.create($image, { 'mode' : Taggable.MODES.REGISTERED, 'alreadyLoaded': false });
        };

        $(this.toolbar.get('PublicImages')).on('image:click', imageFn);
        //$(this.toolbar.get('RecentlyViewedImages')).on('image:click', imageFn);
    }

    return {
        create: function(selector, user) {
            return new Workbench(selector, user);
        }
    }

});
