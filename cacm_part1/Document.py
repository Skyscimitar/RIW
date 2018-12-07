# class to represent cacm.all documents
from nltk.tokenize import RegexpTokenizer


class Document:

    # regex pattern to remove punctuation from tokens
    pattern = r'\w+'

    def __init__(self, id, title, summary=None, keywords=None):
        self.id = id
        self.title = title
        self.summary = summary if summary is not None else ""
        self.keywords = keywords if keywords is not None else ""


    def tokenize(self):
        # this tokenizer accepts a regex pattern as an input for a more accurat tokinisation
        tokenizer = RegexpTokenizer(self.pattern)
        tokens = []
        tokens += tokenizer.tokenize(self.title)
        tokens += tokenizer.tokenize(self.summary)
        tokens += tokenizer.tokenize(self.keywords)
        return tokens

    def __str__(self):
        return ("Title: {}, Summary: {}, Keywords: {}".format(self.title, self.summary, self.keywords))