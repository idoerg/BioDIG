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
    'jquery', 'underscore', 'settings', 'biodig/ui/users/ActivationStatus', 'biodig/ui/users/Login',
    'biodig/ui/users/Register', 'bootstrap', 'jquery_ui'
];

require(deps, function($, _, settings, ActivationStatus, Login, Register) {
    // setup login, register, and logout forms
    var login = Login.create();
    $('.login > a').on('click', function() {
        login.show();
    });

    var register = Register.create();
    $('.register > a').on('click', function() {
        register.show();
    });

    $('.logout > a').on('click', function() {
        var form = document.createElement("form");
        form.setAttribute("method", "post");
        form.setAttribute("action", settings.SITE_URL + "logout/");
        document.body.appendChild(form);
        form.submit();
    });

    // setup the activation status to update
    var activation_status = $('#activation-status');
    var user = activation_status.find('input[name="user_id"]').val();
    var activation = activation_status.find('input[name="activation_key"]').val();
    ActivationStatus.create(activation-status).start(user, activation);
});
