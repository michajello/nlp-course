from os import listdir
import numpy as np
from elasticsearch import Elasticsearch
import regex as re
from collections import Counter
import lir

es = Elasticsearch()
index_name = 'my_index_multi'

dataset_path = "../dataset"
filtered_bigrams = Counter()
filtered_tokens = Counter()

files = [f for f in listdir(dataset_path)]

for file in files:
    with open(dataset_path + "/" + file, mode='r', encoding='utf-8') as doc:
        result = es.indices.analyze(index=index_name, body={
            "analyzer": "analyzer_shingle",
            "text": doc.read()})

        bigrams = Counter(
            [r['token'] for r in result['tokens'] if re.match("\p{L}+\s\p{L}+", r['token']) and r['type'] == 'shingle'])
        tokens = Counter(
            [r['token'] for r in result['tokens'] if re.match("\p{L}+", r['token']) and r['type'] == "<ALPHANUM>"])
        filtered_bigrams.update(bigrams)
        filtered_tokens.update(tokens)


def pmi(bigram):
    words = bigram.split(' ')
    a = (filtered_bigrams[bigram]) / sum(filtered_bigrams.values())
    b = (filtered_tokens[words[0]]) / sum(filtered_tokens.values())
    c = (filtered_tokens[words[1]]) / sum(filtered_tokens.values())
    return np.log(a / (b * c))


pmis = sorted([(x, pmi(x)) for x in filtered_bigrams.keys()], key=lambda x: (-1) * x[1])
print("PMI: ", pmis[:30])


def llr_fun(bigram):
    words = bigram.split(' ')
    w1 = words[0]
    w2 = words[1]
    k11 = filtered_bigrams.get(bigram)
    k12 = k21 = 0
    for b in filtered_bigrams.items():
        tokens = b[0].split(' ')
        if tokens[0] == w1 and tokens[1] != w2:
            k12 += 1
        if tokens[0] != w1 and tokens[1] == w2:
            k21 += 1

    k22 = sum(filtered_bigrams.values()) - k11 - k21 - k12
    return k11, k12, k21, k22


llrs = [(b, lir.llr_2x2(*llr_fun(b))) for b in filtered_bigrams.keys()]

print("LLR: ", sorted(llrs[:30], key=lambda x: -x[1]))

