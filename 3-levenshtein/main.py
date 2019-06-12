from elasticsearch import Elasticsearch
import Levenshtein
import regex as re
from pprint import pprint
from collections import Counter
import matplotlib.pyplot as plt
import csv

es = Elasticsearch()
index_name = 'my_index_lev'

ids = [h["_id"] for h in es.search(index=index_name, doc_type="_doc",
    body={
        "query": {
            "match_all": {}
        }
    },
    size=1300
)["hits"]["hits"]]

data_counter = Counter()

for idd in ids:
    term_vectors = es.termvectors(index=index_name, doc_type="_doc", id=idd, body={"term_statistics": "true"})["term_vectors"]["text"]["terms"]
    single_counter = Counter(dict([(key, value["term_freq"]) for key, value in term_vectors.items()]))
    data_counter.update(single_counter)

data_counter = Counter(dict([(key.replace('\xad', ''), value) for key, value in data_counter.items() if len(key) > 1 and not re.match(r'\d+', key)]))

poz = [x + 1 for x in range(len(data_counter))]
occurences = [v[1] for v in data_counter.most_common()]

plt.plot(poz, occurences)
plt.xscale('log')
plt.yscale('log')
plt.show()
forms_set = set()

with open('./polimorfologik-2.1/polimorfologik-2.1.txt', 'r', encoding='utf-8') as file:
    reader = csv.reader(file, delimiter=';')
    for row in reader:
        forms_set.add(row[1].lower())


not_existing_words = []

for word in data_counter.most_common():
    if word[0] not in forms_set:
        not_existing_words.append(word)

pprint(not_existing_words[:30])

triple_missing = [x for x in not_existing_words if x[1] == 3]

pprint(triple_missing[:30])

for word in triple_missing[:30]:
    corect = []
    for form in forms_set:
        lev_dist = Levenshtein.distance(word[0], form)
        if lev_dist < 4:
            corect.append((form, lev_dist))

    corect.sort(key=lambda x: x[1])
    print(word)
    pprint(corect[:3])
