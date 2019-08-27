def foo1(a, b, c=1, d=2):
    """Some function number 1.

    Args:
        a (int): the first param
        b (str): the second param
        c (int): some parameter
        d (int): another parameter
    Returns:
        int: sum of the two ints
    """
    return a + b


def foo2(e, f, g=1, h=2):
    """Some function number 1.

    Args:
        e (int): the first param
        f (str): the second param
        g (int): some parameter 2
        h (int): another parameter 2
    Returns:
        int: sum of the two ints
    """
    return e + f


import argparse
from itertools import chain

from docstr2argparse import parse_arguments

parser = argparse.ArgumentParser(description='A terribly needed script!')

# print(dict(parse_arguments(foo1))) # this will be a simple dictonary!!!

for name, kwds in chain(parse_arguments(foo1), parse_arguments(foo2)):
    parser.add_argument(name, **kwds)

args = parser.parse_args()

print(foo1(args.a, args.b, args.c, args.d) + foo1(args.e, args.f, args.g, args.h))