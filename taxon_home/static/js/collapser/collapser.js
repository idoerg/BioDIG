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
					
					$(this).data('collapseEl', $element);
					
					$(this).on('click', function() {
						if ($(this).data('collapsed')) {
							$(this).data('collapsed', false);
							$element.slideDown();
							var $collapseImg = $(this).find('img.collapse');
							if ($collapseImg.length > 0) {
								var prevSrc = $collapseImg.attr('src');
								$collapseImg.attr('src', prevSrc.replace('arrow_right', 'arrow_down'));
							}
							
							if (options.callback) {
								options.callback(false, $(this));
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
							
							if (options.callback) {
								options.callback(true, $(this));
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
		},
		collapse : function() {
			this.each(function() {
				var $element = $(this).data('collapseEl');
				if ($element) {
					$(this).data('collapsed', true);
					$element.slideUp();
					var $collapseImg = $(this).find('img.collapse');
					if ($collapseImg.length > 0) {
						var prevSrc = $collapseImg.attr('src');
						$collapseImg.attr('src', prevSrc.replace('arrow_down', 'arrow_right'));
					}
				}
			});
		},
		open : function() {
			this.each(function() {
				var $element = $(this).data('collapseEl');
				if ($element) {
					$(this).data('collapsed', false);
					$element.slideDown();
					var $collapseImg = $(this).find('img.collapse');
					if ($collapseImg.length > 0) {
						var prevSrc = $collapseImg.attr('src');
						$collapseImg.attr('src', prevSrc.replace('arrow_right', 'arrow_down'));
					}
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

