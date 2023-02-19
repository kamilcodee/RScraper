import unittest

from rscraper import Config
from rscraper import SubmissionScraper


class SubmissionScraperTest(unittest.TestCase):

    def setUp(self) -> None:
        self.config = Config()
        self.subject = SubmissionScraper(self.config)

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
        base_url = 'https://www.reddit.com/r/CasualUK'

        actual_url = self.subject._create_url(base_url, after)
        expected_url = ''.join([base_url, '.json', f'?limit={self.config.max_limit_per_request}'])

        self.assertEqual(expected_url, actual_url)

    def test_urlCreationWithAfter(self):
        """
        Url creation uses after and returns expected value, when it is set
        """

        after = 'AFTER'
        base_url = 'https://www.reddit.com/r/CasualUK'

        actual_url = self.subject._create_url(base_url, after)
        expected_url = ''.join([base_url, '.json', f'?limit={self.config.max_limit_per_request}', f'&after={after}'])

        self.assertEqual(expected_url, actual_url)

    def test_urlCreationWithLimitPerRequestWithAfter(self):
        """
        Url creation uses limit and returns expected value, when it is overriden
        """

        limit = 44
        after = 'AFTER'
        base_url = 'https://www.reddit.com/r/CasualUK'

        self.config.max_limit_per_request = limit

        expected_url = ''.join([base_url, '.json', f'?limit={limit}', f'&after={after}'])
        actual_url = self.subject._create_url(base_url, after)

        self.assertEqual(expected_url, actual_url)
