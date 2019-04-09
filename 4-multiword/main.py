from os import listdir
import numpy as np
from elasticsearch import Elasticsearch
import regex as re
from collections import Counter

es = Elasticsearch()
index_name = 'my_index_multi'

ids = [i["_id"] for i in es.search(index=index_name, doc_type="_doc",
                                   body={
                                       "query": {
                                           "match_all": {}
                                       }
                                   },
                                   size=1300
                                   )["hits"]["hits"]]

data_counter = Counter()

dataset_path = "../dataset"
filtered_bigrams = Counter()
filtered_tokens = Counter()

files = [f for f in listdir(dataset_path) if "1993" in f]

for file in files:
    with open(dataset_path + "/" + file, mode='r', encoding='utf-8') as doc:
        result = es.indices.analyze(index=index_name, body={
            "analyzer": "analyzer_shingle",
            "text": doc.read()})

        bigrams = Counter(
            [r['token'] for r in result['tokens'] if re.match("\p{L}+\s\p{L}+", r['token']) and r['type'] == 'shingle'])
        tokens = Counter([r['token'] for r in result['tokens'] if re.match("\p{L}+", r['token']) and r['type'] == "<ALPHANUM>"])
        filtered_bigrams.update(bigrams)
        filtered_tokens.update(tokens)

        print(filtered_bigrams)
        print(filtered_tokens)


def pmi(bigram):
    words = bigram.split(' ')
    a = (filtered_bigrams[bigram]) / sum(filtered_bigrams.values())
    b = (filtered_tokens[words[0]]) / sum(filtered_tokens.values())
    c = (filtered_tokens[words[1]]) / sum(filtered_tokens.values())
    return np.log(a / (b * c))


pmis = sorted([(x, pmi(x)) for x in filtered_bigrams.keys()], key=lambda x: (-1) * x[1])

print(pmis  [:30])


