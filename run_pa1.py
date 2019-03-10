from cacm_part1.VectorialModel import VectorialModel
from tqdm import tqdm
import json
from time import time

# load inverted index:

with open("pa1-inv-index.txt", 'r') as f:
    inverted_index = json.load(f)

# load documents:
with open("documents_dict.txt", 'r') as f:
    documents = json.load(f)

cleaned_query = VectorialModel.parse_query("computer science applied to networks")
postings = VectorialModel.posting_union(cleaned_query, inverted_index)
print("Genarting document vectors")
start_time = time()
vectors = VectorialModel.doc_vectors(postings, cleaned_query, inverted_index)
end_time = time()
print("Generation finished, took %.2f seconds" % (end_time - start_time))

print("Searching using cosine measurement")
start_time = time()
cosines = VectorialModel.cosinus(cleaned_query, vectors)
res = VectorialModel.search_result(cosines, postings)
end_time = time()
print("Search finished, took %.2f seconds" % (end_time - start_time))
print("First ten results: {}".format(res[:10]))
res_docs = []
for doc_id in res[:10]:
    doc = documents[str(doc_id)]["title"]
    print(doc)
    res_docs.append(doc)
print("First ten titles", res_docs)