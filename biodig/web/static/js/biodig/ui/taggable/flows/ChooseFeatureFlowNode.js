var deps = [
    'jquery', 'underscore', 'biodig/ui/dialogs/FlowNode',
    'text!biodig/tmpl/taggable/dialogs/choose-feature.html'
];

define(deps, function($, _, FlowNode, ChooseFeatureTmpl) {

    var ChooseFeatureTemplate = _.template(ChooseFeatureTmpl);

    return {
        create: function(transition) {
            var node = FlowNode.create(ChooseFeatureTemplate, transition);

            // add the controls onto the FlowNode for displaying
            // the limiting of features
            $(node).on('render', function() {
                var $organismselect = node.view().find('select[name="select-organism"]');
                var $typeselect = node.view().find('select[name="select-organism"]');
                var $featureselect = node.view().find('select[name="select-feature"]');

                var changeFn = function() {
                    var organism = $.parseJSON(
                        unescape($organismselect.find('option:selected').data('organism'))
                    );
                    var type = $.parseJSON(
                        unescape($typeselect.find('option:selected').data('type'))
                    );

                    // clear out the feature select box
                    $featureselect.empty();

                    // refill the feature select box
                    $.each(node.data().features, function(id, feature) {
                        if (feature.organism == organism.id && feature.type == type.name) {
                            var $option = $('<option />').text(feature.name + " - " + feature.uniquename)
                                .data('feature', escape(JSON.stringify(feature)));
                            $featureselect.append($option);
                        }
                    });
                };

                $organismselect.on('change', changeFn);
                $typeselect.on('change', changeFn);
            });


            return node;
        }
    };

});
