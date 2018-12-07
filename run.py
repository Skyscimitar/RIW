# bin/python3
import sys
import getopt
from cacm_part1.DocumentParser import DocumentParser


def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "h f", ["help", "file"])
    except getopt.GetoptError:
        print("For help, type: --help")
        sys.exit(2)
    
    HELP = """
        This program tokenizes an input file respecting the following
        format:
            - .I : document's id
            - .T : indicates start of document's title
            - .W : indicates start of document's summary
            - .K : indicates the start of the document's keywords

        options:
            -h --help : shows this help message
            -f --file : the path to the input file
    """

    for o, a in opts:
        if o in ("-h", "--help"):
            print(HELP)
            sys.exit(0)
        if o in ("-f", "--file"):
            i = opts[0].index(o)
            if (len(args) == 0):
                print("Please enter a filename")
                sys.exit(1)
            filename = args[i]
            doc_list = DocumentParser.parse_entry_file(filename)
            tokens = DocumentParser.tokenize(doc_list)
            print(tokens)
            sys.exit(0)
        print("Please enter a file name -f or --file")
        sys.exit(2)
        

if __name__ == '__main__':
    sys.exit(main())