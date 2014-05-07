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
                'class': 'success',
                'prefix': 'Success!'
            },
            'ERROR': {
                'class': 'danger',
                'prefix': 'Error!'
            },
            'WARNING': {
                'class': 'warning',
                'prefix': 'Warning!'
            },
            'INFO': {
                'class': 'info',
                'prefix': 'Info'
            },
        }
    }

    StatusMessager.prototype.add = function(type, message) {
        var data = $.extend({}, this.construct[type], {'message':message});
        var $message = $(StatusMessageTemplate(data));
        $message.alert();

        // setup timeout for close
        setTimeout(function() {
            $message.alert('close');    
        }, 3000);

        this.$container.append($message);
    };

    return {
        create: function(selector) {
            return new StatusMessager(selector);
        }
    }

});
