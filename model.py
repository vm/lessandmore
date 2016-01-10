import os
import random

from gensim.models.word2vec import Word2Vec
import numpy as np
from pattern import en

def cossim(u, v):
    """calculates the cosine similarity of two vectors"""

    dot = np.dot(u, v)
    euclid = np.sum(u ** 2) * np.sum(v ** 2)
    return np.where(euclid == 0.0, 0, dot / euclid)

class Transformer(object):
    """class for transforming text to be less about some things and more about others"""

    def __init__(self, fn='models/GoogleNews-vectors-negative300.bin', threshold=0.4):
        """creates a Tranformer

        :param fn: location of the model to load
        :type fn: str
        """

        url = 'https://drive.google.com/file/d/0B7XkCwpI5KDYNlNUTTlSS21pQmM'
        download_msg = 'Download the Google News model here: ' + url

        if not os.path.isfile(fn):
            raise ValueError('File {} not found!\n'.format(fn) + download_msg)

        self.model = Word2Vec.load_word2vec_format(fn, binary=True)
        self.threshold = threshold

        # dumb caching
        self._last_less = None
        self._last_more = None

    def transform(self, text, less, more):
        """transforms a body of text to have less of less and more of more!

        :param text: text to transform
        :type text: str

        :param less: list of 'less' words
        :type less: list

        :param more: list of 'more' words
        :type more: list

        :returns: transformed text
        :rtype: str
        """

        last_was_article = False
        new_text = []

        less = [l for l in less if not self._ignore(l, en.tag(l)[0][1])]
        more = [m for m in more if not self._ignore(m, en.tag(m)[0][1])]

        # iterate over words
        for word, pos in en.tag(text):

            if word not in self.model or self._ignore(word, pos):
                if self._is_punc(pos):
                    new_text.append(u'\b' + word)
                else:
                    new_text.append(word)
            else:
                new_word = self._transform_word(word, pos, less, more)

                # handle 'a' v. 'an'
                if new_text and new_text[-1] in ['a', 'an']:
                    new_text[-1] = 'an' if new_word[0] in 'aeiou' else 'a'

                new_text.append(new_word)

        ret = ''

        # remove at backspaces - this is dumb
        for t in new_text:
            if t.startswith('\b'):
                ret += t[1:]
            else:
                ret += ((' ' + t) if ret != '' else t)

        return ret

    def _transform_word(self, word, pos, less, more):
        """transforms a word to be less less and more more

        :param word: word to transform
        :type word: str

        :param pos: part of speech of the word
        :type pos: str

        :param less: list of 'less' words
        :type less: list

        :param more: list of 'more' words
        :type more: list

        :returns: transformed word
        :rtype: str
        """

        new_word = self._get_similar_word(word, less, more)
        new_pos = en.tag(new_word)[0][1]

        if (pos[:2] != new_pos[:2]) or word == new_word:
            return word

        # handle noun
        if pos.startswith('NN'):

            # pluralization
            if pos.endswith('S') and not new_pos.endswith('S'):
                new_word = en.pluralize(new_word)

            elif not pos.endswith('S') and new_pos.endswith('S'):
                new_word = en.singularize(new_word)

            # capitalization
            if word[0].isupper():
                new_word = new_word[0].upper() + new_word[1:]
            else:
                new_word = new_word.lower()

        # handle verb
        elif pos.startswith('VB'):

            tense, person, number = en.tenses(word)[0][:3]

            # conjugation
            conjugated = en.conjugate(new_word,
                                    tense=tense,
                                    person=person,
                                    number=number,
                                    parse=False)

            if conjugated is not None:
                new_word = conjugated

        # remove underscores for joint words
        new_word = new_word.replace('_', ' ')

        return new_word

    def _get_less_more_diff(self, less, more):
        """gets the vector difference between less and more

        :param less: list of 'less' words
        :type less: list

        :param more: list of 'more' words
        :type more: list

        :returns: difference
        :rtype: numpy.ndarray
        """

        if not ((self._last_less and self._last_more) and
                (set(self._last_less) == set(less)) and
                (set(self._last_more) == set(more))):

            lmd = (np.sum(self.model[m] for m in more) -
                   np.sum(self.model[l] for l in less))

            self._last_less_more_diff = lmd

        return self._last_less_more_diff

    def _get_similar_word(self, word, less, more, topn=2):
        """gets a similar word to word thats less less and more more

        :param word: word
        :type word: str

        :param less: list of 'less' words
        :type less: list

        :param more: list of 'more' words
        :type more: list

        :returns: most similar word
        :rtype: str
        """

        less_more_diff = self._get_less_more_diff(less, more)

        similar_words = self.model.most_similar(positive=[word] + more,
                                                negative=less,
                                                topn=topn)

        similar_words = [w[0] for w in similar_words]

        # set probability based on the similarity between the
        # difference between more and less and the difference between
        # the new and old word
        probabs = np.zeros(topn+1)

        for i,w in enumerate(similar_words):
            # similarity to the analogy

            if w in less:
                probabs[i] = 0.0
            else:
                diff = self.model[w] - self.model[word]
                s = cossim(less_more_diff, diff)

                # similarity to the less
                s += np.sum(self.model.similarity(word, l) for l in less)

                probabs[i] = s

        # add word with probability at threshold
        similar_words += [word]
        probabs[-1] = self.threshold if word not in less else 0.0

        # normalize
        probabs -= probabs.min()
        probabs /= probabs.sum()

        return self._get_random_choice(similar_words, probabs)

    def _get_random_choice(self, values, probabs):
        """gets a random choice from values based on probabs

        :param values: values to chooce from
        :type values: list

        :param probabs: probabilities for each value
        :type probabs: list

        :returns: random value
        :rtype: type(values[0])
        """

        rand_value = random.random()

        total = 0
        for i,p in enumerate(probabs):
            total += p

            if rand_value < total:
                return values[i]

        return values[-1]

    def _ignore(self, word, pos):
        """determines whether a word should be ignored

        a word should be ignored if it is a(n):
            - preposition
            - article
            - punctuation
            - number
            - first/second person pronouns

        :param word: word
        :type word: str

        :param pos: part of speech of the word
        :type pos: str

        :returns: whether the word should be ignored
        :rtype: bool
        """

        ignore_pos = ['IN', 'DT', 'WR']

        return (any(pos.startswith(p) for p in ignore_pos) or
                self._is_number(word) or
                self._is_punc(pos))

    def _is_punc(self, pos):
        """determines whether a part of speech is punctuation"""

        puncs = ['.', ',', '"', ":"]

        return pos in puncs

    def _is_number(self, word):
        """determines whether a word is a number"""

        try:
            float(word)
            return True
        except ValueError:
            return False
