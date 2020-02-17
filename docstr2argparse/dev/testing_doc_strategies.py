%load_ext autoreload
%autoreload 2
import argparse
import re

from vodkas import apex3d, peptide3d, iadbs, plgs, get_fastas
from docstr2argparse.parse import parse_google, get_positional_or_keyword_params, foo2argparse


def foo():
    pass
parse_google(foo.__doc__)
parse_google(apex3d.__doc__)
parse_google(get_fastas.__doc__)
f = apex3d

foo2argparse(f)





document(apex3d).print_help()
document(peptide3d).print_help()
document(iadbs).print_help()


args = document_many({'ape': apex3d, 'ia':iadbs, 'pep':peptide3d})
args.print_help()


from pprint import pprint
pprint(foo2argparse(apex3d))

# TODO:
# add support for multiple functions
# add defaults to optional parameters
# add complaints about missing descriptions/types.
# add defaults to the end of the description.



# A = ap.ArgumentParser('APEX')
# A.add_argument('manna')
# A.print_help()

# A.parse_args(['10'])

# B = ap.ArgumentParser('BPEX')
# B.add_argument('hosanna')
# B.print_help()

# # vars(B)
# # vars(B._positionals._group_actions)
# # vars(B._positionals._group_actions[0])

# C = ap.ArgumentParser(parents=[A,B], conflict_handler='resolve')
# C.add_argument('manna')
# C.print_help()

# D = ap.ArgumentParser()
# DA = D.add_argument_group('A')


# C.parse_args(['10', '20', '30','30'])


# parent_parser = ap.ArgumentParser(add_help=False)
# parent_parser.add_argument('--parent', type=int)

# foo_parser = ap.ArgumentParser(parents=[parent_parser])
# foo_parser.add_argument('foo')
# foo_parser.parse_args(['--parent', '2', 'XXX'])
# foo_parser.print_help()

# bar_parser = ap.ArgumentParser(parents=[parent_parser])
# bar_parser.add_argument('--bar')
# bar_parser.parse_args(['--bar', 'YYY'])
# bar_parser.print_help()