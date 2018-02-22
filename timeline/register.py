from core.models import Module
from timeline.utils.entries import *


INIT = "init" + Module.__name__
UPDATE = "update" + Module.__name__

EntryFactory.register(InitEntry, INIT, Module)
EntryFactory.register(UpdatedEntry, UPDATE, Module)
