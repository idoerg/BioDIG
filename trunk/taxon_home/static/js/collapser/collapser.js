(function($){
	/**
		JQuery Collapser Plugin
		Author: Andrew Oberlin
		Date: August 22, 2012
		
		Description: Collapses the div specified using a selector
		
		Dependencies:
			jQuery 1.7.2 or higher
			jQuery UI 1.8.18 or higher
	**/
	var public_methods = {
		/**
			Calls the zoomable plugin on initialization and only does so on load of the
			image so that it can properly get the height and width
		**/
		init: function(options) {
			return this.each(function() {
				$(this).data('collapsed', false);
				if (options.selector) {
					var selector = options.selector;
					var $element;
					if (options.siblings) {
						$element = $(this).siblings(options.selector);
					}
					else {
						$element = $(options.selector);
					}
					$element.show();
					$(this).on('click', function() {
						if ($(this).data('collapsed')) {
							$(this).data('collapsed', false);
							$element.slideDown();
							var $collapseImg = $(this).find('img.collapse');
							if ($collapseImg.length > 0) {
								var prevSrc = $collapseImg.attr('src');
								$collapseImg.attr('src', prevSrc.replace('arrow_right', 'arrow_down'));
							}
						}
						else {
							$(this).data('collapsed', true);
							$element.slideUp();
							var $collapseImg = $(this).find('img.collapse');
							if ($collapseImg.length > 0) {
								var prevSrc = $collapseImg.attr('src');
								$collapseImg.attr('src', prevSrc.replace('arrow_down', 'arrow_right'));
							}
						}
					});
					
					$(this).find('input', 'button').on('click', function(event) {
						event.stopPropagation();
					});
				}
				else {
					console.error('No element specified for collapser');
				}
			});
		}
	};

	$.fn.collapser = function(method) {

		// Method calling logic
		if ( public_methods[method] ) {
			return public_methods[ method ].apply( this, Array.prototype.slice.call( arguments, 1 ));
		} 
		else if ( typeof method === 'object' || ! method ) {
			return public_methods.init.apply( this, arguments );
		} 
		else {
			$.error( 'Method ' +  method + ' does not exist on jQuery.collapser' );
		}  
	};
})( jQuery );

