import re

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


if __name__ == "__main__":
    print(parse_query("NOT macbook AND NOT dell"))

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
