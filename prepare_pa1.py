import os
from tqdm import tqdm
import simplejson
from nltk.tokenize import RegexpTokenizer
import sys
import json

class pa1Document(object):

    pattern = r'\w+'

    def __init__(self, title=None, id=None, content=None):
        self.title = title
        self.id = id
        self.content = content

    def tokenize(self):
        tokenizer = RegexpTokenizer(self.pattern)
        self.content = tokenizer.tokenize(self.content)
    

    def __json__(self):
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content
        }

    for_json = __json__

    @classmethod
    def from_json(cls, json):
        obj = cls()
        obj.id = json['id']
        obj.title = json['title']
        obj.content = json['content']


# generate paths for all files
def generate_paths():
    paths = []
    for sub_dir in os.listdir("pa1-data"):
        folder = os.path.join("pa1-data", sub_dir )
        files = [os.path.join(folder, f ) for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]
        paths += files
    return paths

# parse files into documents
def load_files(paths):
    documents = {}
    id = 0
    for path in tqdm(paths):
        tokens = ""
        with open(path, 'r') as f:
            for line in f:
                line = line.strip().lower()
                tokens += line + ' '
        documents[str(id)] = pa1Document(path, str(id), tokens)
        documents[str(id)].tokenize()
        id += 1

    # serialize parsed documents
    with open('documents_dict.txt', 'w') as outfile:
        simplejson.dump(documents, outfile, for_json=True)
    
    return documents

# inverted index function for pa1 collection
def inverted_index(documents):
    inv_index = {}
    for doc_id in tqdm(list(documents.keys())):
        document = documents[doc_id]
        for token in document.content:
            if token not in inv_index:
                inv_index[token] = {doc_id: 1}
            else:
                if doc_id not in inv_index[token]:
                    inv_index[token][doc_id] = 1
                else:
                    inv_index[token][doc_id] += 1
    return inv_index

def generate_inverted_index(documents):
    print("Creating inverted index")
    inv_index = inverted_index(documents)

    # serialize inverted_index
    with open('pa1-inv-index.txt', 'w') as outfile:
        json.dump(inv_index, outfile)
    return inv_index

if __name__ == "__main__":
    print("Beginning preparation")
    paths = generate_paths()
    documents = load_files(paths)
    inverted_index = generate_inverted_index(documents)
    print("Preparation finished")
    sys.exit(0)