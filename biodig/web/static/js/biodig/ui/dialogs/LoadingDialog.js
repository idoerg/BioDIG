var deps = [
    'jquery', 'underscore', 'lib/util', 'text!biodig/tmpl/loading/loading.html', 'bootstrap'
];

define(deps, function($, _, util, LoadingTmpl) {

    var LoadingTemplate = _.template(LoadingTmpl);

    function LoadingDialog() {
        this.$el = LoadingTemplate({
            'name': 'loading-' + util.uuid4()
        });
    }

    LoadingDialog.prototype.show = function() {
        var box = $(this.$el.attr('id'));
        if (box.length > 0) {
            box.modal('show');
        }
        else {
            this.$el.appendTo($('body'));
            this.$el.find('.modal-body').empty().append(this.tmpl(data));
            this.$el.modal();
        }
    };

    LoadingDialog.prototype.hide = function() {
        this.$el.modal('hide');
    };

    return {
        create: function() {
            return new LoadingDialog();
        }
    };

});
