# NLP naive inverted index
Using the Reuters21578 corpus, Build a naive inverted index which would allow
you to query words and return as a result all the documents (i.e. reuters' news
articles containing said word).

To download the corpus on your machine type `./download_corpus.sh` or `sh
download_corpus.sh` at the root of the project (provided you have a unix based
OS, otherwise download the data manually
[here](http://www.daviddlewis.com/resources/testcollections/reuters21578/) and
put it in a folder called data at the root of the project). 

Make sure you
have nltk installed by typing `conda install nltk` or `pip install nltk`
depending on the package manager that you use.

### Creating the index
type `python indexer.py` to generate the index and store it in
`output/inverted_index.txt` if you wish to specify another output file just pass
it as argument with the `-o` or `--ouput_file` flag.

### Compressing the index
To compress your index type `python compressor.py`. By default, the compresser
will use `output/inverted_index.txt` as it's input file and
`output/compressed_index.txt` as its output file. You can change both these
defaults with `-i` or `--input_file` and `-o` or `--output_file` respectively.

### Querying your index
type `python query.py -q <insert a single word>`. By default the query script
will take as input the index stored in `output/inverted_index.txt` and will
store the result of the query in `output/sampleQueries.json`. Similarly, you can
change the defaults with `-i` or `--input_file` and `-o` or `--output_file`
respectively.

Keep in mind that the uncompressed index contains terms with variable casing, so
if you query the word airplane, you will get case-sensitive results. However, if
you are querying a compressed index, you should keep all characters lower-cased
because the compression step will lowercase all dictionary terms. In this case,
querying the word airplane will returns case-insenstive results and having a
single upper case character while querying a compressed index is garanteed to
return 0 results.
