'''This file is just for common utilities that are reusable in different modules'''

import argparse
import json
import sys
import os
from typing import Dict, Iterable, List, Tuple
from tqdm import tqdm


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


def load_index(filename: str) -> Dict[str, Tuple[int, List[int]]]:
    '''Loads the inverted index stored in <filename>.'''

    print(f"\nLoading inverted index from {filename}")

    inv_idx = []                                           # as loaded by json.loads(), type(inv_idx) == List[str, List[int,List[int]]]
    inverted_index: Dict[str, Tuple[int, List[int]]] = {}  # This will contain the correct format and type

    with open(filename, mode='r') as file:
        i = 0
        for line in tqdm(file):
            inv_idx.append(json.loads(line))
            token: str = inv_idx[i][0]
            frequency: int = inv_idx[i][1][0]
            postings_list: List[int] = inv_idx[i][1][1]
            inverted_index[token] = (frequency, postings_list)
            i -= -1

    return inverted_index


def save_index_to_disk(inverted_index: Dict[str, Tuple[int, set]], outfile: str,) -> None:
    
    assert type(outfile) == str, "When using function save_index_to_disk you have to provide an outfile arg."
    printable: Tuple[str, Tuple[int, List[int]]] = sorted(inverted_index.items(), key=lambda token: token[0])
    write2disk(printable, outfile)


def write2disk(lines: Iterable, outfile) -> None:
    '''
    This is a general utility for writing intermediate and final computations
    into output files. The <lines> argument needs to be iterable.
    '''

    print(f'\nWriting output into file {outfile}')

    if type(outfile) == str:
        with open(outfile, mode='w', encoding='UTF-8') as f:
            for l in tqdm(lines):
                print(json.dumps(l), file=f)

    else:  # output must be sys.stdout (so it's already a file obj)
        for l in tqdm(lines):
            print(json.dumps(l), file=outfile)


def write_json_obj_2_disk(obj: dict, outfile, indentation=None):
    '''Writes obj dict representing a json obj to oufile.'''
    if type(outfile) == str:
        with open(outfile, mode='w', encoding='UTF-8') as f:
            json.dump(obj, f, indent=indentation)

    else:  # output must be sys.stdout (so it's already a file obj)
        json.dump(obj, outfile, indent=indentation)


def load_json_from_disk(infile):
    '''Reads json obj from infile.'''

    if type(infile) == str:
        with open(infile, mode='r', encoding='UTF-8') as f:
            obj = json.load(f)

    else:  # infile must be a file obj
        obj = json.load(infile)

    return obj


def ensure_dir_exists(dir):
    '''Checks that <path> exists, otherwise creates it'''

    if os.path.isdir(dir):
        return

    print(f'Creating {dir}/ directory')
    os.mkdir(dir)
