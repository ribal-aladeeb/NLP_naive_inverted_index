'''
This block will convert the corpus into a list of term-docID pairs. This 
'''

import argparse
import os
from os import remove, removexattr
import sys
from typing import List, Tuple
import utils
import nltk
from tqdm import tqdm


def init_params():
    parser = argparse.ArgumentParser(description='Process command line arguments')
    parser.add_argument('-i', '--input_file', default='data', help='Input file')
    parser.add_argument('-o', '--output_file', default=sys.stdout, help='Output file')  # Does not include any directory names, strictly the filenames
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

                docs.append(document)

                start_idx = end_idx
                end_idx = start_idx + 1

            else:
                still_looking = False

    return docs


def extract_text_tag_contents(doc: str) -> List[str]:
    return doc[doc.find('<TEXT'):doc.find('</TEXT>')+len('</TEXT>')]


def remove_tags(doc: str) -> str:
    '''
    Removes any tags inside of doc. Should only be applied to a string that
    starts and ends with <TEXT> </TEXT> (output of extract_text_tag_contents
    func).
    '''
    doc_content = doc
    tag_start = doc_content.find('<')

    while tag_start >= 0 :  # implies the substring exists

        tag_end: int = doc_content.find('>', tag_start)
        tag_type: str = doc_content[tag_start+1:tag_end]

        # print(f'TAG TYPE: ->>>>>>{tag_type}')

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


def generate_pairs(docs: List[str]) -> Tuple[str, int]:
    '''Generate term-docID tuples'''
    pairs = []
    tokenizer = nltk.RegexpTokenizer(r'\w+')
    
    for id in tqdm(range(len(docs))):
        tokenized = tokenizer.tokenize(docs[id])
        for token in tokenized:
            pairs.append((token, id))

    return pairs



def run() -> None:
    # def run(indir: str, outfile) -> None:
    args = init_params()
    indir = args.input_file
    outfile = f'output/{args.output_file}' if type(args.output_file) == str else args.output_file
    lines: list = unpack_corpus_step1(indir)
    utils.write2disk(lines, outfile)


def run_one_shot():
    args = init_params()
    indir = args.input_file
    lines = unpack_corpus_step1(indir)
    # docs: List[str] = segment_docs(lines)
    docs = document_extracter(lines)

    print(f'documents length {len(docs)}')
    for i in range(5):
        print('\n\n' + '++++++++++'*5 + ' NORMAL DOC:')
        print()
        print(docs[-i])
        print()
        print('='*20)
        print()
        print('++++++++++'*5 + ' EXTRACTED NORMAL DOC:')
        print(remove_tags(extract_text_tag_contents(docs[-i])))
        print()
    exit()

    spec_trimmed = trimdocs(special[:10])
    timeed = trimdocs(docs[:10])
    exit()
    for i in range(3):
        print(docs[i])
        print('\n\n')
    exit()
    print(f'documents length {len(docs)}')
    print(f'special docs length {len(special)}')
    # for i in range(5):
    #     print(special[i])
    count = 0
    for i in tqdm(range(len(special))):
        if special[i].find('<TITLE') < 0 or special[i].find('</TITLE>') < 0:
            print(special[i])
            print(f'\n************ DOC {i} has no title tag\n\n')
            count += 1
    print(f'\n{count} docs do not have a title tag out of {len(special)}')
    exit()
    pairs: Tuple[str, int] = generate_pairs(docs)
    # cleaned: Tuple[str, int] = clean_punctuation(pairs)


if __name__ == "__main__":
    run_one_shot()
