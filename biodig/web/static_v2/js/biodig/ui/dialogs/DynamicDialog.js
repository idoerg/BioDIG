var deps = [
    'jquery', 'underscore', 'lib/util',
    'text!biodig/tmpl/taggable/dialogs/structure.html'
];

define(deps, function($, _, util, DialogStructureTmpl) {

    var DialogStructureTemplate = _.template(DialogStructureTmpl);

    function DynamicDialog(name, title, tmpl) {
        this.tmpl = tmpl;
        this.$el = $(DialogStructureTemplate({ 'name' : name, 'title': title }));
    }

    DynamicDialog.prototype.show = function(data) {
        var box = $(this.$el.attr('id'));
        if (box.length > 0) {
            box.find('.modal-body').empty().append(this.tmpl(data));
            box.modal('show');
        }
        else {
            this.$el.appendTo($('body'));
            this.$el.find('.modal-body').empty().append(this.tmpl(data));
            this.$el.modal();
        }
    }

    DynamicDialog.prototype.accept = function(callback) {
        this.$el.find('.accept').on('click', callback);
    };

    return {
        create: function(name, title, tmpl) {
            return new DynamicDialog(name, title, tmpl);
        }
    };
});