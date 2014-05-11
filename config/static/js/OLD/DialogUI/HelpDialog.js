function HelpDialog(pageBlock, pageTitle, contents) {
    this.block = pageBlock;
    this.dialog = $('<div />', {
        'class' : 'dialog',
    });
    
    this.block = pageBlock;
    
    this.title = $('<div />', {
        'class' : 'dialog-title',
        'text' : 'Information for ' + pageTitle
    });
    
    this.closeButton = $('<span />', {
        'class' : 'ui-icon ui-icon-circle-close close-button'
    });
    
    this.title.append(this.closeButton);
    
    this.contents = $('<div />', {
        'class' : 'dialog-contents'
    });

    this.contents.append(contents);
    
    this.finalizeUI = $('<div />', {
        'class' : 'dialog-contents'
    });
    
    this.finalizeBody = $('<div />');
    
    this.cancelButton = $('<button />', {
        'class' : 'dialog-button',
        'text': 'Close',
        'style' : 'margin-left: 10px'
    });
    
    this.finalizeBody.append(this.cancelButton);
    this.finalizeBody.css('border-top', '1px solid #CCC');
    this.finalizeBody.css('padding-top', '5px');
    
    this.finalizeUI.append(this.finalizeBody);
    
    this.dialog.append(this.title);
    this.dialog.append(this.contents);
    this.dialog.append(this.finalizeUI);
    
    this.submitCallback = null;
    this.cancelButton.on('click', Util.scopeCallback(this, this.onCancel));
    this.closeButton.on('click', Util.scopeCallback(this, this.onCancel));
    
    $('body').append(this.dialog);
};

HelpDialog.prototype.onCancel = function() {
    this.hide();
};

HelpDialog.prototype.hide = function() {
    this.block.hide();
    $(window).off('resize');
    this.dialog.hide();
};

HelpDialog.prototype.show = function() {
    this.block.show();
    var self = this;
    $(window).on('resize', function() {
        self.center($(this).width(), $(this).height());
    });
    this.center($(window).width(), $(window).height());
    this.dialog.show();
};

HelpDialog.prototype.center = function(width, height) {
    if (height > this.dialog.height()) {
        this.dialog.css('top', (height - this.dialog.height())/2 + 'px');
    }
    else {
        this.dialog.css('top', '0px');
    }
    
    this.dialog.css('left', (width - this.dialog.width())/2 + 'px');
};