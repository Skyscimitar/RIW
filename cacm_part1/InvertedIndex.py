from .Document import Document

class InvertedIndex:

    @staticmethod
    def invert_index(tokens):
        """
        This function creates the inverted index from a regular index.
        :param tokens: {doc_id : [tokens]}
        :type tokens: dict
        """
        
        inv_index = {}
            #doc_id est une liste triee
        for doc_id in tokens.keys():
            for token in tokens[doc_id]:

                if token not in inv_index:
                    inv_index[token] = [doc_id]
                
                else:
                    if doc_id not in inv_index[token]:
                        inv_index[token].append(doc_id)
                        inv_index[token].sort()
                        
        return inv_index