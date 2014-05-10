var deps = [
    'jquery', 'underscore', 'lib/util', 'settings', 'biodig/clients/ImageClient',
    'text!biodig/tmpl/imageuploader/item.html'
];

define(deps, function($, _, util, settings, ImageClient, UploadItemTmpl) {
    var UploadItemTemplate = _.template(UploadItemTmpl);

    function UploadItem(file) {
        this.$el = $(UploadItemTemplate({
            'settings': settings,
            'file': file
        }));

        this.client = ImageClient.create();
        this.uuid = util.uuid4();
        this.file = file;

        // setup the ocmponents of the UI
        this.$image = this.$el.find('.preview-thumbnail');
        this.$uploadButton = this.$el.find('button.upload');
        this.$status = this.$el.find('.status-container');
        this.$filename = this.$el.find('.filename');

        this.states = {
            'loading': settings.STATIC_URL + 'images/loading.gif',
            'success': settings.STATIC_URL + 'images/success.png',
            'error': settings.STATIC_URL + 'images/caution.png'
        };

        // setup the image preview
        this.$image.load(function() {
            var $container = $(this).parent();
            var ratio = $(this).width()/$(this).height();
            var containerRatio = $container.width()/$container.height();
            if (ratio > containerRatio) {
                $(this).css('width', $container.width());
                var topVal = ($container.height() - $(this).height())/2;
                $(this).css('top', topVal);
            }
            else if (ratio <= containerRatio) {
                $(this).css('height', $container.height());
                var leftVal = ($container.width() - $(this).width())/2;
                $(this).css('left', leftVal);
            }
        });

        // setup close button click event to remove the section
        var self = this;
        this.$el.find('.close-button').on('click', util.scope(this, self.remove));

        // Setup the upload button to start the upload and update the UI
        this.$uploadButton.on('click', function() {
            self.upload();
        });
    }

    UploadItem.prototype.image = function(src) {
        this.$image.attr('src', src);
    };

    UploadItem.prototype.view = function() {
        return this.$el;
    };

    UploadItem.prototype.uid = function() {
        return this.uuid;
    };

    UploadItem.prototype.remove = function() {
        var self = this;
        this.$el.slideUp('slow', function() { self.$el.remove(); });
        $(this).trigger('remove');
    };

    UploadItem.prototype.upload = function() {
        var description = this.$el.find('textarea[name="description"]');
        var altText = this.$el.find('textarea[name="alt-text"]');
        var self = this;

        // update view to show a loading state
        this.$uploadButton.attr('disabled', true).parent().addClass('disabled-cell-container');
        this.$status.removeClass('hidden').addClass('show').attr('src', self.states['loading']);

        $.when(self.client.create(self.file, description, altText))
            .done(function(image) {
                self.$status.find('.status').attr('src', self.states['success']);
                var filename = image.url.split('/');
                filename = filename[filename.length - 1];
                self.$filename.text(filename);

                $(self).trigger('success');
            })
            .fail(function(e) {
                self.$uploadButton.attr('disabled', false).parent().removeClass('disabled-cell-container');
                self.$status.find('.status').attr('src', self.states['error']);
            });
    };

    return {
        create: function(file) {
            return new UploadItem(file);
        }
    }
});
