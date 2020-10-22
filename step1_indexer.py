'''
This block will convert the corpus into a list of term-docID pairs. This 
'''

import argparse
import os
import sys
from typing import List
import utils


def init_params():
    parser = argparse.ArgumentParser(description='Process command line arguments')
    parser.add_argument('-i', '--input_file', default=sys.stdin, help='Input file')
    parser.add_argument('-o', '--output_file', default=sys.stdout, help='Output file')  # Does not include any directory names, strictly the filenames
    args = parser.parse_args()

    return args


if __name__ == "__main__":
    init_params()


def unpack_corpus_step1(path: str) -> List[str]:
    '''Given corpus <path>, returns a list where element is the full str content of a file'''

    sgmfiles: List[str] = sorted([fname for fname in os.listdir(path) if '.sgm' in fname])
    files_contents = []

    for filename in sgmfiles:
        with open(f'{path}/{filename}', mode='r', encoding='UTF-8', errors='ignore') as file:
            files_contents += [file.read()]

    return files_contents


def run(indir: str, outfile) -> None:

    lines: list = unpack_corpus_step1(indir)
    utils.write2disk(lines, outfile)


if __name__ == "__main__":
    args = init_params()
    outfile = f'output/{args.output_file}' if type(args.output_file) == str else args.output_file
    run(args.input_file, outfile)
