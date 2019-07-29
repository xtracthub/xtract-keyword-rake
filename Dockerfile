FROM python:latest

COPY xtract_keyword_rake_main.py stop-words-en.txt words_dictionary.json /

RUN pip install nltk PyPDF2 rake_nltk

ENTRYPOINT ["python", "xtract_keyword_rake_main.py"]
