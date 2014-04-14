define(['jquery','URLBuilder'], function($, URLBuilder) {
    /**
     *  Sprintf
    **/
    String.prototype.format = function()
     {
        var content = this;
        for (var i=0; i < arguments.length; i++)
        {
             var replacement = '{' + i + '}';
             content = content.replace(replacement, arguments[i]); 
        }
        return content;
     };

 

    /**
     *  Validator for a TagGroup client.
    **/
    var ValidatorFactory = {
        getInstance: function() {
            // validator
            return {
                create: function(name) {
                    if (!name) throw { detail : 'Not a valid name' }
                },
                get: function(TagGroupid) {
                	if (!TagGroupid || isNaN(TagGroupid)) throw { detail : 'The id is not a valid positive number' }
                },
		list: function(opts) {
                	if (!opts['owner'] || isNaN(opts['owner'])) throw { detail : 'The ow is not a valid positive number' }
			if (!opts['name']) throw { detail : 'Not a valid name' }
                },
		update: function(TagGroupId) {
                           if (!TagGroupId || isNaN(TagGroupId)) throw { detail : 'The id is not a valid positive number' }
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
        if (! ('image_id' in opts)){
            throw { message : 'Image ID is necessary for TagGroup Client use' };
        }

        this.url = opts.url.format(opts.image_id);
	if (this.url[this.url.length -1] != '/') {
            this.url += '/';
	}
        this.validator = ValidatorFactory.getInstance();
        this.token= opts.token || null;
    }

    TagGroupClient.prototype.create = function(name) {
        try {
    		this.validator.create(name);
    	}
    	catch (e) {
    		return $.Deferred(function(deferredObj) {
                deferredObj.reject(e);
            }).promise();
    	}
    	var self=this;
        // Add the Authorization Header only if the token is set
        var addAuthToken = this.token ?
            function (xhr) {
                xhr.setRequestHeader('Authorization', 'Token ' + self.token) ;
            } :
            function(xhr) {};

        return $.Deferred(function(deferredObj) {
            $.ajax({
                url : self.url,
                method : 'POST',
                beforeSend : addAuthToken,
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
        try {
    		this.validator.get(id);
    	}
    	catch (e) {
    		return $.Deferred(function(deferredObj) {
                deferredObj.reject(e);
            }).promise();
    	}
        var self=this;
        var addAuthToken = this.token ?
            function (xhr) {
                xhr.setRequestHeader('Authorization', 'Token ' + self.token) ;
            } :
            function(xhr) {};
        return $.Deferred(function(deferredObj) {
            $.ajax({
                url : self.url + id,
                method : 'GET',
                beforeSend : addAuthToken,
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
        try {
    		this.validator.list(opts);
    	}
    	catch (e) {
    		return $.Deferred(function(deferredObj) {
                deferredObj.reject(e);
            }).promise();
    	}

    	var urlBuilder = URLBuilder.newBuilder(this.url);
    	$.each(opts, function(key, val) {
    		urlBuilder.addQuery(key, val, URLBuilder.NOT_EMPTY);
    	});
        var self=this;
        var addAuthToken = this.token ?
            function (xhr) {
                xhr.setRequestHeader('Authorization', 'Token ' + self.token) ;
            } :
            function(xhr) {};

  	
  	return $.Deferred(function(deferredObj) {
    		$.ajax({
    			url: urlBuilder.complete(),
    			method: 'GET',
                        beforeSend : addAuthToken,
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

   TagGroupClient.prototype.update = function(TagGroupId) {
    	try {
    		this.validator.update(TagGroupId);
    	}
    	catch (e) {
    		return $.Deferred(function(deferredObj) {
                deferredObj.reject(e);
            }).promise();
    	}
    	var self=this;
        var addAuthToken = this.token ?
            function (xhr) {
                xhr.setRequestHeader('Authorization', 'Token ' + self.token) ;
            } :
            function(xhr) {};
    	var data = {
            name : name
        };
    	
    	return $.Deferred(function(deferredObj) {
    		$.ajax({
    			url: self.url + TagGroupId,
    			method: 'PUT',
                        beforeSend : addAuthToken,
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
        url : '/rest/v2/images/{0}/tagGroups/'
    };

    var TagGroupClientFactory = {
        getInstance : function(opts) {
            return new TagGroupClient($.extend({}, settings, opts));
        }
    };

    return TagGroupClientFactory;
});
