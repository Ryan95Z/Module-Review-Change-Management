$(document).ready( function(){
	$('.dropdown').click( function(e){
		var cwe = $(this);
		var id = cwe.attr('id');
		// find the element to display
		var dropdown = $("[aria-labelledby='" + id + "']");
		if(cwe.hasClass('show')) {
			// hide the dropdown
			cwe.removeClass('show');
			dropdown.slideUp("fast");
		} else {
			// show the dropdown
			cwe.addClass('show');
			dropdown.slideDown("fast");
		}
	});
});