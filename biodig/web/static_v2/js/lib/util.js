define(['jquery'], function($) {
    /*
     -------------------------------------------------------------------------------------
                             Static utility methods for general javascript
     -------------------------------------------------------------------------------------
    */
    var Util = {};
    Util.endL = "\n";
    Util.tab = "    ";

    Util.scope = function(scope, fn) {
        return function() {
            return fn.apply(scope, arguments);
        };
    };

    Util.cookie = function(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
         }

         return cookieValue;
    };

    Util.csrfSafeMethod = function(method) {
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    };

    Util.auth = function(token) {
        return token ?
            function (xhr, settings) {
                xhr.setRequestHeader('Authorization', 'Token ' + token) ;
            } :
            function(xhr, settings) {
                if (!Util.csrfSafeMethod(settings.type)) {
                    xhr.setRequestHeader("X-CSRFToken", Util.cookie('csrftoken'));
                }
            };
    };

    /**
     *  Sprintf
    **/
    Util.format = function() {
        var content = arguments[0];
        for (var i=1; i < arguments.length; i++) {
             var replacement = '{' + (i - 1) + '}';
             content = content.replace(replacement, arguments[i]);
        }
        return content;
    };

    Util.uuid4 = function() {
        return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
            var r = Math.random()*16|0, v = c == 'x' ? r : (r&0x3|0x8);
            return v.toString(16);
        });
    };

    Util.convertObjectToXml = function(obj) {
        var xml = '<?xml version="1.0" encoding="UTF-8"?>' + Util.endL;

        for (var key in obj) {
            var innerXml = "<" + key + ">" + Util.endL;
            innerXml += Util.convertObjectToXmlHelper(1, obj[key]);
            innerXml += "</" + key + ">" + Util.endL;
            xml += innerXml;
        }

        return xml;
    };

    Util.convertObjectToXmlHelper = function(depth, obj) {
        var xml = "";
        var tab = "";
        for (var i = 0; i < depth; i++) {
            tab += Util.tab;
        }

        if ($.isArray(obj)) {
            for (var key in obj) {
                var innerXml = tab + "<item>" + Util.endL;
                innerXml += Util.convertObjectToXmlHelper(depth + 1, obj[key]) + Util.endL;
                innerXml += tab + "</item>" + Util.endL;
                xml += innerXml;
            }
        }
        else if (typeof obj == "object") {
            for (var key in obj) {
                var innerXml = tab + "<" + key + ">" + Util.endL;
                innerXml += Util.convertObjectToXmlHelper(depth + 1, obj[key]) + Util.endL;
                innerXml += tab + "</" + key + ">" + Util.endL;
                xml += innerXml;
            }
        }
        else {
            return tab + obj;
        }

        return xml;
    };

    return Util;
});
