import regex as re
import http.client
import lir
from os import listdir
from collections import Counter


def llrs(bigram_counter, tokens_counter):

    llrs_list = []
    total_count = sum(bigram_counter.values())
    for bigram, count in bigram_counter.items():
        k11 = count
        k12 = tokens_counter[bigram[1]] - count
        k21 = tokens_counter[bigram[0]] - count
        k22 = total_count - tokens_counter[bigram[1]] - tokens_counter[bigram[0]]
        llr_value = lir.llr_2x2(k11, k12, k21, k22)
        llrs_list.append((bigram, llr_value))
    return llrs_list


dataset_path = "../dataset"

files = [f for f in listdir(dataset_path)]
con = http.client.HTTPConnection('localhost', port=9200)
bigram_counter, tokens_counter = Counter(), Counter()

for f in files:
    previous_token = "[]"
    with open(dataset_path + "/" + f, mode='r', encoding='utf-8',) as _f:
        text = _f.read().lower()
        con.request(method="POST", url="", body=text.encode('utf-8'))
        result = con.getresponse().readlines()
        result = [line.decode("utf-8") for line in result if "disamb" in line.decode("utf-8")]

        for line in result:
            line = line.split("\t")
            word = line[1]
            tag = line[2].split(":")[0]

            token = word + ":" + tag
            if re.match("\p{L}+", word):
                if re.match("\p{L}+", previous_token):
                    bigram_counter.update([(previous_token, token)])
                previous_token = token
                tokens_counter.update([token])
            else:
                previous_token = "[]"

llrs = sorted(llrs(bigram_counter, tokens_counter), key=lambda x: x[1], reverse=True)
top50_llrs = [x for x in llrs if x[0][0].split(":")[1] == "subst" and x[0][1].split(":")[1] in ["adj", "subst"]][:50]

print(top50_llrs)



