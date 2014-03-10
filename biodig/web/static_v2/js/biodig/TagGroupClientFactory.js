define(['jquery','URLBuilder'], function($, URLBuilder) {
     /**
     *  Validator for a TagGroup client.
    **/
    var ValidatorFactory = {
        getInstance: function() {
            // validator
            return {
                create: function(name) {
                    if (!name) throw { validation_error : 'Not a valid name' }
                },
                get: function(name,TagGroupid) {
                	if (!TagGroupid || isNan(TagGroupid)) throw { validation_error : 'The id is not a valid positive number' }
                        if (!name) throw { validation_error : 'Not a valid name' }
                }
            }
        }
    };
    
    /**
     *  TagGroupClient constructor that takes in the options
     *  such as url.
     *  
     *  @param opts: The options to customize this client.
    **/
    function TagGroupClient(opts) {
        if (! ('image_id' in opts))( {
            throw { message : 'Image ID is necessary for TagGroup Client use' };
        }

        this.url = sprintf(opts.url, opts.image_id);
	if (this.url[this.url.length -1] != '/') {
            this.url += '/';
	}
        this.validator = ValidatorFactory.getInstance();
    }

    TagGroupClient.prototype.create = function(name) {
        return $.Deferred(function(deferredObj) {
            $.ajax({
                url : this.url,
                method : 'POST',
                dataType : 'json',
                data : {
                    name: name
                },
                success : function(data) {
                    deferredObj.resolve(data);
                },
                error : function(jqXHR, textStatus, errorThrown) {
                    var e = $.parseJSON(jqXHR.responseText); 
                    deferredObj.reject(e);
                }
            });
        }).promise();
    };
    
    TagGroupClient.prototype.get = function(id) {
        return $.Deferred(function(deferredObj) {
            $.ajax({
                url : this.url + id,
                method : 'GET',
                dataType : 'json',
                success : function(data) {
                    deferredObj.resolve(data);
                },
                error : function(jqXHR, textStatus, errorThrown) {
                    var e = $.parseJSON(jqXHR.responseText); 
                    deferredObj.reject(e);
                }
            });
        }).promise();
    };

    TagGroupClient.prototype.list = function(opts) {
    	var urlBuilder = URLBuilderFactory.newBuilder(this.url);
    	$.each(opts, function(key, val) {
    		urlBuilder.addQuery(key, val, URLBuilderFactory.NOT_EMPTY);
    	});
    	
    	return $.Deferred(function(deferredObj) {
    		$.ajax({
    			url: urlBuilder.complete(),
    			method: 'GET',
    			success: function(data, textStatus, jqXHR) {
                    deferredObj.resolve(data);
                },
                error: function(jqXHR, textStatus, errorThrown) {
                    var e = $.parseJSON(jqXHR.responseText);
                    deferredObj.reject(e);
                }
    		});
    	}).promise();
    };

   TagGroupClient.prototype.update = function(tag_group_id) {
    	try {
    		this.validator.update(tag_group_id);
    	}
    	catch (e) {
    		return $.Deferred(function(deferredObj) {
                deferredObj.reject(e);
            }).promise();
    	}
    	
    	var data = {};
    	if (tag_group_id) data['tag_group_id'] = tag_group_id;
    	
    	return $.Deferred(function(deferredObj) {
    		$.ajax({
    			url: this.url + id,
    			method: 'PUT',
    			data: data,
    			success: function(data) {
    				deferredObj.resolve(data);
    			},
    			error: function(jqXHR, textStatus, errorThrown) {
                    var e = $.parseJSON(jqXHR.responseText);
                    deferredObj.reject(e);
                }
    		});
    	}).promise();
    };


    var settings = {
        url : '/images/%u/tagGroups/'
    };

    var TagGroupClientFactory = {
        getInstance : function(opts) {
            return new TagGroupClient($.extend({}, settings, opts));
        }
    };

    return TagGroupClientFactory;
});
