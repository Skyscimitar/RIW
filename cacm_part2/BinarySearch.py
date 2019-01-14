from .ReqParser import parse_query
from cacm_part1.BinarySearchMethods import BinarySearchMethods

def binarySearch(query, invertedindex, doc_ids):
    search = parse_query(query)
    print(search)
    doc_list = resolveTerm(search, invertedindex, doc_ids)
    return doc_list


def resolveTerm(query, inverted_index, doc_ids):
    if "operation" in query:
        if query["operation"] == "AND":
            res = BinarySearchMethods.resolve_and(resolveTerm(query["search"][0], inverted_index, doc_ids), resolveTerm(query["search"][1], inverted_index, doc_ids))
            if query["is_not"]:
                res = BinarySearchMethods.resolve_not(res, doc_ids)
            return res
        elif query["operation"] == "OR":
            res = BinarySearchMethods.resolve_or(resolveTerm(query["search"][0], inverted_index, doc_ids), resolveTerm(query["search"][1], inverted_index, doc_ids))
            if query["is_not"]:
                res = BinarySearchMethods.resolve_not(res, doc_ids)
            return res
        elif query["operation"] is None:
            return resolveTerm(query["search"][0], inverted_index, doc_ids)
    else:
        # pas d'operation -> on cherche une liste de postings
        if query["is_not"]:
            res = list(inverted_index[query["search"]].keys())
            res = [int(i) for i in res]
            return BinarySearchMethods.resolve_not(res, doc_ids)
        res = list(inverted_index[query["search"]].keys())
        res = [int(i) for i in res]
        return res


            
