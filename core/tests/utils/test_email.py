from django.test import TestCase
from core.utils.email import Email
from mscms.settings import EMAIL_HOST_USER


class EmailTest(TestCase):
    def setUp(self):
        self.email = Email

    def test_email(self):
        """
        Test case to assert structure of email is maintained
        """
        subject = "Test Subject"
        to_email = "test@test.com"
        body = "I am the body of the email"

        mail = self.email(subject, to_email, body)

        # assert everything is working as expected
        self.assertEquals(mail.subject, subject)
        self.assertEquals(mail.to_email, [to_email])
        self.assertEquals(mail.body, body)
        self.assertEquals(mail.from_email, EMAIL_HOST_USER)
