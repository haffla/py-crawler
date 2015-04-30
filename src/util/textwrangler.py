import re

class TextWrangler(object):

    @staticmethod
    def tokenize(text):
        words = re.split('\W+', text)
        return [w.lower() for w in words if w != ""]


    @staticmethod
    def build_dict(tokens, dictionary, stopwords, i):
        for t in tokens:
            if t not in stopwords:
                occurrences = tokens.count(t)
                if t not in dictionary:
                    dictionary[t] = [(i, occurrences)]
                else:
                    ids = [j[0] for j in dictionary[t]]
                    if i not in ids:
                        dictionary[t].append((i, occurrences))