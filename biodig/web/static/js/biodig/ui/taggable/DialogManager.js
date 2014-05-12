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
        'biodig/ui/taggable/flows/AddGeneLinkFlow', 'biodig/ui/taggable/flows/DeleteGeneLinkFlow',
        'text!biodig/tmpl/taggable/dialogs/choose-organism.html',
        'text!biodig/tmpl/taggable/dialogs/choose-tag-group.html',
        'text!biodig/tmpl/taggable/dialogs/choose-tag.html',
        'text!biodig/tmpl/taggable/dialogs/edit-tag-group.html',
        'text!biodig/tmpl/taggable/publication/request-preview.html',
        'text!biodig/tmpl/taggable/publication/choose-request.html'
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
            require(registeredDeps, function(DynamicFlowDialog, EditTagGroupFlow, EditTagFlow,
                AddTagFlow, AddGeneLinkFlow, DeleteGeneLinkFlow, ChooseOrganismTmpl,
                ChooseTagGroupTmpl, ChooseTagTmpl, EditTagGroupTmpl, PublicationRequestPreviewTmpl,
                ChoosePublicationRequestTmpl) {

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
                    'DeleteGeneLink': DynamicFlowDialog.create('DeleteGeneLink', 'Delete Gene Link',
                        DeleteGeneLinkFlow.get()),
                    'AddPublicationRequest': DynamicDialog.create('AddPublicationRequest', 'Send Publication Request',
                        _.template(PublicationRequestPreviewTmpl)),
                    'DeletePublicationRequest': DynamicDialog.create('DeletePublicationRequest', 'Cancel Publication Request',
                        _.template(ChoosePublicationRequestTmpl)),
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
