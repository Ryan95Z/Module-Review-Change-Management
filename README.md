# Module Summary Change Management System
[![Build Status](https://travis-ci.org/Ryan95Z/Module-Summary-Change-Management-System.svg?branch=master)](https://travis-ci.org/Ryan95Z/Module-Summary-Change-Management-System)

## Requirements
* Python 3
* Django 1.11.7

To install the requirements: `pip install -r requirements.txt`

## Installation for development
(Assuming that the requirements for the application have been satisfied)
1. Clone the repositroy - `git clone https://github.com/Ryan95Z/Module-Summary-Change-Management-System.git .`
2. Add the email file - `cp -v ./mscms/email_settings-example.py ./mscms/email_settings.py`.
3. Run the migrations - `python manage.py migrate`.
4. Create a superuser - `python manage.py createsuperuser` and complete the form in the terminal.
5. Run the development server - `python manage.py runserver`

## Executing the Unit Tests
To run all unit tests, run `python manage.py test`

## Coding Standards
All Python code in this application must conform to the PEP8 Python coding standard. Inforamtion about the style guide can be found here: [PEP8 Coding Standards](https://www.python.org/dev/peps/pep-0008/)
