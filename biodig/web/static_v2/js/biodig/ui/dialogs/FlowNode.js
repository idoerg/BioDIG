define([], function() {
    function FlowNode(template, transition) {
        this.template = template;
        this.transition = transition;
        this.beforeCheck = null;
        this.mydata = null;
    }

    FlowNode.prototype.data = function(data) {
        this.mydata = data;
    };

    FlowNode.prototype.nextData = function() {
        return transition.apply(null, arguments);
    };

    FlowNode.prototype.view = function() {
        return this.template(this.mydata);
    };

    FlowNode.prototype.before = function(callback) {
        this.beforeCheck = callback;
        return this;
    };

    FlowNode.prototype.skip = function() {
        if (this.beforeCheck) {
            return this.beforeCheck(this.mydata);
        }
        return false;
    };

    return {
        create: function(template, transition) {
            return new FlowNode(template, transition);
        }
    }
});
