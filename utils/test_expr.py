"""test_expr.py: 

    Handle tests.

"""
    
__author__           = "Dilawar Singh"
__copyright__        = "Copyright 2015, Dilawar Singh and NCBS Bangalore"
__credits__          = ["NCBS Bangalore"]
__license__          = "GNU GPL"
__version__          = "1.0.0"
__maintainer__       = "Dilawar Singh"
__email__            = "dilawars@ncbs.res.in"
__status__           = "Development"

import re
import numpy as np

import logging
logger_ = logging.getLogger('gv.test')


class LTL():

    def __init__(self, expr):
        """
        assertion; 
        op : operator
        interval: in the given interval
        """
        self.expr = expr
        self.assertion, self.op, self.interval = expr.split(';')
        self.start = None
        self.stop = None
        self.interval = self.interval.split()
        self.field = None
        self.binop = None
        self.value = None
        self.error = 0.01
        self.le = None # lambda expression
        self.test_func = None

        self.keywords = [ 'EQ' , 'AE', 'GT', 'LT', 'GE', 'LE'
                , 'EH' # eventually happen
                , 'HA' # Happen after
                , 'AH' # always happens
                , 'NH' # Never happens
                , 'H\d+' # happends N times.
                ]

        self.parse()

    def getField(self):
        fs = self.assertion.split()
        self.field = fs[0].strip()
        self.binop = fs[1].strip()
        self.value = float(fs[2].strip())

    def getInterval(self):
        self.start = float(self.interval[0].strip())
        self.stop = float(self.interval[1].strip())

    def lambda_expr(self):
        """
        NOTICE: This function returns False on sucess.
        
        Always return False on success
        """
        self.le = 'lambda x, y : '
        if self.binop == 'AE': self.le += 'not (x - y)/x < %s' % self.error
        elif self.binop == 'EQ': self.le += 'not x == y '
        elif self.binop == 'NE': self.le += 'not x != y '
        elif self.binop == 'LT': self.le += 'not x < y'
        elif self.binop == 'LE': self.le += 'not x <= y'
        elif self.binop == 'GT': self.le += 'not x > y'
        elif self.binop == 'GE': self.le += 'not x >= y'
        else:
            warnings.warn('BINOP %s not supported yet' % self.binop)
            self.le += 'False'
        self.test_func = eval(self.le)

    def parse(self):
        self.getField()
        self.getInterval()
        self.lambda_expr()


def assert_test(time, node, molecule):
    """Assert a test on node """
    logger_.info("Running test on molecule: %s" % molecule)
    vec = node['recorder'].vector
    ltl = node['ltl']
    N = len(vec)
    dt = time / N
    startN, stopN = int(ltl.start/dt), int(ltl.stop/dt)
    data = vec[startN:stopN]
    func = np.vectorize(ltl.test_func)
    res = func(data, ltl.value)
    witness = startN + np.flatnonzero(res)
    time_witness = witness * dt
    value_witness = np.take(vec, witness)
    if len(witness) == 0: print("\t Passed")
    else:
        outfile = "%s.witness" % molecule
        witness_mat = np.vstack([time_witness, value_witness]).T
        print("\tFailed. Witness is printed below (time, value)")
        print(witness_mat)
        print("NOTICE: These witness are also saved to file: %s" % outfile)
        np.savetxt(outfile, witness_mat, delimiter=',')
