# bin/python3

import sys
import getopt
import gc
import numpy as np
import matplotlib.pyplot as plt
import math
from cacm_part1.DocumentParser import DocumentParser
from cacm_part1.InvertedIndex import InvertedIndex
from cacm_part2.BinarySearch import binarySearch
from cacm_part1.VectorialModel import VectorialModel
from time import time

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


"""
    Generate the tokens and vocab from the cacm document collection
    Prints the calculated coefficiens k, B for the document collection
    Plots the regression line for different vocabulary sizes
    Only prints if display is set to True
    returns: doc_list, tokens, vocab, tokens_lengths and vocab_lengths
"""
def preprocessing(filename, display=False):

    # Load the documents from the file
    doc_list = DocumentParser.parse_entry_file(filename)

    # generate tokens from documents
    tokens, token_counts = DocumentParser.tokenize(doc_list, "cacm/common_words")

    # generate vocabulary from tokens
    vocab, vocab_lengths = DocumentParser.calculate_vocabulary(tokens)

    for i in range(len(token_counts)):
        token_counts[i] = math.log10(token_counts[i])
    for i in range(len(vocab_lengths)):
        vocab_lengths[i] = math.log10(vocab_lengths[i])
    
    token_counts = np.asarray(token_counts)
    vocab_lengths = np.asarray(vocab_lengths)

    if display:
        coefs = estimate_coef(token_counts, vocab_lengths)
        print("Coefficients: " + str(coefs))
        k = 10**coefs[0]
        b = coefs[1]
        print("k= " + str(10**coefs[0]) + " b= " + str(coefs[1]))
        voc_million = k * (10**6)**b
        print("Vocabulaire 1million tokens: " + str(voc_million))
        plot_regression_line(token_counts, vocab_lengths, coefs)
    
    return doc_list, tokens, token_counts, vocab, vocab_lengths


"""
    Test the binarySearch method on the corpus
    Prints time and results for various searches
"""
def binary_search_test(tokens, doc_ids):

    # Genarte inverted index for the collection
    print("Generating inverted index")
    start_time = time()
    inverted_index = InvertedIndex.invert_index(tokens)
    end_time = time()
    print("Genartion finished, took: %.2f seconds" % (end_time - start_time))

    print("Binary search AND test starting")
    start_time = time()
    res = binarySearch("network AND computer", inverted_index, doc_ids)
    end_time = time()
    print("AND test finished, returned: {}, took: {} seconds".format(res, end_time-start_time))

    print("Binary search OR test starting")
    start_time = time()
    res = binarySearch("network OR computer", inverted_index, doc_ids)
    end_time = time()
    print("OR test finished, returned: {}, took: {} seconds".format(res[10], end_time-start_time))

    print("Binary search NOT test starting")
    start_time = time()
    res = binarySearch("NOT computer", inverted_index, doc_ids)
    end_time = time()
    print("NOT test finished, returned: {}, took: {} seconds".format(res[10], end_time-start_time))

    return True

"""
    Tests the vectorial search method using various ponderations
"""
def vectorial_search_test(doc_list, tokens):

    # Genarte inverted index for the collection
    print("Generating inverted index")
    start_time = time()
    inverted_index = InvertedIndex.invert_index(tokens)
    end_time = time()
    print("Genartion finished, took: %.2f seconds" % (end_time - start_time))

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

    docs = {}
    common_words = DocumentParser.read_common_words()
    for doc in doc_list:
        docs[doc.id] = len(DocumentParser.remove_common_words(doc.tokenize(), common_words))

    print("Genarting ponderated vectors")
    start_time = time()
    ponderated_vectors = VectorialModel.doc_vectors_ponderation(postings, cleaned_query, inverted_index, docs)
    end_time = time()
    print("Genartion finished, took %.2f seconds" % (end_time - start_time))

    print("Searching using cosine measurement")
    start_time = time()
    p_cosines = VectorialModel.cosinus(cleaned_query, ponderated_vectors)
    res = VectorialModel.search_result(p_cosines, postings)
    end_time = time()
    print("Search finished, took %.2f seconds" % (end_time - start_time))
    print("First ten results: {}".format(res[:10]))

    return True


def run_all(filename):
    doc_list, tokens, token_counts, vocab, vocab_lengths = preprocessing(filename, display=True)

    doc_ids = []
    for doc in doc_list:
        doc_ids.append(doc.id)

    binary_search_test(tokens, doc_ids)
    vectorial_search_test(doc_list, tokens)

    return True


if __name__ == "__main__":
    sys.exit(run_all("cacm/cacm.all"))