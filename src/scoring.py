import math

class Scoring():

    queries = ['tokens', 'index', 'classification']

    def __init__(self, words_dictionary, length_of_document_list):
        for query in self.queries:
            for term in words_dictionary[query]:
                self.calculate_tf_idf(query, term[1], len(words_dictionary[query]), length_of_document_list)

    def calculate_tf_idf(self, query, tf, df, N):
        result = round( (1 + math.log10(float(tf))) * math.log10(float(N/df)), 6 )
        print(query, result)

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