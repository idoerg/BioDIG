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
                var organism_selector = '#' + node.uid() + ' select[name="select-organism"]';
                var type_selector = '#' + node.uid() + ' select[name="select-type"]';
                var feature_selector = '#' + node.uid() + ' select[name="select-feature"]';

                var changeFn = function() {
                    var organism = $.parseJSON(
                        unescape($(organism_selector + ' option:selected').data('organism'))
                    );
                    var type = $.parseJSON(
                        unescape($(type_selector + ' option:selected').data('type'))
                    );

                    // clear out the feature select box
                    var $featureselect = $(feature_selector);
                    $featureselect.empty();


                    // refill the feature select box
                    $.each(node.data().features, function(id, feature) {
                        if (feature.organism == organism.id && feature.type == type.name) {
                            var $option = $('<option />').text(feature.name + " - " + feature.uniquename)
                                .attr('data-feature', escape(JSON.stringify(feature)));
                            $featureselect.append($option);
                        }
                    });
                };

                $(document).on('change', organism_selector, changeFn);
                $(document).on('change', type_selector, changeFn);
            });


            return node;
        }
    };

});
