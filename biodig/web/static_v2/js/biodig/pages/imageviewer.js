require.config({
    shim: {
        jquery: {
            init: function() {
                return $;
            }
        },
        bootstrap: ['jquery'],
        jquery_ui: ['jquery'],
        underscore : {
            exports : '_'
        }
    },
    paths: {
        jquery: 'lib/jquery-1.11.0.min',
        underscore: 'lib/underscore.min',
        bootstrap: 'lib/bootstrap.min',
        settings: 'lib/settings',
        jquery_ui: 'lib/jquery-ui-1.10.4.min',
        text: 'lib/require-text'
    }
});

var deps = [
    'jquery', 'underscore', 'lib/settings', 'biodig/ui/TaggableImage',
    'text!biodig/tmpl/imageviewer-helpbox.html', 'bootstrap', 'jquery_ui'
];

require(deps, function($, _, settings, TaggableImage, HelpBox) {
    var helpDialog = $(_.template(HelpBox).call(settings));

    $('#helpButton').click(function() {
        var box = $(helpDialog.attr('id'));
        if (box.length > 0) {
            box.modal('show');
        }
        else {
            helpDialog.appendTo($('body')).modal();
        }
    });

    TaggableImage.create('#target-image', { mode : TaggableImage.MODES.PUBLIC });
});
