define([], function() {
    function FlowNode(template, transition) {
        this.template = template;
        this.transition = transition;
        this.beforeCheck = null;
        this.mydata = null;
        this.nextNode = null;
        this.prevNode = null;
    }

    FlowNode.prototype.data = function(data) {
        this.mydata = data;
    };

    FlowNode.prototype.next = function(node) {
        if (arguments.length > 0) {
            // if a parameter is given then we are treating this
            // as a setter, which is chainable
            this.nextNode = node;
            return this;
        }
        else {
            // other wise this is used as a getter
            return this.nextNode;
        }
    };

    FlowNode.prototype.prev = function(node) {
        if (arguments.length > 0) {
            // if a parameter is given then we are treating this
            // as a setter, which is chainable
            this.prevNode = node;
            return this;
        }
        else {
            // other wise this is used as a getter
            return this.nextNode;
        }
    };

    FlowNode.prototype.nextData = function() {
        return this.transition.apply(null, arguments);
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
