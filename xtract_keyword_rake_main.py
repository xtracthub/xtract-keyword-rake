import os
import re
import time
import json
import nltk
import PyPDF2
import argparse
from rake_nltk import Rake


with open('words_dictionary.json', 'r') as words_file:
    dict_of_words = json.load(words_file)


def read_files(file):
    """Reads a file and returns a string of contents.

    Parameter:
    file (str): File path to file to extract contents of.

    Return:
    docs (str): String of contents from file.
    """
    docs = ""
    with open(file, 'rb') as f:
        t = f.read()
        t = t.decode('utf-8', errors='replace')
        docs += t
    return docs


def pdf_to_text(filepath):
    count = 0
    text = ""

    with open(filepath, 'rb') as pdfFileObj:
        pdf_reader = PyPDF2.PdfFileReader(pdfFileObj)
        num_pages = pdf_reader.numPages
        while count < num_pages:
            pageObj = pdf_reader.getPage(count)
            count += 1
            text += pageObj.extractText()

        return text


def extract_keyword(file_path, top_n=20):
    """Extracts keywords from a file.

    Parameters:
    file_path (str): File path of file to extract keywords from.
    top_n (int): Number of keywords to return.

    Return:
    metadata (dict): Dictionary containing top_n words and their scores.
    """
    tokens = []
    stop_words = ['\n']
    with open(os.getcwd() + '/stop-words-en.txt', 'r') as f:
        stop_words += [x.strip() for x in f.readlines()]

    if file_path.endswith('.pdf'):
        docs = pdf_to_text(file_path)
    else:
        docs = read_files(file_path)

    tokens.extend([x for x in nltk.word_tokenize(docs.lower()) if re.match("[a-zA-Z]{2,}", x)])
    for word in tokens[:]:
        try:
            if not(word.lower() in dict_of_words.keys()):
                tokens.remove(word)
        except:
            tokens.remove(word)
    tokens = ' '.join(map(str, tokens))

    r = Rake(stopwords=stop_words)
    r.extract_keywords_from_text(tokens)
    word_degrees = sorted(r.get_word_degrees().items(), key=lambda item: item[1], reverse=True)

    metadata = {"keywords": {}}
    metadata["keywords"].update(word_degrees[:top_n])

    return metadata


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--path', help='Filepath to extract keywords from',
                        required=True, type=str)

    args = parser.parse_args()

    t0 = time.time()
    meta = extract_keyword(args.path)
    print(meta)
    t1 = time.time()
    print(t1 - t0)

