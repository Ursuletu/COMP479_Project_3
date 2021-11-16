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

    reader.extract_data()
