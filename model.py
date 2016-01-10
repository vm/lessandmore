import os

from gensim.models.word2vec import Word2Vec

class Transformer(object):
    """class to transform text to be less and more about different things"""

    def __init__(self, fn='models/GoogleNews-vectors-negative300.bin'):
        """creates a Tranformer

        :param fn: location of the model to load
        :type fn: str
        """

        url = 'https://drive.google.com/file/d/0B7XkCwpI5KDYNlNUTTlSS21pQmM'
        download_msg = 'Download the Google News model here: ' + url

        if not os.path.isfile(fn):
            raise ValueError('File {} not found!\n'.format(fn) + download_msg)

        self.model = Word2Vec.load_word2vec_format(fn, binary=True)

    def transform(self, text, less, more):
        """transforms text to have less of less and more of more!

        :param text: text to transform
        :type text: str

        :param less: list of 'less' words
        :type less: list

        :param more: list of 'more' words
        :type more: list

        :returns: transformed text
        :rtype: str
        """

        output = []
        less = [l for l in less if self.is_interesting(l)]
        more = [m for m in more if self.is_interesting(m)]

        for word in text.split():
            if self.is_interesting(word):
                new_word = self.model.most_similar(positive=[word] + more,
                                                   negative=less)[0][0]
                output.append(new_word)
            else:
                output.append(word)

        return ' '.join(output)

    def is_interesting(self, word):
        """determines whether a word is interesting

        a word is iteresting if it:
        - is a noun
        - is a verb
        - is an adjective
        - is an adverb

        :param word: word
        :type word: str

        :returns: whether the word is interesting
        :rtype: bool
        """

        return True
