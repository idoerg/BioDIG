var deps = [
    'jquery', 'biodig/ui/dialogs/DynamicDialog', 'settings', 'text!biodig/tmpl/users/login.html'
];

define(deps, function($, DynamicDialog, settings, LoginTmpl) {
    var LoginTemplate = _.template(LoginTmpl);

    function Login() {
        this.dialog = DynamicDialog.create('Login', 'Login', LoginTemplate);
        $(this.dialog).on('accept', function(event, $el) {
            $el.find('form[name="login"]')[0].submit();
        });
    }

    Login.prototype.show = function() {
        this.dialog.show(settings);
    };

    Login.prototype.hide = function() {
        this.dialog.hide();
    };

    return {
        create: function() {
            return new Login();
        }
    };
});
