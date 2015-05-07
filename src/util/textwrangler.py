import re


class TextWrangler(object):

    @staticmethod
    def tokenize(text):
        words = re.split('\W+', text)
        return [w.lower() for w in words if w != ""]

    @staticmethod
    def build_dict(tokens, dictionary, stopwords, url):
        for t in tokens:
            if t not in stopwords:
                occurrences = tokens.count(t)
                site_id = TextWrangler.get_last_part_of_url(url)
                if t not in dictionary:
                    dictionary[t] = [(site_id, occurrences)]
                else:
                    ids = [j[0] for j in dictionary[t]]
                    if site_id not in ids:
                        dictionary[t].append((site_id, occurrences))

    @staticmethod
    def get_last_part_of_url(url):
        if url[-1] == '/':
            # remove trailing slash
            url = url[:-1]
        last_part = url.split("/")[-1]
        if last_part.find('.') != -1:
            last_part = last_part.split('.')[0]
        return last_part
