from timeline.utils.notifications.factory import NotificationFactory
from timeline.utils.notifications.notices import (DiscussionNotice,
                                                  ReplyNotice,
                                                  TLStagingNotice,
                                                  TLConfirmedNotice,
                                                  MentionNotice,
                                                  ModuleLeaderNotice)


# set the notification factory
NotificationFactory.register(DiscussionNotice, "discussion")
NotificationFactory.register(ReplyNotice, "reply")
NotificationFactory.register(TLStagingNotice, "staged")
NotificationFactory.register(TLConfirmedNotice, "confirmed")
NotificationFactory.register(MentionNotice, "mention")
NotificationFactory.register(ModuleLeaderNotice, "module_leader")