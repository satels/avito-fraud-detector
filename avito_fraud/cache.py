from avito_fraud.conf import WORDS_CACHE_SIZE


class WordsCache(dict):

    def __init__(self, *args, **kwargs):
        super(WordsCache, self).__init__(*args, **kwargs)
        self.writable = True

    def stop_write(self):
        if self.writable and len(self) >= WORDS_CACHE_SIZE:
            self.writable = False
            return True
        return False

    def __setitem__(self, *args, **kwargs):
        if self.writable:
            super(WordsCache, self).__setitem__(*args, **kwargs)

    def update(self, *args, **kwargs):
        if self.writable:
            super(WordsCache, self).update(*args, **kwargs)
