from abc import ABC, abstractmethod
from timeline.models import Notification, Watcher
from django.urls import reverse


class BaseNotice(ABC):
    """
    Base class for all notifications
    """
    def __init__(self, content_template, link_name):
        """
        Arguments:
            content_template    String of the nessage that will be
                                displayed to the user with format margkers

            link_name           Name of the django url
        """
        if len(content_template) < 1:
            raise ValueError("content_template cannot be empty")

        if len(link_name) < 1:
            raise ValueError("link_name cannot be empty")

        # public instance variables
        self.content_template = content_template
        self.link_name = link_name

        # protected instance variables
        self._watchers = Watcher
        self._notification = Notification

    #############################
    # Public Methods
    #############################
    @abstractmethod
    def create(self, **kwargs):
        """
        Method to create the notification based on
        provided kwargs. Kwargs are dependent on class implementation
        """
        pass

    def factory(self):
        """
        Method used by NotificationFactory to create
        a notification for the user.

        Arguments:
            void

        Return:
            new object of class
        """
        return self.__class__()

    def get_url(self, data):
        """
        Creates the url for this particular notification.

        Arguments:
            data        Dict of expected parameters for url

        Return:
            String of url
        """
        return reverse(self.link_name, kwargs=data)

    #############################
    # Protected Methods
    #############################
    def _get_watchers(self, module_code):
        """
        Gets watchers for a particular model.

        Arguments:
            module_code     String of particular model code

        Return:
            Queryset of watcher objects
        """
        return self._watchers.objects.filter(watching__pk=module_code)

    def _create_notification(self, content, recipient, link):
        """
        Adds a notification to the database

        Arguments:
            content     String message for notification
            recipient   User that is getting the notification
            link        URL to where the notification is relevant

        Return:
            void
        """
        self._notification.objects.create(
            content=content,
            recipient=recipient,
            link=link,
        )


class DiscussionNotice(BaseNotice):
    """
    Notification when a post has been added to a timeline entry
    """

    def __init__(self):
        content_template = "{} has written a comment for {}"
        super(DiscussionNotice, self).__init__(
            content_template=content_template,
            link_name='discussion'
        )

    def create(self, **kwargs):
        """
        Method for creating DiscussionNotice.

        kwargs expected:
            discussion      Discussion model
            user            User object
        """
        discussion = kwargs.get('discussion', None)
        user = kwargs.get('user', None)

        if discussion is None:
            raise ValueError("discussion object must not be None")

        if user is None:
            raise ValueError("user object must not be None")

        # get the timeline entry assocaited with posted comment
        entry = discussion.entry

        # create the notification message
        content = self.content_template.format(
            user.username,
            entry.module_code
        )

        # get the url
        url = self.get_url({
            'module_pk': entry.module_code,
            'pk': entry.pk,
        })

        # get all user that are watching this module
        watchers = self._get_watchers(entry.module_code)

        # go through each watcher and create a notfication for them.
        for w in watchers:
            # ignore the user that triggered the notification for other users
            if w.watcher_username() != user.username:
                self._notification.objects.create(
                    content=content,
                    recipient=w.user,
                    link=url,
                )


class ReplyNotice(BaseNotice):
    """
    Notification when a reply is added to a post
    """
    def __init__(self):
        content_template = "{} has replied to your post"
        super(ReplyNotice, self).__init__(
            content_template=content_template,
            link_name='discussion'
        )

    def create(self, **kwargs):
        """
        Creates ReplyNotice

        kwargs expected:
            discussion      Discussion model
            user            User object
            parent          Parent discussion model
        """
        discussion = kwargs.get('discussion', None)
        user = kwargs.get('user', None)
        parent = kwargs.get('parent', None)

        if discussion is None:
            raise ValueError("discussion keyword should not be None")

        if user is None:
            raise ValueError("user keyword should not be None")

        if parent is None:
            raise ValueError("parent keyword should not be None")

        # get the author of the post that recieved
        # the reply. This will be the user that recieves the notification.
        recipient = parent.author

        if recipient.username == user.username:
            return

        # get the timeline entry
        entry = discussion.entry

        # get the url
        url = self.get_url({
            'module_pk': entry.module_code,
            'pk': entry.pk,
        })

        content = self.content_template.format(user.username)

        # create the notification
        self._notification.objects.create(
            recipient=recipient,
            content=content,
            link=url
        )


class TLEntryNotice(BaseNotice):
    """
    Generic change entry for Timeline
    """
    def __init__(self):
        content_template = "A change has been made to {}"
        super(TLEntryNotice, self).__init__(
            content_template=content_template,
            link_name='module_timeline'
        )

    def create(self, **kwargs):
        """
        Creates TLEntryNotice

        kwargs expected:
            entry      Timeline entry that has been added
        """
        entry = kwargs.get('entry', None)

        if entry is None:
            raise ValueError("entry keyword should not be None")

        module_code = entry.module_code
        content = self.content_template.format(module_code)

        # get the watchers
        watchers = self._get_watchers(entry.module_code)

        # get the url
        url = self.get_url({
            'module_pk': module_code
        })

        # notify all users that watch the module
        # that the change has been added.
        for w in watchers:
            self._notification.objects.create(
                content=content,
                recipient=w.user,
                link=url,
            )


class TLChangeNotice(BaseNotice):
    """
    Base notification when a change of status
    has beem made to a timeline entry. For example,
    moving from draft to staging.
    """
    def __init__(self, content_template):
        super(TLChangeNotice, self).__init__(
            content_template=content_template,
            link_name='module_timeline'
        )

    def create(self, **kwargs):
        """
        Creates TLChangeNotice

        kwargs expected:
            user       User object
            entry      Timeline entry that has been added
        """
        approver = kwargs['user']
        entry = kwargs['entry']
        module_code = entry.module_code

        content = self.content_template.format(
            approver.username,
            module_code
        )

        # get all watchers
        watchers = self._get_watchers(module_code)

        # get the url
        url = self.get_url({
            'module_pk': module_code
        })

        # notify all users
        # ignore user who triggered notification
        for w in watchers:
            if w.watcher_username() != approver.username:
                self._create_notification(content, w.user, url)


class TLStagingNotice(TLChangeNotice):
    """
    Notification when entry has been moved from draft
    to staging.
    """
    def __init__(self):
        content_template = "{} has approved a change for staging to {}"
        super(TLStagingNotice, self).__init__(
            content_template=content_template,
        )


class TLConfirmedNotice(TLChangeNotice):
    """
    Notification when entry has been moved from staging
    to confirmed.
    """
    def __init__(self):
        content_template = "{} has confirmed a change to {}"
        super(TLConfirmedNotice, self).__init__(
            content_template=content_template,
        )


class MentionNotice(BaseNotice):
    def __init__(self):
        content_template = "{} mentioned you in a post for {}"
        super(MentionNotice, self).__init__(
            content_template=content_template,
            link_name='discussion'
        )

    def create(self, **kwargs):
        author = kwargs['author']
        entry = kwargs['entry']
        mention_user = kwargs['mention']
        module_code = entry.module_code

        content = self.content_template.format(author.username, module_code)
        url = self.get_url({
            'module_pk': module_code,
            'pk': entry.pk,
        })

        self._create_notification(content, mention_user, url)


class ModuleLeaderNotice(BaseNotice):
    def __init__(self):
        content_template = "You have been made the module leader of {}"
        super(ModuleLeaderNotice, self).__init__(
            content_template=content_template,
            link_name='/'  # need to think of a better url for this.
        )

    def create(self, **kwargs):
        module_code = kwargs['module_code']
        module_leader = kwargs['module_leader']

        content = self.content_template.format(module_code)

        url = '/'

        self._create_notification(content, module_leader, url)
