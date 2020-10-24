'''
This block will convert the corpus into an inverted index and write the output into any file passed as argument to the script with -o | --output_file
'''

import argparse
import os
import sys
from typing import Iterable, List, Tuple, Dict, Set
import utils
import nltk
from tqdm import tqdm


def init_params():
    parser = argparse.ArgumentParser(description='Process command line arguments')
    parser.add_argument('-i', '--input_file', default='data', help='Input file')
    parser.add_argument('-o', '--output_file', default='output/inverted_index.txt', help='Output file')  # Does not include any directory names, strictly the filenames
    args = parser.parse_args()

    return args


def unpack_corpus_step1(path: str) -> List[str]:
    '''Given corpus <path>, returns a list where element is the full str content of a file'''

    sgmfiles: List[str] = sorted([fname for fname in os.listdir(path) if '.sgm' in fname])
    files_contents = []

    for filename in sgmfiles:
        with open(f'{path}/{filename}', mode='r', encoding='UTF-8', errors='ignore') as file:
            files_contents += [file.read()]

    return files_contents


def document_extracter(lines: List[str]):
    '''
    <lines> is the contents of each .sgm file from the <unpack_corpus_step1>
    func. It is a design decision to include only the contents of the text tags
    for the construction of the index.
    '''

    print("Extracting documents from .sgm file contents")
    docs: List[str] = []
    for line in tqdm(lines):
        still_looking = True
        start_idx = end_idx = 0

        while still_looking:
            start_idx = line.find('<REUTERS', start_idx)

            if start_idx >= 0:  # means that the file still contains the substring

                end_idx = line[start_idx:].find('</REUTERS>') + start_idx + len('</REUTERS>')
                assert end_idx > 0, f"The end Index is negative {end_idx}"

                document: str = line[start_idx:end_idx]

                clean_doc = clean_reccuring_patterns(remove_tags(extract_text_contents(document)))
                docs.append(clean_doc)

                start_idx = end_idx
                end_idx = start_idx + 1

            else:
                still_looking = False

    return docs


def extract_text_contents(doc: str) -> List[str]:
    return doc[doc.find('<TEXT'):doc.find('</TEXT>')+len('</TEXT>')]


def remove_tags(doc: str) -> str:
    '''
    Removes any tags inside of doc. Should only be applied to a string that
    starts and ends with <TEXT> </TEXT> (output of extract_text_tag_contents
    func).
    '''
    doc_content = doc
    tag_start = doc_content.find('<')

    while tag_start >= 0:  # implies the substring exists

        tag_end: int = doc_content.find('>', tag_start)
        tag_type: str = doc_content[tag_start+1:tag_end]

        if tag_type != '/TEXT':
            '''
            Implications: 
                1. Tag must be TITLE or BODY or DATE and needs to be
                removed. 
                2. Add a space so that two words surrounding the tags
                don't get merged into a single one during tokenization purposes.
            '''
            doc_content = doc_content[:tag_start] + doc_content[tag_end+1:]

        else:  # must have reached end of document content
            doc_content = doc_content[:tag_start]

        tag_start = doc_content.find('<')

    return doc_content


def clean_reccuring_patterns(doc: str) -> str:
    '''
    ['&#2;', '&#3;'] are two patterns that occur very often at the begining and
    end of documents respectively. Filter them out of documents before create
    the term-docID pairs reduces the number of pairs from 4.5M to 3M pairs and
    from 17 to 12 seconds of processing.
    '''
    for pattern in ['&#2;', '&#3;']:
        start = doc.find(pattern)
        end = start + len(pattern) + 1
        doc = doc[:start] + ' ' + doc[end:]

    return doc


def generate_term_docID_pairs(docs: List[str]) -> Tuple[str, int]:
    '''Generate term-docID tuples'''

    print('Generating term-docID pairs')
    pairs = []
    tokenizer = nltk.RegexpTokenizer(r'\w+')

    for id in tqdm(range(len(docs))):
        tokenized = tokenizer.tokenize(docs[id])
        for token in tokenized:
            pairs.append((token, id+1))

    return pairs


def generate_inverted_index(pairs: List[Tuple[str, ]]):
    '''
    Given pairs of term_docIDs (which are unsorted and can contain
    duplicates), generate the inverted_index.
    '''

    print('Generating the inverted index')

    inverted_index: Dict[Tuple[int, set]] = {}

    for token, docId in tqdm(pairs):
        _, postings_list = inverted_index.get(token, (0, set()))
        postings_list.add(docId)

        frequency: int = len(postings_list)
        inverted_index[token] = (frequency, postings_list)
        # it's a set, we can't blindly increment because there are potential
        # duplicates in the pairs.

    return inverted_index


def sorted_postings(inverted_index: Dict[str, Tuple[int, set]]) -> Dict[str, Tuple[int, List[int]]]:
    '''Sorts postings lists for each term'''
    sorted_index: Dict[str, Tuple[int, List[int]]] = {}

    for token in inverted_index:
        postings_set: set = inverted_index[token][1]
        sorted_postings: list = sorted(list(postings_set))
        frequencies = inverted_index[token][0]
        sorted_index[token] = (frequencies, sorted_postings)

    return sorted_index


def from_scratch_index_creation(input_dir=None) -> Dict[str, Tuple[int, set]]:
    '''
    Created the inverted index from scratch, i.e from the corpus file
    collection to the dict struct.
    '''
    indir = input_dir if input_dir != None else init_params().input_file
    lines: List[str] = unpack_corpus_step1(indir)
    docs: List[str] = document_extracter(lines)
    pairs: Tuple[str, int] = generate_term_docID_pairs(docs)
    inverted_index: Dict[str, Tuple[int, List[int]]] = sorted_postings(generate_inverted_index(pairs))
    return inverted_index


def save_index_to_disk(inverted_index: Dict[str, Tuple[int, set]], outfile=None) -> None:
    printable: Tuple[str, Tuple[int, List[int]]] = sorted(inverted_index.items(), key=lambda token: token[0])
    output_file = outfile if outfile != None else init_params().output_file
    utils.write2disk(printable, output_file)


def run_one_shot():
    '''Runs the creation of the index and stores it to disk.'''

    inverted_index: Dict[str, Tuple[int, set]] = from_scratch_index_creation()
    save_index_to_disk(inverted_index)


if __name__ == "__main__":
    run_one_shot()
