'''This file will allow you to query the inverted index created by the indexer'''

import argparse
import sys
from typing import Tuple, List, Dict
import json
from tqdm import tqdm
import utils

def init_params():
    parser = argparse.ArgumentParser(description='Process command line arguments')
    parser.add_argument('-i', '--input_file', default='output/inverted_index.txt', help='Input file')
    parser.add_argument('-q', '--query_string', default=None, help='Input file')
    parser.add_argument('-o', '--output_file', default='output/sampleQueries.json', help='Output file')  # Does not include any directory names, strictly the filenames
    args = parser.parse_args()

    return args


def load_index(filename:str) -> Dict[str, Tuple[int, List[int]]]:
    '''Loads the inverted index stored in <filename>.'''

    print(f"Loading inverted index from {filename}")

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


def exec_query(word: str, index: Dict[str, Tuple[int, List[int]]]) -> Tuple[str, int, list, str]:
    # query_file = 'sampleQueries.json'
    
    result = {}

    result['query'] = word
    if word in index:

        query_hits: Tuple[int, List[int]] = index[word]
        frequency: int = query_hits[0]
        postings_list: List[int] = query_hits[1]

        result['frequency'] = frequency
        result['postings'] = postings_list
        result['message'] =  'successful'
    
    else:
       
        result['frequency'] = 0
        result['postings'] = []
        result['message'] =  'unsuccessful'

    return result


if __name__ == '__main__':
    args = init_params()

    if args.query_string == None or type(args.query_string) != str:
        print("Please provide a query str with flag -q")
        exit()

    inv_index: Dict[str, Tuple[int, List[int]]] = load_index(args.input_file)
    
    result: dict = exec_query(args.query_string, inv_index)

    print(f'<{result["query"]}> query was {result["message"]}: {result["frequency"]} hits found')
    
    utils.write_json_obj_2_disk(result, args.output_file)
    