import math
from src.util.textwrangler import TextWrangler


class Scoring():

    weight_matrix = {}
    doc_lengths = {}
    queries = ['tokens', 'index', 'classification', 'tokens classification']
    scores = []

    def __init__(self, words_dictionary, url_list):
        self.do_weight_matrix(words_dictionary, url_list)
        self.calculate_scoring_for_query(words_dictionary, url_list, self.queries)

    def do_weight_matrix(self, words_dictionary, url_list):
        len_url_list = len(url_list)
        # go through all words in the documents
        for word in words_dictionary.keys():
            # set the length of all documents because we need it later to calculate the tf_idf
            doc_freq = len(words_dictionary[word])
            # go through all docs
            for url in url_list:
                docname_last_part = TextWrangler.get_last_part_of_url(url)
                tuples = words_dictionary[word]
                result = 0
                # Then go through all the tuples to check the term frequency of each word in this doc (url)
                for dtf_tuple in tuples:
                    # ONLY if the word is on in this doc (url) then calculate tf_idf
                    if dtf_tuple[0] == docname_last_part:
                        result = self.calculate_tf_idf(dtf_tuple[1], doc_freq, len_url_list)
                # We add the result to the weight matrix and each document is now represented as a real-valued vector of tf-idf weights
                if docname_last_part in self.weight_matrix:
                    self.weight_matrix[docname_last_part].append((word, result))
                else:
                    self.weight_matrix[docname_last_part] = [(word, result)]
            self.set_doc_lengths()

    def set_doc_lengths(self):
        # we take each document and calculate the doc length
        for doc in self.weight_matrix:
            result = 0
            for dtf_tuple in self.weight_matrix[doc]:
                # For each word (on this doc which we're iterating) we take the term frequency and we square it ..
                # .. doing this, we are able to calculate the doc length because the terms are our axes and the docs are our vectors
                result += dtf_tuple[1]*dtf_tuple[1]
            # Like this, we succeeded to calculate the doc length of every given url by calculating the scalar product of the vectors
            self.doc_lengths[doc] = round(math.sqrt(result), 6)

    @staticmethod
    def calculate_tf_idf(tf, df, n):
        result = round((1 + math.log10(float(tf))) * math.log10(float(n / df)), 6)
        return result

    # Aufgabe: http://people.f4.htw-berlin.de/fileadmin/user_upload/Dozenten/WI-Dozenten/Classen/DAWeb/daw-sm-python.pdf
    # TODO

    def calculate_scoring_for_query(self, words_dictionary, url_list, search_queries):
        scores = {}
        doc_ids = [TextWrangler.get_last_part_of_url(url) for url in url_list]
        for query in search_queries:
            for doc_id in doc_ids:
                scores[doc_id] = 0  # 1
            # for each query term t
            for t in query.split(' '):
                # fetch postings list for t
                posting_list_for_t = words_dictionary[t]
                for dtf_tuple in posting_list_for_t:
                    document = dtf_tuple[0]
                    tf = dtf_tuple[1]
                    df = len(posting_list_for_t)
                    # calculate wt,q
                    wtq = self.calculate_tf_idf(tf, df, len(url_list)) # ich glaube das ist eher wt,q
                    # wir brauchen hier irgendwie den "tf-idf weight of term i in the query."
                    wtd = self.get_wtd(self.weight_matrix[document], t)
                    print(wtd, wtq) # ist das gleiche was auch in der Matrix steht
                    # result = wtq x wtd
                    scores[document] += wtq #* wtd
            for d in self.doc_lengths:
                scores[d] /= self.doc_lengths[d]  # 9
            # filter out docs that have score == 0
            filtered_scores = {k: v for k, v in scores.items() if v > 0}
            self.scores.append((query.split(' '), filtered_scores))

    def get_wtd(self, doc, t):
        for d in doc:
            if d[0] == t:
                return d[1]

        # #1  float Scores[N] = 0
        # #2  float Length[N]
        # #3  for each query term t (done)
        # #4  do calculate wt,q and fetch postings list for t (done)
        # #5  for each pair(d,tft,d ) in postings list
        # #6  do Scores[d]+ = wt,d × wt,q
        # #7  Read the array Length
        # #8  for each d
        # #9  do Scores[d] = Scores[d]/Length[d]
        # #10 return Top K components of Scores[]