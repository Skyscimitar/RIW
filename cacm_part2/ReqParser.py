import re
import boolean

bool_parser = boolean.BooleanAlgebra()

# {
#   'search': [
#       {
#           'search': 'macbook', 
#           'is_not': True
#       }, 
#       {
#           'search': 'dell', 
#           'is_not': True
#       }
#   ], 
#   'operation': 'AND', 
#   'is_not': False
# }

def parse_query(q):
    q = q.strip()
    k = re.match(r"^(?P<not_1>NOT )? ?(?P<kw_1>\w+)( (?P<op>(AND|OR)) (?P<not_2>NOT )? ?(?P<kw_2>\w+))?$",q)
    search = []
    if k.group('kw_1') is None:
        raise ValueError("No keyword specified")
    search.append(
        {
            "search":k.group('kw_1'),
            "is_not":k.group('not_1') is not None
        }
    )
    if k.group('kw_2') is not None:
        search.append(
            {
                "search":k.group('kw_2'),
                "is_not":k.group('not_2') is not None
            }
        )
    return {
        "search": search,
        "operation": k.group('op'),
        "is_not": False
    }

# macbook
# NOT macbook
# macbook AND pro
# macbook AND pro
# macbook AND NOT pro
# dell OR mackbook
# (mackbook AND pro) OR dell
# (mackbook AND NOT pro) OR dell
# (mackbook AND pro) OR (mackbook AND pro)
# (mackbook AND pro) OR (dell OR NOT xps)
# (mackbook AND pro) OR (dell AND xps)
# macbook AND pro AND (13 OR 15)

def parenthetic_contents(string):
    """Generate parenthesized contents in string as pairs (level, contents)."""
    # https://gist.github.com/constructor-igor/5f881c32403e3f313e6f
    stack = [string]
    still_open_bracket = 0
    yield (0,string,0,len(string))
    for i, c in enumerate(string):
        if c == '(':
            stack.append(i)
            still_open_bracket += 1
        elif c == ')' and stack:
            start = stack.pop()
            still_open_bracket -= 1
            if still_open_bracket < 0:
                raise Exception("Syntax error in the query. (Too much opened brackets) pos : {}, query : {}".format(i,string))
            yield (len(stack), string[start + 1: i], start, i+1)
    if still_open_bracket > 0:
        raise Exception("Syntax error in the query. (Not closed bracket) pos : {}, query : {}".format(i,string))

def evaluate_tok(s):
    a = re.split(r"NOT ", s, flags=re.IGNORECASE)
    if len(a) > 1:
        return a[1].strip(), True
    else:
        return a[0].strip(), False

def add_tok(parsed_pointer, tok_to_add):
    tok = evaluate_tok(tok_to_add)
    parsed_pointer["search"].append({
        "search": tok[0],
        "operation": None,
        "is_not": tok[1]
    })

def recur_replace(parsed, search_dict):
    if type(parsed) is list:
        for i, search in enumerate(parsed):
            if type(search["search"]) is str:
                if search["search"] in search_dict:
                    # search is $x
                    search_dict[search["search"]]["is_not"] = parsed[i]["is_not"]
                    parsed[i] = search_dict[search["search"]]
            else:
                recur_replace(search["search"], search_dict)

def parse(query, debug=False):
    search_dict = {}
    search_id = 1
    while True:
        nested_par_list = list(parenthetic_contents(query))
        nested_par_list.sort(key=lambda x: x[0], reverse=True)
        sub_query = nested_par_list[0]
        search = parse_no_par(sub_query[1], debug)
        if sub_query[0] == 0:
            break
        identifier = "$"+str(search_id)
        search_dict[identifier] = search
        query = query[:sub_query[2]] + identifier + query[sub_query[3]:]
        search_id += 1
    final_parse = parse_no_par(query)
    for _ in range(search_id-1):
        recur_replace(final_parse["search"], search_dict)
    return final_parse

def parse_no_par(s, debug=False):
    if debug:
        print(s)

    p_or = [b.strip() for b in s.split("OR")]
    p_or = [[c.strip() for c in b.split("AND")] for b in p_or]

    parsed = {
        "search": None,
        "operation": None,
        "is_not": False
    }

    if len(p_or) > 1:
        parsed = {
            "search": [],
            "operation": "OR",
            "is_not": False
        }
        for p in p_or:
            if len(p) == 1:
                # p is a single token
                add_tok(parsed,p[0])
            else:
                # p is a p_and, not a single token
                p_and = p
                parsed["search"].append({
                    "search": [],
                    "operation": "AND",
                    "is_not": False
                })
                parsed_pointer = parsed["search"][-1]
                for p in p_and:
                    add_tok(parsed_pointer,p)
    else:
        p_and = p_or[0]
        if len(p_and) == 1:
            # it was only a single token
            tok = evaluate_tok(p_and[0])
            parsed = {
                "search": tok[0],
                "operation": None,
                "is_not": tok[1]
            }
        else:
            parsed = {
                "search": [],
                "operation": "AND",
                "is_not": False
            }
            for p in p_and:
                add_tok(parsed,p)
    if debug:
        print(parsed)
    return parsed

if __name__ == "__main__":
    print(parse("linux AND NOT (windows OR NOT (linux AND mac)))"))
    # parse("windows AND (mac OR NOT (windows AND linux))", debug=True)
    # parse("windows", debug=True)
    # parse("NOT windows", debug=True)
    # parse("NOT windows OR mac", debug=True)
    # parse("NOT windows OR mac AND linux", debug=True)
    # parse("NOT windows OR mac AND NOT linux", debug=True)
    # parse("NOT windows OR mac AND lamp AND NOT linux", debug=True)
    # parse("NOT windows OR mac AND lamp AND NOT linux", debug=True)


def test_token_alone():
    assert parse_query("mackbook") == {
        "search": [{
            "search": "mackbook",
            "is_not": False
        }],
        "operation": None,
        "is_not": False
    }

def test_not_token_alone():
    assert parse_query("NOT mackbook") == {
        "search": [{
            "search": "mackbook",
            "is_not": True
        }],
        "operation": None,
        "is_not": False
    }
