from collections import Counter
import numpy as np

glove = None


class Glove(object):

    def __init__(self, path='./data/glove.6B.50d.txt'):
        self.path = path
        self.embedding = None
        pos = path.find('glove.6B.') + len('glove.6B.')
        self.dim = int(path[pos:(pos + 2)])
        self.cache = dict()

    def get_vector(self, word):
        if not self.embedding:
            self.__load_embedding()
        if word in self.cache:
            return self.cache[word]
        if word in self.embedding:
            self.cache[word] = self.embedding[word]
        else:
            self.cache[word] = None
        return self.cache[word]

    def __load_embedding(self):
        # print('Load glove embedding...')
        self.embedding = Counter()
        for line in open(self.path, encoding='utf-8'):
            line = line.strip().split()
            if len(line) == 0:
                continue
            word = line[0]
            vector = list(map(float, line[1:]))
            assert (len(vector) == self.dim)
            self.embedding[word] = np.asarray(vector)


def get_word_embedding(word):
    global glove
    if not glove:
        glove = Glove()
    word = word.lower()
    return glove.get_vector(word)
