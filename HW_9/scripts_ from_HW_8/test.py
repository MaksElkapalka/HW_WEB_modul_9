import json

authors_fiile_path = "../beautiful_soup/authors.json"

with open(authors_fiile_path, encoding="utf8") as af:
    data = json.load(af)
    for el in data:
        print(el)
        break
