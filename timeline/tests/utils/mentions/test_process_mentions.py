from django.urls import reverse
from timeline.tests.common import BasicUserTestCase
from timeline.utils.mentions import process_mentions


class TestProcessMentions(BasicUserTestCase):
    """
    Test case for process mentions function in timeline utils.
    """

    def setUp(self):
        super(TestProcessMentions, self).setUp()
        self.link_markdown = "[{}]({})"
        self.func = process_mentions

    def test_valid_process(self):
        """
        Test process mentions with all valid users
        """
        # test string
        template = "{} this is a good idea. {} what do you think?"
        sample = template.format("@user1", "@admin")

        # preparing expected values
        user1 = self.__get_user_markdown(self.user1)
        admin = self.__get_user_markdown(self.admin)
        expected_output = template.format(user1, admin)

        # test process mentions
        output = self.func(sample)
        self.assertEquals(output, expected_output)

    def test_process_non_existing_user(self):
        """
        Test mentions with users that are not in the database
        """
        sample = "@ryan is this working? @bill"
        output = self.func(sample)
        self.assertEquals(output, sample)

    def test_process_mix_of_users(self):
        """
        Test with existing and non-existing users
        """
        template = "{} are you a test? {} is a fake user"
        sample = template.format("@user1", "@ryan")

        # prepare expected values
        user1 = self.__get_user_markdown(self.user1)
        expected_output = template.format(user1, "@ryan")

        # test process mentions
        output = self.func(sample)
        self.assertEquals(output, expected_output)

    def test_process_with_no_mentions(self):
        """
        Test process with no mentions
        """
        sample = "Hello World. I am working today"
        output = self.func(sample)
        self.assertEquals(output, sample)

    def test_process_empty_inputs(self):
        """
        Test process in event that it is empty
        """
        sample = ''
        output = self.func(sample)
        self.assertEquals(output, sample)

    def test_process_none_input(self):
        """
        Test process when input is None:
        """
        with self.assertRaises(ValueError):
            self.func(None)

    def test_process_invalid_input_type(self):
        """
        Test process will prevent invalid data types
        """
        # test with int
        with self.assertRaises(ValueError):
            self.func(1233)

        # test with list
        with self.assertRaises(ValueError):
            self.func(['@ryan', 'Hello', 'World'])

        # test with object
        # dummy class definition
        class dummy(object):
            mentions = "@ryan hello world"

        # test the dummy class cannot be processed
        obj = dummy()
        with self.assertRaises(ValueError):
            self.func(obj)

    def __get_user_markdown(self, user):
        """
        Help method to create markdown automatically
        """
        url = reverse('user_profile', kwargs={'pk': user.pk})
        mention = "@{}".format(user.username)
        return self.link_markdown.format(mention, url)
