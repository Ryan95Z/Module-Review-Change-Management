/**
 * discussion.js
 * Responsible for providing the dynamic features for the discussion
 * area for an entry on the timeline.
 */

jQuery(function($) {
    // globals
    var g_visable_form = null;

    $(document).ready( function() {

        /**
         * Drops down the form when a user wants to make a reply
         * to an existing comment.
         */
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

        /**
         * Posts a top level comment when the post button
         * is clicked.
         */
        $('#post-comment').click( function(event){
            event.preventDefault();
            var root_ul = $('ul.discussion-root');
            var form = $(this).parent().first();
            var action_url = form.attr('action');
            var textarea = form.children('#reply-textarea').children('textarea').first();
            var comment = textarea.val().trim();
            var csrf_token = $('input[name="csrfmiddlewaretoken"]').first().val();

            // Markup for the comment
            var html = '<li class="discussion-comment user-comment" data-node="{:id}">';
            html += '<div class="comment-header"><span class="comment-user">';
            html += '<a href="{:author_url}">{:author}</a></span><span class="comment-time">{:time}</span></div>';
            html += '<div class="comment-content" data-textedit="#text-{:id}-edit">{:content}</div></div>';
            html += '<div style="display: none;" id="text-{:id}-edit"><textarea class="form-control" cols="40" rows="4">{:md}</textarea></div>'
            html += '<div class="comment-options">';
            html += '<button class="reply"  data-for={:timestamp}><i class="fa fa-reply" aria-hidden="true"></i> Reply</button>';
            html += '<a href="{:edit_url}" class="comment-action comment-edit"><i class="fa fa-pencil" aria-hidden="true"></i><span>Edit</span></a>'
            html += '<a href="{:delete_url}" class="comment-action comment-delete"><i class="fa fa-trash" aria-hidden="true"></i>Delete</a>'
            html += '</div></li>';

            // Markup for the form. This includes the preview,
            // write, reply, delete and edit features.
            html += '<li id="{:timestamp}" class="discussion-comment discussion-reply-form">';
            html += '<ul class="nav nav-tabs" role="tablist"><li class="nav-item">';
            html += '<a class="nav-link active" id="write-tab-{:id}" data-toggle="tab" href="#write-{:id}" role="tab" aria-controls="write-{:id}" aria-selected="true">Write</a>';
            html += '</li><li class="nav-item">';
            html += '<a class="nav-link nav-preview-replies" id="preview-tab-{:id}" data-toggle="tab" href="#preview-{:id}" role="tab" aria-controls="preview-{:id}" aria-selected="true" data-container="prev">Preview</a>';
            html += '</li></ul><div class="tab-content">';
            html += '<div class="tab-pane fade show active" id="write-{:id}" role="tabpanel" aria-labelledby="write-tab">';
            html += '<form action="{:action_url}" method="POST" id="form-{:timestamp}" data-level="{:level}">';
            html += '<input name="csrfmiddlewaretoken" value="{:csrf}" type="hidden">';
            html += '<textarea name="comment" cols="40" required="" class="form-control" rows="4" id="id_comment" placeholder="Add your comments here. Markdown is active."></textarea>';
            html += '<input type="hidden" name="parent" value="{:id}">';
            html += '<button type="submit" class="btn btn-success btn-sm btn-reply">Reply</button>';
            html += '</div><div class="tab-pane fade" id="preview-{:id}" role="tabpanel" aria-labelledby="preview-tab-{:id}">';
            html += '<div class="md-preview"></div></div></div></li>';

            // Ajax request for saving a comment. 
            // Will then add the markup to UI when request successful.
            $.ajax({
                url: action_url,
                data: {
                    'comment': comment,
                },
                type: 'POST',
                dataType: 'json',
                beforeSend: function(xhr, settings) {
                    // Get the CSRF token. See csrf_ajax.js for more information.
                    $.ajaxSettings.beforeSend(xhr, settings);
                },
                success: function(data){
                    var output = null;
                    var comment_msg = $('#no-comments-msg');
                    // clear the textarea data.
                    textarea.val('');

                    // add data for markup that is already saved.
                    data['csrf'] = csrf_token;
                    data['action_url'] = action_url;
                    
                    // level is zero as top level comment
                    data['level'] = 0; 

                    // add the response data to the markup template.
                    output = process_html(html, data);

                    // remove the no comment message if this is the first comment.
                    if(comment_msg.length > 0) {
                        comment_msg.remove();
                    }

                    // add the html li to the root ul.
                    root_ul.append(output);
                }
            });         
        });

        /**
         * Posts a reply for a comment on the discussion page.
         */
        $('body').on('click', 'button.btn-reply', function(event){
            event.preventDefault();
            var form = $(this).parent().first();
            var form_id = form.attr('id');

            // get the timestamp from the form id.
            var timestamp_id = form_id.substr(5);

            // get the form url
            var action_url = form.attr('action');

            // get the comments
            var textarea = form.children('textarea');
            var comment = textarea.val().trim();
            var hidden = form.children('input[name="parent"]').val();
            var node_level = form.attr('data-level');
            var parent_li = $('li#' + timestamp_id);
            var expected_ul = parent_li.next();
            var csrf_token = $('input[name="csrfmiddlewaretoken"]').first().val();
            var need_ul = !expected_ul.hasClass('discussion-responses');
            var output = null;

            // markdown template for the comment
            var ul_html = '<ul class="discussion-responses">{:li}<ul>';
            var li_html = '<li class="discussion-comment user-comment">';
            li_html += '<div class="comment-header"><span class="comment-user">';
            li_html += '<a href="{:author_url}">{:author}</a></span><span class="comment-time">{:time}</span></div>';
            li_html += '<div class="comment-content" data-textedit="#text-{:id}-edit">{:content}</div></div>';
            li_html += '<div style="display: none;" id="text-{:id}-edit"><textarea class="form-control" cols="40" rows="4">{:md}</textarea></div>'
            li_html += '<div class="comment-options">';

            // if the level is 0, then it can have replies
            // so we append the form template.
            if (node_level < 1) {
                // edit and delete optins
                li_html += '<button class="reply" data-for={:timestamp}><i class="fa fa-reply" aria-hidden="true"></i> Reply</button>';
                li_html += '<a href="{:edit_url}" class="comment-action comment-edit"><i class="fa fa-pencil" aria-hidden="true"></i><span>Edit</span></a>'
                li_html += '<a href="{:delete_url}" class="comment-action comment-delete"><i class="fa fa-trash" aria-hidden="true"></i>Delete</a>'
                li_html += '</div></li>';

                // reply form
                li_html += '<li id="{:timestamp}" class="discussion-comment discussion-reply-form">';
                li_html += '<ul class="nav nav-tabs" role="tablist"><li class="nav-item">';
                li_html += '<a class="nav-link active" id="write-tab-{:id}" data-toggle="tab" href="#write-{:id}" role="tab" aria-controls="write-{:id}" aria-selected="true">Write</a>';
                li_html += '</li><li class="nav-item">';
                li_html += '<a class="nav-link nav-preview-replies" id="preview-tab-{:id}" data-toggle="tab" href="#preview-{:id}" role="tab" aria-controls="preview-{:id}" aria-selected="true" data-container="prev">Preview</a>';
                li_html += '</li></ul><div class="tab-content">';
                li_html += '<div class="tab-pane fade show active" id="write-{:id}" role="tabpanel" aria-labelledby="write-tab">';
                li_html += '<form action="{:action_url}" method="POST" id="form-{:timestamp}" data-level="{:level}">';
                li_html += '<input name="csrfmiddlewaretoken" value="{:csrf}" type="hidden">';
                li_html += '<textarea name="comment" cols="40" required="" class="form-control" rows="4" id="id_comment" placeholder="Add your comments here. Markdown is active."></textarea>';
                li_html += '<input type="hidden" name="parent" value="{:id}">';
                li_html += '<button type="submit" class="btn btn-success btn-sm btn-reply">Reply</button>';
                li_html += '</div><div class="tab-pane fade" id="preview-{:id}" role="tabpanel" aria-labelledby="preview-tab-{:id}">';
                li_html += '<div class="md-preview"></div></div></div></li>';
            } else {
                // otherwise we add only delete and edit options.
                li_html += '<a href="{:edit_url}" class="comment-action comment-edit"><i class="fa fa-pencil" aria-hidden="true"></i><span>Edit</span></a>'
                li_html += '<a href="{:delete_url}" class="comment-action comment-delete"><i class="fa fa-trash" aria-hidden="true"></i>Delete</a>'
                li_html += '</div></li>';
            }
            
            // Save the new response to the database.
            $.ajax({
                url: action_url,
                data: {
                    'comment': comment,
                    'parent': hidden,
                },
                type: 'POST',
                dataType: 'json',
                beforeSend: function(xhr, settings) {
                    // Get the CSRF token. See csrf_ajax.js for more information.
                    $.ajaxSettings.beforeSend(xhr, settings);
                },
                success: function(data){
                    // remove the contents that user typed
                    textarea.val('');
                    parent_li.slideUp();

                    // add extra information that is already saved.
                    data['csrf'] = csrf_token;
                    data['action_url'] = action_url;
                    
                    // increase node level as it is a child in the MPTT tree.
                    ++node_level;
                    data['level'] = node_level;

                    if (need_ul) {
                        // if a ul is not present, process the data
                        // and add new ul.
                        output = process_html(ul_html, {'li': li_html});
                        output = process_html(output, data)
                        parent_li.after(output);
                    } else {
                        // if ul present, nest the new response.
                        output = process_html(li_html, data);
                        expected_ul.append(output);
                    }
                }
            });
        });
    
        /**
         * Event to automatically delete a comment.
         */
        $('body').on('click', 'a.comment-delete', function(event) {
            event.preventDefault();
            var action_url = $(this).attr('href');
            var li = $(this).parent().parent();
            var li_reply_form = li.next();

            // no comments message if all comments are removed.
            var para_html = '<p id="no-comments-msg">There is no active discussion for this entry. You can start one now!</p>';
            var root_ul = $('ul.discussion-root');
            var discussion_container = $('div.discussion-container');
            var child_ul = li_reply_form.next();

            // remove the comment from the database.
            $.ajax({
                type: 'POST',
                url: action_url,
                data: {},
                dataType: 'JSON',
                beforeSend: function(xhr, settings) {
                    // Get the CSRF token. See csrf_ajax.js for more information.
                    $.ajaxSettings.beforeSend(xhr, settings);
                },
                success: function(data) {
                    // remove the comment
                    li.remove();

                    // remove its reply form
                    li_reply_form.remove();

                    // if no other comments, add no comments message
                    if (root_ul.children().length < 1) {
                        discussion_container.append(para_html);
                    }

                    // remove any responses that a comment had as they
                    // are automatically deleted from the database.
                    if (child_ul.hasClass('discussion-responses')) {
                        child_ul.remove();
                    }
                },
            });
        });

        /**
         * Converts the comment to be an editable area
         * when the edit anchor button is clicked.
         */
        $('body').on('click', 'a.comment-edit', function(event){
            event.preventDefault();
            var __this = $(this);
            var anchor_span = __this.children('span');
            var li = __this.parent().parent();
            var comment_content = li.children('.comment-content');

            // get the edit area
            var edit_area = $(comment_content.attr('data-textedit'));

            // hide the current comment and display the markdown
            comment_content.hide();
            edit_area.show();

            // switch the current anchor to be a done anchor
            // to enable the a.comment-done onClick event to work. 
            anchor_span.text('Done');
            __this.removeClass('comment-edit');
            __this.addClass('comment-done');
        });

        /**
         * Saves the changes that a user has made to a comment,
         * then switches the anchor button to be edit again.
         */
        $('body').on('click', 'a.comment-done', function(event){
            event.preventDefault();
            var __this = $(this);
            var li = __this.parent().parent();
            var action_url = __this.attr('href');
            var anchor_span = __this.children('span');

            // get the comment stuff
            var comment_content = li.children('.comment-content');
            var edit_area = $(comment_content.attr('data-textedit'));
            
            // get the markdown from the textarea
            var comment_md = edit_area.children('textarea').first().val();

            // hide edit area and show new comment
            edit_area.hide();
            comment_content.show();

            // Posts the updated comment to be save.
            $.ajax({
                type: 'POST',
                url: action_url,
                data: {
                    'comment': comment_md,
                },
                dataType: 'JSON',
                beforeSend: function(xhr, settings) {
                    // Get the CSRF token. See csrf_ajax.js for more information.
                    $.ajaxSettings.beforeSend(xhr, settings);
                },
                success: function(data) {
                    // update the comment
                    comment_content.html(data['html']);
                    
                    // update the label.
                    anchor_span.text('Edit');

                    // switch the classes to make the edit event work again
                    __this.addClass('comment-edit');
                    __this.removeClass('comment-done');
                }
            });
        });

        /**
         * Provides the preview of markdown for the top level comment form.
         */
        $('body').on('click', 'a.nav-preview', function(event){
            var textarea = $('#reply-textarea').children('textarea');
            
            // get the markdown
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
                    // Get the CSRF token. See csrf_ajax.js for more information.
                    $.ajaxSettings.beforeSend(xhr, settings);
                },
                success: function(data) {
                    // show the markdown in preview view
                    preview.html(data['markdown']);
                }
            });
        });

        /**
         * Enables the reply form to preview the markdown.
         */
        $('body').on('click', 'a.nav-preview-replies', function(event){
            var __this = $(this);
            var preview_id = __this.attr('aria-controls');

            // trim the preview_id to just get the node id.
            var node_id = preview_id.replace("preview-", "");
            var preview = $('#' + preview_id).children('div.md-preview');
            var write = $('#write-'+node_id);
            var textarea = write.children('form').children('textarea');
            

            // get the markdown from the user.
            var md = textarea.val();

            $.ajax({
                type: 'POST',
                url: '/timeline/api/markdown/',
                data: {
                    'markdown': md,
                },
                dataType: 'JSON',
                beforeSend: function(xhr, settings) {
                    // Get the CSRF token. See csrf_ajax.js for more information.
                    $.ajaxSettings.beforeSend(xhr, settings);
                },
                success: function(data) {
                    console.log(data);
                    // show the markdown in preview view
                    preview.html(data['markdown']);
                }
            });
        });

    });
    

    
    /**
     * Turns a html string template and adds the data
     * to create markup. To do this, the data parameter needs
     * to be json or a dictionary, where the keys correspond
     * to tokens in the html template. For example: Given the JSON
     * {'id': 1}, there will be a token {:id} that will be mapped by this
     * function. Any keys in the json that don't match, will be ignored.
     *
     * @param   html    string of html with the {:tokens} for the various JSON keys.
     * @param   data    JSON or dictionary object.
     * @return          HTML with the tokens filled in.   
     */
    function process_html(html, data) {
        var re;
        var keys = Object.keys(data);
        // go through each key
        for (var k in keys) {
            // create regex for token
            re = new RegExp('\{(:' + keys[k] + ')\}', 'g');
            // find the token and replace everything with value
            html = html.replace(re, data[keys[k]]);
        }
        return html;
    }
});