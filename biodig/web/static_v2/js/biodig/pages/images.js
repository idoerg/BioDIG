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
    'jquery', 'biodig/ui/paginator/ImagePaginator', 'biodig/ui/users/Login', 'settings'
];

require(deps, function($, ImagePaginator, Login, settings) {
    // setup login and logout forms
    var login = Login.create();
    $('.login > a').on('click', function() {
        login.show();
    });

    $('.logout > a').on('click', function() {
        var form = document.createElement("form");
        form.setAttribute("method", "post");
        form.setAttribute("action", settings.SITE_URL + "logout/");
        document.body.appendChild(form);
        form.submit();
    });

    ImagePaginator.create('#images-container', { totalImages: parseInt($('input#totalImages').val()) });
});
