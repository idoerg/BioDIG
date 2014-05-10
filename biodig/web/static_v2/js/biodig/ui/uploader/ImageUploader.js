var deps = [
    'jquery', 'underscore', 'lib/util', 'settings', 'biodig/ui/uploader/UploadItem',
    'text!biodig/tmpl/imageuploader/uploader.html'
];

define(deps, function($, _, util, settings, UploadItem, ImageUploaderTmpl) {

    var ImageUploaderTemplate = _.template(ImageUploaderTmpl);

    var Helper = {
        bindEvents: function() {
            var self = this;
            // highlight the images overlay button on mouseover
            $(document).on({
                mouseenter: function() {
                    self.$uploader.find('button[name="add-images-overlay"]').addClass('uploader-menu-button-hover');
                },
                mouseleave: function() {
                    self.$uploader.find('button[name="add-images-overlay"]').removeClass('uploader-menu-button-hover');
                }
            }, this.$uploader.find('input[name="add-images"]'));

            // Clicking clear uploads should remove all uploads
            this.$uploader.find('button[name="clear-uploads"]').on('click', function() {
                $.each(self.completed, function(id, item) {
                    item.remove();
                });
            });

            // clicking clear all should remove everyting from the body
            this.$uploader.find('button[name="clear-all"]').on('click', function() {
                $.each(self.queued, function(id, item) {
                    item.remove();
                });

                $.each(self.completed, function(id, item) {
                    item.remove();
                });
            });

            // starting the uploads should start every upload
            this.$uploader.find('button[name="start-uploads"]').on('click', function() {
                $.each(self.queued, function(id, item) {
                    item.upload();
                });
            });

            // image upload change (the big one)
            this.$uploader.find('input[name="add-images"]').on('change', function() {
                if ($(this)[0].files) {
                    var file = $(this)[0].files[0];
                    var fileInputClone = $(this).clone();

                    if (Helper.is_image(file)) {
                        var reader = new FileReader();
                        var item = UploadItem.create(file);

                        reader.onload = function(e) {
                            item.image(e.target.result);
                        };

                        item.on('remove', function() {
                            if (self.queued[item.uid()]) {
                                delete self.queued[item.uid()];
                            }

                            if (self.completed[item.uid()]) {
                                delete self.completed[item.uid()];
                            }
                        });

                        item.on('success', function() {
                            self.completed[item.uid()] = self.queued[item.uid()];
                            delete self.queued[item.uid()];
                        });

                        self.queued[item.uid()] = item;

                        self.$body.append(item.view());
                        reader.readAsDataURL(file);
                    }
                }
            });
        },
        is_image: function(file) {
            if (file.type.indexOf('image') !== -1) {
                return true;
            }
            else {
                var accepted = util.set('gif', 'jpg', 'png', 'tiff', 'jpeg', 'bmp');
                var ext = file.name.substring(file.name.lastIndexOf('.') + 1).toLowerCase();
                return set.contains(ext);
            }
        }
    }


    function ImageUploader(selector) {
        this.$container = $(selector);
        this.$uploader = $(ImageUploaderTemplate(settings));
        this.$container.append(this.$uploader);
        this.$body = this.$uploader.find('.uploader-body');
        this.completed = {};
        this.queued = {};
        util.scope(this, Helper.bindEvents)();
    }

    return {
        create: function(selector) {
            return new ImageUploader(selector);
        }
    }
});
