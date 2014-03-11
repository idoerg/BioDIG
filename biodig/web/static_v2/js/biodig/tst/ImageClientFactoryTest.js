require.config({
    shim: {
        jquery: {
            init: function() {
                return $; 
            }
        },
        bootstrap: ['jquery'],
        underscore : {
            exports : '_'
        }
    },
    paths: {
        jquery: '/static_v2/js/lib/jquery/1.10.2/jquery.min',
        underscore: '/static_v2/js/lib/underscore.min',
        bootstrap: '/static_v2/js/lib/bootstrap.min',
        URLBuilderFactory: '/static_v2/js/biodig/URLBuilderFactory',
        ImageClientFactory: '/static_v2/js/biodig/ImageClientFactory'
    }
})

var dependencies = [
    'jquery', 'ImageClientFactory'
];

require(dependencies, function($, ImageClientFactory) {
    var client = ImageClientFactory.getInstance({ url : '/web/rest/v2/images/' });

    $('#CreateImageForm  button[name=submitButton]').on('click', function() {
        var files = $('#CreateImageForm input[name=image]')[0].files;
        if (files.length == 0) {
            console.error("No files selected");
            return;
        }
        var reader = new FileReader();
        reader.readAsDataURL(files[0], 'UTF-8');
        reader.onload = function(evt) {
            var description = $('#CreateImageForm input[name=description]').val();
            var altText = $('#CreateImageForm input[name=altText]').val();
            $.when(client.create(evt.target.result, description, altText))
                .done(function(image) {
                    console.log(image);
                })
                .fail(function(e) {
                    console.error(e);
                });
        };
    });
});
