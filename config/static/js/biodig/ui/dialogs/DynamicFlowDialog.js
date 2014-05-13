var deps = [
    'jquery', 'underscore', 'lib/util', 'biodig/ui/dialogs/FlowNode',
    'text!biodig/tmpl/taggable/dialogs/structure.html', 'bootstrap'
];

define(deps, function($, _, util, FlowNode, DialogStructureTmpl) {

    var DialogStructureTemplate = _.template(DialogStructureTmpl);

    var Helper = {
        nextView: function(data) {
            // get the next node and move the current pointer
            // (this shouldn't be called on a final node)
            this.current = this.current.next();
            this.current.data(data);

            // check to see if we can automate this stage of the workflow
            // and skip it altogether
            var nextData = this.current.skip();
            if (nextData) {
                return util.scope(this, Helper.nextView)(nextData);
            }

            return this.current.view();
        }
    };

    function DynamicFlowDialog(name, title, first) {
        this.first = FlowNode.create().before(function(data) { return data; }).next(first);
        this.$el = $(DialogStructureTemplate({ 'name' : name, 'title': title }));
        this.current = this.first;

        var self = this;
        var nextView = util.scope(this, Helper.nextView);
        // setup the listener for the Dialog on click
        this.$el.find('.accept').on('click', function() {
            if (self.current.next()) {
                var $body = self.$el.find('.modal-body');
                var data = self.current.nextData($body);
                $body.empty().append(nextView(data));

                // set the accept button to say "Accept" if we have moved to the last node
                if (self.current.next() == null) {
                    var $accept = self.$el.find('.accept');
                    $accept.text('Accept');
                }

                $(self).trigger('next', [self.$el, data]);
            }
            else {
                var $body = self.$el.find('.modal-body');
                var data = self.current.nextData($body);
                $(self).trigger('accept', [self.$el, data]);
                self.$el.modal('hide');
            }
        });

        this.$el.find('.cancel').on('click', function() {
            self.$el.modal('hide');
            $(self).trigger('cancel');
        });
    }

    DynamicFlowDialog.prototype.show = function(data) {
        var self = this;
        var box = $(this.$el.attr('id'));
        this.current = this.first;
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
    }

    DynamicFlowDialog.prototype.accept = function(callback) {
        $(self).trigger('accept', [self.$el]);
    };

    DynamicFlowDialog.prototype.close = function(callback) {
        this.$el.find('.cancel').first().trigger('click');
    };

    return {
        create: function(name, title, first) {
            return new DynamicFlowDialog(name, title, first);
        }
    };
});
