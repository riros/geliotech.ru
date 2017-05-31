$(function() {
		/*
 * Replace all SVG images with inline SVG
 */
jQuery('.ico-svg').each(function(){
	var $img = jQuery(this);
	var imgID = $img.attr('id');
	var imgClass = $img.attr('class');
	var imgURL = $img.attr('src');

	jQuery.get(imgURL, function(data) {
		// Get the SVG tag, ignore the rest
		var $svg = jQuery(data).find('svg');

		// Add replaced image's ID to the new SVG
		if(typeof imgID !== 'undefined') {
			$svg = $svg.attr('id', imgID);
		}
		// Add replaced image's classes to the new SVG
		if(typeof imgClass !== 'undefined') {
			$svg = $svg.attr('class', imgClass+' replaced-svg');
		}

		// Remove any invalid XML tags as per http://validator.w3.org
		$svg = $svg.removeAttr('xmlns:a');

		// Check if the viewport is set, if the viewport is not set the SVG wont't scale.
		if(!$svg.attr('viewBox') && $svg.attr('height') && $svg.attr('width')) {
			$svg.attr('viewBox', '0 0 ' + $svg.attr('height') + ' ' + $svg.attr('width'))
		}

		// Replace image with new SVG
		$img.replaceWith($svg);

	}, 'xml');

});


//Owl Carousel
$(".header-slider .slider").owlCarousel({
	
		slideSpeed : 300,
		paginationSpeed : 400,
		singleItem: true,
		pagination: true,
		autoPlay: true,
		navigation: true,
		navigationText: [
		"<i class='fa fa-chevron-left'></i>",
		"<i class='fa fa-chevron-right'></i>"
		] 
		});



//E-mail Ajax Send
	$(".contact-form").submit(function() { //Change
		var th = $(this);
		$.ajax({
			type: "POST",
			url: "mail.php", //Change
			data: th.serialize()
		}).done(function() {
			alert("Thank you!");
			setTimeout(function() {
				// Done Functions
				th.trigger("reset");
			}, 1000);
		});
		return false;
	});

//Toggle Menu
$(".toggle-mnu").click(function() {
  $(this).toggleClass("on");
  $(".hidden-nav").slideToggle();
  return false;
});

//EqualHeights
//$('.s-decision-item p').equalHeights();
$('.s-service .s-service-item p').equalHeights();



});
