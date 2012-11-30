(function($){
	/**
		JQuery Taggable Plugin
		Author: Andrew Oberlin
		Date: July 4, 2012
		
		Description: Takes in a picture and allows the user to zoom in and out 
			using the controls created by the zoomable plugin. The user can also drag the
			image around and zoom if they wish to do so. The main focus however is on
			using the canvas element to draw tags assign descriptions to those tags
			and then save the tags for viewing using ajax. Supports rectangular tags and 
			polygonal tags.
		
		Dependencies:
			jQuery 1.7.2 or higher
			jQuery UI 1.8.18 or higher
			Util.js in js/util
			zoomable.js and all of its dependencies
			KineticJs 3.10.0
			taggable.css
	**/  
	var publicMethods = {
		init : function(options) {
			// evaluate options
			var settings = {
				parent : $(this).parent(),
				originalData : [],
				title : 'Genome Links',
				alreadyLoaded : false,
				siteUrl : '/'
			};
			
			// make sure that the imagesUrl ends in a slash
			if (options.imagesUrl[options.imagesUrl.length - 1] != '/') {
				options.imagesUrl += '/';
			}
			
			if (options.siteUrl[options.siteUrl.length - 1] != '/') {
				options.siteUrl += '/';
			}
			
			$.extend(settings, options);
			
			// do this for each thing this has been called on
			return this.each(function() {
				// the object that keeps track of the tagging application
				var taggableObj = new TaggerUI(
					$(this), settings.parent, settings.originalData, settings.imageMetadata,
					settings.genomicInfo, settings.imagesUrl, settings.siteUrl,
					settings.alreadyloaded, settings.callback
				);
				
				// saves the taggable object in the data cache for reference
				$(this).data('taggable', taggableObj);
			});
		}
	};
	
	$.fn.taggable = function(method) {

		// Method calling logic
		if ( publicMethods[method] ) {
			return publicMethods[ method ].apply( this, Array.prototype.slice.call( arguments, 1 ));
		} 
		else if ( typeof method === 'object' || ! method ) {
			return publicMethods.init.apply( this, arguments );
		} 
		else {
			$.error( 'Method ' +  method + ' does not exist on jQuery.taggable' );
		}  
	};
})( jQuery );