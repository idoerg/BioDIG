(function($){
	/**
		JQuery Zoomable Plugin
		Author: Andrew Oberlin
		Date: July 4, 2012
		
		Description: Takes in a picture and allows the user to zoom in and out 
			using the controls created by the plugin. The user can also drag the
			image around and zoom if they wish to do so.
		
		Dependencies:
			jQuery 1.7.2 or higher
			jQuery UI 1.8.18 or higher
			zoomable.css
	**/
	var private_methods = {
		/**
			Creates the entire structure of the plugin. Renders the zoomable template and 
			creates the controls for zooming in and out
		**/
		createStructure: function(options, $parent, $img) {
			$img.off('load');
			// renders the zoomable template, structural
			var id = $img.attr('id');
			$parent.append(private_methods.renderTmpl(id)); 
			
			if (options.actualImageSrc) {
				var actualImage = new Image();
				actualImage.onload = function() {
					private_methods.resetForActualImage(actualImage, $img);
				};
				actualImage.src = options.actualImageSrc;
			}
			
			// uses the jQueryUI slider plugin to create the controls as a slider
			$('#' + id + '-zoomable-slider').slider({
				orientation: 'vertical',
				range: 'min',
				min: 0,
				max: 100,
				value: 0
			});
			
			// this is the container of everything and the image needs to be moved inside of it
			var $zoomableContainer = $('#' + id + '-zoomable-container');
			if ('originalHeight' in options) {
				$zoomableContainer.height(options.originalHeight);
			}
			if ('originalWidth' in options) {
				$zoomableContainer.width(options.originalWidth);
			}
			
			$zoomableContainer.append($img);
			
			// makes the image fit inside of the zoomable container no matter what its
			// aspect ratio is
			var imgRatio = $img.width()/$img.height();
			var containerRatio = $zoomableContainer.width()/$zoomableContainer.height();
			if (imgRatio > containerRatio) {
				$img.css('width', $zoomableContainer.width());
				var topVal = ($zoomableContainer.height() - $img.height())/2;
				$img.css('top', topVal);
			}
			else if (imgRatio < containerRatio) {
				$img.css('height', $zoomableContainer.height());
				var leftVal = ($zoomableContainer.width() - $img.width())/2;
				$img.css('left', leftVal);
			}
			
			// controls are setup for the zooming bar (PLUS)
			$('#' + id + '-zoomable-plus').on('click', function() {
				$('#' + id + '-zoomable-slider').slider('value', $('#' + id + '-zoomable-slider').slider('value') + 1);
				if (options.zoom_callback) {
					if (options.zoom_callback_args) {
						options.zoom_callback.apply(this, options.zoom_callback_args);
					}
					else {
						options.zoom_callback();
					}
				}
			});
			
			
			// controls are setup for the zooming bar (MINUS)
			$('#' + id + '-zoomable-minus').on('click', function() {
				$('#' + id + '-zoomable-slider').slider('value', $('#' + id + '-zoomable-slider').slider('value') - 1);
				if (options.zoom_callback) {
					if (options.zoom_callback_args) {
						options.zoom_callback.apply(this, options.zoom_callback_args);
					}
					else {
						options.zoom_callback();
					}
				}
			});
			
			// stores the original height for use later
			$img.data('originalHeight', $img.height());
			$img.data('originalWidth', $img.width());
			
			// sets up the slider to change the zoom level
			$('#' + id + '-zoomable-slider').on('slidechange', function(event, ui) {
				private_methods.changeEvent(event, ui, id);
				if (options.zoom_callback) {
					if (options.zoom_callback_args) {
						options.zoom_callback.apply(this, options.zoom_callback_args);
					}
					else {
						options.zoom_callback();
					}
				}
			});
			
			// sets up the zoomSlider to be hidden by default and appear on mouseover
			$zoomableContainer.children('.zoomable-slider-container').hide();
			
			$zoomableContainer.on('mouseover', function() {
				$(this).children('.zoomable-slider-container').show();
			});
			
			$zoomableContainer.on('mouseout', function() {
				$(this).children('.zoomable-slider-container').hide();
			});
		},
		renderTmpl: function(id) {
			return $('<div> \
						<div id="' + id + '-zoomable-container" class="zoomable-container"> \
							<div class="zoomable-slider-container"> \
							<div class="zoomable-plus zoomable-controls"> \
								<button id="' + id + '-zoomable-plus">+</button> \
							</div> \
							<div id="' + id + '-zoomable-slider" class="zoomable-slider"> \
							</div> \
							<div class="zoomable-minus zoomable-controls"> \
								<button id="' + id + '-zoomable-minus">-</button> \
						   </div> \
						</div> \
					</div> \
				</div>');
		},
		/**
			Zooms in by scaling the image and adjusting its position to be correct.
			Called by the slider's change event.
		**/
		changeEvent: function(event, ui, id) {
			var $img = $('#' + id);
			
			// gets scale based on the slider value
			var scale = private_methods.levelToZoom(ui.value);
			
			// figures out the new height and width after scaling
			var newHeight = scale*$img.data('originalHeight');
			var newWidth = scale*$img.data('originalWidth');
			
			// adjusts left and right to center the zoom
			var curLeft = parseInt($img.css('left').split('px')[0]);
			var curTop = parseInt($img.css('top').split('px')[0]);
			
			var newLeft = curLeft - (newWidth - $img.width())/2;
			var newTop  = curTop - (newHeight - $img.height())/2;

			// finalizes zoom by applying the properties
			$img.css('height', newHeight);
			$img.css('width', newWidth);
			
			$img.css('left', newLeft + "px");
			$img.css('top', newTop + "px");
		},
		/**
			Zooms in or out based on the percent and the
			image's original height and width
		**/
		levelToZoom: function(percent) {
			// convert 1% change = 5% change in zoom level
			return 1 + percent*0.05;
		},
		resetForActualImage: function(actualImage, curImage) {
			curImage.attr('src', actualImage.src);
		}
	};
	
	var public_methods = {
		/**
			Calls the zoomable plugin on initialization and only does so on load of teh
			image so that it can properly get the height and width
		**/
		init: function(options) {
			return this.each(function() {
				$(this).addClass('zoomable-src');
				$(this).parent().addClass('zoomable-parent');
				
				var self = this;
				
				var init = function() { 
					// creates the structure
					private_methods.createStructure(options, $(self).parent(), $(self));
					$(self).draggable();
					
					// checks for callback and callback arguments
					if (options.callback && !$(self).data('zoomable')) {
						if (options.callback_args) {
							options.callback.apply(self, options.callback_args);
							$(self).data('zoomable', true);
						}
						else {
							options.callback();
							$(self).data('zoomable', true);
						}
					}
				};
				if (options.alreadyLoaded) {
					init();
				}
				else {
					$(this).load(init);
				}
			});
		},
		zoom: function(magnitude) {
			var id = $(this).attr('id');
			var zoomSlider = $('#' + id + '-zoomable-slider');
			var newVal = zoomSlider.slider("value") + magnitude;
			newVal = newVal < 100 ? newVal : 100;
			newVal = newVal > 0 ? newVal : 0;
			zoomSlider.slider("value", newVal);
		}
	};

	$.fn.zoomable = function(method) {

		// Method calling logic
		if ( public_methods[method] ) {
			return public_methods[ method ].apply( this, Array.prototype.slice.call( arguments, 1 ));
		} 
		else if ( typeof method === 'object' || ! method ) {
			return public_methods.init.apply( this, arguments );
		} 
		else {
			$.error( 'Method ' +  method + ' does not exist on jQuery.zoomable' );
		}  
	};
})( jQuery );

