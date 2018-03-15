from abc import ABC, abstractmethod
from timeline.models import Notification, Watcher
from django.urls import reverse


class BaseNotification(ABC):
    def __init__(self, n_type, content_template, link_name):
        self.type = n_type
        self.content_template = content_template
        self.link_name = link_name

        self._watchers = Watcher
        self._notification = Notification

    @abstractmethod
    def create(self, **kwargs):
        pass

    def factory(self):
        return self.__class__()

    def get_url(self, data):
        return reverse(self.link_name, kwargs=data)

    def get_watchers(self, module_code):
        return self._watchers.objects.filter(watching__pk=module_code)


class DiscussionNotification(BaseNotification):
    def __init__(self):
        content_template = "{} has written a common for {}"
        super(DiscussionNotification, self).__init__(
            n_type='discussion_notification',
            content_template=content_template,
            link_name='discussion'
        )

    def create(self, **kwargs):
        discussion = kwargs['discussion']
        user = kwargs['user']

        entry = discussion.entry
        content = self.content_template.format(
            user.username,
            entry.module_code
        )

        url = self.get_url({
            'module_pk': entry.module_code,
            'pk': entry.pk,
        })

        watchers = self.get_watchers(entry.module_code)
        for w in watchers:
            if w.watcher_username() != user.username:
                self._notification.objects.create(
                    content=content,
                    recipient=w.user,
                    link=url,
                )


class ReplyNotification(BaseNotification):
    def __init__(self):
        content_template = "{} has replied to your post"
        super(ReplyNotification, self).__init__(
            n_type='reply_notification',
            content_template=content_template,
            link_name='discussion'
        )

    def create(self, **kwargs):
        discussion = kwargs['discussion']
        user = kwargs['user']
        parent = kwargs['parent']

        entry = discussion.entry
        recipient = parent.author
        url = self.get_url({
            'module_pk': entry.module_code,
            'pk': entry.pk,
        })

        content = self.content_template.format(user.username)
        self._notification.objects.create(
            content=content,
            recipient=recipient,
            link=url
        )
