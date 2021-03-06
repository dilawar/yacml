"""yacml.py: 

"""
    
__author__           = "Dilawar Singh"
__copyright__        = "Copyright 2015, Dilawar Singh and NCBS Bangalore"
__credits__          = ["NCBS Bangalore"]
__license__          = "GNU GPL"
__version__          = "1.0.0"
__maintainer__       = "Dilawar Singh"
__email__            = "dilawars@ncbs.res.in"
__status__           = "Development"


import yacml2moose
import config
import yparser.yparser as yp
import yparser.bnf as bnf
import yparser.ast_processor as astp
import yparser.pre_processor
import moose
import moose.utils as mu
import lxml.etree as etree

logger_ = config.logger_

def loadModel( filename, **kwargs ):
    """Main entry function
    """

    config.args_['input_flie'] = filename
    xml = yp.parse( filename )
    
    xml0file = '%s0.xml' % filename
    with open( xml0file , 'w' ) as f:
        f.write( etree.tostring( xml, pretty_print = True ) )
    logger_.info( 'Wrote xml0 to %s' % xml0file )

    xml = astp.flatten( xml )
    xml1file = '%s1.xml' % filename
    with open( xml1file, 'w' ) as f:
        f.write( etree.tostring( xml, pretty_print = True ) ) 
    logger_.info( 'Wrote xml1 to %s' % xml1file )

    yacml2moose.load( xml, **kwargs )

# if __name__ == '__main__':
#     import argparse
#     # Argument parser.
#     description = '''YACML: Yet Another Chemical Markup Language'''
#     argp = argparse.ArgumentParser(description=description)
#     argp.add_argument('--model_file', '-f'
#             , required = True
#             , type = str
#             , help = 'Model file'
#             )
#     
#     argp.add_argument('--sim_time', '-st'
#             , metavar='variable'
#             , default = 10.0
#             , type = float
#             , help = 'A generic option'
#             )
# 
#     argp.add_argument('--solver', '-s'
#             , default = 'moose'
#             , type = str
#             , help = "Which solver to use: moose | scipy"
#             )
# 
#     argp.add_argument('--outfile', '-o'
#             , default = None
#             , type = str
#             , help = "Name of the plot file"
#             )
# 
#     argp.add_argument('--log', '-l'
#             , default = 'warning'
#             , type = str
#             , help = 'Debug levels: [debug, info, warning, error, critical]'
#             )
# 
#     class Args: pass 
#     args = Args()
#     argp.parse_args(namespace=args)
#     main(vars(args))
