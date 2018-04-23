from timeline.models import TimelineEntry
from forms.models.tracking_form import (ModuleAssessment, ModuleReassessment,
                                        ModuleChangeSummary, ModuleSoftware,
                                        ModuleSupport, ModuleTeaching)


def revert_changes(parent_entry):
    """
    Function to reset the tracking form if changes are
    denied by a reviewer.
    """
    if not isinstance(parent_entry, TimelineEntry):
        raise ValueError("parent_entry needs to a TimelineEntry")

    # get all children for the entry
    children = list(TimelineEntry.objects.filter(
        parent_entry_id=parent_entry.pk
    ))

    if len(children) < 1:
        return False

    # get the latest version number for the timeline
    archive_version_number = children[0].content_object.copy_number

    # process each child to reset it back to master
    for child in children:

        # the object that needs to be changed back to master
        revert = child.get_revert_object()
        master = child.content_object

        # if there is no object to go back to, then delete master
        # as it is not required.
        if revert is None:
            master.delete()
            continue

        # move copy number back as we are going back to a previous version
        copy_number = (master.copy_number - 1)

        # set archive record to master
        revert.version_number = 1
        revert.copy_number = copy_number
        revert.current_flag = True
        revert.archive_flag = False
        revert.staging_flag = False

        # remove current master
        master.delete()
        revert.save()

    # delete the parent entry
    parent_entry.delete()

    # clean up the database by removing archived records
    # that we created for this entry.
    revert = RevertTrackingFormChanges(
        archive_version_number,
        parent_entry.module_code
    )
    revert.remove_archive_versions()
    return True


class RevertTrackingFormChanges(object):
    """
    Helper class that will remove the old archive tracking
    records to the master state.
    """

    # models that need to be processed
    models = [ModuleAssessment, ModuleReassessment, ModuleChangeSummary,
              ModuleSoftware, ModuleSupport, ModuleTeaching]

    def __init__(self, version_number, module_code):
        self.version = version_number
        self.module_code = module_code

    def remove_archive_versions(self):
        """
        Method that resets eveything back to the previous version
        """
        for model in self.models:
            # removed the old archive versions
            # since the changes are already in master
            objs = model.objects.filter(
                version_number=self.version,
                module_id=self.module_code
            )
            objs.delete()

            # filter is used in cases where there in cases
            # for the Software or Assessment.
            master = model.objects.filter(
                version_number=1,
                module_id=self.module_code
            )
            # set each master back to current as changes
            # are no longer needed.
            for m in master:
                m.copy_number -= 1
                m.current_flag = True
                m.archive_flag = False
                m.staging_flag = False
                m.save()
        return True
