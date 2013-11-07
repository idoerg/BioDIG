(function($){
	/**
		JQuery Select Box Plugin
		Author: Andrew Oberlin
		Date: Febuary 4, 2013
		
		Description: Creates a pretty select box to replace the current one
		
		Dependencies:
			jQuery 1.7.2 or higher
			jQuery UI 1.8.18 or higher
	**/
	var private_methods = {
		
	};
	
	var public_methods = {
		/**
			Calls the image updater initialization on a div
		**/
		init: function(options) {
			return this.each(function() {
				var container = $('<div />', { 
					'class' : 'selectContainer ' + $(this).attr('class'),
					'name' : $(this).attr('name')
				});
				var selectView = $('<div />', { 'class' : 'selectView' }).appendTo(container);
				var selectValue = $('<span />', { 'class' : 'selectValue' }).appendTo(selectView);
				var image = $('<img />', { 
					'src' : options.imagesUrl + 'arrow_down.png',
					'class' : 'selectIcon'
				}).appendTo(selectView);
				
				var menu = $('<div />', { 'class' : 'selectMenu' }).appendTo(container).hide();
				selectView.on('click', function() {
					menu.toggle();
				});
				
				$(document).mouseup(function(e) {
					if (container.has(e.target).length === 0) {
						menu.hide();
					}
				});
				
				var self = $(this);
				
				$(this).children('option').each(function(index) {
					var option = $('<div />', {
						'class' : 'selectOption' ,
						'text'  : $(this).text()
					}).appendTo(menu);
					
					var value = $(this).val();
					
					if (index == 0) {
						self.val(value);
						selectValue.text(option.text());
					}
					
					option.on('click', function() {
						self.val(value);
						selectValue.text(option.text());
						menu.hide();
						var change = self.data('change');
						if (change) {
							change(value);
						}
					});
				});
				
				container.insertAfter($(this));
				
				menu.width(container.width() - 2);
				
				$(this).hide();
			});
		},
		change : function(changeFn) {
			return this.each(function() {
				$(this).data('change', changeFn);
			});
		}
	};

	$.fn.selectBox = function(method) {

		// Method calling logic
		if ( public_methods[method] ) {
			return public_methods[ method ].apply( this, Array.prototype.slice.call( arguments, 1 ));
		} 
		else if ( typeof method === 'object' || ! method ) {
			return public_methods.init.apply( this, arguments );
		} 
		else {
			$.error( 'Method ' +  method + ' does not exist on jQuery.selectBox' );
		}  
	};
})( jQuery );

