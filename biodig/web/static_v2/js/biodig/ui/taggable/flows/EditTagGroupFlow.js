var deps = [
    'jquery', 'biodig/ui/dialogs/FlowNode',
    'text!biodig/tmpl/taggable/dialogs/choose-tag-group.html',
    'text!biodig/tmpl/taggable/dialogs/edit-tag-group.html'
];

define(deps, function($, FlowNode, ChooseTagGroupTmpl, EditTagGroupTmpl) {
    // When editing a tag group one must choose the tag group to edit first
    var EditTagGroupFlow = [
        FlowNode.create(_.template(ChooseTagGroupTmpl), function(body) {
            // get the json stringified tag group stored in the data section
            // of the option and turn it back into an object for rendering
            return $.parseJSON(
                unescape(body.find('.select-tag-group option:selected').data('tagGroup'))
            );
        }),
        FlowNode.create(_.template(EditTagGroupTmpl), function(body) {
            return { "name" : body.find('input[name="name"]').val() };
        })
    ];

    return {
        get: function() {
            return EditTagGroupFlow;
        }
    }
});
