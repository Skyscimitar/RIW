import os
from tqdm import tqdm
import sys
import json
import numpy as np
from math import log, pow
from cacm_part1.NewDocument import NewDocument as Document
from test_queries_parser import parse_qrels, parse_query_text
from cacm_part1.VectorialModel import VectorialModel
from cacm_part1.InvertedIndex import InvertedIndex

file = "cacm/cacm.all"
common_words_file = "cacm/common_words"

def read_stop_words(common_words_file):
        common_words = []
        try:
            with open(common_words_file, 'r') as f:
                for line in f:
                    common_words.append(line.strip('\n'))
        except IOError:
            print("Common words file not found")
        return common_words

def parse_entry_file(file, common_words):
        with open(file, 'r') as f:
            current_token = ''
            docs = {}
            id = None
            title = ""
            summary = ""
            keywords = ""
            for line in f:
                if line[:2] == '.I' :
                    if id is not None:
                        doc = Document(id, title, summary=summary, keywords=keywords, stopwords=common_words)
                        docs[id] = doc
                    title = ""
                    summary = ""
                    keywords = ""
                    id = line[3:].strip('\n')
                elif line[:2] == '.T':
                    current_token = '.T'
                    continue
                elif line[:2] == '.W':
                    current_token = '.W'
                    continue
                # elif line[:2] == '.A':
                #     current_token = '.A'
                #     continue
                elif line[:2] == '.A' or line[:2] == '.X' or line[:2] == '.N' or line[:2] == '.B':
                    current_token = ''
                else:
                    if current_token == '.T':
                        title += ' ' + line.strip()
                    elif current_token == '.W':
                        summary += ' ' + line.strip()
                    elif current_token == '.K':
                            keywords = ' ' + line.strip()
                    # elif current_token == '.A':
                    #     authors += line.strip().split(',')[0]
            return docs

def calculate_tokens_and_vocab(docs):
    pre_tokens = []
    post_tokens = []
    for doc_id in list(docs.keys()):
        pre_tokens += docs[doc_id].pre_tokens
        post_tokens += docs[doc_id].post_tokens
    pre_vocab = set(pre_tokens)
    post_vocab = set(post_tokens)
    return post_tokens, post_vocab

def half_way_tokens_and_vocab(docs):
    keys = list(docs.keys())
    tokens = []
    for i in range(int(len(keys)/2)):
        tokens += (docs[keys[i]].post_tokens)
    return tokens, set(tokens)


def get_tokens_dict(docs):
    tokens = {}
    for key in docs.keys():
        tokens[docs[key].id] = docs[key].post_tokens
    return tokens


def test_accuracy_recall(documents, tokens, return_doc_count=10):
    inverted_index = InvertedIndex.invert_index(tokens)
    test_queries = parse_query_text()
    test_rels = parse_qrels()
    accuracies = []
    recalls = []
    docs = {}
    for doc_id in documents.keys():
        docs[doc_id] = len(documents[doc_id].post_tokens)
    for key in tqdm(list(test_rels.keys())):
        cleaned_query = VectorialModel.parse_query(test_queries[key])
        postings = VectorialModel.posting_union(cleaned_query, inverted_index)
        vectors = VectorialModel.doc_vectors_ponderation(postings, cleaned_query, inverted_index, docs)
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
    beta = max_accuracy / max_recall
    alpha = 1 / (beta**2 + 1)
    e_mesure = 1 - 1/(alpha/max_accuracy + (1 - alpha)/max_recall)
    f_mesure = 1 - e_mesure
    print("E-mesure: %.2f, F-Mesure: %.2f" % (e_mesure, f_mesure))


if __name__ == "__main__":
    common_words = read_stop_words(common_words_file)
    docs = parse_entry_file(file, common_words)
    tokens, vocab = calculate_tokens_and_vocab(docs)
    print("Number of tokens: %i, Vocabulary size: %i" % (len(tokens), len(vocab)))
    htokens , hvocab = half_way_tokens_and_vocab(docs)
    print("Halfway tokens: %i, Halfway vocab: %i" % (len(htokens), len(hvocab)))
    b = log(float(len(vocab)/len(hvocab)))/log(len(tokens)/len(htokens))
    k = len(vocab)/pow(len(tokens), b)
    print("k: %.2f, b: %.2f" % (k, b))
    voc_million = voc_million = k * (10**6)**b
    print("Vocabulary for 1 million tokens: %.2f" % voc_million)
    tokens = get_tokens_dict(docs)
    test_accuracy_recall(docs, tokens, 50)