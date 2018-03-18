from abc import ABC, abstractmethod
from timeline.models import Notification, Watcher
from django.urls import reverse


class BaseNotice(ABC):
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

    def _create_notification(self, content, recipient, link):
        self._notification.objects.create(
            content=content,
            recipient=recipient,
            link=link,
        )


class DiscussionNotice(BaseNotice):
    def __init__(self):
        content_template = "{} has written a comment for {}"
        super(DiscussionNotice, self).__init__(
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


class ReplyNotice(BaseNotice):
    def __init__(self):
        content_template = "{} has replied to your post"
        super(ReplyNotice, self).__init__(
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


class TLEntryNotice(BaseNotice):
    def __init__(self):
        content_template = "A change has been made to {}"
        super(TLEntryNotice, self).__init__(
            n_type='tl_entry__notification',
            content_template=content_template,
            link_name='module_timeline'
        )

    def create(self, **kwargs):
        entry = kwargs['entry']
        module_code = entry.module_code
        content = self.content_template.format(module_code)
        watchers = self.get_watchers(entry.module_code)
        url = self.get_url({
            'module_pk': module_code
        })

        for w in watchers:
            self._notification.objects.create(
                content=content,
                recipient=w.user,
                link=url,
            )


class TLChangeNotice(BaseNotice):
    def __init__(self, n_type, content_template):
        super(TLChangeNotice, self).__init__(
            n_type='tl_approved__notification',
            content_template=content_template,
            link_name='module_timeline'
        )

    def create(self, **kwargs):
        approver = kwargs['user']
        entry = kwargs['entry']
        module_code = entry.module_code

        content = self.content_template.format(
            approver.username,
            module_code
        )

        watchers = self.get_watchers(module_code)
        url = self.get_url({
            'module_pk': module_code
        })

        for w in watchers:
            if w.watcher_username() != approver.username:
                self._create_notification(content, w.user, url)


class TLStagingNotice(TLChangeNotice):
    def __init__(self):
        content_template = "{} has approved a change for staging to {}"
        super(TLStagingNotice, self).__init__(
            n_type='tl_staged__notification',
            content_template=content_template,
        )


class TLConfirmedNotice(TLChangeNotice):
    def __init__(self):
        content_template = "{} has confirmed a change to {}"
        super(TLConfirmedNotice, self).__init__(
            n_type='tl_confirmed__notification',
            content_template=content_template,
        )
