var deps = [
    'jquery', 'biodig/ui/dialogs/FlowNode',
    'text!biodig/tmpl/taggable/dialogs/choose-tag-group.html',
    'text!biodig/tmpl/taggable/dialogs/edit-tag.html'
];

define(deps, function($, FlowNode, ChooseTagGroupTmpl, EditTagTmpl) {

    var AddTagFlow = [
        FlowNode.create(_.template(ChooseTagGroupTmpl), function(body) {
            return {
                'color': $.parseJSON(unescape(body.find('input[name="color"]').val())),
                'points': $.parseJSON(unescape(body.find('input[name="points"]').val())),
                'group': $.parseJSON(
                    unescape(body.find('.select-tag-group option:selected').data('tagGroup'))
                )
            };
        }).before(function(data) {
            // if a tag group has already been selected then skip this step
            if (data.group) {
                return data;
            }

            var keys = Object.keys(data.tagGroups);
            // if there is only one tag group skip this step
            if (keys.length == 1) {
                data.group = data.tagGroups[keys[0]];
                delete data.tagGroups;
                return data;
            }

            return false;
        }),
        FlowNode.create(_.template(EditTagTmpl), function(body) {
            return {
                "points" : $.parseJSON(unescape(body.find('input[name="points"]').val())),
                "color" : $.parseJSON(unescape(body.find('input[name="color"]').val())),
                "group" : $.parseJSON(unescape(body.find('input[name="group"]').val())).id,
                "name" : body.find('input[name="name"]').val()
            };
        })
    ];

    // set the pointers according the array order for ease
    for (var i = 0; i < AddTagFlow.length; i++) {
        if (i < AddTagFlow.length - 1) AddTagFlow[i].next(AddTagFlow[i+1]);
        if (i > 0) AddTagFlow[i].prev(AddTagFlow[i-1]);
    }


    return {
        get: function() {
            return AddTagFlow[0];
        }
    }
});
