'''This file will allow you to query the inverted index created by the indexer'''

import argparse
import sys
import os
from typing import Tuple, List, Dict
import json
from tqdm import tqdm
import utils
from utils import ensure_dir_exists


def init_params():
    parser = argparse.ArgumentParser(description='Process command line arguments')
    parser.add_argument('-i', '--input_file', default='output/inverted_index.txt', help='Input file')
    parser.add_argument('-q', '--query_string', default=None, help='Input file')
    parser.add_argument('-o', '--output_file', default='output/sampleQueries.json', help='Output file')  # Does not include any directory names, strictly the filenames
    args = parser.parse_args()

    return args





def exec_query(query: str, index: Dict[str, Tuple[int, List[int]]]) -> Dict[str, dict]:
    # query_file = 'sampleQueries.json'

    result = {}

    if query in index:

        query_hits: Tuple[int, List[int]] = index[query]
        frequency: int = query_hits[0]
        postings_list: List[int] = query_hits[1]

        result['frequency'] = frequency
        result['postings'] = postings_list
        result['message'] = 'successful'

    else:

        result['frequency'] = 0
        result['postings'] = []
        result['message'] = 'unsuccessful'

    return {
        query: {'frequency': result['frequency'],
                'postings': result['postings'],
                'message': result['message']}
    }


def ensure_query_file(qfile: str):
    '''
    Ensure that the file exists otherwise creates it. This file will contain an
    aggregation of all the queries executed against the inverted index.
    '''
    if os.path.isfile(qfile):
        return

    with open(qfile, mode='w') as f:
        f.write("{}")  # because we want utils.load_json_from_disk to load an empty dict instead of raising an exception


if __name__ == '__main__':

    args = init_params()
    utils.ensure_dir_exists('output')
    ensure_query_file(args.output_file)

    if args.query_string == None or type(args.query_string) != str:
        print("Please provide a query str with flag -q")
        exit()

    inv_index: Dict[str, Tuple[int, List[int]]] = utils.load_index(args.input_file)

    result: dict = exec_query(args.query_string, inv_index)
    x = result[args.query_string]
    print(f'<{args.query_string}> query was {x["message"]}: {x["frequency"]} hits found')

    queries: dict = utils.load_json_from_disk(args.output_file)

    del x['message']

    queries.update(result)

    utils.write_json_obj_2_disk(queries, args.output_file, indentation=4)
