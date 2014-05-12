require.config({ 
    baseUrl : '../js/',
    shim : {
        jquery : {
            init: function() {
                return $;
            }
        }
    },
    paths : {
        jquery : '/static_v2/js/lib/jquery-1.11.0.min',
        TagGroupClientFactory : '/static_v2/js/biodig/TagGroupClientFactory',
        URLBuilder: '/static_v2/js/biodig/clients/URLBuilderFactory'
    }
});

var deps = ['jquery', 'TagGroupClientFactory'];

require(deps, function($, TagGroupClientFactory,URLBuilder) {
    var tagGroupClient = TagGroupClientFactory.getInstance({
        image_id : 1,
        token : '70599f3827b731b9c39500fb1e2268abaf59462d'
    });
    
    // setting up POST tester
    $('#PostTagGroupForm #p').on('click', function() {

        var name = $('#PostTagGroupForm input[name=name]').val();
        $.when(tagGroupClient.create(name))
            .done(function(data) {
                alert("Created!");
            })
            .fail(function(e) {
                alert("Failed with error: " + e.detail);
            });
    });

    // setting up GET tester
    $('#GetTagGroupForm #g').on('click', function() {

        var tagGroupId= $('#GetTagGroupForm input[name=TagGroupId]').val();
        $.when(tagGroupClient.get(tagGroupId))
            .done(function(data) {
                alert("Got it!");
            })
            .fail(function(e) {
                alert("Failed with error: " + e.detail);
            });
    });
    
    // setting up list tester
    $('#ListForm #l').on('click', function() {

    var opts = {
        ldate : $('#ListForm input[name=ldate]').val(),
        cdate : $('#ListForm input[name=cdate]').val(),
                owner : $('#ListForm input[name=owner]').val(),
                name : $('#ListForm input[name=name]').val()
              };
       
        $.when(tagGroupClient.list(opts))
            .done(function(data) {
                alert("Got it!");
            })
            .fail(function(e) {
                alert("Failed with error: " + e.detail);
            });
    });
    
   // setting up UPDATE tester
    $('#UpdateForm #u').on('click', function() {
        var TagGroupId= $('#UpdateForm input[name=TagGroupId]').val();
        $.when(tagGroupClient.update(TagGroupId))
            .done(function(data) {
                alert("Got it!");
            })
            .fail(function(e) {
                alert("Failed with error: " + e.detail);
            });
      });
});
