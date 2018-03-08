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
            html += '<a href="{:author_url}">{:author}</a></span><span class="comment-time">{:time}</span></div>';
            html += '<div class="comment-content">{:content}</div></div>';
            html += '<div class="comment-content-pre">{:md}</div>'
            html += '<div class="comment-options">';
            html += '<button class="reply"  data-for={:timestamp}><i class="fa fa-reply" aria-hidden="true"></i> Reply</button>';
            html += '<a href="{:edit_url}" class="comment-action comment-edit"><i class="fa fa-pencil" aria-hidden="true"></i><span>Edit</span></a>'
            html += '<a href="{:delete_url}" class="comment-action comment-delete"><i class="fa fa-trash" aria-hidden="true"></i>Delete</a>'
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
                    var output = null;
                    var comment_msg = $('#no-comments-msg');
                    textarea.val('');
                    data['csrf'] = csrf_token;
                    data['action_url'] = action_url;
                    data['level'] = 0;
                    output = process_html(html, data);
                    if(comment_msg.length > 0) {
                        comment_msg.remove();
                    }
                    root_ul.append(output);
                }
            });         
        });


        $('body').on('click', 'button.btn-reply', function(event){
            event.preventDefault();
            var form = $(this).parent().first();
            var form_id = form.attr('id');
            var timestamp_id = form_id.substr(5);
            var action_url = form.attr('action');
            var textarea = form.children('textarea');
            var comment = textarea.val().trim();
            var hidden = form.children('input[name="parent"]').val();
            var node_level = form.attr('data-level');
            var parent_li = $('li#' + timestamp_id);
            var expected_ul = parent_li.next();
            var csrf_token = $('input[name="csrfmiddlewaretoken"]').first().val();
            var need_ul = !expected_ul.hasClass('discussion-responses');
            var output = null;

            var ul_html = '<ul class="discussion-responses">{:li}<ul>';
            var li_html = '<li class="discussion-comment user-comment">';
            li_html += '<div class="comment-header"><span class="comment-user">';
            li_html += '<a href="{:author_url}">{:author}</a></span><span class="comment-time">{:time}</span></div>';
            li_html += '<div class="comment-content">{:content}</div></div>';
            li_html += '<div class="comment-content-pre">{:md}</div>'
            li_html += '<div class="comment-options">';

            if (node_level < 1) {
                li_html += '<button class="reply" data-for={:timestamp}><i class="fa fa-reply" aria-hidden="true"></i> Reply</button>';
                li_html += '<a href="{:edit_url}" class="comment-action comment-edit"><i class="fa fa-pencil" aria-hidden="true"></i><span>Edit</span></a>'
                li_html += '<a href="{:delete_url}" class="comment-action comment-delete"><i class="fa fa-trash" aria-hidden="true"></i>Delete</a>'
                li_html += '</div></li>';
                li_html += '<li id="{:timestamp}" class="discussion-comment discussion-reply-form">';
                li_html += '<form action="{:action_url}" method="POST" id="{:timestamp}">';
                li_html += '<input name="csrfmiddlewaretoken" value="{:csrf}" type="hidden">'
                li_html += '<textarea name="comment" cols="40" required="" class="form-control" rows="4" id="id_comment" placeholder="Add your comments here. Markdown is active."></textarea>';
                li_html += '<input type="hidden" name="parent" value="{:id}">';
                li_html += '<button type="submit" class="btn btn-success btn-sm btn-reply">Reply</button>';
                li_html += '</form></li>';
            } else {
                li_html += '<a href="{:edit_url}" class="comment-action comment-edit"><i class="fa fa-pencil" aria-hidden="true"></i><span>Edit</span></a>'
                li_html += '<a href="{:delete_url}" class="comment-action comment-delete"><i class="fa fa-trash" aria-hidden="true"></i>Delete</a>'
                li_html += '</div></li>';
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
                    parent_li.slideUp();
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

        $('body').on('click', 'a.comment-delete', function(event) {
            event.preventDefault();
            var action_url = $(this).attr('href');
            var li = $(this).parent().parent();
            var li_reply_form = li.next();
            var para_html = '<p id="no-comments-msg">There is no active discussion for this entry. You can start one now!</p>';
            var root_ul = $('ul.discussion-root');
            var discussion_container = $('div.discussion-container');
            var child_ul = li_reply_form.next();

            $.ajax({
                type: 'POST',
                url: action_url,
                data: {},
                dataType: 'JSON',
                beforeSend: function(xhr, settings) {
                    $.ajaxSettings.beforeSend(xhr, settings);
                },
                success: function(data) {
                    li.remove();
                    li_reply_form.remove();
                    if (root_ul.children().length < 1) {
                        discussion_container.append(para_html);
                    }

                    if (child_ul.hasClass('discussion-responses')) {
                        child_ul.remove();
                    }
                },
            });
        });

        $('body').on('click', 'a.comment-edit', function(event){
            event.preventDefault();
            var __this = $(this);
            var li = __this.parent().parent();
            var comment_content = li.children('.comment-content');
            var md_comment_content = li.children('.comment-content-pre');
            var md = md_comment_content.html();
            var anchor_span = __this.children('span');
            comment_content.html(md);
            comment_content.addClass('comment-content-edit');
            comment_content.attr('contenteditable','true');
            anchor_span.text('Done');
            __this.removeClass('comment-edit');
            __this.addClass('comment-done');
        });

        $('body').on('click', 'a.comment-done', function(event){
            event.preventDefault();
            var __this = $(this);
            var li = __this.parent().parent();
            var action_url = __this.attr('href');
            var comment_content = li.children('.comment-content');
            var md_comment_content = li.children('.comment-content-pre');
            var html = comment_content.html();
            var anchor_span = __this.children('span');
            comment_content.removeClass('comment-content-edit');
            comment_content.attr('contenteditable','false');
            html = html.replace(/((<br>))/g, '\n');
            $.ajax({
                type: 'POST',
                url: action_url,
                data: {
                    'comment': html,
                },
                dataType: 'JSON',
                beforeSend: function(xhr, settings) {
                    $.ajaxSettings.beforeSend(xhr, settings);
                },
                success: function(data) {
                    comment_content.html(data['html']);
                    md_comment_content.html(data['md']);
                    anchor_span.text('Edit');
                    __this.addClass('comment-edit');
                    __this.removeClass('comment-done');
                }
            });
        });

        $('body').on('click', 'a.nav-preview', function(event){
            var textarea = $('#reply-textarea').children('textarea');
            var md = textarea.val();
            var preview = $('#markdown-preview');
            $.ajax({
                type: 'POST',
                url: '/timeline/api/markdown/',
                data: {
                    'markdown': md,
                },
                dataType: 'JSON',
                beforeSend: function(xhr, settings) {
                    $.ajaxSettings.beforeSend(xhr, settings);
                },
                success: function(data) {
                    preview.html(data['markdown']);
                }
            });
        });

        $('body').on('click', 'a.nav-preview-replies', function(event){
            var __this = $(this);
            var preview_id = __this.attr('aria-controls');
            var node_id = preview_id.substr(preview_id.length - 3);
            var preview = $('#' + preview_id).children('div.md-preview');
            var write = $('#write-'+node_id);
            var textarea = write.children('form').children('textarea');
            var md = textarea.val();
            $.ajax({
                type: 'POST',
                url: '/timeline/api/markdown/',
                data: {
                    'markdown': md,
                },
                dataType: 'JSON',
                beforeSend: function(xhr, settings) {
                    $.ajaxSettings.beforeSend(xhr, settings);
                },
                success: function(data) {
                    preview.html(data['markdown']);
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