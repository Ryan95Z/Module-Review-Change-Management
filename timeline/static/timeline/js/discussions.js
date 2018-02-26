jQuery(function($) {

	var g_visable_form = null;

	$(document).ready( function() {
		$('a.reply-action').click(function(event){
			var form_id = $(this).attr('data-for');
			var form = $("#" + form_id);
			if (g_visable_form != null) {
				g_visable_form.slideUp();
				
			}
			g_visable_form = form;
			form.slideDown();
		});
	});
});