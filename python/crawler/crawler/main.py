# Kashapova Dilyara, 11-001

import urllib.error
from urllib.request import urlopen

import pymorphy2
from bs4 import BeautifulSoup
from natasha import (Doc, MorphVocab, Segmenter, NewsEmbedding, NewsMorphTagger)
import re

post_id = 89123
N_step = 50
my_link = "https://habr.com/ru/post/"
pages_folder = "pages/"
index_pages_name = "index.txt"

is_downloaded = True
tokens_file = "tokens.txt"
lemmas_tokens_file = "lemmas.txt"

## task 1
# пропускаем этот этап
if not is_downloaded:
    index_file = open(index_pages_name, 'w', encoding="utf-8")
    count = 0

    # считывем посты по ссылке => сохраняем в файл index.txt и папку pages ('выкачка')
    for i in range(0, 100):
        while True:
            current_i = i + count
            url = my_link + str(post_id - current_i * N_step)
            try:
                with urlopen(url) as response:
                    page_body = response.read().decode()
                    with open(pages_folder + str(i) + ".txt", 'w', encoding="utf-8") as f:
                        f.write(page_body)
                    index_file.write(str(i) + ": " + url + "\n")
                print(i, ": page finished download")
                break
            except urllib.error.HTTPError:
                print("Can't download: error on page", (post_id - current_i * N_step))
                count += 1
    index_file.close()

REMOVE_MORPH = ['ADJ', 'NOUN', 'PROPN', 'VERB']
morph = MorphVocab()
segmenter = Segmenter()
emb = NewsEmbedding()
morph_tagger = NewsMorphTagger(emb)

all_lemmas = {}
all_lemmas_indexes = {}

for i in range(0, 100):
    f = open(pages_folder + str(i) + ".txt", 'r', encoding="utf-8")
    soup = BeautifulSoup(f.read(), features="html.parser")
    f.close()

    # удаляем ненужное => css & js
    for script in soup(["script", "style"]):
        script.extract()

    text = soup.get_text()

    text = re.sub(r"\d+", "", text, flags=re.UNICODE)
    text = re.sub(r"[${}_\\-]", " ", text)
    # разбить на строки и удалить начальный и конечный пробелы в каждой
    lines = (line.strip() for line in text.splitlines())
    chunks = (phrase.strip() for line in lines for phrase in line.split(" "))
    # опустить пустые строки
    text = ' '.join(chunk for chunk in chunks if chunk)

    doc = Doc(text)
    doc.segment(segmenter)
    doc.tag_morph(morph_tagger)

    for token in doc.tokens:
        if token.pos in REMOVE_MORPH:
            token.lemmatize(morph)
            lemma = token.lemma.lower()
            if lemma not in all_lemmas:
                all_lemmas[lemma] = set()
                all_lemmas_indexes[lemma] = set()
            all_lemmas[lemma].add(token.text.lower())
            all_lemmas_indexes[lemma].add(i)


lem_f = open(lemmas_tokens_file, 'w', encoding="utf-8")
tot_f = open(tokens_file, 'w', encoding="utf-8")

for key in all_lemmas.keys():
    lem_f.write(key + ":")
    for s_el in all_lemmas[key]:
        lem_f.write(" " + s_el)
        tot_f.write(s_el + "\n")
    lem_f.write("\n")

lem_f.close()
tot_f.close()
