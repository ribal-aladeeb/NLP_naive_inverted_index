'''
This script will compress and optimize the index.
DISCLAIMER: these functions will modify the argument index so pass a deep copy if you wish to maintain. The
reason being that performing a copy at each step is very inefficient.
'''

import utils
import re
import argparse
from typing import Tuple
import json


stop_words = ('the', 'be', 'of', 'and', 'a', 'to', 'in', 'he', 'have', 'it', 'that', 'for', 'they', 'I', 'with', 'as', 'not', 'on', 'she', 'at', 'by', 'this', 'we', 'you', 'do', 'but', 'from', 'or', 'which', 'one', 'would', 'all', 'will', 'there', 'say', 'who', 'make', 'when', 'can', 'more', 'if', 'no', 'man', 'out', 'other', 'so', 'what', 'time', 'up', 'go', 'about', 'than', 'into', 'could', 'state', 'only', 'new', 'year', 'some', 'take', 'come', 'these', 'know', 'see', 'use', 'get', 'like', 'then', 'first', 'any', 'work', 'now', 'may', 'such', 'give', 'over', 'think', 'most', 'even', 'find', 'day',
              'also', 'after', 'way', 'many', 'must', 'look', 'before', 'great', 'back', 'through', 'long', 'where', 'much', 'should', 'well', 'people', 'down', 'own', 'just', 'because', 'good', 'each', 'those', 'feel', 'seem', 'how', 'high', 'too', 'place', 'little', 'world', 'very', 'still', 'nation', 'hand', 'old', 'life', 'tell', 'write', 'become', 'here', 'show', 'house', 'both', 'between', 'need', 'mean', 'call', 'develop', 'under', 'last', 'right', 'move', 'thing', 'general', 'school', 'never', 'same', 'another', 'begin', 'while', 'number', 'part', 'turn', 'real', 'leave', 'might', 'want', 'point')

assert len(stop_words) == 150, "stop_words should be 150 words long"


def init_params():
    parser = argparse.ArgumentParser(description='Process command line arguments')
    parser.add_argument('-i', '--input_file', default='output/inverted_index.txt', help='Input file')
    parser.add_argument('-o', '--output_file', default='output/compressed_index.txt', help='Output file')  # Does not include any directory names, strictly the filenames
    args = parser.parse_args()

    return args


def remove_numbers(index: dict) -> dict:
    '''Removes all tokens that are numbers.'''

    print('\nRemoving all numbers...')
    to_remove = []
    for token in index:
        # match = re.search("[0-9]+", token)
        match = token.isnumeric()

        if match:
            to_remove.append(token)

    for token in to_remove:
        del index[token]

    return index


def case_fold(index: dict) -> dict:
    '''Lower cases all tokens'''

    print('\nPerforming case folding...')
    to_fold = [token for token in index if token != token.lower()]

    for token in to_fold:

        if token.lower() in index:

            postings_list1 = index[token.lower()][1]
            postings_list2 = index[token][1]

            merged_postings_list = sorted(list(set(postings_list1).union(set(postings_list2))))
            freq = len(merged_postings_list)
            index[token.lower()] = (freq, merged_postings_list)

        else:
            index[token.lower()] = index[token]

        del index[token]

    return index


def remove_stop_words(index: dict, stopwords: Tuple[str]) -> dict:
    '''This function removes stopwords from the index'''

    print(f'\nRemoving {len(stopwords)} from the index...')
    to_remove = [t for t in index if t in stop_words]

    for token in to_remove:
        del index[token]

    return index


def update_table(table: dict, oldname: str, newname: str, newindex: dict) -> dict:

    def percent(p: float): return round(p, 2)  # display floats in percentage format

    table = table.copy()  # It's a small dict, let's try to remain functional
    table[newname] = {}

    orig_token_count = table['unfiltered']['tokens']['number']
    prev_token_count = table[oldname]['tokens']['number']
    curr_token_count = len(newindex)

    deltaDiff = percent((prev_token_count - curr_token_count) / prev_token_count * 100)
    totalDiff = percent((orig_token_count - curr_token_count) / orig_token_count * 100)

    table[newname]['tokens'] = {
        'number': curr_token_count,
        'delta %': deltaDiff,
        'total %':  totalDiff,
    }

    orig_ptg_count = table['unfiltered']['non-positional postings']['number']
    prev_ptg_count = table[oldname]['non-positional postings']['number']
    curr_ptg_count = sum([newindex[token][0] for token in newindex])  # index 0 contains frequencies

    deltaDiff = percent((prev_ptg_count - curr_ptg_count) / prev_ptg_count * 100)
    totalDiff = percent((orig_ptg_count - curr_ptg_count) / orig_ptg_count * 100)

    table[newname]['non-positional postings'] = {
        'number': curr_ptg_count,
        'delta %': deltaDiff,
        'total %': totalDiff
    }

    return table


def display_table(table: dict) -> str:
    '''Returns a properly formatted string of the compression table'''
    
    display = '\noperations\t\t\ttokens\t\t\t\t\tpostings\n'
    display += '\t\t\tnumber\t∆%\tT%'*2 + '\n\n'

    for index_type in table:
        display += index_type+'\t'
        for i in ['tokens', 'non-positional postings']:
            x = table[index_type][i]
            display += f"\t{x['number']}\t{x['delta %']}\t{x['total %']}\t\t"
        display += '\n'

    return display


def run():
    args = init_params()

    print(f'\nCompression performed on {args.input_file} and stored in {args.output_file}')

    unfiltered: dict = utils.load_index(args.input_file)

    table = {
        'unfiltered': {
            'tokens': {
                'number': len(unfiltered),
                'delta %': round(0.0, 2),
                'total %': round(0.0, 2)
            },
            'non-positional postings': {
                'number': sum([unfiltered[token][0] for token in unfiltered]),
                'delta %': round(0.0, 2),
                'total %': round(0.0, 2)
            }
        }
    }

    no_numbers: dict = remove_numbers(unfiltered.copy())
    table = update_table(table, 'unfiltered', 'no numbers', no_numbers)

    case_folding: dict = case_fold(no_numbers)
    table = update_table(table, 'no numbers', 'case folding', case_folding)

    remove30 = remove_stop_words(case_folding, stop_words[:30])
    table = update_table(table, 'case folding', '30 stop words', remove30)

    remove150 = remove_stop_words(case_folding, stop_words)
    table = update_table(table, '30 stop words', '150 stop words', remove150)

    final = remove150

    utils.save_index_to_disk(final, args.output_file)

    print(f'\nCompression Table:')
    print(display_table(table))


if __name__ == '__main__':
    run()
