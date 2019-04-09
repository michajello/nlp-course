from elasticsearch import Elasticsearch
from os import listdir

es = Elasticsearch()
index_name = "my_index_multi"
es.indices.delete(index=index_name, ignore=[400, 404])

print(es.indices.create(
    index=index_name,
    body={
        "settings": {
            "analysis": {
                "filter": {
                    "my_synonyms": {
                        "type": "synonym",
                        "synonyms": [
                            "kpk => kodeks postępowania karnego",
                            "kpc => kodeks postępowania cywilnego",
                            "kk => kodeks karny",
                            "kc => kodeks cywilny"
                        ]
                    },
                    "filter_shingle": {
                        "type": "shingle",
                        "max_shingle_size": 2,
                        "min_shingle_size": 2,
                        # "output_unigrams": "true"
                    },
                },

                "analyzer": {
                    "my_analyzer": {
                        "tokenizer": "standard",
                        "filter": ["my_synonyms", "lowercase", "morfologik_stem"]
                    },
                    "analyzer_shingle": {
                        "tokenizer": "standard",
                        "filter": ["standard", "lowercase",  "filter_shingle"]
                    }
                }
            }
        },
        "mappings": {
            "_doc": {
                "properties": {
                    "text": {
                        "analyzer": "analyzer_shingle",
                        # "search_analyzer": "analyzer_shingle",
                        # "index_analyzer": "analyzer_shingle",
                        "type": "text"
                    }
                }
            }
        }
    }

)
)

dataset_path = "../dataset"

for file in listdir(dataset_path):
    with open(dataset_path + "/" + file, mode='r', encoding='utf-8') as doc:
        es.create(index=index_name, id=file, doc_type="_doc", body={"text": doc.read()})
