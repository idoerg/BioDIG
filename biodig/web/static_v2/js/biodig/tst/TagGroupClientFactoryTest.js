require.config({
    shim : {
        jquery : {
            init: function() {
                return $;
            }
        }
    },
    paths : {
        jquery : '/static/js/jquery/1.11.0/jquery.min',
        TagGroupClientFactory : '/static/js/biodig/TagGroupClientFactory',
        URLBuilder: '/static/js/biodig/URLBuilder'
    }
});

var deps = ['jquery', 'TagGroupClientFactory'];

require(deps, function($, TagGroupClientFactory) {
    // setting up POST tester
    $('#tagGroupForm #p').on('click', function() {
        var tagGroupClient = TagGroupClientFactory.getInstance({ image_id : 1 });
        var name = $('#tagGroupForm input[name=name]').val();
        tagGroupClient.create(name)
            .done(function(data) {
                alert("Created!");
            })
            .fail(function(e) {
                alert("Failed with error: " + e.message);
            });
    });

    // setting up GET tester
    $('#tagGroupForm #g').on('click', function() {
        var tagGroupClient = TagGroupClientFactory.getInstance({ image_id : 1 });
        var name = $('#tagGroupForm input[name=name]').val();
        var tagGroupId= $('#tagGroupForm input[tagGroupId=tagGroupId]').val();
        tagGroupClient.get(name)
        tagGroupClient.getTagGroup(tagGroupId)
            .done(function(data) {
                alert("Got it!");
            })
            .fail(function(e) {
                alert("Failed with error: " + e.message);
            });
    });
    
    // setting up list tester
    $('#tagGroupForm #l').on('click', function() {
        var tagGroupClient = TagGroupClientFactory.getInstance({ image_id : 1 });
	var opts = {
		lastModified: $('#tagGroupForm input[lastmodified=lastmodified]').val(),
		dateCreated: 
	};
        var lastModified = $('#tagGroupForm input[lastmodified=lastmodified]').val();
        var dateCreated = $('#tagGroupForm input[dateCreated=datecreated]').val();
        var user = $('#tagGroupForm input[user=user]').val();
        var image_id= $('#tagGroupForm input[image_id=image_id]').val();
        var name= $('#tagGroupForm input[name=name]').val();
        tagGroupClient.list(opts)
            .done(function(data) {
                alert("Got it!");
            })
            .fail(function(e) {
                alert("Failed with error: " + e.message);
            });
    });
    
   // setting up UPDATE tester
    $('#tagGroupForm #u').on('click', function() {
        var tagGroupClient = TagGroupClientFactory.getInstance({ image_id : 1 });
        var image_id = $('#tagGroupForm input[image_id=image_id]').val();
        var tagGroupId= $('#tagGroupForm input[tagGroupId=tagGroupId]').val();
        tagGroupClient.getTagGroup(name)
        tagGroupClient.getTagGroup(tagGroupId)
            .done(function(data) {
                alert("Got it!");
            })
            .fail(function(e) {
                alert("Failed with error: " + e.message);
            });
});
