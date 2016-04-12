import math
import csv
import json
from copy import deepcopy
from category_variables import manufacturer_categories, webstore_categories

class tfidf:

    def __init__(self):
        self.amazon_words = set()
        self.manufacturer_words = set()
        self.corpus = set()
        self.master_table = {'table':{}}
        self.words_table = {}
        self.word_doc_freq = {}
        self.tf_idf = {}

    def start(self):
        self.tokenize()
        self.make_words_dicts()
        self.make_master_table()
        self.compute_tfidf()
        self.print_tfidf()

    def _tokenize(self):
        self.make_corpus([manufacturer_categories, webstore_categories])

    def make_words_dicts(self):
        self.words_table = self.words()
        self.word_doc_freq = deepcopy(self.words_table)
        self.tf_idf = deepcopy(self.words_table)

    def make_master_table(self):
        table = self.master_table['table']
        for category in self.corpus:
            if not category in table.keys():
                table[category] = deepcopy(self.words_table)
                for word in self._wordizer(category):
                    if word in table[category].keys():
                        table[category][word] += 1
                    else:
                        table[category][word] = 1

    def compute_tfidf(self):
        self._compute_tf()
        self._compute_idf()

    def _compute_idf(self):
        """TODO: Separate out tf-idf from idf method."""
        table = self.master_table['table']
        num_documents = len(table.keys())
        for word in self.word_doc_freq.keys():
            for category in table.keys():
                if word in category:
                    self.word_doc_freq[word] += 1
        for category in table.keys():
            for word in table[category].keys():
                tf = table[category][word]
                frequency = float(self.word_doc_freq[word])
                idf = math.log(num_documents/(1 + frequency))
                tfidf_sum = tf * idf
                self.tf_idf[word] = tfidf_sum

    def _compute_tf(self, log_normalize=False, dbl_normalize=True ):
        table = self.master_table['table']
        for category in table.keys():
            max_raw_freq = float(max(table[category].values()))
            for word in table[category].keys():
                table = self.master_table['table']
                frequency = table[category][word]
                if log_normalize:
                    log_norm = math.log(1+frequency)
                    table[category][word] = log_norm
                elif dbl_normalize:
                    dbl_norm = 0.5 + (0.5*(frequency/(max_raw_freq)))
                    table[category][word] = dbl_norm
                else:
                    #norm is just term frequency, which is already computed
                    pass



    def words(self):
        return { wordj:0 for wordj in 
                set(wordi for document in self.corpus 
                for wordi in self._wordizer(document))
        }

    def make_corpus(self, documents):
        for document in documents:
            for category in document.keys():
                self.corpus.add(category)

    def _wordizer(self, text):
        return text.replace('>', ' ').
                    replace('(', '').
                    replace(')', '').
                    replace('/', ' ').
                    replace('|', ' ').
                    replace(' - ', ' ').
                    replace('&', '').
                    replace('  ', ' ').
                    split(' ')

    def print_tfidf(self):
        print self.tf_idf
        new_tfidf = {}
        for key, value in self.tf_idf.items():
            new_tfidf[key.lower()] = value
        with open('tfidf_words.json', 'w') as f:
            json.dump(
                new_tfidf, f, 
                sort_keys = True, indent = 4, ensure_ascii=False
            )



if __name__ == '__main__':
    tf_idf = tfidf() 
    tf_idf.start()