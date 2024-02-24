from natasha import Doc, Segmenter, MorphVocab, NewsEmbedding, NewsMorphTagger

segmenter = Segmenter()
morph_vocab = MorphVocab()
emb = NewsEmbedding()
morph_tagger = NewsMorphTagger(emb)

inverted_index_file = "inverted_indexes.txt"
indexes = {}

# из файла выделяем индексы
with open(inverted_index_file, 'r', encoding="utf-8") as f:
    lines = f.readlines()
    for line in lines:
        pages_arr = line.split(' ')
        pages_arr = [x.replace(r'\n', '') for x in pages_arr]
        indexes[pages_arr[0]] = {int(k) for k in pages_arr[1:]}

# процесс поиска
while True:
    print("Введите запрос:")
    search_request = input().replace("(", " ( ").replace(")", " ) ").split(' ')
    search_request = list(filter(None, search_request))
    brackets_count = 0

    # проверка скобок
    for e in search_request:
        if e == '(':
            brackets_count += 1
        if e == ')':
            brackets_count -= 1
    if brackets_count > 0:
        search_request = search_request + [')'] * brackets_count
    if brackets_count < 0:
        search_request = ['('] * -brackets_count + search_request

    # () > not > and > or
    search_request_final = "("
    for i in range(0, len(search_request)):
        x = search_request[i].lower()
        if x == 'and':
            search_request[i] = x
            search_request_final += ").intersection("
        elif x == 'not':
            search_request[i] = x
            search_request_final += ").difference("
        elif x == 'or':
            search_request[i] = x
            search_request_final += ").union("
        elif x == '(':
            search_request[i] = x
            search_request_final += "("
        elif x == ')':
            search_request[i] = x
            search_request_final += ")"
        else:
            doc = Doc(x)
            doc.segment(segmenter)
            doc.tag_morph(morph_tagger)
            doc.tokens[0].lemmatize(morph_vocab)
            lemma = doc.tokens[0].lemma.lower()
            search_request[i] = lemma
            if lemma in indexes.keys():
                search_request_final += str(indexes[lemma])
            else:
                search_request_final += "set()"
    search_request_final += ")"

    # полученное выражение с замененными операторами
    #print(search_request_final)
    #eval - полезна, когда необходимо выполнить динамически обновляемое выражение Python из какого-либо ввода
    search_request_result = eval(search_request_final)

    if len(search_request_result) == 0:
        print("Pages not found")
    else:
        print("Search request result: " + str(search_request_result) + "\n")
