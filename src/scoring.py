import math
from src.util.textwrangler import TextWrangler

class Scoring():

    queries = ['tokens', 'index', 'classification']
    weight_matrix = {}
    doc_lengths = {}

    def __init__(self, words_dictionary, url_list):
        for word in words_dictionary.keys():
            doc_freq = len(words_dictionary[word])
            for url in url_list:
                docname_last_part = TextWrangler.get_last_part_of_url(url)
                tuples = words_dictionary[word]
                result = 0
                for tuple in tuples:
                    if tuple[0] == docname_last_part:
                        result = self.calculate_tf_idf(tuple[1], doc_freq, len(url_list))
                if url in self.weight_matrix:
                    self.weight_matrix[url].append((word, result))
                else:
                    self.weight_matrix[url] = [(word, result)]

        self.set_doc_lengths()

    def set_doc_lengths(self):
        for doc in self.weight_matrix:
            result = 0
            for tuple in self.weight_matrix[doc]:
                result += tuple[1]*tuple[1]
            self.doc_lengths[doc] = math.sqrt(result)

    def calculate_tf_idf(self, tf, df, N):
        result = round( (1 + math.log10(float(tf))) * math.log10(float(N/df)), 6 )
        return result

    # Was ist das ? http://people.f4.htw-berlin.de/fileadmin/user_upload/Dozenten/WI-Dozenten/Classen/DAWeb/doc_lengthes.txt
    #Ihn fragen, was genau ausgeben werden muss

    # Aufgabe:
    # http://people.f4.htw-berlin.de/fileadmin/user_upload/Dozenten/WI-Dozenten/Classen/DAWeb/daw-sm-python.pdf


    # TODO Was wir brauchen:
        # tf-idf = (1 + log tf) * log(N/df)
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