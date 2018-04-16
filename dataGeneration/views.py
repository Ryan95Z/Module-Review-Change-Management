from django.shortcuts import render
from forms.models import ModuleAssessment,ModuleSoftware,ModuleSupport, ModuleTeaching,ModuleDescription
from core.models import *
from django.views import View
from timeline.models import  *
from django.http import HttpResponse
import random
import csv
#Create your views here.

# def index(request):
#     software_list = Module.objects.all()
#     date_dict = {"software_records":software_list}
#     return render(request,'lab_sheet.html',date_dict)


class labSheetDownload(View):
    '''
    this will be calleed for downloading the csv data
    '''
    def get(self, request, *args, **kwargs):

        software_list = ModuleSoftware.objects.all()
        indicative = ModuleTeaching.objects.all()
        modules = Module.objects.all()
        support_list = ModuleSupport.objects.all()
        _modules = []

        # Define the header row for the csv file
        rows = [[
          	'Module Code',
        	'Module Name',
            'Software Required',
            'Version of Software Rquired',
            'Indicative Hours for Practical Workshops',
            'Skills of the Tutor Required '
        ]]
        for module in modules:
            try:
                software = software_list.get(module=module.module_code)
                teaching = indicative.get(module=module.module_code)
                support = support_list.get(module=module.module_code)
            except:
                software = None
                teaching = None
                support = None

            # append the rows for the csv file
            rows.append([
                module.module_code,
                module.module_name,
                software.software_name if software != None else '',
                software.software_version if software != None else '',
                teaching.teaching_practical_workshops if teaching != None else '',
                support.lab_support_skills if (support != None and support.lab_support_skills != '') else 'No Lab Tutor Required',
            ])

        # Write the table data to a temporary csv file
        # define the file name
        filename = "/tmp/labsheet_{}.csv".format(random.randint(1, 100000))

        # Open the file for writing and use csv module for writing
        with open(filename, 'w') as myfile:
            # Initialize the csv writer
            wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
            # write the data (header + rows) using the csv writer
            wr.writerows(rows)
            print(rows)

        # Read the csv file, and send the file as an HTTP response back to the client,
        # which gets downloaded on the user's machine
        with open(filename, 'r') as myfile:
            # Create an HTTPResponse with attachment
            response = HttpResponse(myfile, content_type='text/csv')
            # Set the reponse headers (this triggers the download on client side)
            response['Content-Disposition'] = 'attachment; filename=LabOrganisationSheet.csv'
            return response




class labSheetView(View):
    '''
        gets the list of elements in the table.
        each module is iterated over and then checked for module code in software, teaching and support
    '''
    def get(self, request, *args, **kwargs):
        software_list = ModuleSoftware.objects.all()
        indicative = ModuleTeaching.objects.all()
        modules = Module.objects.all()
        support_list = ModuleSupport.objects.all()
        _modules = []

        for module in modules:
            #error handling, so If an error is encountered, a try block code execution is stopped and transferred down to the except block.
            try:
                software = software_list.get(module=module.module_code)
                teaching = indicative.get(module=module.module_code)
                support = support_list.get(module=module.module_code)
            except:
                software = None
                teaching = None
                support = None
            _modules.append({
                'module_code': module.module_code,
                'module_name': module.module_name,
                'software_name': software.software_name if software != None else '',
                'software_version': software.software_version if software != None else '',
                'indicative_hours': teaching.teaching_practical_workshops if teaching != None else '',
                'skills': support.lab_support_skills if (support != None and support.lab_support_skills != '') else 'No Lab Tutor Required',
            })


        return render(request,'lab_sheet.html', { 'modules': _modules })
