from django.test import TestCase
from core.utils.email import UserPasswordEmail
from core.models import User, UserManager
from mscms.settings import EMAIL_HOST_USER


class UserPasswordEmailTest(TestCase):
    def setUp(self):
        manager = UserManager()
        manager.model = User

        self.password = "password"
        self.user = manager.create(
            username="Test",
            first_name="Tester",
            last_name="Test",
            email="test@test.com",
            password=self.password
        )
        self.email = UserPasswordEmail

    def test_email(self):
        """
        Test case for checking that properties are correct
        for the class.
        """
        mail = self.email(self.user, self.password)

        # expected body of the email
        expected_body = mail.template.format(
            self.user.first_name,
            self.user.username,
            self.password
        )

        # check the msg property
        self.assertEquals(mail.msg, expected_body)

        # check that super class properties are correct
        self.assertEquals(mail.subject, mail.subject_title)
        self.assertEquals(mail.to_email, [self.user.email])
        self.assertEquals(mail.from_email, EMAIL_HOST_USER)
        self.assertEquals(mail.body, expected_body)
