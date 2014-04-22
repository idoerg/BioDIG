define([], function() {
    function FlowNode(template, transition) {
        this.template = template;
        this.transition = transition;
        this.beforeCheck = null;
        this.data = null;
    }

    FlowNode.prototype.data = function(data) {
        this.data = data;
    };

    FlowNode.prototype.nextData = function() {
        return transition.apply(null, arguments);
    };

    FlowNode.prototype.view = function() {
        return this.template(this.data);
    };

    FlowNode.prototype.before = function(callback) {
        this.beforeCheck = callback;
        return this;
    };

    FlowNode.prototype.skip = function() {
        if (this.beforeCheck) {
            return this.beforeCheck(this.data);
        }
        return false;
    };

    return {
        create: function(template, transition) {
            return new FlowNode(template, transition);
        }
    }
});
