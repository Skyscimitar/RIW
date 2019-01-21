

class BinarySearchMethods:

    @staticmethod
    def resolve_and(l1, l2):
        output = []
        while len(l1) > 0 and len(l2) > 0:
            if l1[0] == l2[0]:
                output.append(l1[0])
                l1 = l1[1:]
                l2 = l2[1:]
            elif l1[0] < l2[0]:
                l1 = l1[1:]
            else:
                l2 = l2[1:]
        return output
    
    @staticmethod
    def resolve_or(l1, l2):
        print(l1)
        output = []
        while len(l1) > 0 and len(l2) > 0:
            if (l1[0] == l2[0]):
                output.append(l1[0])
                l1 = l1[1:]
                l2 = l2[1:]
            elif l1[0] < l2[0]:
                output.append(l1[0])
                l1 = l1[1:]
            else:
                output.append(l2[0])
                l2 = l2[1:]
        if len(l2) > 0:
            output += l2
        elif len(l1) > 0:
            output += l1
        return output

    @staticmethod
    def resolve_not(l, doc_ids):
        output = []
        while len(l) > 0 and len(doc_ids) > 0:
            if l[0] == doc_ids[0]:
                l = l[1:]
                doc_ids = doc_ids[1:]
            else:
                output.append(doc_ids[0])
                doc_ids = doc_ids[1:]
        if len(doc_ids) > 0:
            output += doc_ids
        return output
 

    
                
