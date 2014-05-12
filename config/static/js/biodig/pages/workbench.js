require.config({
    shim: {
        jquery: {
            init: function() {
                return $;
            }
        },
        bootstrap: ['jquery'],
        jquery_ui: ['jquery'],
        colorpicker: ['jquery'],
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
        kinetic: 'lib/kinetic-v5.1.0.min',
        colorpicker: 'lib/colorpicker/colorpicker'
    }
});

var deps = [
    'jquery', 'biodig/ui/workbench/Workbench'
];

require(deps, function($, Workbench) {
    var user = $('input[name="user_id"]').val();
    Workbench.create('.workbench-container', user);
});
