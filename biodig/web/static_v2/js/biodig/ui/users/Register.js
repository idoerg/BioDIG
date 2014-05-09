var deps = [
    'jquery', 'biodig/ui/dialogs/DynamicDialog', 'settings', 'text!biodig/tmpl/users/register.html'
];

define(deps, function($, DynamicDialog, UserClient, settings, RegisterTmpl) {
    var RegisterTemplate = _.template(RegisterTmpl);

    function Register() {
        this.dialog = DynamicDialog.create('Register', 'Register', RegisterTemplate);
        this.client = UserClient.create();
        
        $(this.dialog).on('accept', function(event, $el) {
            var user = {
                'username': $el.find('input[name="username"]').val(),
                'password': $el.find('input[name="password"]').val(),
                'email': $el.find('input[name="email"]').val()
            }

            var firstname = $el.find('input[name="firstname"]').val();
            if (firstname) user['firstname'] = firstname;

            var lastname = $el.find('input[name="lastname"]').val();
            if (lastname) user['lastname'] = lastname;


        });
    }

    Register.prototype.show = function() {
        this.dialog.show(settings);
    };

    Register.prototype.hide = function() {
        this.dialog.hide();
    };

    return {
        create: function() {
            return new Register();
        }
    };
});
