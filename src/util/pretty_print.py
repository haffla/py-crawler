from src.util.textwrangler import TextWrangler


class Printer():

    @staticmethod
    def print_scoring(scores):
        print("\n----- Scoring ----\n")
        for score in scores:
            print(score[0])
            Printer.pretty_print_dict(score[1])
            print()

    @staticmethod
    def pretty_print_dict(dicto):
        # TODO Output nach Values sortieren
        for key in sorted(dicto):
            print("%s: %s" % (key, dicto[key]))

    @staticmethod
    def print_link_structure(links_dictionary):
        print("\n----- Link Structure ----\n")
        for url in sorted(links_dictionary):
            links = [TextWrangler.get_last_part_of_url(u) for u in links_dictionary[url]]
            link_string = ""
            for link in links:
                link_string += link
                if link != links[-1]:
                    link_string += ","
            print(TextWrangler.get_last_part_of_url(url) + ":" + link_string)

    @staticmethod
    def print_words(dictionary):
        print("\n----- Index ----\n")
        for key in sorted(dictionary):
            print("(" + key + ", df:" + str(len(dictionary[key])) + ")", "->", dictionary[key])

    @staticmethod
    def print_doclengths(dictionary):
        print("\n----- Document Lengths ----\n")
        for key in sorted(dictionary):
            print(key + ": " + str(dictionary[key]))

    @staticmethod
    def print_pageranks(dictionary):
        print("\n----- Page Rank ----\n")
        for key in sorted(dictionary):
            print(TextWrangler.get_last_part_of_url(key) + ": " + str(dictionary[key]))