from nltk.tokenize import RegexpTokenizer

class NewDocument(object):

    pattern = r"'?\w[\w']*(?:-\w+)?'?"
    
    def __init__(self, id, title, authors=None, summary=None,
        keywords=None, stopwords=None):
        self.id = id
        self.title = title
        self.authors= authors if authors is not None else ""
        self.summary = summary if summary is not None else ""
        self.keywords = keywords if keywords is not None else ""
        self.pre_tokens = self.tokenize()
        self.post_tokens = self.remove_stop_words(stopwords)

    
    def tokenize(self):
        tokenizer = RegexpTokenizer(self.pattern)
        tokens = []
        tokens += tokenizer.tokenize(self.title)
        tokens += tokenizer.tokenize(self.summary)
        tokens += tokenizer.tokenize(self.keywords)
        # tokens += tokenizer.tokenize(self.authors)
        for i, token in enumerate(tokens):
            tokens[i] = token.lower()
        return tokens

    
    def remove_stop_words(self, stopwords):
        return [_ for _ in self.pre_tokens if not _ in stopwords]