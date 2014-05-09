var deps = [
    'jquery', 'settings', 'lib/util', 'biodig/clients/URLBuilderFactory'
];

define(deps, function($, settings, util, URLBuilderFactory) {

    /**
     *  Validator for the User client.
    **/
    var ValidatorFactory = {
        validate_email: function(email) {
            var atpos = email.indexOf("@");
            var dotpos = email.lastIndexOf(".");
            if (atpos < 1 || dotpos < atpos+2 || dotpos+2 >= email.length) {
                return false;
            }
            else {
                return true;
            }
        },
        getInstance: function() {
            // validator
            return {
                create: function(username, password, email) {

                    if (!username) throw { detail : 'The username of the user was empty' }

                    if (!password) throw { detail : 'The password for this user was empty' }

                    if (!email || !ValidatorFactory.validate_email(email)) throw { detail : 'The email is not a valid email address' }

                },
                get: function(id) {
                	if (!id || isNaN(id)) throw { detail : 'The id is not a valid positive number' }
                },
                update: function(id, opts) {
                	if (!id || isNaN(id)) throw { detail : 'The id is not a valid positive number' }

                	if ($.isEmptyObject(opts))
                        throw { detail : 'No changes have been made to this user' }
                },
                delete: function(id) {
                    if (!id || isNaN(id)) throw { detail : 'The id is not a valid positive number' }
                },
                activate: function(id, activation_key) {
                    if (!id || isNaN(id)) throw { detail : 'The id is not a valid positive number' }
                    if (!activation_key) throw { detail: 'The activation must not be empty' }
                }
            }
        }
    };

    /**
     *  User Client constructor that takes in the options
     *  such as url.
     *
     *  @param opts: The options to customize this client.
    **/
    function UserClient(opts) {
        this.url = opts.url;
        if (this.url[this.url.length - 1] != '/') {
            this.url += '/';
        }

        this.token = opts.token || null;

        this.validator = ValidatorFactory.getInstance();
    }

    /**
     *  Creates an User on the server by sending the data over
     *  to the server when enacted. An error state callback will be
     *  called on validation error. The error will contain information
     *  about the validation error.
     *
     *  @param UserData: The raw data from a FileReader in Base64 encoding
     *                    for the User to send.
     *  @param description: The description of the User.
     *  @param altText: The alternate text for this User.
     *
     *  @return A deferred object that will enact the correct server action
     *          to create the User.
    **/
    UserClient.prototype.create = function(username, password, email, firstname, lastname) {
        try {
            this.validator.create(username, password, email);
        }
        catch (e) {
            return $.Deferred(function(deferredObj) {
                deferredObj.reject(e);
            }).promise();
        }

        var self = this;

        var data = {
            'username' : username,
            'password' : password,
            'email' : email
        };

        if (firstname) data['first_name'] = firstname;
        if (lastname) data['last_name'] = lastname;

        return $.Deferred(function(deferredObj) {
            $.ajax({
                url: self.url,
                method: 'POST',
                beforeSend: util.auth(self.token),
                data: data,
                success: function(data, textStatus, jqXHR) {
                    deferredObj.resolve(data);
                },
                error: function(jqXHR, textStatus, errorThrown) {
                    try {
                        var e = $.parseJSON(jqXHR.responseText);
                        deferredObj.reject(e);
                    }
                    catch (e) {
                        deferredObj.reject({ detail: 'An unidentified error occurred with the server.'});
                    }
                }
            });
        }).promise();
    };

    /**
     *  Gets a list of Users that is paginated. Allows for filtering
     *  by owner and date.
     *
     *  @param opts: The optional query parameters for the list function.
     *               Takes the following properties:
     *
     *  		     owner: The username of the owner to search.
     *  			 dateCreated: The formatted date string for the date created.
     *  			 lastModified: The formatted date string for the date last modified.
     *  			 limit: The number of entries to retrieve.
     *               offset: The number of entries to skip before listing.
    **/
    UserClient.prototype.list = function(opts) {
    	var urlBuilder = URLBuilderFactory.newBuilder(this.url);
    	$.each(opts, function(key, val) {
    		urlBuilder.addQuery(key, val, URLBuilderFactory.NOT_EMPTY);
    	});

        // Add the Authorization Header only if the token is set
        var self = this;

    	return $.Deferred(function(deferredObj) {
    		$.ajax({
    			url: urlBuilder.complete(),
                beforeSend: util.auth(self.token),
    			method: 'GET',
    			success: function(data, textStatus, jqXHR) {
                    deferredObj.resolve(data);
                },
                error: function(jqXHR, textStatus, errorThrown) {
                    try {
                        var e = $.parseJSON(jqXHR.responseText);
                        deferredObj.reject(e);
                    }
                    catch (e) {
                        deferredObj.reject({ detail: 'An unidentified error occurred with the server.'});
                    }
                }
    		});
    	}).promise();
    };

    /**
     *  Gets a single User given the id.
     *
     *  @param id: The id of the User.
    **/
    UserClient.prototype.get = function(id) {
    	try {
    		this.validator.get(id);
    	}
    	catch (e) {
    		return $.Deferred(function(deferredObj) {
    			deferredObj.reject(e);
    		});
    	}

        var self = this;

    	return $.Deferred(function(deferredObj) {
    		$.ajax({
    			url: self.url + id,
    			beforeSend: util.auth(self.token),
                method: 'GET',
    			success: function(data, textStatus, jqXHR) {
                    deferredObj.resolve(data);
                },
                error: function(jqXHR, textStatus, errorThrown) {
                    try {
                        var e = $.parseJSON(jqXHR.responseText);
                        deferredObj.reject(e);
                    }
                    catch (e) {
                        deferredObj.reject({ detail: 'An unidentified error occurred with the server.'});
                    }
                }
    		});
    	}).promise();
    };

    /**
     *  Updates the given User with the description and altText, which
     *  are optional.
     *
     *  @param description: The new description of the User.
     *  @param altText: The new altText for the User.
    **/
    UserClient.prototype.update = function(id, opts) {
    	try {
    		this.validator.update(id, opts);
    	}
    	catch (e) {
    		return $.Deferred(function(deferredObj) {
                deferredObj.reject(e);
            }).promise();
    	}

        var self = this;

    	return $.Deferred(function(deferredObj) {
    		$.ajax({
    			url: self.url + id,
                beforeSend: util.auth(self.token),
    			method: 'PUT',
    			data: opts,
    			success: function(data) {
    				deferredObj.resolve(data);
    			},
    			error: function(jqXHR, textStatus, errorThrown) {
                    try {
                        var e = $.parseJSON(jqXHR.responseText);
                        deferredObj.reject(e);
                    }
                    catch (e) {
                        deferredObj.reject({ detail: 'An unidentified error occurred with the server.'});
                    }
                }
    		});
    	}).promise();
    };

    UserClient.prototype.delete = function(id) {
        try {
            this.validator.delete(id);
        }
        catch (e) {
            return $.Deferred(function(deferredObj) {
                deferredObj.reject(e);
            }).promise();
        }

        return $.Deferred(function(deferredObj) {
            $.ajax({
                url: self.url + id,
                beforeSend: util.auth(self.token),
                method: 'DELETE',
                success: function(data) {
                    deferredObj.resolve(data);
                },
                error: function(jqXHR, textStatus, errorThrown) {
                    try {
                        var e = $.parseJSON(jqXHR.responseText);
                        deferredObj.reject(e);
                    }
                    catch (e) {
                        deferredObj.reject({ detail: 'An unidentified error occurred with the server.'});
                    }
                }
            });
        }).promise();
    };

    UserClient.prototype.activate = function(id, activation_key) {
        try {
            this.validator.activate(id, activation_key);
        }
        catch (e) {
            return $.Deferred(function(deferredObj) {
                deferredObj.reject(e);
            }).promise();
        }

        var self = this;

        return $.Deferred(function(deferredObj) {
            $.ajax({
                url: self.url + id + '/activate/' + activation_key,
                method: 'POST',
                beforeSend: util.auth(self.token),
                success: function(data, textStatus, jqXHR) {
                    deferredObj.resolve(data);
                },
                error: function(jqXHR, textStatus, errorThrown) {
                    try {
                        var e = $.parseJSON(jqXHR.responseText);
                        deferredObj.reject(e);
                    }
                    catch (e) {
                        deferredObj.reject({ detail: 'An unidentified error occurred with the server.'});
                    }
                }
            });
        }).promise();
    };

    // default settings for an UserClient
    var defaults = {
        url: settings.SITE_URL + 'rest/v2/users/',
        token: null
    };

    var UserClientFactory = {
        /**
         *  Creates an instance of the User Client.
        **/
        create: function(opts) {
            return new UserClient($.extend({}, defaults, opts));
        }
    };

    return UserClientFactory;
});
