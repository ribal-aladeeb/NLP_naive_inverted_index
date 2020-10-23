from indexer import save_index_to_disk
import query
import indexer


def test_index_loader():
    '''
    Ensure that the generated index is the same as the one loaded from file
    when executing a query.
    '''

    default_corpus_input_dir = 'data'
    default_index_output_file = 'output/test_index.txt'
    inverted_index = indexer.from_scratch_index_creation(default_corpus_input_dir)
    save_index_to_disk(inverted_index, default_index_output_file)
    loaded_index = query.load_index(default_index_output_file)
    assert(loaded_index == inverted_index), f'The loaded index is not equivalent to the original one'

