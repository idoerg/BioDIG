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
        TagClientFactory : '/static_v2/js/biodig/TagClientFactory',
        URLBuilder: '/static_v2/js/biodig/clients/URLBuilderFactory'
    }
});

var deps = ['jquery', 'TagClientFactory'];

require(deps, function($, TagClientFactory,URLBuilder) {
    var tagClient = TagClientFactory.getInstance({
        image_id : 1,
    tagId : 2,
        token : '70599f3827b731b9c39500fb1e2268abaf59462d'
    });
    
    // setting up POST tester
    $('#PostTagForm #p').on('click', function() {

    var name= $('#PostTagForm input[name=name]').val();
    var points= [
         {
      x : Number($('#PostTagForm input[name=X1]').val()),
          y : Number($('#PostTagForm input[name=Y1]').val())
     },
         {
      x : Number($('#PostTagForm input[name=X2]').val()),
          y : Number($('#PostTagForm input[name=Y2]').val())
     }        
         ];
        var color= {
        r : Number($('#PostTagForm input[name=r]').val()),
        g : Number($('#PostTagForm input[name=g]').val()),
        b : Number($('#PostTagForm input[name=b]').val())
    };
        $.when(tagClient.create(name,points,color))
            .done(function(data) {
                alert("Created!");
            })
            .fail(function(e) {
                alert("Failed with error: " + e.detail);
            });
    });

    // setting up GET tester
    $('#GetTagForm #g').on('click', function() {

        var tagId= $('#GetTagForm input[name=TagId]').val();
        $.when(tagClient.get(tagId))
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
        offset : $('#ListForm input[name=offset]').val(),
        limit : $('#ListForm input[name=limit]').val(),
        ldate : $('#ListForm input[name=ldate]').val(),
        cdate : $('#ListForm input[name=cdate]').val(),
                owner : $('#ListForm input[name=owner]').val(),
                name : $('#ListForm input[name=name]').val()
              };
       
        $.when(tagClient.list(opts))
            .done(function(data) {
                alert("Got it!");
            })
            .fail(function(e) {
                alert("Failed with error: " + e.detail);
            });
    });
    
   // setting up UPDATE tester
    $('#UpdateForm #u').on('click', function() {
        var TagId= $('#UpdateForm input[name=TagId]').val();

        $.when(tagClient.update(TagId))
            .done(function(data) {
                alert("Got it!");
            })
            .fail(function(e) {
                alert("Failed with error: " + e.detail);
            });
      });
});
