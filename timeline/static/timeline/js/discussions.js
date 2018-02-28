jQuery(function($) {

	var g_visable_form = null;

	$(document).ready( function() {
		$('button.reply').click(function(event){
			var form_id = $(this).attr('data-for');
			var form = $("#" + form_id);

			if (g_visable_form != null) {

				var g_id = g_visable_form.attr('id');
				var current = form.attr('id');
				if (g_id == current) { return; }

				g_visable_form.slideUp();
				
			}
			g_visable_form = form;
			form.slideDown();
		});
	});
});