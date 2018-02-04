from django.core.mail import EmailMessage
from mscms.settings import EMAIL_HOST_USER


class Email(object):
    """
    Wrapper class for creating an email in Django
    """
    def __init__(self, subject, to_email, body):
        self.subject = subject
        self.from_email = EMAIL_HOST_USER
        self.to_email = [to_email]
        self.body = body

        self.__mail = EmailMessage(
            self.subject,
            self.body,
            self.from_email,
            self.to_email
        )

    def send(self):
        """
        Send the email
        """
        self.__mail.send()


class UserPasswordEmail(Email):
    """
    Class to automatically create the email when a user is created
    """

    # subject of the email
    subject = "Module Management - User Account"

    # text template of the message that is sent to the user's email.
    # Has to be formated this way to prevent the extra space being
    # displayed in the email.
    template = """
To {},

Your account for the Module Change Management System has been created.
Username: {}
Password: {}

Please change your password upon first logging into the system.

From,
Admin
"""

    def __init__(self, user, password):
        # add the information to the body template
        self.msg = self.template.format(
            user.first_name,
            user.username,
            password
        )

        super(UserPasswordEmail, self).__init__(
            self.subject,
            user.email,
            self.msg
        )
