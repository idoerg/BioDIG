var deps = [
    'jquery', 'underscore', 'biodig/ui/dialogs/FlowNode',
    'text!biodig/tmpl/taggable/dialogs/choose-tag-group.html',
    'text!biodig/tmpl/taggable/dialogs/choose-tag.html',
    'text!biodig/tmpl/taggable/dialogs/edit-tag.html'
];

define(deps, function($, _, FlowNode, ChooseTagGroupTmpl, ChooseTagTmpl, EditTagTmpl) {
    // When editing a tag one must first choose the tag group and then choose the
    // tag to edit (needs to be elastic enough to allow for )
    var EditTagFlow = [
        FlowNode.create(_.template(ChooseTagGroupTmpl), function(body) {
            // get the json stringified tag stored in the data section
            // of the option and turn it back into an object for rendering
            var group = $.parseJSON(
                unescape(body.find('.select-tag-group option:selected').data('tagGroup'))
            );

            return { "tags" : group.tags };
        }).before(function(data) {
            if (!data["tagGroups"]) return data;

            // check to see if there is only one tag group given in the
            // data and if so skip this node (return of true means to skip)
            var keys = Object.keys(data['tagGroups']);
            if (keys.length == 1) {
                return {
                    'tags' : data['tagGroups'][keys[0]].tags
                }; // returns the tags for the next thing
            }

            return false;
        }),
        FlowNode.create(_.template(ChooseTagTmpl), function(body) {
            return $.parseJSON(
                unescape(body.find('.select-tag option:selected').data('tag'))
            );
        }).before(function(data) {
            var keys = Object.keys(data['tags']);
            if (keys.length == 1) {
                return data['tags'][keys[0]]; // returns the tag for the next thing
            }

            return false;
        }),
        FlowNode.create(_.template(EditTagTmpl), function(body) {
            return {
                "id" : body.find('input[name="id"]').val(),
                "name" : body.find('input[name="name"]').val()
            };
        })
    ];

    // set the pointers according the array order for ease
    for (var i = 0; i < EditTagFlow.length; i++) {
        if (i < EditTagFlow.length - 1) EditTagFlow[i].next(EditTagFlow[i+1]);
        if (i > 0) EditTagFlow[i].prev(EditTagFlow[i-1]);
    }


    return {
        get: function() {
            return EditTagFlow[0];
        }
    }
});
