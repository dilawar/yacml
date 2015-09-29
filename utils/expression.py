"""expression.py: 

    Function on expression.
"""
    
__author__           = "Dilawar Singh"
__copyright__        = "Copyright 2015, Dilawar Singh and NCBS Bangalore"
__credits__          = ["NCBS Bangalore"]
__license__          = "GNU GPL"
__version__          = "1.0.0"
__maintainer__       = "Dilawar Singh"
__email__            = "dilawars@ncbs.res.in"
__status__           = "Development"


def get_ids(expr):
    ids = re.findall(r'(?P<id>[_a-zA-Z]\w+)', expr)
    return ids
