import unittest

from rscraper import Config


class ConfigTest(unittest.TestCase):
    def setUp(self):
        self.subject = Config()

    def test_defaultUserAgent1(self):
        """
        Test default user agent
        """

        res = self.subject.user_agent()

        self.assertIsNotNone(res)

    def test_defaultUserAgent2(self):
        """
        Test custom user agent generation
        """

        expected_val = 'A' * 2

        def get_user_agent():
            return expected_val

        self.subject.user_agent = get_user_agent

        res = self.subject.user_agent()

        self.assertEqual(res, expected_val)
