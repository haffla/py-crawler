from src.util.textwrangler import TextWrangler


class Printer():

    @staticmethod
    def print_scoring(scores):
        print("\n----- Scoring ----\n")
        for score in scores:
            print(score[0])
            Printer.print_sorted_by_values(score[1])
            print()

    @staticmethod
    def print_sorted_by_values(d):
        genexp = ((k, d[k]) for k in sorted(d, key=d.get, reverse=True))
        for k, v in genexp:
            print(k + ": ", v)

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
        Printer.print_sorted_by_values(dictionary)

    @staticmethod
    def print_pageranks(dictionary):
        print("\n----- Page Rank ----\n")
        for key in sorted(dictionary):
            print(key + ": " + str(dictionary[key]))