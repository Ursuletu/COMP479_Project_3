from datetime import datetime
import os
import string

from bs4 import BeautifulSoup
from nltk.tokenize import word_tokenize
from nltk.stem import *


# Extracts article body and id from reuters corpus .sgm files and returns a dictionary with each term pointing to a
# list of article ids in which the term appears.
def extract_data():
    now = datetime.now()
    index = {}

    for file in sorted(os.listdir(os.getcwd() + '/reuters_files/')):
        if file.endswith(".sgm"):
            with open(os.getcwd() + '/reuters_files/' + file, 'rb') as f:
                data = f.read()
                f.close()

            soup = BeautifulSoup(data, 'html.parser')
            articles = soup.find_all('reuters')

            for tag in articles:
                if len(tag('body')) > 0:
                    body = word_tokenize(str(tag('body')[0].contents[0]))
                    ids = str(tag['newid'])
                    for token in body:
                        if token in string.punctuation:  # Checks if token is part of Python's list of punctuations
                            break
                        else:
                            if token in index:
                                index[token].append(int(ids))
                            else:
                                index[token] = [int(ids)]


    #print(index)
    print("SPIMI inspired procedure time: " + str(datetime.now() - now))
    return index


# Takes a dictionary and searches for a single term query
def search_in_index(query, index):
    if query in index:
        print('Number of articles mentioning ' + str(query) + ': ' + str(len(index[query])))
    else:
        print('No articles mentioning ' + str(query) + ' found.')


# Takes index and outputs it to a file in the local folder
def output_to_file(index):

    with open('index.txt', 'w') as file:
        for key, value in sorted(index.items()):
            file.write(key + ': ')
            file.write(str(value))
            file.write('\n')
    file.close()


# Takes index and returns an index without numbers (defined as strings that do not contain any alphabetic characters)
def compress_index_no_numbers(index):
    compressed_index = dict(index)

    for entry in index:
        if not any(character.isalpha() for character in entry):
            del compressed_index[entry]

    return compressed_index


# Takes index and returns a down-cased index. Postings lists belonging to case variations are merged
def compress_index_case_folding(index):
    compressed_index = {}

    for entry in index:
        # If entry exists, append to list of document IDs
        if (entry.lower()) in compressed_index:
            compressed_index[entry.lower()].extend(index[entry])
        # Else, create new index entry for down-cased entry
        else:
            compressed_index[entry.lower()] = index[entry]

    # Sort postings list and remove duplicates
    for entry in compressed_index:
        compressed_index[entry] = sorted(set(compressed_index[entry]))

    return compressed_index


# Takes an a list of stop words and removes them from the index
def compress_index_stop_words(words, index):
    compressed_index = dict(index)

    for w in words:
        if w in compressed_index:
            del compressed_index[w]

    return compressed_index


# Takes an index and stems keys
def compress_index_stem(index):
    compressed_index = {}
    stemmer = PorterStemmer()

    for entry in index:
        # If entry exists, append to list of document IDs
        if (stemmer.stem(entry)) in compressed_index:
            compressed_index[stemmer.stem(entry)].extend(index[entry])
        # Else, create new index entry for stemmed entry
        else:
            compressed_index[stemmer.stem(entry)] = index[entry]

    return compressed_index


# Takes an index and outputs its postings length
def postings_length(index):
    postings = 0
    for entry in index:
        postings = postings + len(index[entry])
    return postings
