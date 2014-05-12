var deps = [
    'jquery', 'underscore', 'lib/util', 'biodig/ui/dialogs/DynamicDialog',
    'text!biodig/tmpl/taggable/dialogs/change-visible-tag-groups.html',
    'text!biodig/tmpl/taggable/dialogs/download-metadata.html'
];

define(deps, function($, _, util, DynamicDialog, ChangeVisibleTagGroupsTmpl, DownloadMetadataTmpl) {

    var ChangeVisibleTagGroupsTemplate = _.template(ChangeVisibleTagGroupsTmpl);
    var DownloadMetadataTemplate = _.template(DownloadMetadataTmpl);

    var registeredDeps = [
        'biodig/ui/dialogs/DynamicFlowDialog', 'biodig/ui/taggable/flows/EditTagGroupFlow',
        'biodig/ui/taggable/flows/EditTagFlow','biodig/ui/taggable/flows/AddTagFlow',
        'biodig/ui/taggable/flows/AddGeneLinkFlow',
        'text!biodig/tmpl/taggable/dialogs/choose-organism.html',
        'text!biodig/tmpl/taggable/dialogs/choose-tag-group.html',
        'text!biodig/tmpl/taggable/dialogs/choose-tag.html',
        'text!biodig/tmpl/taggable/dialogs/edit-tag-group.html'
    ];

    function DialogManager() {
        this.dialogs = {
            'ChangeVisibleTagGroups': DynamicDialog.create('ChangeVisibleTagGroups',
                'Change Visible Tag Groups', ChangeVisibleTagGroupsTemplate),
            'DownloadMetadata' : DynamicDialog.create('DownloadMetadata',
                'Download Image Metadata', DownloadMetadataTemplate)
        };
    }

    DialogManager.prototype.get = function(name) {
        return this.dialogs[name];
    };

    DialogManager.prototype.loadRegistered = function() {
        var self = this;
        return $.Deferred(function(deferred_obj) {
            require(registeredDeps, function(DynamicFlowDialog, EditTagGroupFlow,
                EditTagFlow, AddTagFlow, AddGeneLinkFlow, ChooseOrganismTmpl, ChooseTagGroupTmpl, ChooseTagTmpl,
                EditTagGroupTmpl) {

                /*var addGeneLinkFlow = [
                    FlowNode.create(_.template(ChooseTagTmpl), function(body) {
                        // get the json stringified geneLink array stored in the data section
                        // of the option and turn it back into an object for rendering
                        return $.parseJSON(
                            body.find('.select-tag option:selected').data('geneLinks')
                        );
                    }),
                    FlowNode.create(_.template(AddGeneLinkTmpl))
                ];

                var deleteGeneLinkFlow = [
                    FlowNode.create(_.template(ChooseTagTmpl), function(body) {
                        // get the json stringified geneLink array stored in the data section
                        // of the option and turn it back into an object for rendering
                        return $.parseJSON(
                            body.find('.select-tag option:selected').data('geneLinks')
                        );
                    }),
                    FlowNode.create(_.template(AddGeneLinkTmpl))
                ];*/

                var dialogs = {
                    'AddOrganism': DynamicDialog.create('AddOrganism', 'Add Organism to Image',
                        _.template(ChooseOrganismTmpl)),
                    'DeleteOrganism': DynamicDialog.create('DeleteOrganism',
                        'Delete Organism from Image', _.template(ChooseOrganismTmpl)),
                    'AddTagGroup': DynamicDialog.create('AddTagGroup', 'Add Tag Group',
                        _.template(EditTagGroupTmpl)),
                    'EditTagGroup': DynamicFlowDialog.create('EditTagGroup', 'Edit Tag Group',
                        EditTagGroupFlow.get()),
                    'DeleteTagGroup': DynamicDialog.create('DeleteTagGroup', 'Delete Tag Group',
                        _.template(ChooseTagGroupTmpl)),
                    'AddTag': DynamicFlowDialog.create('AddTag', 'Add Tag',
                        AddTagFlow.get()),
                    'EditTag': DynamicFlowDialog.create('EditTag', 'Edit Tag',
                        EditTagFlow.get()),
                    'DeleteTag': DynamicDialog.create('DeleteTag', 'Delete Tag',
                        _.template(ChooseTagTmpl)),
                    'AddGeneLink': DynamicFlowDialog.create('AddGeneLink', 'Add Gene Link',
                        AddGeneLinkFlow.get()),
                    //'DeleteGeneLink': DynamicDialog.create('DeleteGeneLink', 'Delete Gene Link',
                    //    _.template(ChooseGeneLinkTmpl + DeleteGeneLinkTmpl))
                };

                $.extend(self.dialogs, dialogs);
                deferred_obj.resolve();
            });
        }).promise();
    };

    return {
        create: function() {
            return new DialogManager();
        }
    }

});
