import math
from src.util.textwrangler import TextWrangler


class Scoring():

    weight_matrix = {}
    doc_lengths = {}
    queries = ['tokens', 'index', 'classification', 'tokens classification']
    scores = []

    def __init__(self, crawler):
        self.do_weight_matrix(crawler.words_dictionary, crawler.url_list)
        self.calculate_scoring_for_query(crawler, self.queries)

    def do_weight_matrix(self, words_dictionary, url_list):
        len_url_list = len(url_list)
        # go through all words in the documents
        for word in words_dictionary:
            # save the document frequency of this word
            # because we need it later to calculate the tf_idf
            doc_freq = len(words_dictionary[word])
            # go through all docs
            for url in url_list:
                doc = TextWrangler.get_last_part_of_url(url)
                tuples = [(d, f) for (d, f) in words_dictionary[word] if d == doc]
                # it's either length 0 or 1
                if len(tuples) > 0:
                    result = self.calculate_tf_idf(tuples[0][1], doc_freq, len_url_list)
                    if doc in self.weight_matrix:
                        self.weight_matrix[doc].append((word, result))
                    else:
                        self.weight_matrix[doc] = [(word, result)]
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

    def calculate_scoring_for_query(self, crawler, search_queries):
        scores = {}
        doc_ids = [TextWrangler.get_last_part_of_url(url) for url in crawler.url_list]
        for query in search_queries:
            for doc_id in doc_ids:
                scores[doc_id] = 0  # 1
            # for each query term t
            query_terms = query.split(' ')
            length_query = 0
            for t in query_terms:
                # fetch postings list for t
                posting_list_for_t = crawler.words_dictionary[t]
                tf = query.count(t)
                df = len(posting_list_for_t)
                wtq = self.calculate_tf_idf(tf, df, len(crawler.url_list))
                length_query += wtq*wtq
                for dtf_tuple in posting_list_for_t:
                    document = dtf_tuple[0]
                    wtd = self.get_wtd(document, t)
                    result = wtd * wtq
                    scores[document] += result
            for d in self.doc_lengths:
                scores[d] /= (self.doc_lengths[d] * math.sqrt(length_query))
            # filter out docs that have score == 0
            filtered_scores = {k: v for k, v in scores.items() if v > 0}
            self.scores.append((query_terms, filtered_scores))

    # gets idf for term from weight matrix
    def get_wtd(self, doc, term):
        return next(v for (t, v) in self.weight_matrix[doc] if t == term)
