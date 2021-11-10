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

    # Create all dictionaries required:
    dictionary_default = reader.extract_data()
    dictionary_numberless = reader.compress_index_no_numbers(dictionary_default)
    dictionary_downcased = reader.compress_index_case_folding(dictionary_numberless)
    dictionary_no_stop_words1 = reader.compress_index_stop_words(stop_words30, dictionary_downcased)
    dictionary_no_stop_words2 = reader.compress_index_stop_words(stop_words150, dictionary_downcased)
    dictionary_stemmed = reader.compress_index_stem(dictionary_downcased)  # in relation to dictionary_downcased

    # Calculating length of each dictionary:
    default_length = len(dictionary_default)
    no_numbers_length = len(dictionary_numberless)
    case_folding_length = len(dictionary_downcased)
    stop_words_30_length = len(dictionary_no_stop_words1)
    stop_words_150_length = len(dictionary_no_stop_words2)
    stemming_length = len(dictionary_stemmed)

    # Calculating length of each dictionary's postings list
    postings_default = reader.postings_length(dictionary_default)
    postings_no_numbers = reader.postings_length(dictionary_numberless)
    postings_case_folding = reader.postings_length(dictionary_downcased)
    postings_30_words = reader.postings_length(dictionary_no_stop_words1)
    postings_150_words = reader.postings_length(dictionary_no_stop_words2)
    postings_stemmed = reader.postings_length(dictionary_stemmed)

    # Query Search:
    print('Query search for three sample queries (project, apple, airplane) in naive index: ')
    reader.search_in_index('project', dictionary_default)
    reader.search_in_index('apple', dictionary_default)
    reader.search_in_index('airplane', dictionary_default)
    print()

    print('Query search for three sample queries (project, apple, airplane) in compressed index: ')
    reader.search_in_index('project', dictionary_stemmed)
    reader.search_in_index('apple', dictionary_stemmed)
    reader.search_in_index('airplane', dictionary_stemmed)
    print()

    print('Query search for challenge words (pineapple, Phillippines, Brierley, Chrysler) in naive index: ')
    reader.search_in_index('pineapple', dictionary_default)
    reader.search_in_index('Phillippines', dictionary_default)
    reader.search_in_index('Philippines', dictionary_default)
    reader.search_in_index('Brierley', dictionary_default)
    reader.search_in_index('Chrysler', dictionary_default)
    print()

    print('Query search for challenge words (pineapple, Phillippines, Brierley, Chrysler) in compressed index: ')
    reader.search_in_index('pineapple', dictionary_stemmed)
    reader.search_in_index('Phillippines', dictionary_stemmed)
    reader.search_in_index('Philippines', dictionary_stemmed)
    reader.search_in_index('Brierley', dictionary_stemmed)
    reader.search_in_index('Chrysler', dictionary_stemmed)
    print()

    stemmer = PorterStemmer()

    print('Query search for challenge words after stemming query (pineapple, Phillippines, Brierley, Chrysler) in compressed index: ')
    reader.search_in_index(stemmer.stem('pineapple'), dictionary_stemmed)
    reader.search_in_index(stemmer.stem('Phillippines'), dictionary_stemmed)
    reader.search_in_index(stemmer.stem('Philippines'), dictionary_stemmed)
    reader.search_in_index(stemmer.stem('Brierley'), dictionary_stemmed)
    reader.search_in_index(stemmer.stem('Chrysler'), dictionary_stemmed)
    print()

    # Creating table for stats
    # Percentage Decrease = (Starting Value − Final Value) / (Starting Value) × 100
    t = PrettyTable([' ', 'Distinct Terms', '%Δ(dt)', '%T(dt)', '', 'Non-Positional Postings', '%Δ(np)', '%T(np)'])
    t.add_row(['unfiltered', default_length, 'DNA', 'DNA', '', postings_default, 'DNA', 'DNA'])
    t.add_row(['no numbers', no_numbers_length, round((default_length - no_numbers_length) / default_length * 100, 2),
               round((default_length - no_numbers_length) / default_length * 100, 2), '', postings_no_numbers,
               round((postings_default - postings_no_numbers) / postings_default * 100, 2),
               round((postings_default - postings_no_numbers) / postings_default * 100, 2)])
    t.add_row(['case folding', case_folding_length,
               round((no_numbers_length - case_folding_length) / no_numbers_length * 100, 2),
               round((default_length - case_folding_length) / default_length * 100, 2), '', postings_case_folding,
               round((postings_no_numbers - postings_case_folding) / postings_no_numbers * 100, 2),
               round((postings_default - postings_case_folding) / postings_default * 100, 2)])
    t.add_row(['30 stop words', stop_words_30_length,
               round((case_folding_length - stop_words_30_length) / case_folding_length * 100, 2),
               round((default_length - stop_words_30_length) / default_length * 100, 2), '', postings_30_words,
               round((postings_case_folding - postings_30_words) / postings_case_folding * 100, 2),
               round((postings_default - postings_30_words) / postings_default * 100, 2)])
    t.add_row(['150 stop words', stop_words_150_length,
               round((case_folding_length - stop_words_150_length) / case_folding_length * 100, 2),
               round((default_length - stop_words_150_length) / default_length * 100, 2), '', postings_150_words,
               round((postings_case_folding - postings_150_words) / postings_case_folding * 100, 2),
               round((postings_default - postings_150_words) / postings_default * 100, 2)])
    t.add_row(
        ['stemming', stemming_length, round((case_folding_length - stemming_length) / case_folding_length * 100, 2),
         round((default_length - stemming_length) / default_length * 100, 2), '', postings_stemmed,
         round((postings_case_folding - postings_stemmed) / postings_case_folding * 100, 2),
         round((postings_default - postings_stemmed) / postings_default * 100, 2)])

    print(t)
