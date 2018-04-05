from abc import ABC, abstractmethod
from django.core.exceptions import ObjectDoesNotExist

from forms.models.tracking_form import *

# Function which accepts a number of forms as kwargs and returns a list of those which are unbound
def get_unbound_forms(**kwargs):
    unbounds = []
    for form_name, form in kwargs.items():
        if hasattr(form, "instance"):
            if form.instance.pk == None:
                unbounds.append(form_name)
        if hasattr(form, "queryset"):
            if not form.queryset:
                unbounds.append(form_name)
    return unbounds

class AbstractTrackingFormWrapper(ABC):

    def __init__(self, module):
        self.module = module
        self.populate()
    
    @abstractmethod
    def populate(self):
        pass

    def change_to_current(self):
        for name, obj in self.form_sections.items():
            self.__set_current_flag(obj)
        for name, objects in self.form_set_sections.items():
            for obj in objects:
                self.__set_current_flag(obj)

    def change_to_staging(self):
        for name, obj in self.form_sections.items():
            self.__set_staging_flag(obj)
        for name, objects in self.form_set_sections.items():
            for obj in objects:
                self.__set_staging_flag(obj)
                

    def __set_current_flag(self, obj):
        obj.archive_flag=False
        obj.staging_flag=False
        obj.current_flag=True
        obj.save()
    
    def __set_staging_flag(self, obj):
        obj.archive_flag=False
        obj.staging_flag=True
        obj.current_flag=False
        obj.save()
        
class CurrentTrackingFormWrapper(AbstractTrackingFormWrapper):

    def __init__(self, module):
        super(CurrentTrackingFormWrapper, self).__init__(module)

    def populate(self):
        self.form_sections = {
            "change_summary": ModuleChangeSummary.objects.filter(module=self.module, current_flag=True).first(),
            "teaching_hours": ModuleTeaching.objects.filter(module=self.module, current_flag=True).first(),
            "support": ModuleSupport.objects.filter(module=self.module, current_flag=True).first(),
            "reassessment": ModuleReassessment.objects.filter(module=self.module, current_flag=True).first(),
        }
        self.form_set_sections = {
            "assessments": ModuleAssessment.objects.filter(module=self.module, current_flag=True),
            "software": ModuleSoftware.objects.filter(module=self.module, current_flag=True)
        }

class StagedTrackingFormWrapper(AbstractTrackingFormWrapper):

    def __init__(self, module):
        super(StagedTrackingFormWrapper, self).__init__(module)
    
    def populate(self):
        self.form_sections = {
            "change_summary": ModuleChangeSummary.objects.filter(module=self.module, staging_flag=True).first(),
            "teaching_hours": ModuleTeaching.objects.filter(module=self.module, staging_flag=True).first(),
            "support": ModuleSupport.objects.filter(module=self.module, staging_flag=True).first(),
            "reassessment": ModuleReassessment.objects.filter(module=self.module, staging_flag=True).first()
        }
        self.form_set_sections = {
            "assessments": ModuleAssessment.objects.filter(module=self.module, staging_flag=True),
            "software": ModuleSoftware.objects.filter(module=self.module, staging_flag=True)
        }

class ArchivedTrackingFormWrapper(AbstractTrackingFormWrapper):

    def __init__(self, module, version_number):
        self.version_number = version_number
        super(TrackingFormWrapper, self).__init__(module)
    
    def populate(self):
        self.form_sections = {
            "change_summary": ModuleChangeSummary.objects.filter(module=self.module, version_number=self.version_number).first(),
            "teaching_hours": ModuleTeaching.objects.filter(module=self.module, version_number=self.version_number).first(),
            "support": ModuleSupport.objects.filter(module=self.module, version_number=self.version_number).first(),
            "reassessment": ModuleReassessment.objects.filter(module=self.module, version_number=self.version_number).first()
        }
        self.form_set_sections = {
            "assessments": ModuleAssessment.objects.filter(module=self.module, version_number=self.version_number),
            "software": ModuleSoftware.objects.filter(module=self.module, version_number=self.version_number)
        }
