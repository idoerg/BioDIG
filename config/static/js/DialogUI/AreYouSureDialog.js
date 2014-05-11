/**
    Creates a reusable AreYouSureDialog Box, which will perform a callback
    upon a yes. Should be simple to use and easy to implement.
    
    Author: Andrew Oberlin
    Date: October 18, 2012
    
    Requirements:
        1. jQuery 1.7.2
**/
function AreYouSureDialog() {
    this.dialogBox = $('<div></div>');
    this.callback = null;
    var self = this;
    this.dialogBox.dialog({
        autoOpen  : false,
        title     : '',
        buttons   : [
            {
                text: "Yes",
                click: function() {
                if (self.callback) {
                    self.callback();
                }
                $(this).dialog("close"); 
                }
            },
            {
                text: "No",
                click: function() { 
                    $(this).dialog("close"); 
                }
            }
        ],
        draggable : false,
        resizable : false
    });    
};

AreYouSureDialog.prototype.open = function(acceptCallback) {
    this.callback = acceptCallback;
    this.dialogBox.dialog("open");
};

AreYouSureDialog.prototype.close = function() {
    this.dialogBox.dialog("close");
};

AreYouSureDialog.prototype.setMessage = function(message) {
    this.dialogBox.html(message);
};

AreYouSureDialog.prototype.setTitle = function(title) {
    this.dialogBox.dialog("option", "title", title);
};