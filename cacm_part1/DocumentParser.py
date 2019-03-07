from .Document import Document

class DocumentParser:

    @staticmethod
    def parse_entry_file(filename):
        """This function parses the entry file considering the different tokens."""

        try:
            with open(filename, 'r' ) as f:
                current_token = ''
                creating_document = False
                doc_list = []
                doc_id = None
                title = ""
                summary = ""
                keywords = ""
                authors = ""
                for line in f:
                    # read the tokens to identify the next action to perform
                    if line[:2] == '.I':
                        if creating_document:
                            title = title.strip()
                            summary = summary.strip()
                            keywords = keywords.strip()
                            authors = authors.strip()
                            doc = Document(doc_id, authors, title, summary, keywords)
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
                    elif line[:2] == '.A':
                        current_token = '.A'
                    elif line[0] == '.':
                        current_token = ""
                    else:
                        if current_token == '.T':
                            title += ' ' + line.strip()
                        elif current_token == '.W':
                            summary += ' ' + line.strip()
                        elif current_token == '.K':
                            keywords = ' ' + line.strip()
                        elif current_token == '.A':
                            authors += line.strip().split(',')[0]
            return doc_list

        except IOError:
            print("File not found, please enter a valid filename")


    @staticmethod
    def tokenize(doc_list, common_words=None):
        """This function establishes the list of tokens for the vocabulary."""

        tokens = {}
        token_counts = []
        if common_words is not None:
            common_words = DocumentParser.read_common_words(common_words)
            for doc in doc_list:
                tokens[doc.id] =  DocumentParser.remove_common_words(doc.tokenize(), common_words)
                if len(token_counts) > 1:
                    token_counts.append(token_counts[-1] + len(tokens[doc.id]))
                else:
                    token_counts.append(len(tokens[doc.id]))
        else:
            for doc in doc_list:
                tokens[doc.id] = doc.tokenize()
                if len(token_counts)>1:
                    token_counts.append(token_counts[-1] + len(tokens[doc.id]))
                else:
                    token_counts.append(len(tokens[doc.id]))
        return tokens , token_counts


    @staticmethod
    def read_common_words(filename = "cacm/common_words"):
        """This function lists all the common words to be removed from the dictionnary."""

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
        """This function removes the common words from the dictionnary."""

        output = []
        for word in tokens:
            if word.lower() not in common_words:
                output.append(word)
        return output

    
    @staticmethod
    def calculate_vocabulary(tokens):
        """This function creates a vocabulary from the dictionnary.
        :return: vocab, a dictionnary of distinct words
        :return: vocab_lengths, the number of occurence of each word in vocab
        """

        vocab = {}
        vocab_lengths = []
        for key in tokens.keys():
            for word in tokens[key]:
                if word not in vocab.keys():
                    vocab[word] = 1
                else:
                    vocab[word] +=1
            vocab_lengths.append(len(vocab.keys()))
        return vocab , vocab_lengths