jQuery(function($){
	$('#id_tutor_year').change( function(){
		var year = $(this).val();
		var url = $('#form').attr('data-url');

		$.ajax({
			url: url,
			method: 'POST',
			dataType: 'html',
			data: {
				'year': year,
			},
			beforeSend: function(xhr, settings) {
				// Get the CSRF token. See csrf_ajax.js for more information.
				$.ajaxSettings.beforeSend(xhr, settings);
			},
			success: function(data) {
				$('#module_list').html(data);
			}
		});
	});
});