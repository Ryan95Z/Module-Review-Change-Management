# Module Summary Change Management System

## Requirements
* Python 3
* Django 1.11.7

To install the requirements: `pip install -r requirements.txt`

## Installation for development
(Assuming that the requirements for the application have been satisfied)
1. Clone the repositroy - `git clone https://github.com/Ryan95Z/Module-Summary-Change-Management-System.git .`
2. Run the migrations - `python manage.py makemigrations` and `python manage.py migrate`.
3. Create a superuser - `python manage.py createsuperuser` and complete the form in the terminal.
4. Run the development server - `python manage.py runserver`

## Executing the Unit Tests
To run all unit tests, run `python manage.py test`

## Coding Standards
All Python code in this application must conform to the PEP8 Python coding standard. Inforamtion about the style guide can be found here: [PEP8 Coding Standards](https://www.python.org/dev/peps/pep-0008/)
