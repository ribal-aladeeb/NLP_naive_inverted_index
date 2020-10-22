'''This file is just for common utilities that are reusable in different modules'''

import argparse
import json
import sys
import os


def common_params():
    '''Initializes the params common to all modules'''
    parser = argparse.ArgumentParser(description='Process command line arguments')
    parser.add_argument('-i', '--input_file', default=sys.stdin, help='Input file')
    parser.add_argument('-o', '--output_file', default=sys.stdout, help='Output file')
    cmd_args = parser.parse_args()

    if type(cmd_args.input_file) == str:  # because sys.stdin will fail this assert
        assert os.path.isfile(cmd_args.input_file), f'Input file {cmd_args.input_file} does not exists'

    common_params.args = cmd_args

    return common_params.args


def write2disk(lines: list, outfile) -> bool:
    '''This is a general utility for writing intermediate and final computations into output files'''
    if type(outfile) == str:
        with open(outfile, mode='w', encoding='UTF-8') as f:
            for l in lines:
                print(json.dumps(l), file=f)

    else: # output must be sys.stdout (so it's already a file obj)
        for l in lines:
            print(json.dumps(l), file=outfile)
