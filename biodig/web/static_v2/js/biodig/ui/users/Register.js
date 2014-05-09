var deps = [
    'jquery', 'biodig/ui/dialogs/DynamicDialog', 'biodig/clients/UserClient', 'settings',
    'text!biodig/tmpl/users/register.html'
];

define(deps, function($, DynamicDialog, UserClient, settings, RegisterTmpl) {
    var RegisterTemplate = _.template(RegisterTmpl);

    function Register() {
        this.dialog = DynamicDialog.create('Register', 'Register', RegisterTemplate);
        this.client = UserClient.create();

        var self = this;
        $(this.dialog).on('accept', function(event, $el) {
            var user = [
                $el.find('input[name="username"]').val(),
                $el.find('input[name="password"]').val(),
                $el.find('input[name="email"]').val()
            ]

            var firstname = $el.find('input[name="firstname"]').val();
            if (firstname) user.push(firstname);

            var lastname = $el.find('input[name="lastname"]').val();
            if (lastname) user.push(lastname);

            self.client.create.apply(user)
                .done(function(user) {
                    self.hide();
                })
                .fail(function(e) {
                    // TODO: Error message on failed registration
                });
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
