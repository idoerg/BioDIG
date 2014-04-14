var deps = [
    'jquery', 'underscore', 'settings', 'lib/util', 'biodig/clients/ImageClientFactory',
    'text!biodig/tmpl/imagecell.html', 'text!biodig/tmpl/imagetable.html'
];

define(deps, function($, _, settings, util, ImageClient, ImageCell, ImageTable) {

    var ImagePaginatorHelper = {
        setupControls: function(paginator) {
            // setup the last button
            paginator.$pagination.find('.last.pagination-control').on('click', function() {
                paginator.toPage(Math.ceil(paginator.totalImages / paginator.limit - 1));
            });

            // setup the next button click
            paginator.$pagination.find('.next.pagination-control').on('click', function() {
                paginator.nextPage();
            });

            // setup the previous button click
            paginator.$pagination.find('.previous.pagination-control').on('click', function() {
                paginator.prevPage();
            });

            // setup the first button click
            paginator.$pagination.find('.first.pagination-control').on('click', function() {
                paginator.toPage(0);
            });

            // setup the toPage section
            paginator.$pagination.find('.numbers_holder > input').keyup(function(e) {
                if(e.keyCode == 13) { // presses enter to go to page
                    if (isNaN($(this).val() || $(this).val() - 1 < 0) {
                        console.log("The input to the pagination is invalid with value: " +
                            $(this).val());
                        return;
                    }
                    paginator.toPage($(this).val() - 1);
                }
            });
        },
        fit: function($img, $container) {
            var imgRatio = $img.width()/$img.height();
            var containerRatio = $container.width()/$container.height();
            if (imgRatio > containerRatio) {
                $img.css('width', $container.width());
                var topVal = ($container.height() - $img.height())/2;
                $img.css('top', topVal);
            }
            else if (imgRatio < containerRatio) {
                $img.css('height', $container.height());
                var leftVal = ($container.width() - $img.width())/2;
                $img.css('left', leftVal);
            }
        }
    };

    function ImagePaginator(selector, opts) {
        this.container = selector;
        this.$container = $(selector);

        this.limit = opts.limit;
        this.currentPage = opts.currentPage;
        this.imagesPerRow = opts.imagesPerRow;
        this.urlkey = opts.useActualImages ? 'url' : 'thumbnail';

        this.imageClient = ImageClient.getInstance();

        // add the table to hold all the image cells
        this.$container.empty().append(ImageTable);

        this.$table = this.$container.find('.image-table > table > tbody');
        this.$pagination = this.$container.find('.image-table > .image-pagination');
        this.imageCellTemplate = _.template(ImageCell);

        ImagePaginatorHelper.setupControls(this);

        this.toPage(this.currentPage);
    }

    ImagePaginator.prototype.nextPage = function() {
        this.toPage(this.currentPage + 1);
    };

    ImagePaginator.prototype.prevPage = function() {
        this.toPage(this.currentPage - 1);
    };

    ImagePaginator.prototype.toPage = function(index) {
        if (index < 0) {
            console.log("Paginator index out of bounds at index: " + index + ". Ignoring...");
            return;
        }

        var self = this;

        $.when(this.imageClient.list({ limit: self.limit, offset: index * self.limit }))
            .done(function(images) {
                util.scope(self, self.renderPage)(images, index);
            })
            .fail(util.scope(self, self.renderError));
    };

    ImagePaginator.prototype.renderPage = function(images, index) {
        var self = this;
        this.currentPage = index;
        this.$pagination.find('.numbers_holder > input').val(this.currentPage);
        self.$table.empty();

        var tr;
        $.each(images, function(index, image) {
            if (index % self.imagesPerRow == 0) {
                tr = $('<tr />').appendTo(self.$table);
            }

            image['url'] = image[urlkey];
            image['width'] = (100.0 / this.imagesPerRow) + "%";

            tr.appendTo(self.imageCellTemplate(image));
        });
    };

    ImagePaginator.prototype.renderError = function(error) {
        console.error(error.detail);
    };


    // returns a factory for creating the image paginator
    return {
        create: function(selector, opts) {
            var defaults = {
                'limit' : 20,
                'currentPage' : 1,
                'imagesPerRow' : 5,
                'useActualImages' : false
            };

            $.extend(defaults, opts);
            $.extend(defaults, settings);

            return new ImagePaginator(selector, defaults);
        }
    };
});
