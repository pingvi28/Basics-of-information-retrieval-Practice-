from numpy import dot
from numpy.linalg import norm
import re
from natasha import Doc, Segmenter, MorphVocab, NewsEmbedding, NewsMorphTagger

segmenter = Segmenter()
morph_vocab = MorphVocab()
emb = NewsEmbedding()
morph_tagger = NewsMorphTagger(emb)
REMOVE_MORPH = ['ADJ', 'NOUN', 'PRON', 'VERB']

class Search_system:
    index_file_name = "index.txt"
    lemmas_tf_idf_files_folder = "page_lemmas_tf_idf/"

    def __init__(self):
        self.segmenter = Segmenter()
        self.morph_vocab = MorphVocab()
        emb = NewsEmbedding()
        self.morph_tagger = NewsMorphTagger(emb)

        self.lemmas_tfidf = []

        # подгружаем леммы
        for i in range(0, 100):
            with open(self.lemmas_tf_idf_files_folder + str(i) + ".txt", 'r', encoding="utf-8") as f:
                self.lemmas_tfidf.append({})
                lines = f.readlines()
                for line in lines:
                    arr = line.split(' ')
                    self.lemmas_tfidf[i][arr[0]] = [float(arr[1]), float(arr[2])]

        self.index_to_links = {}

        #подгружаем ссылки
        with open(self.index_file_name, 'r', encoding="utf-8") as f:
            lines = f.readlines()
            for line in lines:
                arr = line.split(' ')
                arr[0] = arr[0].replace(r':', '')
                self.index_to_links[int(arr[0])] = arr[1][:-1]

    def search(self, request):

        doc = Doc(request)
        doc.segment(segmenter)
        doc.tag_morph(morph_tagger)

        search_request = []

        for token in doc.tokens:
            if token.pos in REMOVE_MORPH:
                token.lemmatize(morph_vocab)
                search_request.append(token.lemma.lower())

        # reset input words by lemmas
        unique_lemmas = {}
        total_lemmas = 0
        for i in range(0, len(search_request)):
            doc = Doc(search_request[i])
            doc.segment(self.segmenter)
            doc.tag_morph(self.morph_tagger)
            doc.tokens[0].lemmatize(self.morph_vocab)
            lemma = doc.tokens[0].lemma.lower()
            search_request[i] = lemma
            if lemma not in unique_lemmas.keys():
                unique_lemmas[lemma] = 0
            unique_lemmas[lemma] += 1
            total_lemmas += 1

        # get tf-idf for input
        search_request_tf = {}
        for key in unique_lemmas.keys():
            search_request_tf[key] = unique_lemmas[key] / total_lemmas

        # vector search
        results = {}
        for i in range(0, 100):
            cur_file_lemmas = self.lemmas_tfidf[i]
            list1 = []
            list2 = []
            for key in cur_file_lemmas.keys():
                list1.append(cur_file_lemmas[key][0])
                list2.append(search_request_tf[key] if key in search_request_tf.keys() else 0.0)
            if norm(list2) == 0:
                continue
            result = dot(list1, list2) / (norm(list1) * norm(list2))
            if result == 0:
                continue
            results[i] = result

        sorted_pages_indexes = sorted(results, reverse=False)
        return [self.index_to_links[index] for index in sorted_pages_indexes]

