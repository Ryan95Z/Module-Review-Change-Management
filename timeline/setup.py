# from core.models import Module
# from timeline.utils.factory import EntryFactory
# from timeline.utils.entries import InitEntry, UpdatedEntry


from timeline.utils.notifications.factory import NotificationFactory
from timeline.utils.notifications.notices import (DiscussionNotice,
                                                  ReplyNotice,
                                                  TLStagingNotice,
                                                  TLConfirmedNotice,
                                                  MentionNotice,
                                                  ModuleLeaderNotice)


# set up the entry factory for module
# INIT = "init" + Module.__name__
# UPDATE = "update" + Module.__name__

# EntryFactory.register(InitEntry, INIT, Module)
# EntryFactory.register(UpdatedEntry, UPDATE, Module)


# set the notification factory
NotificationFactory.register(DiscussionNotice, "discussion")
NotificationFactory.register(ReplyNotice, "reply")
NotificationFactory.register(TLStagingNotice, "staged")
NotificationFactory.register(TLConfirmedNotice, "confirmed")
NotificationFactory.register(MentionNotice, "mention")
NotificationFactory.register(ModuleLeaderNotice, "module_leader")
