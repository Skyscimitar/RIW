from .Document import Document

class DocumentParser:

    @staticmethod
    def parse_entry_file(filename):
        try:
            with open(filename, 'r' ) as f:
                current_token = ''
                creating_document = False
                doc_list = []
                doc_id = None
                title = ""
                summary = ""
                keywords = ""
                for line in f:
                    # read the tokens to identify the next action to perform
                    if line[:2] == '.I':
                        if creating_document:
                            doc = Document(doc_id, title, summary, keywords)
                            doc_list.append(doc)
                        title = ""
                        summary = ""
                        keywords = ""
                        doc_id = line[3:].strip('\n')
                        creating_document = True
                    elif line[:2] == '.T':
                        current_token = '.T'
                    elif line[:2] == '.W':
                        current_token = '.W'
                    elif line[:2] == '.K':
                        current_token = '.K'
                    elif line[0] == '.':
                        current_token = ""
                    else:
                        if current_token == '.T':
                            title += line
                        elif current_token == '.W':
                            summary += line
                        elif current_token == '.K':
                            keywords += line
            return doc_list

        except IOError:
            print("File not found, please enter a valid filename")


    @staticmethod
    def tokenize(doc_list, common_words=None):
        tokens = {}
        if common_words is not None:
            common_words = DocumentParser.read_common_words(common_words)
            for doc in doc_list:
                tokens[doc.id] =  DocumentParser.remove_common_words(doc.tokenize(), common_words)
        else:
            for doc in doc_list:
                tokens[doc.id] = doc.tokenize()
        return tokens


    @staticmethod
    def read_common_words(filename):
        common_words = []
        try:
            with open(filename, 'r') as f:
                for line in f:
                    common_words.append(line.strip('\n'))
        except IOError:
            print("Common words file not found")
        return common_words


    @staticmethod
    def remove_common_words(tokens, common_words):
        output = []
        for word in tokens:
            if word.lower() not in common_words:
                output.append(word)
        return output

    
    @staticmethod
    def calculate_vocabulary(tokens):
        vocab = {}
        for key in tokens.keys():
            for word in tokens[key]:
                if word not in vocab.keys():
                    vocab[word] = 1
                else:
                    vocab[word] +=1
        return vocab