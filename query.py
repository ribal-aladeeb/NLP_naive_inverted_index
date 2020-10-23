'''This file will allow you to query the inverted index created by the indexer'''

from typing import Tuple, List, Dict
import json
from tqdm import tqdm


def load_index(filename='output/inverted_index.txt') -> Dict[str, Tuple[int, List[int]]]:
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


def query(word: str) -> Tuple[str, list]:
    pass


if __name__ == '__main__':
    pass
