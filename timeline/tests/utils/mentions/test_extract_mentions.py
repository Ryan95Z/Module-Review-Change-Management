from timeline.tests.common import BasicUserTestCase
from timeline.utils.mentions import extract_mentions


class TestExtractMentions(BasicUserTestCase):
    """
    Test case for extract mentions util function
    """

    def setUp(self):
        super(TestExtractMentions, self).setUp()
        self.func = extract_mentions

    def test_valid_extract_mentions(self):
        """
        Test extract function with mentions
        """
        sample = "@ryan this is a test, @test are we testing. @user1"

        # test with no author_username
        output = self.func(sample)
        expected = ['ryan', 'test', 'user1']
        self.assertEquals(output, expected)

        # test with author username
        output = self.func(sample, self.user1.username)
        expected = ['ryan', 'test']
        self.assertEquals(output, expected)

    def test_extract_with_no_mentions(self):
        """
        Test extract function with no mentions
        """
        sample = "Hello World. I am a test."

        # test with no author username
        output = self.func(sample)
        expected = []
        self.assertEquals(output, expected)

        # test with author username
        output = self.func(sample)
        self.assertEquals(output, expected)

    def test_extract_with_none(self):
        """
        Test extract function with different none parameters
        """
        # only None comment
        with self.assertRaises(ValueError):
            self.func(None)

        # both parameters are none
        with self.assertRaises(ValueError):
            self.func(None, None)

        # pnly username is none
        with self.assertRaises(ValueError):
            self.func('test', None)
