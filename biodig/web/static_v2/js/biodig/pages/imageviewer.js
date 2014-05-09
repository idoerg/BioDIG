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
    'jquery', 'underscore', 'settings', 'biodig/ui/taggable/Taggable', 'biodig/ui/users/Login',
    'text!biodig/tmpl/helpbox/imageviewer.html', 'bootstrap', 'jquery_ui'
];

require(deps, function($, _, settings, Taggable, Login, HelpBox) {
    // setup the help dialog box for this page
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

    // setup login and logout forms
    var login = Login.create();
    $('.login > a').on('click', function() {
        login.show();
    });

    $('.logout > a').on('click', function() {
        var form = document.createElement("form");
        form.setAttribute("method", "post");
        form.setAttribute("action", "{{ SITE_URL }}logout/");
        document.body.appendChild(form);
        form.submit();
    });

    // setup the Taggable plugin to run in public mode
    Taggable.create('#target-image', { mode : Taggable.MODES.REGISTERED });
});
