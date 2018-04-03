#!/usr/bin/env python3


import subprocess

from main_crosses import main_crosses
from main_minmax import main_minmax
from main_reparse import main_reparse


def main():
    fout_reparse = open('log_reparse', 'w')
    fout_crosses = open('log_crosses', 'w')
    fout_minmax = open('log_minmax', 'w')
    print('start of main_reparse')
    subprocess.call(['./main_reparse.py',], stdout=fout_reparse)
    print('start of main_crosses')
    subprocess.call(['./main_crosses.py',], stdout=fout_crosses)
    print('start of main_minmax')
    subprocess.call(['./main_minmax.py',], stdout=fout_minmax)
    print('finish')
    return


main()
