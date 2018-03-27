from django import forms
from core.models import ProgrammeTutor, Module

YEAR_LEVELS = {
    'Year 1': 'L4',
    'Year 2': 'L5',
    'Year 3': 'L6',
    'MSC': 'L7',
}


class TutorForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(TutorForm, self).__init__(*args, **kwargs)

        instance = kwargs.get('instance', None)

        # if we are not processing an existing model, default
        # to the first year of modules
        if instance is None:
            self.fields['modules'].queryset = Module.objects.filter(
                module_level="L4"
            )
        # otherwise, get the modules for this tutpr
        else:
            level = YEAR_LEVELS[instance.tutor_year]
            self.fields['modules'].queryset = Module.objects.filter(
                module_level=level
            )

            # remove the user field as we are not changing them.
            self.fields.pop('programme_tutor_user')

        # check to get modules into the model
        if 'tutor_year' in self.data:
            tutor_year = self.data.get('tutor_year')
            try:
                level = YEAR_LEVELS[tutor_year]
                self.fields['modules'].queryset = Module.objects.filter(
                    module_level=level
                )
            except KeyError:
                msg = "{} is an invalid tutor year".format(tutor_year)
                self.add_error('tutor_year', msg)
            except (ValueError, TypeError):
                pass

    class Meta:
        model = ProgrammeTutor
        fields = ('programme_name', 'tutor_year',
                  'programme_tutor_user', 'modules')

        widgets = {
            'modules': forms.CheckboxSelectMultiple()
        }
