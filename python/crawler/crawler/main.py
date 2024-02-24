# Kashapova Dilyara, 11-001

import urllib.error
from urllib.request import urlopen

post_id = 89123
N_step = 50
my_link = "https://habr.com/ru/post/"
pages_folder = "pages/"
index_pages_name = "index.txt"

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
