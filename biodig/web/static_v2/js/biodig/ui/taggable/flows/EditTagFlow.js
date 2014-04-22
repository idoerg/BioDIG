var deps = [
    'jquery', 'biodig/ui/dialogs/FlowNode',
    'text!biodig/tmpl/taggable/dialogs/choose-tag-group.html',
    'text!biodig/tmpl/taggable/dialogs/edit-tag-group.html'
];

define(deps, function($, FlowNode, ChooseTagGroupTmpl, EditTagGroupTmpl) {
    // When editing a tag one must first choose the tag group and then choose the
    // tag to edit (needs to be elastic enough to allow for )
    var EditTagFlow = [
        FlowNode.create(_.template(ChooseTagGroupTmpl), function(body) {
            // get the json stringified tag stored in the data section
            // of the option and turn it back into an object for rendering
            return $.parseJSON(
                body.find('.select-tag option:selected').data('tag')
            );
        }).before(function(tagGroups) {
            // check to see if there is only one tag group given in the
            // data and if so skip this node (return of true means to skip)
            var keys = Object.keys(tagGroups);
            if (keys.length == 1) {
                return tagGroups[keys[0]].tags; // returns the tags for the next thing
            }

            return false;
        }),
        FlowNode.create(_.template(EditTagTmpl))
    ];


    return {
        get: function() {
            return EditTagGroupFlow;
        }
    }
});
