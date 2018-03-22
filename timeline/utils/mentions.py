import re
from core.models import User
from django.urls import reverse
from timeline.utils.notifications.helpers import push_notification

MENTION_REGEX = '\@([a-zA-z]+)'


def process_mentions(message):
    """
    Processes any @ mentions into valid markdown to become urls

    Arguments:
        message     String message from user

    Return
        original message with url markdown
    """
    pattern = re.compile(MENTION_REGEX)

    # turn message into space seperated array
    message = re.findall(r'\S+|\n', message)

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


def extract_mentions(comment, author_username):
    # extract all of the mentions from the comment
    pattern = re.compile(MENTION_REGEX)
    mentions = pattern.findall(comment)

    # remove any trace of the user who wrote the comment
    # from being mentioned in their own comment
    return [u for u in mentions if u != author_username]


def push_mention_notifications(comment, comment_author, entry):
    username = comment_author.username

    # extract mentions from comment
    mentions = extract_mentions(comment, username)

    # loop through each mention username and push
    # a notification to them.
    for m in mentions:
        user = User.objects.get(username=m)
        push_notification(
            'mention',
            author=comment_author,
            entry=entry,
            mention=user
        )
    return len(mentions)
