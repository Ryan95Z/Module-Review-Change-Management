jQuery(function($) {

	var g_visable_form = null;

	$(document).ready( function() {
		$('button.reply').on('click', function(event){
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

		$('#post-comment').click( function(event){
			event.preventDefault();
			var root_ul = $('ul.discussion-root');
			var form = $(this).parent().first();
			var action_url = form.attr('action');
			var textarea = form.children('#reply-textarea').children('textarea').first();
			var comment = textarea.val().trim();
			var csrf_token = $('input[name="csrfmiddlewaretoken"]').first().val();

			var html = '<li class="discussion-comment user-comment">';
			html += '<div class="comment-header"><span class="comment-user">';
			html += '<a href="#">{:author}</a></span><span class="comment-time">{:time}</span></div>';
			html += '<div class="comment-content">{:content}</div></div>';
			html += '<div class="comment-options">';
			html += '<button class="reply"  data-for={:timestamp}><i class="fa fa-reply" aria-hidden="true"></i> Reply</button>';
			html += '</div></li>';
			html += '<li id="{:timestamp}" class="discussion-comment discussion-reply-form">';
            html += '<form action="{:action_url}" method="POST" id="{:timestamp}">';
            html += '<input name="csrfmiddlewaretoken" value="{:csrf}" type="hidden">'
            html += '<textarea name="comment" cols="40" required="" class="form-control" rows="4" id="id_comment" placeholder="Add your comments here. Markdown is active."></textarea>';
            html += '<input type="hidden" name="parent" value="{:id}">';
            html += '<button type="submit" class="btn btn-success btn-sm btn-reply">Reply</button>';
            html += '</form></li>';

			$.ajax({
				url: action_url,
				data: {
					'comment': comment,
				},
				type: 'POST',
				dataType: 'json',
				beforeSend: function(xhr, settings) {
        			$.ajaxSettings.beforeSend(xhr, settings);
				},
				success: function(data){
					data['csrf'] = csrf_token;
					data['action_url'] = action_url;
					console.log(data);
					var h = process_html(html, data);
					root_ul.append(h);
				}
			});			
		});
	});

	function process_html(html, data) {
		var re;
		var keys = Object.keys(data);
		for (var k in keys) {
			re = new RegExp('\{(:' + keys[k] + ')\}', 'g');
			html = html.replace(re, data[keys[k]]);
		}
		return html;
	}
});