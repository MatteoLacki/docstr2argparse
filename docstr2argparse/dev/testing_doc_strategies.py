%load_ext autoreload
%autoreload 2
import argparse
import re

from vodkas import apex3d, peptide3d, iadbs, plgs
from vodkas.fastas import get_fastas
from vodkas.fs import move

from docstr2argparse.parse import parse_google, get_positional_or_keyword_params, foo2argparse, document

from pathlib import Path
from furious_fastas import fastas, Fastas

# p = Path(r"X:\SYMPHONY_VODKAS\fastas\custom\Ute_fucking_bigger_fastas\20200124_upsp_human_yeas8_ecoli_cont_rev_validated.fasta")
# p = Path(r"X:\SYMPHONY_VODKAS\fastas\custom\Ute_fucking_bigger_fastas\20200124_upsp_human_yeas8_ecoli_cont_rev_validated.fasta")
p = Path("/mnt/ms/data/SYMPHONY_VODKAS/fastas/custom/Ute_fucking_bigger_fastas/20200124_upsp_human_yeas8_ecoli_cont_rev_validated.fasta")
p.exists()
fs = fastas(p)
if contaminate:
    from furious_fastas.contaminants import contaminants
    fs.extend(contaminants)
fs_gnl = Fastas(f.to_ncbi_general() for f in fs)
assert fs_gnl.same_fasta_types(), "Fastas are not in the same format."
if reverse:
    fs_gnl.reverse()
outpath = p.parent/(p.stem + '_contaminated_reversed_pipelineFriendly.fasta')
local_tmp = Path('~').expanduser()
fs_gnl.write(local_tmp/outpath.name)
move(local_tmp/outpath.name, outpath)
