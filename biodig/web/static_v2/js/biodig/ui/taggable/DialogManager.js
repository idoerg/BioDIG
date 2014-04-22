var deps = [
    'jquery', 'underscore', 'lib/util', 'biodig/ui/dialogs/DynamicDialog',
    'text!biodig/tmpl/taggable/dialogs/change-visible-tag-groups.html',
    'text!biodig/tmpl/taggable/dialogs/download-metadata.html'
];

define(deps, function($, _, util, DynamicDialog, ChangeVisibleTagGroupsTmpl, DownloadMetadataTmpl) {

    var ChangeVisibleTagGroupsTemplate = _.template(ChangeVisibleTagGroupsTmpl);
    var DownloadMetadataTemplate = _.template(DownloadMetadataTmpl);

    var regDeps = $.map([
        'add-organism.html', 'delete-organism.html', 'choose-tag-group.html',
        'edit-tag-group.html', 'delete-tag-group.html', 'choose-tag.html', 'edit-tag.html',
        'delete-tag.html', 'choose-gene-link.html', 'add-gene-link.html', 'delete-gene-link.html'
    ], function(dialog) {
        return 'text!biodig/tmp/taggable/dialogs/' + dialog;
    });

    regDeps.push('biodig/ui/dialogs/FlowNode');


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
            require(regDeps, function(AddOrganismTmpl, DeleteOrganismTmpl, ChooseTagGroupTmpl,
                    EditTagGroupTmpl, DeleteTagGroupTmpl, ChooseTagTmpl, EditTagTmpl, DeleteTagTmpl,
                    ChooseGeneLinkTmpl, AddGeneLinkTmpl, DeleteGeneLinkTmpl, FlowNode) {



                
                var addGeneLinkFlow = [
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
                ];

                var dialogs = {
                    'AddOrganism': DynamicDialog.create('AddOrganism', 'Add Organism to Image',
                        _.template(AddOrganismTmpl)),
                    'DeleteOrganism': DynamicDialog.create('DeleteOrganism',
                        'Delete Organism from Image', _.template(DeleteOrganismTmpl)),
                    'AddTagGroup': DynamicDialog.create('AddTagGroup', 'Add Tag Group',
                        _.template(EditTagGroupTmpl)),
                    'EditTagGroup': DynamicDialog.create('EditTagGroup', 'Edit Tag Group',
                        _.template(ChooseTagGroupTmpl + EditTagGroupTmpl)),
                    'DeleteTagGroup': DynamicDialog.create('DeleteTagGroup', 'Delete Tag Group',
                        _.template(ChooseTagGroupTmpl + DeleteTagGroupTmpl)),
                    'EditTag': DynamicDialog.create('EditTag', 'Edit Tag',
                        _.template(ChooseTagTmpl + EditTagTmpl)),
                    'DeleteTag': DynamicDialog.create('DeleteTag', 'Delete Tag',
                        _.template(ChooseTagTmpl + DeleteTagTmpl)),
                    'AddGeneLink': DynamicDialog.create('AddGeneLink', 'Add Gene Link',
                        _.template(AddGeneLinkTmpl)),
                    'DeleteGeneLink': DynamicDialog.create('DeleteGeneLink', 'Delete Gene Link',
                        _.template(ChooseGeneLinkTmpl + DeleteGeneLinkTmpl))
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
