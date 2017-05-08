from avito_fraud.conf import TOP_WORDS
from avito_fraud.utils import timeit
import collections
import re


@timeit
def import_nltk():
    import nltk
    return nltk

nltk = import_nltk()


metrics = ["кв", "см", "мм", "м", "р", "кг", 'x', 'х', 'шт', 'рубл', 'руб', 'л', 'cm', 'ватт', 'kg', 'km', 'm', 'mm', 'г', 'мл', 'км']
cached_stopwords = frozenset(nltk.corpus.stopwords.words("russian") + metrics)

tokenizer = nltk.RegexpTokenizer(r'[а-яa-z]+', flags=re.I)

ru_stemmer = nltk.SnowballStemmer('russian')
en_stemmer = nltk.SnowballStemmer('english')

en_to_ru_table = dict(zip(
    map(ord, 'eyopakxcETOPAHKXCBM'),
    map(ord, 'еуоракхсЕТОРАНКХСВМ'),
))

ru_to_en_table = dict(zip(
    map(ord, 'укехаросКЕНХВАРОСМТ'),
    map(ord, 'ykexapocKEHXBAPOCMT'),
))

ru_pattern = re.compile(r'[а-я]', flags=re.I)
en_pattern = re.compile(r'[a-z]', flags=re.I)


def get_rank(text, cache):

    fraud_warn = False
    fraud_error = False

    word_counter = collections.Counter(tokenizer.tokenize(text))
    clean_words_counter = collections.Counter()

    for word in word_counter:

        clean_word_lower = cache.get(word)
        if clean_word_lower:
            clean_words_counter[clean_word_lower] += word_counter[word]
            continue

        if word.lower() in cached_stopwords:
            continue

        is_ru = ru_pattern.search(word)
        is_en = en_pattern.search(word)

        if is_ru and is_en:
            fraud_warn = True

            ru_word = word.translate(en_to_ru_table)
            en_word = word.translate(ru_to_en_table)

            if not en_pattern.search(ru_word):
                fraud_error = True
                clean_word = ru_stemmer.stem(ru_word)
            elif not ru_pattern.search(en_word):
                fraud_error = True
                clean_word = en_stemmer.stem(en_word)
            else:
                clean_word = word

        elif is_ru:
            clean_word = ru_stemmer.stem(word)
        elif is_en:
            clean_word = en_stemmer.stem(word)
        else:
            clean_word = word

        clean_word_lower = clean_word.lower()

        cache[word] = clean_word_lower

        clean_words_counter[clean_word_lower] += word_counter[word]

    if clean_words_counter:
        top_items = clean_words_counter.most_common(TOP_WORDS)
        rank = sum(item[1] for item in top_items) / sum(clean_words_counter.values())
    else:
        rank = None

    return rank, fraud_warn, fraud_error
