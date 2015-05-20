import math
from src.util.textwrangler import TextWrangler

class Scoring():

    queries = ['tokens', 'index', 'classification']
    weight_matrix = {}
    doc_lengths = {}

    def __init__(self, words_dictionary, url_list):
        self.do_weight_matrx(words_dictionary, url_list)

    def do_weight_matrx(self, words_dictionary, url_list):
        # go throug all words in the documents
        for word in words_dictionary.keys():
            # set the length of all documents because we need it later to calculate the tf_idf
            doc_freq = len(words_dictionary[word])
            # go through all docs
            for url in url_list:
                docname_last_part = TextWrangler.get_last_part_of_url(url)
                tuples = words_dictionary[word]
                result = 0
                # Then go through all the tuples to check the term frequency of each word in this doc (url)
                for tuple in tuples:
                    # ONLY ff the word is on in this doc (url) then calculate tf_idf
                    if tuple[0] == docname_last_part:
                        result = self.calculate_tf_idf(tuple[1], doc_freq, len(url_list))
                # We add the result to the weight matrix and now every document is now represented as a real-valued vector of tf-idf weights
                if url in self.weight_matrix:
                    self.weight_matrix[url].append((word, result))
                else:
                    self.weight_matrix[url] = [(word, result)]
            self.set_doc_lengths()

    def set_doc_lengths(self):
        # we take each document and calculate the doc length
        for doc in self.weight_matrix:
            result = 0
            for tuple in self.weight_matrix[doc]:
                # For each word (on this doc which we're iterating) we take the term frequency and we square it ..
                # .. doing this, we are able to calculate the doc length because the terms are our axes and the docs are our vectors
                result += tuple[1]*tuple[1]
            # Like this, we succeeded to calculate the doc length of every given url by calculating the scalar product of the vectors
            self.doc_lengths[doc] = round (math.sqrt(result), 6 )

    def calculate_tf_idf(self, tf, df, N):
        result = round( (1 + math.log10(float(tf))) * math.log10(float(N/df)), 6 )
        return result

    # Aufgabe:
    # http://people.f4.htw-berlin.de/fileadmin/user_upload/Dozenten/WI-Dozenten/Classen/DAWeb/daw-sm-python.pdf


    # TODO
        #0  tf-idf = (1 + log tf) * log(N/df)
        #1  float Scores[N] = 0
        #2  float Length[N]
        #3  for each query term t
        #4  do calculate wt,q and fetch postings list for t
        #5  for each pair(d,tft,d ) in postings list
        #6  do Scores[d]+ = wt,d × wt,q
        #7  Read the array Length
        #8  for each d
        #9  do Scores[d] = Scores[d]/Length[d]
        #10 return Top K components of Scores[]