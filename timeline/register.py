from timeline.utils.factory import EntryFactory
from timeline.utils.entries import InitEntry, UpdatedEntry


def timeline_register(cls):
    init_alis = "init" + cls.__name__
    update_alis = "update" + cls.__name__
    EntryFactory.register(InitEntry, init_alis, cls)
    EntryFactory.register(UpdatedEntry, update_alis, cls)
    return cls
