/*
 -------------------------------------------------------------------------------------
 						Static utility methods for general javascript
 -------------------------------------------------------------------------------------
*/
var Util = {};

Util.scopeCallback = function(scope, fn) {
	return function() {
		fn.apply(scope, arguments);
	};
};

Util.newXMLDoc = function(initialNodeName) {
	var initial = '<' + initialNodeName + '></' + initialNodeName + '>';
	if (window.DOMParser) {
	    parser = new DOMParser();
	    xmlDoc = parser.parseFromString(initial,"text/xml");
	}
	else { //Internet Explorer
	    xmlDoc = new ActiveXObject("Microsoft.XMLDOM");
	    xmlDoc.async = false;
	    xmlDoc.loadXML(initial);
	}
	
	return xmlDoc;
};