
var deps = [
    'jquery', 'underscore', 'beetledig/clients/OrthologClient',
    'beetledig/links/linker',
    'text!beetledig/tmpl/orthologlist.html',
    'text!beetledig/tmpl/ortholog-link-container.html'
];

define(deps, function($, _, OrthologClient, linker, OrthologListTmpl, OrthologLinkTmpl) {
    var OrthologLinkTemplate = _.template(OrthologLinkTmpl);
    var OrthologListTemplate = _.template(OrthologListTmpl);

    function OrthologViewer(selector,links,TC) {
        this.$container = $(selector);
        this.client = OrthologClient.create();
        var self = this;
        $.when(this.client.get(TC))
            .done(function(ortho_Dict) {
                  var addList = function(list,name,link) {
                  var $orthoView = $(OrthologLinkTemplate({'name':name}));
                     var $orthoList = $(OrthologListTemplate({
                          'ortho_list' : list,
                          'name' : name     
                      }));
                     $orthoView.append($orthoList);
                      
                     if (linker){
                         if ('link' in linker && typeof linker.link == 'function'){
                             $orthoView.find('.ortho-btn').on('click',function() {
                                linker.link($(this).data('ortholog'),link);
                                
                             });
                             
                         }
                         else if (typeof linker == 'function'){
                             $orthoView.find(".ortho-btn").on('click', function() {
                               linker($(this).data('ortholog'),link);
                         }); 
                        }
                    }
                    self.$container.append($orthoView); 

                   };
                  if ($.isEmptyObject(links)) {
                       addList (ortho_Dict, 'Ortholog',null);
                  }
                  else {
                       $.each(links, function(name,link) {
                          //window.alert(ortho_Dict[name]+name+link);
                          addList (ortho_Dict[name],name,link);
                          
                    });
                  }
            })
            .fail(function(e) {
                self.$container.append('ERROR: ' + TC + (e.detail || e.message));
            });
        }

    return {
        create : function(selector,links,TC) {
            if (!TC) {
                selector = $(selector);
                TC = selector.data('tcId');
            }
            return new OrthologViewer(selector,links,TC);
        }
        
     }
    
});
