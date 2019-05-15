import re
from os import listdir

pat=re.compile("^.*?ustawa.*?z dnia.*?\n.*?o zmianie ustawy.*?art\. 1",re.DOTALL|re.IGNORECASE)



dataset_path = "../dataset"

amending_bills = []
non_amending_bills = []
for file in listdir(dataset_path):
    with open(dataset_path + "/" + file, mode='r', encoding='utf-8') as doc:
        content = doc.read()[:3000].replace("  ", " ").lower()
        if re.search(pat, content):
            amending_bills.append(file)
        else:
            non_amending_bills.append(file)
