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
        },
        kinetic: {
            init: function() {
                return Kinetic;
            }
        }
    },
    paths: {
        jquery: 'lib/jquery-1.11.0.min',
        underscore: 'lib/underscore.min',
        bootstrap: 'lib/bootstrap.min',
        settings: 'lib/settings',
        jquery_ui: 'lib/jquery-ui-1.10.4.min',
        text: 'lib/require-text',
        kinetic: 'lib/kinetic-v5.1.0.min'
    }
});

var deps = [
    'jquery', 'underscore', 'lib/settings', 'biodig/ui/taggable/Taggable',
    'text!biodig/tmpl/helpbox/imageviewer.html', 'bootstrap', 'jquery_ui'
];

require(deps, function($, _, settings, Taggable, HelpBox) {
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

    Taggable.create('#target-image', { mode : Taggable.MODES.REGISTERED });
});
