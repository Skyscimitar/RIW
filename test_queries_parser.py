import re

def parse_qrels():
    rels = []
    pattern = re.compile(r'0\d')
    with open('cacm/qrels.text', 'r') as f:
        for line in f:
            rel = line.strip().split(' ')
            rels.append(rel[:2])
    doc_rels = {}
    for rel in rels:
        doc_id, related_doc = rel[0], rel[1]
        if pattern.match(doc_id):
            doc_id = doc_id[1]
        if doc_id in doc_rels.keys():
            doc_rels[doc_id].append(related_doc)
        else:
            doc_rels[doc_id] = [related_doc]
    return doc_rels

parse_qrels()

def parse_query_text():
    queries = {}
    lines = []
    with open('cacm/query.text', 'r') as f:
        for line in f:
            lines.append(line.strip())
    id_pattern = re.compile(r'\.I\ \d*')
    current_key = '0'
    current_query = ''
    read_query = False
    for line in lines:
        if id_pattern.match(line):
            current_key = line.split(' ')[1]
            continue
        elif line == '.W':
            read_query = True
            continue
        elif line == '.N' or line == '.A':
            read_query = False
            queries[current_key] = current_query.strip()
        else:
            current_query += ' ' + line
    return queries