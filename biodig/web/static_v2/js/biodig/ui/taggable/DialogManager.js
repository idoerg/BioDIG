var deps = [
    'jquery', 'underscore', 'lib/util', 'biodig/ui/dialogs/DynamicDialog',
    'text!biodig/tmpl/taggable/dialogs/change-visible-tag-groups.html',
    'text!biodig/tmpl/taggable/dialogs/download-metadata.html'
];

define(deps, function($, _, util, DynamicDialog, ChangeVisibleTagGroupsTmpl, DownloadMetadataTmpl) {

    var ChangeVisibleTagGroupsTemplate = _.template(ChangeVisibleTagGroupsTmpl);
    var DownloadMetadataTemplate = _.template(DownloadMetadataTmpl);

    function DialogManager() {
        this.dialogs = {
            'ChangeVisibleTagGroups': DynamicDialog.create('ChangeVisibleTagGroups',
                'Change Visible Tag Groups', ChangeVisibleTagGroupsTemplate),
            'DownloadMetadata' : DynamicDialog.create('DownloadMetadata',
                'Download Image Metadata', DownloadMetadataTemplate)
        };
    }

    DialogManager.prototype.dialog = function(name) {
        return this.dialogs[name];
    };

    DialogManager.prototype.loadRegistered = function() {

    };

    return {
        create: function() {
            return new DialogManager();
        }
    }

});
