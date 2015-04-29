import re


class TextWrangler(object):

    @staticmethod
    def tokenize(text):
        words = re.split('\W+', text)
        return [w.lower() for w in words]


    @staticmethod
    def build_dict(tokens, dictionary, i):
        for t in tokens:
            occurrences = tokens.count(t)
            if t not in dictionary:
                dictionary[t] = [(i, occurrences)]
            else:
                ids = [j[0] for j in dictionary[t]]
                if i not in ids:
                    dictionary[t].append((i, occurrences))