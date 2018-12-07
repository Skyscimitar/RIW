# bin/python3
import sys
import getopt
import gc
from cacm_part1.DocumentParser import DocumentParser


def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "h f", ["help", "file",])
    except getopt.GetoptError:
        print("For help, type: --help")
        sys.exit(2)
    
    HELP = """
        This program tokenizes an input file respecting the following
        format, then calculates it's vocabulary:
            - .I : document's id
            - .T : indicates start of document's title
            - .W : indicates start of document's summary
            - .K : indicates the start of the document's keywords

        options:
            -h --help : shows this help message
            -f --file : the path to the input file
    """

    filename = None
    for o, a in opts:
        if o in ("-h", "--help"):
            print(HELP)
            sys.exit(0)
        elif o in ("-f", "--file"):
            i = opts[0].index(o)
            if (len(args) < i):
                print("Please enter a filename")
                sys.exit(1)
            filename = args[i]
    if filename is None:
        print("Please provide a filename")
    doc_list = DocumentParser.parse_entry_file(filename)
    tokens = DocumentParser.tokenize(doc_list, "cacm/common_words")
    vocab = DocumentParser.calculate_vocabulary(tokens)
    print(vocab)
    tokens = None
    gc.collect()
    sys.exit(0)
        

if __name__ == '__main__':
    sys.exit(main())