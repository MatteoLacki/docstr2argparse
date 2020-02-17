%load_ext autoreload
%autoreload 2
import argparse
import re

from vodkas import apex3d, peptide3d, iadbs, plgs, get_fastas
from vodkas.plgs import parse_plgs_doc

from docstr2argparse.parse import parse_google, get_positional_or_keyword_params, foo2argparse, document

def foo():
    pass

parse_google(foo.__doc__)
parse_google(apex3d.__doc__)
parse_google(get_fastas.__doc__)
f = apex3d

foo2argparse(plgs)[1]
document(apex3d).print_help()
document(peptide3d).print_help()
document(iadbs).print_help()

args = document_many({'ape': apex3d, 'ia':iadbs, 'pep':peptide3d})
args.print_help()

from pprint import pprint
pprint(foo2argparse(apex3d))
plgs_desc, parsed, arg2foo = parse_plgs_doc()
# ap = argparse.ArgumentParser(description='Analyze Waters Raw Data with PLGS.')
# ap.print_help()
from collections import defaultdict





