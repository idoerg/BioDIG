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
            fn.apply(scope, arguments);
        };
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
});
