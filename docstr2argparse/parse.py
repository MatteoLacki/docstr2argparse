import builtins
import argparse
from inspect import signature, _empty
from docstring_parser.parser import parse
import re


def foo2parser(foo):
    """Create a new parser with description matching the short description of the function."""
    return argparse.ArgumentParser(description=parse(foo.__doc__).short_description)


def get_defaults(foo):
    sign = signature(foo)
    return {n: p.default for n,p in sign.parameters.items() if not p.default == _empty}


def parse_arguments(foo):
    defaults = get_defaults(foo)
    parsed_doc = parse(foo.__doc__)
    all_params = {p.arg_name for p in parsed_doc.params}
    assert set(defaults).issubset(all_params), "Some parameters with defaults are not in the description."
    for p in parsed_doc.params:
        if p.arg_name not in ('kwds', 'args'):
            kwds = {}
            kwds['help'] = p.description
            try:
                kwds['type'] = getattr(builtins, p.type_name)
            except AttributeError:
                pass
            arg_name = p.arg_name
            if arg_name in defaults:
                kwds['help'] += " [default = {}]".format(defaults[arg_name])
                kwds['default'] = defaults[arg_name]
                arg_name = "--" + arg_name
            yield arg_name, kwds


def register_docs(foo, parser=None):
    if parser is None:
        parser = foo2parser(foo)
    for name, kwds in parse_arguments(foo):
        parser.add_argument(name, **kwds)
    return parser


def get_params(f):
    """Get parameters from function signature.
    
    Args:
        f (function): A function to investigate.

    Returns:
        dict: Map parameter to its default value.
    """
    return {n:p.default if not p.default == _empty else None 
            for n,p in signature(f).parameters.items()}


def _parse_google_argument_name(arg):
    """Parse google arguments."""
    try:
        arg_type = next(re.finditer(r'\(.*?\)', arg)).group(0)
        arg = arg.replace(arg_type, '')
        arg_type = arg_type[1:-1]
    except StopIteration:
        arg_type = None
    arg = arg.strip()
    return arg, arg_type


def parse_google(docstring, trim=True):
    """Parse goolge style of doctring.

    This is defined as by Sphinx.Napoleon package.

    Args:
        docstring (str): Docstring to parse.
        trim (boolean): Should only existing entries be returned?

    Returns:
        dict: All parameters parsed.
    """
    o = {}
    o['Args'] = o['Arguments'] = []
    o['Attributes'] = []
    o['Example'] = []
    o['Examples'] = []
    o['Keyword Args'] = o['Keyword Arguments'] = []
    o['Methods'] = []
    o['Note'] = []
    o['Notes'] = []
    o['Other Parameters'] = []
    o['Return'] = o['Returns'] = []
    o['Raises'] = []
    o['References'] = []
    o['See Also'] = []
    o['Todo'] = []
    o['Warning'] = o['Warnings'] = []
    o['Warns'] = []
    o['Yield'] = o['Yields'] = []
    # pat = r"\n\s*({}):\s*\n".format("|".join(o))
    pat = r"\n\s*(\S+):\s*\n"
    if docstring:
        split = re.split(pat, docstring)
        desc = split[0].split('\n')
        o['short_description'] = desc[0]
        o['long_description'] = " ".join(x for l in desc[1:] for x in l.split())
        for tag, args in zip(split[1::2], split[2::2]):
            assert tag in o, f"Group not specified in Splinx.Napoleon google-doc-style: '{tag}'"
            args = args.rstrip('\n ')
            for arg in args.split('\n'):
                arg_name, arg_desc = arg.split(':', 1)
                arg_desc = " ".join(arg_desc.split())
                arg_name, arg_type = _parse_google_argument_name(arg_name)
                o[tag].append((arg_name, arg_type, arg_desc))
    for k in list(o.keys()):
        if not o[k]:
            del o[k] 
    return o


if __name__ == '__main__':
    from docstr2argparse.mocked_foo import apex3d as foo
    parser = register_docs(foo)
    args = parser.parse_args()
    print(args.__dict__)
