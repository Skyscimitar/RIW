from cacm_part1.VectorialModel import VectorialModel
from prepare_pa1 import pa1Document
import json
from time import time
import sys
from math import log
import math
import matplotlib.pyplot as plt
import numpy as np
from copy import deepcopy


# assistant functions for plotting
def estimate_coef(x, y): 
    # number of observations/points 
    n = np.size(x) 
  
    # mean of x and y vector 
    m_x, m_y = np.mean(x), np.mean(y) 
  
    # calculating cross-deviation and deviation about x 
    SS_xy = np.sum(y*x) - n*m_y*m_x 
    SS_xx = np.sum(x*x) - n*m_x*m_x 
  
    # calculating regression coefficients 
    b_1 = SS_xy / SS_xx 
    b_0 = m_y - b_1*m_x 
  
    return(b_0, b_1) 


def plot_regression_line(x, y, b): 
    # plotting the actual points as scatter plot 
    plt.scatter(x, y, color = "m", 
               marker = "o", s = 30) 
  
    # predicted response vector 
    y_pred = b[0] + b[1]*x 
  
    # plotting the regression line 
    plt.plot(x, y_pred, color = "g") 
  
    # putting labels 
    plt.xlabel('x') 
    plt.ylabel('y') 
  
    # function to show plot 
    plt.show()


# load inverted index:
def load_index():
    with open("pa1-inv-index.txt", 'r') as f:
        inverted_index = json.load(f)
    return inverted_index


# load documents:
def load_documents():
    with open("documents_dict.txt", 'r') as f:
        documents = json.load(f)
    parsed_documents = {}
    for doc_id in documents.keys():
        document = documents[doc_id]
        new_doc =  pa1Document(title=document['title'], id=doc_id, content=document['content'])
        parsed_documents[doc_id] = new_doc
    return parsed_documents



def calculate_term_frequencies(inverted_index):
    frequencies = []
    for token in inverted_index.keys():
        count = 0
        for doc_id in inverted_index[token].keys():
            count += inverted_index[token][doc_id]
        frequencies.append(count)
    frequencies.sort()
    return frequencies


# calculate total number of tokens and vocabulary size for the collection
def tokens_and_vocab(parsed_documents):
    tokens = []
    half_tokens = []
    keys = list(parsed_documents.keys())
    halfway = False
    for i in range(len(keys)):
        doc_id = keys[i]
        tokens += parsed_documents[doc_id].content
        if not halfway:
            if i > len(keys)/2:
                half_tokens = deepcopy(tokens)
                halfway = True
    vocab = set(tokens)
    half_vocab = set(half_tokens)
    return tokens, vocab, half_tokens, half_vocab

# test vectorial search method
def test_vec_search(inverted_index, parsed_documents):

    cleaned_query = VectorialModel.parse_query("computer science applied to networks")
    postings = VectorialModel.posting_union(cleaned_query, inverted_index)
    print("Genarting document vectors")
    start_time = time()
    vectors = VectorialModel.doc_vectors(postings, cleaned_query, inverted_index)
    end_time = time()
    print("Generation finished, took %.2f seconds" % (end_time - start_time))

    print("Searching using cosine measurement")
    start_time = time()
    cleaned_query = VectorialModel.generate_query_vector(cleaned_query, inverted_index, len(parsed_documents.keys()))
    cosines = VectorialModel.cosinus(cleaned_query, vectors)
    res = VectorialModel.search_result(cosines, postings)
    end_time = time()
    print("Search finished, took %.2f seconds" % (end_time - start_time))
    print("First ten results: {}".format(res[:10]))
    res_docs = []
    for doc_id in res[:10]:
        doc = parsed_documents[str(doc_id)].title
        res_docs.append(doc)
    print("First ten titles", res_docs)


if __name__ == "__main__":
    args = sys.argv
    
    # return information on search tests for the collection
    if len(args) > 1 :
        if args[1]== 'test_search':
            inverted_index = load_index()
            parsed_documents = load_documents()
            test_vec_search(inverted_index, parsed_documents)
    
        # return details about the collection
        elif args[1] == "collection_details":
            parsed_documents = load_documents()
            tokens, vocab, htokens, hvocab = tokens_and_vocab(parsed_documents)
            print("Tokens : %i, vocab length: %i" % (len(tokens), len(vocab)))
            print("Half toknes: %i, half vocab length: %i" % (len(htokens), len(hvocab)))
            b = log(float(len(vocab)/len(hvocab)))/log(len(tokens)/len(htokens))
            k = len(vocab)/pow(len(tokens), b)
            print("k: %.2f, b: %.2f" % (k, b))
            voc_million = voc_million = k * (10**6)**b
            print("Vocabulary for 1 million tokens: %.2f" % voc_million)
            inverted_index = load_index()
            frequencies = calculate_term_frequencies(inverted_index)
            frequencies = frequencies[::-1]
            log_freqs = [log(freq) for freq in frequencies]
            ranks = [i for i in range(1, len(frequencies) + 1)]
            log_ranks = [log(rank) for rank in ranks]
            plt.plot(ranks[:200], frequencies[:200])
            plt.show()
            plt.plot(log_ranks[:200], log_freqs[:200])
            plt.show()
            
        
        # return help
        else:
            print(
                """
                Run tests on the pa1 cs276 collection:
                    - test_search: returns results for the vectorial
                        search method
                    - collection_details: returns details about the
                        collection
                """
            )   
    # return help
    else:
        print(
            """
            Run tests on the pa1 cs276 collection:
                - test_search: returns results for the vectorial
                    search method
                - collection_details: returns details about the
                    collection
            """
        )

