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

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "h f", ["help", "file",])
    except getopt.GetoptError:
        print("For help, type: --help")
        sys.exit(2)
    
    HELP = """
        This program tokenizes an input file respecting the following
        format, then calculates it's vocabulary:
            - .I : document's id
            - .T : indicates start of document's title
            - .W : indicates start of document's summary
            - .K : indicates the start of the document's keywords

        options:
            -h --help : shows this help message
            -f --file : the path to the input file
    """

    filename = None
    for o, a in opts:
        if o in ("-h", "--help"):
            print(HELP)
            sys.exit(0)
        elif o in ("-f", "--file"):
            i = opts[0].index(o)
            if (len(args) < i):
                print("Please enter a filename")
                sys.exit(1)
            filename = args[i]
    if filename is None:
        print("Please provide a filename")
    doc_list = DocumentParser.parse_entry_file(filename)
    tokens, token_counts = DocumentParser.tokenize(doc_list, "cacm/common_words")
    vocab, vocab_lengths = DocumentParser.calculate_vocabulary(tokens)
    for i in range(len(token_counts)):
        token_counts[i] = math.log10(token_counts[i])
    for i in range(len(vocab_lengths)):
        vocab_lengths[i] = math.log10(vocab_lengths[i])
    token_counts = np.asarray(token_counts)
    vocab_lengths = np.asarray(vocab_lengths)
    # coefs = estimate_coef(token_counts, vocab_lengths)
    # print(coefs)
    # k = 10**coefs[0]
    # b = coefs[1]
    # print("k= " + str(10**coefs[0]) + " b= " + str(coefs[1]))
    # voc_million = k * (10**6)**b
    # print("Vocabulaire 1million tokens: " + str(voc_million))
    # plot_regression_line(token_counts, vocab_lengths, coefs)
    doc_ids = []
    for doc in doc_list:
        doc_ids.append(doc.id)
    
    inverted_index = InvertedIndex.invert_index(tokens)
    # res = binarySearch("network AND computer", inverted_index, doc_ids)
    # print(res)
    
    cleaned_q = VectorialModel.parse_query("computer science applied to networks")
    posting = VectorialModel.posting_union(cleaned_q, inverted_index)
    vectors = VectorialModel.doc_vectors(posting, cleaned_q, inverted_index)
    cosines = VectorialModel.cosinus(cleaned_q, vectors)
    vecmod_result = VectorialModel.search_result(cosines, posting)
    print(vecmod_result[:10])

    tokens = None
    token_counts = None
    vocab_lengths = None
    vocab = None
    gc.collect()
    sys.exit(0)
        

if __name__ == '__main__':
    sys.exit(main())