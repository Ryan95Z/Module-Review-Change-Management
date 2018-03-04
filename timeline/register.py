from timeline.utils.factory import EntryFactory
from timeline.utils.entries import InitEntry, UpdatedEntry
from timeline.models.integrate.entry import TLEntry


def timeline_register(cls):
    """
    Decorator function to create factory instances
    a model that needs entries on the timeline
    """
    if not issubclass(cls, TLEntry):
        raise ValueError(
            "timeline register requires instances to inherit TLEntry"
        )
    init_alis = "init" + cls.__name__
    update_alis = "update" + cls.__name__
    EntryFactory.register(InitEntry, init_alis, cls)
    EntryFactory.register(UpdatedEntry, update_alis, cls)
    return cls
