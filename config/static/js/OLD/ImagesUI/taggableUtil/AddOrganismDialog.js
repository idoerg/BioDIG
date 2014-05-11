function AddOrganismDialog(pageBlock) {
    this.block = pageBlock;
    this.dialog = $('<div />', {
        'class' : 'tagging-dialog',
    });
    
    this.block = pageBlock;
    
    this.title = $('<div />', {
        'class' : 'tagging-dialog-title',
        'text' : 'Add Organisms'
    });
    
    this.closeButton = $('<span />', {
        'class' : 'ui-icon ui-icon-circle-close close-button'
    });
    
    this.title.append(this.closeButton);
    
    this.contents = $('<div />', {
        'class' : 'tagging-dialog-contents'
    });
    
    this.name = $('<input />', {
        'type' : 'text'
    });
    
    var nameLabel = $('<span />', {
        'text' : 'Names',
        'style' : 'margin-right: 10px'
    });
    
    this.ids = $('<input />', {
        'type' : 'text'
    });
    
    var idsLabel = $('<span />', {
        'text' : "Id's",
        'style' : 'margin-right: 37px'
    });
    
    var separator = $('<div />', {
            style : 'border-bottom: 1px solid #CCC; margin-bottom: 15px; padding-top: 15px;'
        }).append($('<div />', {
            text : 'OR',
            style : 'position: absolute; margin-top: -10px; left: 145px; background-color: white;'
        }));
    
    this.contents.append(nameLabel);
    this.contents.append(this.name);
    this.contents.append(separator);
    this.contents.append(idsLabel);
    this.contents.append(this.ids);
    
    this.finalizeUI = $('<div />', {
        'class' : 'tagging-dialog-contents'
    });
    
    this.finalizeBody = $('<div />');
    
    this.submitOrganismsButton = $('<button />', {
        'class' : 'tagging-button',
        'text': 'Add'
    });
    
    this.cancelButton = $('<button />', {
        'class' : 'tagging-button',
        'text': 'Cancel',
        'style' : 'margin-left: 10px'
    });
    
    this.finalizeBody.append(this.submitOrganismsButton);
    this.finalizeBody.append(this.cancelButton);
    this.finalizeBody.css('border-top', '1px solid #CCC');
    this.finalizeBody.css('padding-top', '5px');
    
    this.finalizeUI.append(this.finalizeBody);
    
    
    this.dialog.append(this.title);
    this.dialog.append(this.contents);
    this.dialog.append(this.finalizeUI);
    
    this.submitCallback = null;
    
    this.submitOrganismsButton.on('click', Util.scopeCallback(this, this.onSubmit));
    this.cancelButton.on('click', Util.scopeCallback(this, this.onCancel));
    this.closeButton.on('click', Util.scopeCallback(this, this.onCancel));
    
    $('body').append(this.dialog);
};

AddOrganismDialog.prototype.setTagBoard = function(tagBoard) {
    this.tagBoard = tagBoard;
};

AddOrganismDialog.prototype.addSubmitCallback = function(callback) {
    this.submitCallback = callback;
};

AddOrganismDialog.prototype.onSubmit = function() {
    var name = $.trim(this.name.val());
    if (name) {
        var self = this;
        
    }
};

AddOrganismDialog.prototype.onCancel = function() {
    this.hide();
};

AddOrganismDialog.prototype.hide = function() {
    this.block.hide();
    this.dialog.hide();
};

AddOrganismDialog.prototype.show = function() {
    this.block.show();
    this.dialog.show();
};