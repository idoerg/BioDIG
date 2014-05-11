/**
    A javascript client for interacting with the getTags web service.
    Dependencies:
        1. JQuery 1.7.2
**/
function WebServiceClient(url) {
    this.url = url;
};

/**
 * Calls the web service with the address specified. Runs the
 * callback given on the data retrieved. Calls another callback
 * specified by the user--if this is undefined then it alerts the
 * user of the error.
 * 
 * @param args: dictionary of arguments to send to the web service
 * @param callback: the callback to run on successful data
 * @param errorCallback: the callback to run on errored data
 */
WebServiceClient.prototype.call = function(args, callback, errorCallback) {
    // creates the url using the arguments given
    var url = this.url;
    var endOfUrl = '?';
    var i = 0;
    $.each(args, function(key, value) {
        if (i > 0) {
            endOfUrl += '&&';
        }
        
        endOfUrl += key + '=' + value;
        i++;
    });
    
    if (i > 0) {
        url += endOfUrl;
    }
    
    if (!errorCallback) {
        errorCallback = function(status) {
            alert(status);
        };
    }
    
    $.ajax({
        url : url,
        type : 'GET',
        dataType : 'json',
        success : function(data) {
            if (!data.error) {
                delete data.error;
                delete data.errorMessage;
                callback(data);
            }
            else {
                errorCallback(data.errorMessage);
            }
        },
        error : function(jqXHR, textStatus, errorThrown) {
            errorCallback(textStatus);
        }
    });
};