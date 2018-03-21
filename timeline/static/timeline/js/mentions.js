jQuery( function($){
	$(document).ready( function(event){
        var current_textarea = null;
        var os_name = window.navigator.userAgent.indexOf("Mac");
        var open = false;

        $('textarea').keyup(function(e){
            var __this = $(this);
            var start = __this.prop('selectionStart');
            current_textarea = __this;
            $('.mentions').offset(__this.cursorLocation());


            var textarea_val = __this.val();
            var loc = textarea_val.lastIndexOf("\@", start);
            var item = textarea_val.substring(loc, start);
            var space = item.indexOf(" ");
            if(space == -1) space = item.length;
            var name = item.substring(1, space);

            if(e.which == '222' || e.which == 50) {
                open = true;
                $('.mentions').show();
            }

            if (open) {
                $.ajax({
                    url: '/timeline/api/mentions/',
                    type: 'POST',
                    data: {
                        'mentions': name
                    },
                    dataType: 'json',
                    beforeSend: function(xhr, settings) {
                        $.ajaxSettings.beforeSend(xhr, settings);
                    },
                    success: function(data) {
                        var li = '<li class="list-group-item mention-user">{:user}</li>'
                        var usernames = data['usernames']
                        var list = $('#user-list');
                        list.html('');
                        for(var i = 0; i < usernames.length; ++i) {
                            list.append(
                                '<li class="list-group-item mention-user">' + usernames[i].username +'</li>'
                            );
                        }
                    },
                });
            }

            if (e.which == '32' || start == 0) {
                open = false;
                $('.mentions').hide();
            }
        });

        $('body').on('click', '.mention-user', function(e){
            var user = "@".concat($(this).text());
            var cusor_location = current_textarea.prop('selectionStart');
            var textarea_val = current_textarea.val();
            var mention_location = textarea_val.lastIndexOf("\@", cusor_location);
           	var pre_mention_text = textarea_val.substr(0, mention_location);
           	var post_mention_text = textarea_val.substr(cusor_location, textarea_val.length);
           	var updated_text = pre_mention_text + user + post_mention_text;
           	current_textarea.val(updated_text);           
            $('.mentions').hide();
        }); 

        $.fn.cursorLocation = function() {
            var __this = $(this);
            var dummy = $('.textarea');
            var span = "<span id='user-cursor'>|</span>";
            var user_cusor_location = __this.prop('selectionStart');
            var val = __this.val();

            var dummy_val = val.substr(0, user_cusor_location) + span + val.substr(user_cusor_location);
            dummy.html(dummy_val);

            var textarea_coords = __this.offset();
            var cursor_coords = $('#user-cursor').offset();
            var dummy_coords = dummy.offset();
            var top = textarea_coords.top + (cursor_coords.top - dummy_coords.top);
            var left = textarea_coords.left + (cursor_coords.left - dummy_coords.left);
            
            return {
                'top': top,
                'left': left
            }
        }
    });
});