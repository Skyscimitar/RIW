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
from test_queries_parser import parse_qrels, parse_query_text
from tqdm import tqdm

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
    print("Tokens size: %i" % token_counts[-1])

    # generate vocabulary from tokens
    vocab, vocab_lengths = DocumentParser.calculate_vocabulary(tokens)
    print("Vocabulary size: %i" % vocab_lengths[-1])

    for i in range(len(token_counts)):
        token_counts[i] = math.log10(token_counts[i])
    for i in range(len(vocab_lengths)):
        vocab_lengths[i] = math.log10(vocab_lengths[i])
    
    token_counts = np.asarray(token_counts)
    vocab_lengths = np.asarray(vocab_lengths)

    token_counts_half = token_counts[int(len(token_counts)/2)]
    vocab_length_half = vocab_lengths[int(len(token_counts)/2)]

    b = math.log(float(vocab_lengths[-1]/vocab_length_half))/math.log(token_counts[-1]/token_counts_half)
    k = vocab_lengths[-1] / token_counts[-1] ** b
    

    if display:
        print("k= " + str(k) + " b= " + str(b))
        voc_million = k * (10**6)**b
        print("Vocabulaire 1million tokens: " + str(voc_million))
        plot_regression_line(token_counts, vocab_lengths, (k,b))
    
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
    cleaned_query = VectorialModel.generate_query_vector(cleaned_query, inverted_index, len(doc_list))
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


def test_accuracy_recall(doc_list, tokens, return_doc_count):
    inverted_index = InvertedIndex.invert_index(tokens)
    test_queries = parse_query_text()
    test_rels = parse_qrels()
    accuracies = []
    recalls = []
    docs = {}
    common_words = DocumentParser.read_common_words()
    for doc in doc_list:
        docs[doc.id] = len(DocumentParser.remove_common_words(doc.tokenize(), common_words))
    for key in tqdm(list(test_rels.keys())):
        cleaned_query = VectorialModel.parse_query(test_queries[key])
        postings = VectorialModel.posting_union(cleaned_query, inverted_index)
        vectors = VectorialModel.doc_vectors_ponderation(postings, cleaned_query, inverted_index, docs)
        cleaned_query = VectorialModel.generate_query_vector(cleaned_query, inverted_index, len(doc_list))
        cosines = VectorialModel.cosinus(cleaned_query, vectors)
        res = VectorialModel.search_result(cosines, postings)
        res = res[:return_doc_count]
        related_docs = test_rels[key]
        tp = 0
        fn = 0
        for doc in res:
            if str(doc) in related_docs:
                tp+=1
            else:
                fn+=1
        accuracy = tp / len(res)
        recall = tp/(tp + fn)
        accuracies.append(accuracy)
        recalls.append(recall)
    accuracies = np.asarray(accuracies)
    recalls = np.asarray(recalls)
    mean_accuracy = np.mean(accuracies)
    min_accuracy = np.min(accuracies)
    max_accuracy = np.max(accuracies)
    print("Accuracy, recall tests for %i documents returned" % return_doc_count)
    print("Accuracy results: Mean %.2f, Max %.2f, Min %.2f" % (mean_accuracy, max_accuracy, min_accuracy))
    mean_recall = np.mean(recalls)
    min_recall = np.min(recalls)
    max_recall = np.max(recalls)
    print("Recall results: Mean %.2f, Max %.2f, Min %.2f" % (mean_recall, max_recall, min_recall))
    beta = mean_accuracy / mean_recall
    alpha = 1 / (beta**2 + 1)
    e_mesure = 1 - 1/(alpha/mean_accuracy + (1 - alpha)/mean_recall)
    f_mesure = 1 - e_mesure
    print("E-mesure: %.2f, F-Mesure: %.2f" % (e_mesure, f_mesure))



def accuracy_recall_graph(doc_list, tokens):
    inverted_index = InvertedIndex.invert_index(tokens)
    test_queries = parse_query_text()
    test_rels = parse_qrels()
    accuracies = []
    recalls = []
    keys = list(test_rels.keys())
    query = test_queries[keys[0]]
    rels = test_rels[keys[0]]
    cleaned_query = VectorialModel.parse_query(query)
    postings = VectorialModel.posting_union(cleaned_query, inverted_index)
    vectors = VectorialModel.doc_vectors(postings, cleaned_query, inverted_index)
    cleaned_query = VectorialModel.generate_query_vector(cleaned_query, inverted_index, len(doc_list))
    cosines = VectorialModel.cosinus(cleaned_query, vectors)
    res = VectorialModel.search_result(cosines, postings)
    for i in range(1, 51):
        temp_res = res[:i]
        tp = 0
        fn = 0
        for doc in temp_res:
            if str(doc) in rels:
                tp+=1
            else:
                fn+=1
        accuracy = tp / len(res)
        recall = tp/(tp + fn)
        accuracies.append(accuracy)
        recalls.append(recall)
    print(accuracies)
    print(recalls)
    x = np.linspace(1,50, 50)
    plt.plot(x, accuracies, color="r")
    plt.plot(x, recalls, color="b")
    plt.show()








def run_all(filename):
    doc_list, tokens, token_counts, vocab, vocab_lengths = preprocessing(filename, display=False)

    # doc_ids = []
    # for doc in doc_list:
    #     doc_ids.append(doc.id)

    # binary_search_test(tokens, doc_ids)
    # vectorial_search_test(doc_list, tokens)
    test_accuracy_recall(doc_list, tokens, 100)
    # accuracy_recall_graph(doc_list, tokens)

    return True


if __name__ == "__main__":
    sys.exit(run_all("cacm/cacm.all"))