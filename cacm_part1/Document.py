# class to represent cacm.all documents
import nltk


class Document:


    def __init__(self, id, title, summary=None, keywords=None):
        self.id = id
        self.title = title
        self.summary = summary if summary is not None else ""
        self.keywords = keywords if keywords is not None else ""


    def tokenize(self):
        tokens = []
        tokens += nltk.word_tokenize(self.title)
        tokens += nltk.word_tokenize(self.summary)
        tokens += nltk.word_tokenize(self.keywords)
        return tokens
    

    def __str__(self):
        return ("Title: {}, Summary: {}, Keywords: {}".format(self.title, self.summary, self.keywords))