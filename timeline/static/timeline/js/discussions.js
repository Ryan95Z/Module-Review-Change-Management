jQuery(function($) {
    // globals
    var g_visable_form = null;

    $(document).ready( function() {
        $('body').on('click', 'button.reply', function(event){
            var g_id = null;
            var current_id = null;
            // get the form
            var form_id = $(this).attr('data-for');
            var form = $("#" + form_id);

            // check if any forms are already are displayed
            if (g_visable_form != null) {
                g_id = g_visable_form.attr('id');
                current_id = form.attr('id');
                // prevent animation playing if form is already displayed
                if (g_id == current_id) { return; }
                // hide the existing form.
                g_visable_form.slideUp();
            }
            // show the form
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
            html += '<form action="{:action_url}" method="POST" id="{:timestamp}" data-level="{:level}">';
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
                    textarea.val('');
                    data['csrf'] = csrf_token;
                    data['action_url'] = action_url;
                    data['level'] = 0;
                    console.log(data);
                    var output = process_html(html, data);
                    root_ul.append(output);
                }
            });         
        });


        $('body').on('click', 'button.btn-reply', function(event){
            event.preventDefault();
            var form = $(this).parent().first();
            var action_url = form.attr('action');
            var textarea = form.children('textarea');
            var comment = textarea.val().trim();
            var hidden = form.children('input[name="parent"]').val();
            var node_level = form.attr('data-level');
            var parent_li = form.parent().first();
            var expected_ul = parent_li.next();
            var csrf_token = $('input[name="csrfmiddlewaretoken"]').first().val();
            var need_ul = !expected_ul.hasClass('discussion-responses');
            var output = null;

            var ul_html = '<ul class="discussion-responses">{:li}<ul>';
            var li_html = '<li class="discussion-comment user-comment">';
            li_html += '<div class="comment-header"><span class="comment-user">';
            li_html += '<a href="#">{:author}</a></span><span class="comment-time">{:time}</span></div>';
            li_html += '<div class="comment-content">{:content}</div></div>';
            
            if (node_level < 1) {
                li_html += '<div class="comment-options">';
                li_html += '<button class="reply" data-for={:timestamp}><i class="fa fa-reply" aria-hidden="true"></i> Reply</button>';
                li_html += '</div></li>';
                li_html += '<li id="{:timestamp}" class="discussion-comment discussion-reply-form">';
                li_html += '<form action="{:action_url}" method="POST" id="{:timestamp}">';
                li_html += '<input name="csrfmiddlewaretoken" value="{:csrf}" type="hidden">'
                li_html += '<textarea name="comment" cols="40" required="" class="form-control" rows="4" id="id_comment" placeholder="Add your comments here. Markdown is active."></textarea>';
                li_html += '<input type="hidden" name="parent" value="{:id}">';
                li_html += '<button type="submit" class="btn btn-success btn-sm btn-reply">Reply</button>';
                li_html += '</form></li>';
            } else {
                li_html += '</li>';
            }
            
            
            $.ajax({
                url: action_url,
                data: {
                    'comment': comment,
                    'parent': hidden,
                },
                type: 'POST',
                dataType: 'json',
                beforeSend: function(xhr, settings) {
                    $.ajaxSettings.beforeSend(xhr, settings);
                },
                success: function(data){
                    textarea.val('');
                    form.parent().first().slideUp();
                    data['csrf'] = csrf_token;
                    data['action_url'] = action_url;
                    data['level'] = node_level++;
                    if (need_ul) {
                        output = process_html(ul_html, {'li': li_html});
                        output = process_html(output, data)
                        parent_li.after(output);
                    } else {
                        output = process_html(li_html, data);
                        expected_ul.append(output);
                    }
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