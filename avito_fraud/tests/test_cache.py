from avito_fraud.cache import WordsCache
import unittest
from unittest.mock import patch


TEST_WORDS_CACHE_SIZE = 5


class MainTest(unittest.TestCase):

    @patch('avito_fraud.cache.WORDS_CACHE_SIZE', TEST_WORDS_CACHE_SIZE)
    def test_cache(self):
        cache = WordsCache()

        cache['a'] = 'b'
        self.assertEqual(len(cache), 1)
        self.assertTrue(cache.writable)

        cache.update({'b': 'c', 'c': 'd'})
        self.assertEqual(len(cache), 3)
        self.assertTrue(cache.writable)

        self.assertFalse(cache.stop_write())

        cache.update({'d': 'e', 'e': 2})
        self.assertEqual(len(cache), TEST_WORDS_CACHE_SIZE)
        self.assertTrue(cache.writable)

        cache.update({2: 'e', 5: 2})
        self.assertEqual(len(cache), TEST_WORDS_CACHE_SIZE + 2)
        self.assertTrue(cache.writable)
        self.assertTrue(cache.stop_write())

        cache.update({'3': 1e4, 6: .2})
        self.assertEqual(len(cache), TEST_WORDS_CACHE_SIZE + 2)
        self.assertFalse(cache.writable)
        self.assertFalse(cache.stop_write())

        cache['last'] = 'end'
        self.assertEqual(len(cache), TEST_WORDS_CACHE_SIZE + 2)
        self.assertFalse(cache.writable)
        self.assertFalse(cache.stop_write())
