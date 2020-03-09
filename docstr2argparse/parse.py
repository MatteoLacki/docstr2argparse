import builtins
from pprint import pprint
from collections import namedtuple, OrderedDict
from inspect import signature, _empty
import re
import argparse


def defaults(f):
    """Get defaults of the function parameters.
    
    Warning: don't get into the problem of recursive dependencies.

    Args:
        f (function): A function to investigate.

    Returns:
        dict: Map parameter to its default value.
    """
    return {n:p.default for n,p in signature(f).parameters.items() if not p.default == _empty}


def get_positional_or_keyword_params(f):
    """Get positional or keyword parameters from function signature.
    
    Args:
        f (function): A function to investigate.

    Returns:
        dict: Map parameter to its default value.
    """
    return {n:p.default if not p.default == _empty else None 
            for n,p in signature(f).parameters.items() if 
            p.kind.name in ('POSITIONAL_ONLY','POSITIONAL_OR_KEYWORD')}


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


def test_parse_google():
    docstring = """Little function.

    That does not help.
    Anybody. Anywhere.
    Is useless.

    Args:
        sadness (boolean): no nothing.
        pain (float): stay afloat.

    Returns:
        shit: specific one.
    """
    x = parse_google(docstring)
    y = {'Args': [('sadness', 'boolean', 'no nothing.'), ('pain', 'float', 'stay afloat.')], 'Arguments': [('sadness', 'boolean', 'no nothing.'),('pain', 'float', 'stay afloat.')],'Return': [('shit', None, 'specific one.')],'Returns': [('shit', None, 'specific one.')],'short_description': 'Little function.','long_description': 'That does not help. Anybody. Anywhere. Is useless.'}
    assert x == y, 'Parsing is wrong.'


def foo2argparse(f, args_prefix='', positional=True, optional=True, get_short=True, sort=True):
    param2default = get_positional_or_keyword_params(f)
    parsed = parse_google(f.__doc__)
    short_description = parsed['short_description']
    args = parsed['Args']
    args2desc = {n:d for n,_,d in args}
    # checking docs' completeness
    for p in param2default:
        assert p in args2desc, f"Docs of {f} incomplete: {p} is missing."
        assert args2desc[p]!='', f"Docs of {f} incomplete: {p} has empty description."
    if sort:
        args = sorted(args)
    out = []
    for a_name, a_type, a_desc in args:
        o = {'help':a_desc}
        try:
            o['type'] = getattr(builtins, a_type)
        except AttributeError:
            pass
        default = param2default[a_name]
        if default is not None:
            o['default'] = default
            name = '--' + args_prefix + a_name # optionals are those with defaults
            if optional:
                out.append((name, a_name, o))
        else:
            name = args_prefix + a_name
            if positional:
                out.append((name, a_name, o))
    if get_short:
        return short_description, out
    else:
        return out


def document(f, description=''):
    """Document one function.

    Make a parser, ready to be call parse_args().

    Args:
        f (function): Function to document.
        description (str): Description of the parser.

    Returns:
        argparse.ArgumentParser: with instantiated arguments.
    """
    short, params = foo2argparse(f, '')
    description = description if description else short
    arg_parser = argparse.ArgumentParser(description=description)
    for name, orig_name, val in params:
        arg_parser.add_argument(name, **val)
    return arg_parser


def document_many(foo_dict, description=''):
    """Document many functions.

    Make a parser, ready to be call parse_args().

    Args:
        foo_dict (dict): Maps prefixes to functions.
        description (str): Description of the parser.

    Returns:
        argparse.ArgumentParser: with instantiated arguments.
    """
    arg_parser = argparse.ArgumentParser(description=description)
    for fname, f in foo_dict.items():
        short, params = foo2argparse(f, fname+'_')
        for name, orig_name, val in params:
            arg_parser.add_argument(name, **val)
    return arg_parser


class ParserDisambuigationEasy(object):
    """Solve ambuiguious parameter names.

    In case of ambuiguity, prepend function name.
    """
    def __init__(self, foos):
        self.fnames = [f.__name__ for f in foos]
        self.a2d = []
        self.a2fn_o = {}
        for f in foos:
            for n,o,h in foo2argparse(f)[1]:
                if n[0:2] == '--':
                    fn = f.__name__
                    self.a2d.append((f"--{fn}_{o}", h))
                    self.a2fn_o[f"{fn}_{o}"] = fn, o

    def parsed2kwds(self, parsed):
        out = {f:{} for f in self.fnames}
        for a,(f,o) in self.a2fn_o.items():
            out[f][o] = parsed[a]
        return out



# class ParserDisambuigationComplex(object):
#     """Solve ambuiguious parameter names.

#     In case of ambuiguity, prepend function name.
#     """
#     def __init__(self, foos):
#         a2fs = defaultdict(list)
#         self.fnames = set({})
#         for f in foos:
#             for n,o,h in foo2argparse(f)[1]:
#                 if n[0:2] == '--':
#                     a2fs[o].append((f.__name__,h))
#                     self.fnames.add(f.__name__) 
#         a2f = {}
#         a2h = []
#         for a, fs in a2fs.items():
#             for f,h in fs:
#                 f_a = f"{f}_{a}" if len(fs) > 1 else a
#                 a2f[f_a] = (f,a)
#                 a2h.append((f,f_a,h))
#         self.a2fs = a2fs
#         self.a2f = a2f
#         self.a2d = [('--'+f_a,h) for f,f_a,h in sorted(a2h, key=lambda x: (x[0],x[1]))]

#     def parsed2kwds(self, parsed):
#         out = {f:{} for f in self.fnames}
#         for a,(f,o) in self.a2f.items():
#             out[f][o] = parsed[a]
#         return out


ARG = namedtuple('ARG', 'name o_name info')


class FooParser(OrderedDict):
    def __init__(self, foos):
        """Initiate the FooParser.

        Args:
            foos (iterable): Functions to construct parser of optional parameters for.
        """
        for foo in foos:
            args = foo2argparse(foo, 
                                get_short=False,
                                positional=False,
                                args_prefix= foo.__name__+'_')
            self[foo.__name__] = OrderedDict((o, ARG(n,o,h)) for n,o,h in args)

    def parse_kwds(self, parsed_args):
        """Get kwds for foos in the parser.

        Results are saved in field 'kwds'.

        Args:
            parsed_args (dict): A dictionary with parsed values.
        """
        self.kwds = {foo_name:{} for foo_name in self}
        for arg, val in parsed_args.items():
            foo, o_name = arg.split('_', 1)
            if foo in self and o_name in self[foo]:
                self.kwds[foo][o_name] = val
