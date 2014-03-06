define(['jquery'], function($) {
	var NOT_EMPTY = 0;
	var ALLOW_EMPTY = 1;
	
	function URLBuilder(baseURL) {
		this.url = baseURL;
		this.queryParams = {};
	}
	
	URLBuilder.prototype.addQuery = function(key, value, flag) {
		if (flag == NOT_EMPTY && !value) return;
		this.queryParams[key] = value;
	};
	
	URLBuilder.prototype.complete = function() {
		var urlArr = [this.url];
		var index = 0;
		$.each(this.queryParams, function(key, val) {
			urlArr.push(index == 0 ? "?" : "&");
			urlArr.push(encodeURIComponent(key), '=', encodeURIComponent(value));
			index++;
		});
		
		return urlArr.join("");
	};
	
    var URLBuilderFactory = {
        newBuilder : function(baseURL) {
        	return new URLBuilder(baseURL);
        },
        NOT_EMPTY : NOT_EMPTY,
        ALLOW_EMPTY : ALLOW_EMPTY
    };
    
    return URLBuilderFactory;
});