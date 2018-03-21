import re
from core.models import User
from django.urls import reverse


def process_mentions(message):
    """
    Processes any @ mentions into valid markdown to become urls

    Arguments:
        message     String message from user

    Return
        original message with url markdown
    """
    pattern = re.compile('\@([a-zA-z]+)')

    # turn message into space seperated array
    message = message.split()

    # loop through each word, if it is a mention
    # then get the user and create the url
    for index, value in enumerate(message):
        if pattern.match(value) is not None:
            try:
                user = User.objects.get(username=value[1:])
                url = reverse('user_profile', kwargs={'pk': user.pk})

                # replace current value with the url
                message[index] = "[{}]({})".format(value, url)
            except User.DoesNotExist:
                pass

    # assemble the mesage back together
    return ' '.join(map(str, message))
