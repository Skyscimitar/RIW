from cacm_part1.DocumentParser import DocumentParser
from cacm_part1.InvertedIndex import InvertedIndex
from cacm_part1.BinarySearchMethods import BinarySearchMethods
from nltk.tokenize import RegexpTokenizer
import numpy as np
import sys


class VectorialModel():

    @staticmethod
    def parse_query(q):

        #remove common_words from query
        tokenizer = RegexpTokenizer(r'\w+')
        tokens_q = tokenizer.tokenize(q)
        print(tokens_q)

        cleaned_q = DocumentParser.remove_common_words(tokens_q, DocumentParser.read_common_words("cacm/common_words"))
        print(cleaned_q)
        
        return cleaned_q


    @staticmethod
    def posting_union(cleaned_q, inv_index):

        # liste des listes de postings des mots de la query sans common words
        or_lists = [[int(j) for j in list(inv_index[i].keys())] for i in cleaned_q]

        while len(or_lists)>1:
             or_lists[0] = BinarySearchMethods.resolve_or(or_lists[0], or_lists[1])
             or_lists.pop(1)
        posting = or_lists[0]
        
        return posting


    @staticmethod
    def doc_vectors(posting, cleaned_q, inv_index):
        vectors = np.zeros((len(posting), len(cleaned_q)))

        for j in range(len(cleaned_q)):
            occurrences = inv_index[cleaned_q[j]]
            for doc in list(occurrences.keys()):
                if int(doc) in posting:
                    vectors[posting.index(int(doc))][j] = 1
        return vectors

    
    @staticmethod
    def cosinus(cleaned_q, vectors):

        query_vector = np.ones(len(cleaned_q))
        qv_norm = np.linalg.norm(query_vector)

        cosines_list = []

        for i in range(vectors.shape[0]):

            scalar = np.dot(query_vector, vectors[i])
            
            v_norm = np.linalg.norm(vectors[i])

            cos = scalar / (v_norm * qv_norm)

            cosines_list.append(cos)

        return cosines_list

    @staticmethod
    def search_result(cosines_list, posting):
        
        sorted_cosines = cosines_list.copy()
        sorted_cosines.sort(reverse=True)
        result = []
        while (len(sorted_cosines) > 0):
            indices = [i for i,x in enumerate(cosines_list) if x == sorted_cosines[0]]
            doc_ids = [posting[i] for i in indices]
            result += doc_ids
            sorted_cosines = sorted_cosines[len(doc_ids):]
        
        return result