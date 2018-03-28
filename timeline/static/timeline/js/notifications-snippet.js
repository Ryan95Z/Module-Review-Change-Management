SPAN_CLASS = "notification-alert"

jQuery(function($) {
	$(document).ready( function() {
		getNotifications();

		setInterval(function(){ 
			getNotifications(); 
		}, 60000);
	});

	function getNotifications() {
		notification_nav = $('#nav-notification');
		username = notification_nav.attr('data-user');
		url = "/timeline/api/notifications/";
		$.ajax({
			url: url,
			data: {
				'user': username,
			},
			type: 'POST',
			dataType: 'json',
			beforeSend: function(xhr, settings) {
				// Get the CSRF token. See csrf_ajax.js for more information.
				$.ajaxSettings.beforeSend(xhr, settings);
			},
			success: function(data){
				span = notification_nav.children('span');
				if (data['has_notifications'] == true) {
					span.addClass(SPAN_CLASS);
				} else {
					span.removeClass(SPAN_CLASS);
				}
			}
		});
	}
});