jQuery( function($){
	$(document).ready( function(event){
        var current_textarea = null;
        var mention_displayed = false;

       	$('body').on('keyup','textarea', function (e) { 
            var __this = $(this);
            current_textarea = __this;

            // location in textarea of user's cursor
            var cursor = __this.prop('selectionStart');
            var mentions = $('.mentions');

           	// coordinates of user's cursor
            var coords = __this.cursorLocation();
            
            // set the mentions box with the user's coordinates
            // so it can float near it.
            mentions.offset(coords);
            var textarea_val = __this.val();

            // get the last typed character
            var char = textarea_val.slice(cursor - 1, cursor);

            /** 
            	calculate the username that is being typed
             	this needs to be calculated to determine which
             	mention is currently being used. Prevents existing
            	mentions being deleted.
            */

            // get the location of the most recent mention based on cursor
            var mention_location = textarea_val.lastIndexOf("\@", cursor);
            
            // extract typed name by getting using index of the @ and cusor
            var snippet = textarea_val.substring(mention_location, cursor);
            
            // check for a space in case it is between a sentance
            var space = snippet.indexOf(" ");
           	
           	// check for a space. The space determines that
           	// the user is midway through a sentance, otherwise
           	// we must be at the end of user comment
            if(space == -1) space = snippet.length;
            
            // remove the @ from username
            var name = snippet.substring(1, space);

            // only show if @ was typed
            if(char == '@') {
                mention_displayed = true;
                mentions.show();
            }


            // only send a request if mentions are being displayed
            if (mention_displayed == true) {
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
                        var li = '<li class="list-group-item mention-user">{:user}</li>';
                        var usernames = data['usernames'];
                        var list = $('#user-list');
                        var n_usernames = usernames.length;
                        list.html('');
                        if (n_usernames > 0) {
	                        for(var i = 0; i < n_usernames; ++i) {
	                            list.append(process_html(li, {'user': usernames[i].username}));
	                        }
	                    } else {
                    		li = '<li class="list-group-item">{:msg}</li>';
                    		list.append(process_html(li, {'msg': 'No users found'}));
                    	}	
                    },
                });
            }

            // if user enters a space or the cursor is at the start, then we hide the box.
            if (char == ' ' || cursor == 0) {
                mention_displayed = false;
                mentions.hide();
            }
        });

        /**
         * Event to replace the mention search with the actual
         * username that is requested.
         */
        $('body').on('click', '.mention-user', function(e){
            var user = "@".concat($(this).text());
            var cusor_location = current_textarea.prop('selectionStart');
            var textarea_val = current_textarea.val();
            
            // get the closest mention based on the user's cursor location
            var mention_location = textarea_val.lastIndexOf("\@", cusor_location);
           	
           	// get the substring before the mention
           	var pre_mention_text = textarea_val.substr(0, mention_location);
           	
           	// get the substring after the mention 
           	var post_mention_text = textarea_val.substr(cusor_location, textarea_val.length);
           	
           	// insert the username
           	var updated_text = pre_mention_text + user + post_mention_text;
           	current_textarea.val(updated_text);           
            $('.mentions').hide();
        }); 


        /**
         * Gets the coordinates of the user's cusor from a textarea.
         *
         * @param 	void
         * @return  object that contains top and left coordinates
         */
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