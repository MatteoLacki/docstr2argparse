%load_ext autoreload
%autoreload 2
import argparse
import re

from vodkas import apex3d
from docstr2argparse.parse import parse_google, get_params

docstring_long = """Analyze a Waters Raw Folder with Apex3D.


    Args:  
        raw_folder (str): Args: a path to the input folder with raw Waters data.
        output_dir (str): Path to where to place the output. Args:
        lock_mass_z2 (float): The lock mass for doubly charged ion.
        lock_mass_tol_amu (float): Tolerance around lock mass (in atomic mass units, amu).
        low_energy_thr (int): The minimal intensity of a precursor ion so that it ain't a noise peak.
        high_energy_thr (int): The minimal intensity of a fragment ion so that it ain't a noise peak.
        lowest_intensity_thr (int): The minimal intensity of a peak to be analyzed.
        write_xml (boolean): Write the output in an xml in the output folder.
        write_binary (boolean): Write the binary output in an xml in the output folder.
        write_csv (boolean): Write the output in a csv in the output folder (doesn't work).
        max_used_cores (int): The maximal number of cores to use.
        path_to_apex3d (str): Path to the "Apex3D.exe" executable.
        PLGS (boolean): No idea what it is.
        cuda (boolean): Use CUDA.
        unsupported_gpu (boolean): Try using an unsupported GPU for calculations. If it doesn't work, the pipeline switches to CPU which is usually much slower.
        timeout_apex3d (float): Timeout in minutes.
        kwds: other parameters.


    Returns:
        tuple: the path to the outcome (no extension: choose it yourself and believe more in capitalism) and the completed process.


    Yields:
        haha: dszi
    """

docstring_short = """Analyze a Waters Raw Folder with Apex3D.

    HAHAHA
    """

docstring_wrong = """Analyze a Waters Raw Folder with Apex3D.
    
        Ale gówno.
        Ja nie mogę.

        Args:  
            raw_folder (str): Args: a path to the input folder with raw Waters data.
            output_dir (str): Path to where to place the output. Args:
            lock_mass_z2 (float): The lock mass for doubly charged ion.
            lock_mass_tol_amu (float): Tolerance around lock mass (in atomic mass units, amu).
            low_energy_thr (int): The minimal intensity of a precursor ion so that it ain't a noise peak.
            high_energy_thr (int): The minimal intensity of a fragment ion so that it ain't a noise peak.
            lowest_intensity_thr (int): The minimal intensity of a peak to be analyzed.
            write_xml (boolean): Write the output in an xml in the output folder.
            write_binary (boolean): Write the binary output in an xml in the output folder.
            write_csv (boolean): Write the output in a csv in the output folder (doesn't work).
            max_used_cores (int): The maximal number of cores to use.
            path_to_apex3d (str): Path to the "Apex3D.exe" executable.
            PLGS (boolean): No idea what it is.
            cuda (boolean): Use CUDA.
            unsupported_gpu (boolean): Try using an unsupported GPU for calculations. If it doesn't work, the pipeline switches to CPU which is usually much slower.
            timeout_apex3d (float): Timeout in minutes.
            kwds: other parameters.


        Returns:
            tuple: the path to the outcome (no extension: choose it yourself and believe more in capitalism) and the completed process.


        Yields:
            haha: dszi
        """

parse_google(docstring_long)
parse_google(docstring_short)
parse_google(docstring_wrong)

def foo():
    pass

parse_google(foo.__doc__)
doc = parse_google(apex3d.__doc__)
doc['Args']

f = apex3d

def get_parameters(f, args_prefix='', sort = True):
    param2default = get_params(f)
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
    out = {}
    for a_name, a_type, a_desc in args:
        o = {'help':a_desc}
        default = param2default[a_name]
        if default is not None:
            o['default'] = default
            a_name = '--' + args_prefix + a_name # optionals are those with defaults
            o['help'] += f' [default: {default}].'
        else:
            a_name = args_prefix + a_name
        out[a_name] = o
    return short_description, out


def document_one(f):
    short, params = get_parameters(f, '')
    arg_parser = argparse.ArgumentParser(description=short)
    for name, val in params.items():
        arg_parser.add_argument(name, **val)
    return arg_parser

arg_parser = document_one(f)
arg_parser.print_help()

from vodkas import iadbs, peptide3d, get_fastas


parse_google(get_fastas.__doc__)
get_params(get_fastas.__doc__)



def document_many(foo_dict, description=''):
    arg_parser = argparse.ArgumentParser(description=description)
    for fname, f in foo_dict.items():
        short, params = get_parameters(f, fname+'_')
        for name, val in params.items():
            arg_parser.add_argument(name, **val)
    return arg_parser



args = document_many({'ape': apex3d, 'ia':iadbs, 'pep':peptide3d})
args.print_help()





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