"""

=======================
        Note
=======================

This is an example file for configuring the automated
emailing for the applicaiton. Make a copy of this file and rename it
to "email_settings.py" before running the application. This renamed file
will then already be imported into the settings.py file of the applicaiton.

DO NOT push the email_settings.py file to the repo as this will expose
any passwords that are used.


"""

# For example: 'smtp.gmail.com'
EMAIL_HOST = ""

# The email address: such as "example@gmail.com"
EMAIL_HOST_USER = ""

# Password for the above email
EMAIL_HOST_PASSWORD = ""

# Can also be 25 and 465. Though varies between services
EMAIL_PORT = 587
EMAIL_USE_TLS = True

# Standard Django items - DO NOT CHANGE THIS !!!
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
