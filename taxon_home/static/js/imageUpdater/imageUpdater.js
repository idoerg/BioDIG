(function($){
	/**
		JQuery Image Updater Plugin
		Author: Andrew Oberlin
		Date: August 22, 2012
		
		Description: Updates the Images 
		
		Dependencies:
			jQuery 1.7.2 or higher
			jQuery UI 1.8.18 or higher
	**/
	var private_methods = {
		/**
		
		**/
		addPagination: function($self) {
			var settings = $self.data('settings');
			$self.append('<div id="' + settings.organism + 'Pagination" class="image-pagination"> \
					<div style="float:left"> \
						Showing <span class="first-image">1</span>-<span class="last-image">' + settings.picsPerPage +
						'</span> of <span class="num-images">' + settings.numImages + '</span> \
					</div> \
					<div class="last pagination-control"> \
		        		<span>&gt;&gt;</span> \
		        	</div> \
					<div class="next pagination-control"> \
			        	<span>&gt;</span> \
			        </div> \
		        	<div class="numbers_holder" style="float:right;"> \
		        		<input type="text" value="' + settings.currentPage + '"/> \
		        	</div> \
		        	<div class="previous pagination-control"> \
		        		<span>&lt;</span> \
		        	</div> \
			        <div class="first pagination-control"> \
			        	<span>&lt;&lt;</span> \
			        </div> \
			    </div> \
			');
			    
			$self.find('.last').on('click', function() {
				private_methods.callNewImageSet($self, settings.numPages);
			});
			 
		    $self.find('.previous').on('click', function() {
		    	private_methods.callNewImageSet($self, settings.currentPage - 1);
			});
		    
		    $self.find('.next').on('click', function() {
		    	private_methods.callNewImageSet($self, settings.currentPage + 1);
			});
		    
		    $self.find('.first').on('click', function() {
		    	private_methods.callNewImageSet($self, 1);
			});
		    
		    
		},
		/**
			Adds a small template that says no images were found
		**/
		addNoImagesTemplate : function($self) {
			$self.append('<div style="margin-bottom: 10px; text-align: center; color: #3366BB;"> \
				<span> Sorry, no images were found.</span> \
			</div>');
		},
		/**
			Converts the new page to a range of pictures
		**/
		getRange : function(picsPerPage, page) {
	        var lower =  (page - 1) * picsPerPage
	        var upper = lower + picsPerPage - 1
	        return [lower, upper];
	    },
		/**
			Gets a new image set using an ajax call to the change picture 
			application
		**/
		callNewImageSet: function($self, newPage) {
	        var settings = $self.data('settings');
			
			if (newPage < 1) {
	            newPage = 1;
	        }
	        else if (newPage > settings.numPages) {
	            newPage = settings.numPages;
	        }

	        var range = private_methods.getRange(settings.picsPerPage, newPage);
	        $.ajax({
	            url: settings.siteUrl + "images/change/",
	            type: 'POST',
	            data: {
	                rangeX : range[0],
	                rangeY : range[1],
	                organism : settings.organism
	            },
	            dataType: 'json',
	            context: document.body,
	            success: function(data){
	            	numPicsDisplayed = 0
					if ('error' in data && !data.error) {
	                    var $table = $self.find('table tbody').empty();
	                    
	                    var $currentRow = $('<tr>').appendTo($table);
	                    for (var i = 0; i < data.picturesList.length; i++) {
	                        if (i % data.numItemsPerRow == 0) {
	                            $currentRow = $('<tr>').appendTo($table);
	                        }
	                        var $currentCell = $('<td>').appendTo($currentRow).addClass('table_cell');
	
	                        private_methods.createNewPictureCell(data, i, $currentCell);
	                        numPicsDisplayed++;
			            }
	                    settings.numPicsDisplayed = numPicsDisplayed
	                    settings.currentPage = newPage
	                    var $pagination = $('#' + settings.organism + 'Pagination');
	                    $pagination.find('.numbers_holder input').val(settings.currentPage);
	                    firstImage = (settings.currentPage - 1) * settings.picsPerPage + 1;
	                    $pagination.find('.first-image').html(firstImage);
	                    $pagination.find('.last-image').html(firstImage + settings.numPicsDisplayed - 1);
					}
	                else {
	                    if ('errorMessage' in data) {
	                        console.error("Error: " + data.errorMessage);
	                    }
	                    else {
	                        console.error("undefined error thrown");
	                    }
	                }
	            },
	            error: function(jqXHR, textStatus, errorThrown) {
	                console.log("Error: " + errorThrown);
	            }
	        });
	    },
	    createNewPictureCell: function (data, index, $currentCell) {
	        var picture = data.picturesList[index];

	        var $pictureDiv = $('<div>');
	        var $href = $('<a>').attr('href', data.SITE_URL + 'images/editor?imageKey=' + picture.pk);
	        $href.append($('<img>').attr('src', picture.imageName).width(180).height(130));
	                        
	        var $descriptionDiv = $('<div class="description"><span>' + picture.description + '</span></div>');
				
	        $currentCell.append($pictureDiv.append($href));
	        $currentCell.append($descriptionDiv);
	    }
	};
	
	var public_methods = {
		/**
			Calls the image updater initialization on a div
		**/
		init: function(options) {
			return this.each(function() {
				var settings = $.extend({
					'staticUrl' : '/static/',
					'siteUrl' : '/',
					'numPages' : 1,
					'organism' : '',
					'picsPerPage' : 15,
					'currentPage' : 1,
					'numImages' : 0,
					'numPicsDisplayed' : 0
				}, options);
				
				$(this).data('settings', settings);
				
				if (settings.numImages > 0) {
					private_methods.callNewImageSet($(this), settings.currentPage);
					private_methods.addPagination($(this));
				}
				else {
					private_methods.addNoImagesTemplate($(this));
				}
			});
		}
	};

	$.fn.imageUpdater = function(method) {

		// Method calling logic
		if ( public_methods[method] ) {
			return public_methods[ method ].apply( this, Array.prototype.slice.call( arguments, 1 ));
		} 
		else if ( typeof method === 'object' || ! method ) {
			return public_methods.init.apply( this, arguments );
		} 
		else {
			$.error( 'Method ' +  method + ' does not exist on jQuery.imageUpdater' );
		}  
	};
})( jQuery );

