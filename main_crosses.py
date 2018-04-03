#!/usr/bin/env python3


import subprocess

from options_parser import OptionsParser


def main_crosses():
    taus = ['1.5', '2.5', '5']
    Ns = [4, 8, 12, 16, 20, 24, 28, 30]
    options = OptionsParser().options
    folder_cpppolygons = options['folder_cpppolygons']
    app_reparsed_crosses = options['app_reparsed_crosses']
    exe = folder_cpppolygons + '/' + app_reparsed_crosses
    subprocess.call([exe, ])


if __name__ == '__main__':
    main_crosses()
