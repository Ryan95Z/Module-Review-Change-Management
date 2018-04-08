from django.shortcuts import render
from forms.models import ModuleAssessment,ModuleSoftware,ModuleSupport, ModuleTeaching,ModuleDescription,ModuleDescriptionFormVersion,ModuleDescriptionEntry,FormFieldEntity
from core.models import *
from django.views import View
from django.http import HttpResponse
# from forms.utils.module_description import ModuleDescriptionWrapper, CurrentModuleDescriptionWrapper
import random
import csv
from collections import defaultdict


class ModuleSheetDownload(View):
    '''
    this will be calleed for downloading the csv data
    '''
    def get(self, request, *args, **kwargs):
        modules = Module.objects.all()  # gets all the modules
        module_desc_entries = ModuleDescriptionEntry.objects.all()  # gets all module desc entriy eg(string_entry)
        form_fields = FormFieldEntity.objects.all() # gets all fields
        versions = ModuleDescriptionFormVersion.objects.all() #gets all versions

        # group form fields by version
        form_fields_by_version = defaultdict(list)
        for form_field in form_fields:
            form_fields_by_version[form_field.module_description_version_id].append(form_field)

        # this table will have all the modules without any fields (will be shown as a separate table)
        table_without_fields = {
            'headers': ['Module Code','Module Name'],
            'modules': []
        }


        # this list will contain set of all the tables on the page
        multiple_tables = []

        # set of module code which have fields for any version
        module_codes_with_entries = set()

        # loop over different versions and collect module, form data for each version
        for idx, version in enumerate(versions):
            # get all the fields for a specific version
            form_fields = form_fields_by_version[version.module_description_version]
            _headers = ['Module Code','Module Name'] #will be used to create headers
            # add each field as header
            for formfield in form_fields:
                _headers.append(formfield.entity_label)
            # list of modules
            _modules = []
            # go over each module
            for module in modules:
                # gets all entries for this module
                entries = list(self._filterByModule(module_desc_entries, module, version))
                # create row
                _entries = [module.module_code, module.module_name]
                for e in entries:
                    _entries.append(e.string_entry)
                # if we don't have any fields for a module, add them as a separate table
                if len(_entries) == 2:
                    # Add it to last table
                    if _entries not in table_without_fields['modules']:
                        table_without_fields['modules'].append(_entries)
                    continue
                # add row table
                _modules.append(_entries)

                # add the module code (if it has > 0 fields)
                module_codes_with_entries.add(_entries[0])
            # add table for a specific version of fields to list of tables
            multiple_tables.append({ 'headers': _headers,'modules':_modules})

        # Clean up the last table (without fields)
        temp_table = []
        for t in table_without_fields['modules']:
            if t[0] not in module_codes_with_entries:
                temp_table.append(t)
        # Cleaned up list of modules (to be shown as the last table)
        table_without_fields['modules'] = temp_table

        multiple_tables.append(table_without_fields)

        # Write the table data to a temporary csv file
        # define the file name
        filename = "/tmp/table_{}.csv".format(random.randint(1, 100000))

        # Open the file for writing and use cscv module for writing
        with open(filename, 'w') as myfile:
            # Initialize the csv writer
            wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)


            for table in multiple_tables:
                # write the data (header + rows) using the csv writer
                wr.writerows([table['headers']] + table['modules'])
                wr.writerow(["\n"])

        # Read the csv file, and send the file as an HTTP response back to the client,
        # which gets downloaded on the user's machine
        with open(filename, 'r') as myfile:
            # Create an HTTPResponse with attachment
            response = HttpResponse(myfile, content_type='text/csv')
            # Set the reponse headers (this triggers the download on client side)
            response['Content-Disposition'] = 'attachment; filename=ModelSummarySheet.csv'
            return response

    '''
    filter all the entries to module
    '''
    def _filterByModule(self, module_desc_entries, module, version):
        for entry in module_desc_entries:
            # check if module code and version match
            if entry.module_description_id.module.module_code == module.module_code and \
                entry.field_id.module_description_version_id == version.module_description_version:
                yield entry



class ModuleSheetView(View):
    '''
    this will be calleed for displaying the page
    returns the rendered output
    '''
    def get(self, request, *args, **kwargs):
        modules = Module.objects.all()  # gets all the modules
        module_desc_entries = ModuleDescriptionEntry.objects.all()  # gets all module desc entriy eg(string_entry)
        form_fields = FormFieldEntity.objects.all() # gets all fields
        versions = ModuleDescriptionFormVersion.objects.all() #gets all versions

        # group form fields by version
        form_fields_by_version = defaultdict(list)
        for form_field in form_fields:
            form_fields_by_version[form_field.module_description_version_id].append(form_field)

        # this table will have all the modules without any fields (will be shown as a separate table)
        table_without_fields = {
            'headers': ['Module Code','Module Name'],
            'modules': []
        }

        # this list will contain set of all the tables on the page
        multiple_tables = []

        # set of module code which have fields for any version
        module_codes_with_entries = set()

        # loop over different versions and collect module, form data for each version
        for idx, version in enumerate(versions):
            # get all the fields for a specific version
            form_fields = form_fields_by_version[version.module_description_version]
            _headers = ['Module Code','Module Name'] #will be used to create headers
            # add each field as header
            for formfield in form_fields:
                _headers.append(formfield.entity_label)
            # list of modules
            _modules = []
            # go over each module
            for module in modules:
                # gets all entries for this module
                entries = list(self._filterByModule(module_desc_entries, module, version))
                # create row
                _entries = [module.module_code, module.module_name]
                for e in entries:
                    _entries.append(e.string_entry)

                # if we don't have any fields for a module, add them as a separate table
                if len(_entries) == 2:
                    # Add it to last table
                    if _entries not in table_without_fields['modules']:
                        table_without_fields['modules'].append(_entries)
                    continue
                # add row table
                _modules.append(_entries)

                # add the module code (if it has > 0 fields)
                module_codes_with_entries.add(_entries[0])
            # add table for a specific version of fields to list of tables
            multiple_tables.append({ 'headers': _headers,'modules':_modules})

        # Clean up the last table (without fields)
        temp_table = []
        for t in table_without_fields['modules']:
            if t[0] not in module_codes_with_entries:
                temp_table.append(t)
        # Cleaned up list of modules (to be shown as the last table)
        table_without_fields['modules'] = temp_table

        multiple_tables.append(table_without_fields)
        
        return render(request,'module_sheet.html', {'multiple_tables': multiple_tables})

    '''
    filter all the entries to module
    '''
    def _filterByModule(self, module_desc_entries, module, version):
        for entry in module_desc_entries:
            # check if module code and version match
            if entry.module_description_id.module.module_code == module.module_code and \
                entry.field_id.module_description_version_id == version.module_description_version:
                yield entry
