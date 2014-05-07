var deps = [
    'jquery', 'underscore', 'text!biodig/tmpl/taggable/status-message.html', 'bootstrap'
];

define(deps, function($, _, StatusMessageTmpl) {
    var StatusMessageTemplate = _.template(StatusMessageTmpl);

    function StatusMessager(selector) {
        this.$container = $(selector);
        this.SUCCESS = 'SUCCESS';
        this.ERROR = 'ERROR';
        this.WARNING = 'WARNING';
        this.INFO = 'INFO';

        this.construct = {
            'SUCCESS': {
                'alert': 'success',
                'prefix': 'Success!'
            },
            'ERROR': {
                'alert': 'danger',
                'prefix': 'Error!'
            },
            'WARNING': {
                'alert': 'warning',
                'prefix': 'Warning!'
            },
            'INFO': {
                'alert': 'info',
                'prefix': 'Info'
            },
        }
    }

    StatusMessager.prototype.add = function(type, message) {
        var data = $.extend({}, this.construct[type], {'message':escape(message)});
        var $message = $(StatusMessageTemplate(data));
        $message.alert();

        // setup timeout for close
        setTimeout(function() {
            $message.alert('close');
        }, 6000);

        this.$container.append($message);
    };

    return {
        create: function(selector) {
            return new StatusMessager(selector);
        }
    }

});
