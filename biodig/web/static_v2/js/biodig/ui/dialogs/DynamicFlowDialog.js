var deps = [
    'jquery', 'underscore', 'lib/util',
    'text!biodig/tmpl/taggable/dialogs/structure.html'
];

define(deps, function($, _, util, DialogStructureTmpl) {

    var DialogStructureTemplate = _.template(DialogStructureTmpl);

    var Helper = {
        nextView: function(data) {
            // get the next node and move the current pointer
            // (this shouldn't be called on a final node)
            this.current++;
            var nextNode = this.nodes[this.current];
            nextNode.data(data);

            // check to see if we can automate this stage of the workflow
            // and skip it altogether
            var nextData = nextNode.skip();
            if (nextData) {
                return util.scope(this, Helper.nextView)(nextData);
            }

            return nextNode.view();
        }
    };

    function DynamicFlowDialog(name, title, nodes) {
        this.nodes = nodes;
        this.$el = $(DialogStructureTemplate({ 'name' : name, 'title': title }));
        this.current = 0;
    }

    DynamicFlowDialog.prototype.show = function(data) {
        var self = this;
        var box = $(this.$el.attr('id'));
        this.current = 0;
        var nextView = util.scope(this, Helper.nextView);
        if (box.length > 0) {
            box.find('.modal-body').empty().append(nextView(data));
            box.modal('show');
        }
        else {
            this.$el.appendTo($('body'));
            this.$el.find('.modal-body').empty().append(nextView(data));
            this.$el.modal();
        }

        // first node should show next not accept
        this.$el.find('.accept').text('Next');

        this.$el.find('.accept').on('click', function() {
            if (self.current + 1 < self.nodes.length) {
                var data = self.nodes[self.current].nextData();
                self.$el.find('.modal-body').empty().append(nextView(data));

                // set the accept button to say "Accept" if we have moved to the last node
                if (self.current == self.nodes.length - 1) {
                    var $accept = self.$el.find('.accept');
                    $accept.text('Accept');
                }

                $(self).trigger('next', [self.$el, data]);
            }
            else {

                $(self).trigger('accept', [self.$el]);
                self.$el.modal('hide');
            }
        });
    }

    DynamicFlowDialog.prototype.accept = function(callback) {
        $(self).trigger('accept', [self.$el]);
    };

    return {
        create: function(name, title, nodes) {
            return new DynamicFlowDialog(name, title, nodes);
        }
    };
});
