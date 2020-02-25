%load_ext autoreload
%autoreload 2
import argparse
import re
from pathlib import Path

from vodkas import apex3d, peptide3d, iadbs, plgs
from docstr2argparse.parse import parse_google, get_positional_or_keyword_params, foo2argparse, document
from vodkas.fastas import get_fastas

p = Path(r"X:\SYMPHONY_VODKAS\fastas\custom\Ute_fucking_bigger_fastas\20200124_upsp_human_yeas8_ecoli_cont_rev_validated.fasta")
# p = Path("/mnt/ms/data/SYMPHONY_VODKAS/fastas/custom/Ute_fucking_bigger_fastas/20200124_upsp_human_yeas8_ecoli_cont_rev_validated.fasta")
p.exists()
get_fastas(p)

