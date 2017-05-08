from avito_fraud.rank import get_rank
from avito_fraud.cache import WordsCache
import math
import os
import unittest


class MockCache(WordsCache):

    def __init__(self, *args, **kwargs):
        super(MockCache, self).__init__(*args, **kwargs)
        self.getter_success_attempts = 0

    def get(self, *args, **kwargs):
        val = super(MockCache, self).get(*args, **kwargs)
        if val:
            self.getter_success_attempts += 1
        return val


class MainTest(unittest.TestCase):

    def test_cache(self):
        cache = MockCache()

        for fn in ['fraud_warn.txt', 'fraud_err.txt', 'high.txt', 'middle.txt', 'low.txt']:
            text = self.get_fixture_text(fn)
            get_rank(text, cache)

        self.assertTrue(len(cache) > 0)
        self.assertTrue(cache.getter_success_attempts > 0)

    def test_fraud_warning(self):
        self.assertRank('fraud_warn.txt', (0.11023622047244094, True, False))

    def test_fraud_error(self):
        self.assertRank('fraud_err.txt', (0.11013215859030837, True, True))

    def test_high_rank(self):
        self.assertRank('high.txt', (0.7027027027027027, False, False))

    def test_middle_rank(self):
        self.assertRank('middle.txt', (0.1095890410958904, False, False))

    def test_low_rank(self):
        self.assertRank('low.txt', (0.012269938650306749, False, False))

    def test_empty_rank(self):
        self.assertRank('empty.txt', (None, False, False))

    def assertRank(self, fn, rank_data):
        text = self.get_fixture_text(fn)
        right = get_rank(text, {})

        if rank_data[0] is None:
            self.assertEqual(rank_data[0], right[0])
        else:
            self.assertTrue(math.fabs(right[0] - rank_data[0]) < 1e-9,
                'New Rank {}, old: {}'.format(right[0], rank_data[0]))

        self.assertEqual(right[1:], rank_data[1:], 'Fraud data is bad')

    def get_fixture_text(self, fn):
        fn_path = os.path.join(os.path.dirname(__file__), '../../fixtures/', fn)
        ret = open(fn_path, 'rb').read().decode('utf-8', 'ignore')
        return ret
