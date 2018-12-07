# bin/python3

from cacm_part1.DocumentParser import DocumentParser

if __name__ == '__main__':
    doc_list = DocumentParser.parse_entry_file("cacm/cacm.all")
    tokens = DocumentParser.tokenize(doc_list)
    print(tokens)
