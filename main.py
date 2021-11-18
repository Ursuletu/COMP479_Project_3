import math

import reader as reader
from prettytable import PrettyTable
from nltk.corpus import stopwords
from nltk.stem import *

if __name__ == '__main__':

    # Generate two arrays of 30 and 150 words from the first 30 and 150 words in ntlk's english stop words list
    stop_words30 = []
    stop_words150 = []

    i = 0
    for word in stopwords.words('english'):
        stop_words30.extend([word])
        i = i + 1
        if i == 29:
            i = 0
            break

    for word in stopwords.words('english'):
        stop_words150.extend([word])
        i = i + 1
        if i == 149:
            break

    # Index mapping each id to its body
    index = reader.get_index().copy()

    # Inverted index mapping term to list of articles it appears in
    inverted_index = reader.get_inverted_index().copy()

    # Dictionary mapping article ID to its length. Also has 'avg' and 'total' article properties
    article_properties = reader.get_docs_length_and_average().copy()

    query = input("Input your search query: ")

    # Base values
    N = 21577
    k = 5
    b = 0.5
    dft = 0 # Number of documents that contain term t
    tfd = 0 # Number of times term t appears in a document
    retrieval_status_value = 0
    doc_length = 0

    N = article_properties['total']
    avg = article_properties['avg']

    for word in query.split():
        if word in inverted_index: # If query term in dictionary:
            list_of_articles = inverted_index[word] # List of article IDs containing the query term
            print("List of articles for term " + str(word) + " " + str(list_of_articles))

            dft = len(list_of_articles) # How many documents the term appears in
            print("The term appears in a total of " + str(dft) + " articles")
            print()

            for article_id in list_of_articles: # For each article in the list:
                tfd = 0
                doc_length = len(index[str(article_id)]) # Article length
                for token in index[str(article_id)]: # For each token in the body of each article:
                    if token == word: # If the token is found in the article, increment its counter (tfd) by 1
                        tfd = tfd + 1

                print('The term ' + word + ' appears ' + str(tfd) + ' times in article ' + str(article_id))
                print('Article ' + str(article_id) + ' has length ' + str(doc_length))

                article_score = (math.log(N/dft)) * ((k + 1) * tfd)/((k * ((1 - b) + b * (doc_length / avg))) + tfd)
                print('Article ' + str(article_id) + ' score: ' + str(article_score))
                print()
