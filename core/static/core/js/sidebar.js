$(document).ready( function(){
	$('.dropdown').click( function(e){
		var cwe = $(this);
		var id = cwe.attr('id');
		var dropdown = $("[aria-labelledby='" + id + "']");
		if(cwe.hasClass('show')) {
			cwe.removeClass('show');
			dropdown.slideUp("fast");
		} else {
			cwe.addClass('show');
			dropdown.slideDown("fast");
		}
	});
});