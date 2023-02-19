import unittest
from rscraper import SubredditScraper
from rscraper import Config


class SubredditScraperTest(unittest.TestCase):

    def setUp(self):
        self.config = Config()
        self.subject = SubredditScraper(self.config)

    def test_incorrectLimit1(self):
        """
        Providing limit not of type int will raise an error
        :raises TypeError
        """

        with self.assertRaises(TypeError):
            self.subject.limit = 1.23

    def test_incorrectLimit2(self):
        """
        Providing limit <= 0 will raise an error
        :raises ValueError
        """

        with self.assertRaises(ValueError):
            self.subject.limit = -1

    def test_urlCreationNoAfter(self):
        """
        Url creation uses after and returns expected value
        """

        after = None
        self.subject._after = after
        actual_url = self.subject._create_url()

        expected_url = ''.join(
            [self.config.base_url, self.config.subreddits_sub_url, '.json',
             f'?limit={self.config.max_limit_per_request}'])

        self.assertEqual(expected_url, actual_url)

    def test_urlCreationWithAfter(self):
        """
        Url creation uses after and returns expected value, when it is set
        """

        after = 'AFTER'
        self.subject._after = after
        actual_url = self.subject._create_url()

        expected_url = ''.join(
            [self.config.base_url, self.config.subreddits_sub_url, '.json',
             f'?limit={self.config.max_limit_per_request}', f'&after={after}'])

        self.assertEqual(expected_url, actual_url)

    def test_urlCreationWithLimitPerRequest(self):
        """
        Url creation uses limit and returns expected value, when it is overriden
        """

        limit = 44
        new_config = Config()
        new_config.max_limit_per_request = limit

        new_subject = SubredditScraper(new_config)
        actual_url = new_subject._create_url()

        expected_url = ''.join(
            [self.config.base_url, self.config.subreddits_sub_url, '.json',
             f'?limit={limit}'])

        self.assertEqual(expected_url, actual_url)
