from bs4 import BeautifulSoup
from natasha import Doc, Segmenter, NewsEmbedding, NewsMorphTagger, MorphVocab
import re

index_file = "index.txt"
pages_folder = "pages/"
lemmas_tf_idf_files_folder = "page_lemmas_tf_idf/"
tokens_tf_idf_files_folder = "page_tokens_tf_idf/"

tokens_file = "tokens.txt"
lemmas_tokens_file = "lemmas.txt"
inverted_index_file = "inverted_indexes.txt"

REMOVE_MORPH = ['ADJ', 'NOUN', 'PRON', 'VERB']
segmenter = Segmenter()
morph_vocab = MorphVocab()
emb = NewsEmbedding()
morph_tagger = NewsMorphTagger(emb)

tokens_indexes = {}
lemmas_indexes = {}

for i in range(0, 100):
    with open(pages_folder + str(i) + ".txt", 'r', encoding="utf-8") as f:
        soup = BeautifulSoup(f.read(), features="html.parser")

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
            token.lemmatize(morph_vocab)
            lemma = token.lemma.lower()
            text = token.text.lower()

            if lemma not in lemmas_indexes:
                lemmas_indexes[lemma] = set()
            lemmas_indexes[lemma].add(i)

            if text not in tokens_indexes:
                tokens_indexes[text] = set()
            tokens_indexes[text].add(i)

for i in range(0, 100):
    with open(pages_folder + str(i) + ".txt", 'r', encoding="utf-8") as f:
        soup = BeautifulSoup(f.read(), features="html.parser")

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

    total_tokens_count = 0
    unique_tokens = {}
    unique_lemmas = {}

    for token in doc.tokens:
        if token.pos in REMOVE_MORPH:
            token.lemmatize(morph_vocab)
            text = token.text.lower()
            lemma = token.lemma.lower()

            total_tokens_count += 1
            if text not in unique_tokens.keys():
                unique_tokens[text] = 0
            unique_tokens[text] += 1
            if lemma not in unique_lemmas.keys():
                unique_lemmas[lemma] = 0
            unique_lemmas[lemma] += 1

    # подсчет tf-idf у токенов
    with open(tokens_tf_idf_files_folder + str(i) + ".txt", 'w', encoding="utf-8") as f:
        for key in tokens_indexes.keys():
            tf = unique_tokens[key] / total_tokens_count if key in unique_tokens.keys() else 0.0
            f.write(key + " " + str(tf) + " " + str(tf * 100 / len(tokens_indexes[key])) + "\n")

    # подсчет tf-idf у лемм токенов
    with open(lemmas_tf_idf_files_folder + str(i) + ".txt", 'w', encoding="utf-8") as f:
        for key in lemmas_indexes.keys():
            tf = unique_lemmas[key] / total_tokens_count if key in unique_lemmas.keys() else 0.0
            f.write(key + " " + str(tf) + " " + str(tf * 100 / len(lemmas_indexes[key])) + "\n")
