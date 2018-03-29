from timeline.models import TimelineEntry


def process_changes(module_code, *args):
    entries = []
    for obj in args:
        if not isinstance(obj, list):
            entries.append(BuildTLEntry(obj))
        else:
            for i in obj:
                entries.append(BuildTLEntry(i))

    # print(entries)
    p = ParentEntry(module_code, *entries)
    p.create_master()


class BuildTLEntry(object):
    tl = TimelineEntry

    def __init__(self, model):
        self.model = model

    def get_differences(self):
        return self.model.differences()

    def module_code(self):
        return self.model.module_code()

    def content(self):
        diff = self.model.differences()
        md = ""
        for field, changes in diff.items():
            field = field.replace("_", " ")
            original = changes[0]
            updated = changes[1]
            md += "* {}: {} -> {}\n".format(field, original, updated)
        return md

    def sum_changes(self):
        print(self.model)
        n_changes = len(self.model.differences())
        return "There are {} changes to {}".format(
            n_changes, self.model.title()
        )

    def create_entry(self, parent):
        if not self.model.hasDifferences():
            return

        title = self.model.title()
        changes = self.content()
        module_code = self.module_code()
        object_id = self.model.pk
        content_object = self.model

        return TimelineEntry.objects.create(
            title=title,
            changes=changes,
            module_code=module_code,
            object_id=object_id,
            content_object=content_object,
            parent_entry=parent,
            entry_type='Tracking-Form'
        )

    def title(self):
        return self.model.title()


# class BuildListTLEntry(object):
#     tl = TimelineEntry

#     def __init__(self, _list, module_code):
#         self.list = _list
#         self.length = len(_list)
#         self.module_code = module_code

#         self.cls = None
#         if self.length > 0:
#             self.cls = self.list[0].__class__.__name__

#     def get_differences(self):
#         diff = {}
#         if self.length == 0:
#             return None

#         for index, val in enumerate(self.list):
#             diff[index] = val.differences()
#         return diff

#     def sum_changes(self):
#         n_changes = len(self.model.differences())
#         return "There are {} items that have been changed to {}".format(
#             n_changes, self.model.title()
#         )

#     def content(self):
#         if self.length == 0:
#             return None

#         diff = self.get_differences()
#         md = ""
#         for key, nested in diff.items():
#             for field, changes in nested.items():
#                 field = field.replace("_", " ")
#                 original = changes[0]
#                 updated = changes[1]
#                 md += "* {}: {} -> {}".format(
#                     field, original, updated
#                 )
#         return md

#     def create_entry(self, parent):
#         title = self.model.title()
#         changes = self.content()
#         module_code = self.module_code
#         object_id = self.model.pk
#         content_object = self.model

#         return TimelineEntry.objects.create(
#             title=title,
#             changes=changes,
#             module_code=module_code,
#             object_id=object_id,
#             content_object=content_object,
#             parent_entry=parent,
#             entry_type='Tracking-Form'
#         )

#     def title(self):
#         return "list entry"


class ParentEntry(object):
    def __init__(self, module_code, *args):
        self.args = args
        self.module_code = module_code

    def create_master(self):
        title = "Changes"
        content = "Changes to tracking form:\n\n"
        module_code = self.module_code
        object_id = 0
        content_object = None
        for a in self.args:
            content += "* {}\n".format(a.sum_changes())

        master = TimelineEntry.objects.create(
            title=title,
            changes=content,
            module_code=module_code,
            object_id=object_id,
            content_object=content_object,
            entry_type='Tracking-Form'
        )

        for a in self.args:
            a.create_entry(master)
