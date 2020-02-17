%load_ext autoreload
%autoreload 2
from vodkas import apex3d, peptide3d, iadbs, get_fastas
from docstr2argparse.parse import ParserDisambuigation
from collections import defaultdict

foos = [get_fastas, apex3d, peptide3d, iadbs]

cp = ParserDisambuigation(foos)

cp.a2f
cp.a2fs['write_csv']
cp.a2d
cp.fnames

