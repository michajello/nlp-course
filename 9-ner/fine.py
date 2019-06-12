import os
from os import listdir
from os.path import isfile, join
from collections import Counter, OrderedDict
import xml.etree.ElementTree as ET
from pprint import pprint
import numpy as np
import matplotlib.pyplot as plt

onlyfiles = [f for f in listdir("./out_n82") if isfile(join("./out_n82", f))]

freq_stats = Counter()
named_entities = Counter()
for f in onlyfiles:
    tree = ET.parse(os.path.join("./out_n82", f))
    root = tree.getroot()

    for chunk in root:
        for sentence in chunk:
            real_forms = {}
            for tok in sentence:
                word = ''
                for element in tok:
                    if element.tag == 'orth':
                        real_form = element.text
                    elif element.tag == 'ann':
                        name = element.attrib['chan']
                        number = int(element.text)
                        if number > 0:
                            key = (name, number)
                            if key in real_forms.keys():
                                real_forms[key] += ' ' + real_form
                            else:
                                real_forms[key] = real_form
            for f in real_forms.items():
                key = f[0][0]
                new_key = (key, f[1])
                named_entities.update([new_key])
                freq_stats.update([key])

pprint(named_entities.most_common(50))
height = list(OrderedDict(freq_stats.most_common()).values())
bars = list(OrderedDict(freq_stats.most_common()).keys())
y_pos = np.arange(len(bars))


plt.bar(y_pos, height)

plt.xticks(y_pos, bars, rotation='vertical')

plt.tight_layout()
plt.savefig("fine.png")
plt.close()