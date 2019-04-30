from pprint import pprint
import itertools

import requests

API = "http://api.slowosiec.clarin-pl.eu/plwordnet-api/"


def search_meanings(word):
    return requests.get(API + "/senses/search", {"lemma": word}).json()['content']


def get_synsetid_by_sense_id(sense_id):
    return requests.get(API + "/senses/{}/synset".format(sense_id)).json()['id']


def get_synset_by_id(synset_id):
    return requests.get(API + "/synsets/{}/senses".format(synset_id)).json()


def get_synonyms(sense_id):
    return [map_meaning_result(x) for x in get_synset_by_id(get_synsetid_by_sense_id(sense_id))]


def get_synset_relations(synset_id, relation_id):
    body = requests.get(API + "/synsets/{}/relations".format(synset_id)).json()
    # return body
    return [x for x in body if x['synsetFrom']['id'] != synset_id and x['relation']['id'] == relation_id]


def get_synsets_closure(synset_id, relation_id):
    closure = [synset_id]
    related_synsets = get_synset_relations(synset_id, relation_id)
    while related_synsets:
        closure.extend([x['synsetFrom']['id'] for x in related_synsets])

        related_synsets = get_synset_relations(closure[-1], relation_id)

    return closure

def flat_list(l):
    return [item for sublist in l for item in sublist]

def map_meaning_result(x):
    return {"id": x["id"],
            'word': x['lemma']['word'],
            "description": x["domain"]["description"],
            "partOfSpeech": x["partOfSpeech"]["name"]}


# 3
meanings = search_meanings("szkoda")

meanings = [map_meaning_result(x) for x in meanings]

print(meanings)

synonyms = [get_synonyms(x["id"]) for x in meanings]
pprint(synonyms)

# 4
traffic_accident_meaning = [map_meaning_result(x) for x in search_meanings("wypadek drogowy")]
pprint(traffic_accident_meaning)

traffic_accident_synset_id = get_synsetid_by_sense_id(traffic_accident_meaning[0]['id'])
hyperonymy_relation_id = 11

pprint(traffic_accident_synset_id)  # 410902
related_synsets = get_synset_relations(traffic_accident_synset_id, hyperonymy_relation_id)
print(related_synsets)

traffic_accident_closure_synsets_id = get_synsets_closure(traffic_accident_synset_id, hyperonymy_relation_id)
print(traffic_accident_closure_synsets_id)

closure_synsets = [get_synset_by_id(x) for x in traffic_accident_closure_synsets_id]
closure_words = [x[0]["lemma"]["word"] for x in closure_synsets]

print(closure_words)

# 5
accident_meaning = [map_meaning_result(x) for x in search_meanings("wypadek") if
                    x['lemma']['word'] == "wypadek" and x['senseNumber'] == 1]
hyponym_id = 10

accident_synset_id = get_synsetid_by_sense_id(accident_meaning[0]['id'])
accident_hyphonym = get_synset_relations(accident_synset_id, hyponym_id)

accident_hyphonym_synsets = flat_list([get_synset_by_id(x['synsetFrom']['id']) for x in accident_hyphonym])
accident_hyphonym_words = [map_meaning_result(x) for x in accident_hyphonym_synsets]

pprint(accident_hyphonym_words)

#6
second_order_accident_hyphonym = flat_list([get_synset_relations(get_synsetid_by_sense_id(x['id']), hyponym_id) for x in accident_hyphonym_synsets ])
second_order_accident_hyphonym_synsets = flat_list([get_synset_by_id(x['synsetFrom']['id']) for x in second_order_accident_hyphonym if x])
second_order_accident_hyphonym_words = [map_meaning_result(x) for x in second_order_accident_hyphonym_synsets]
print("TASK 6 Find second-order hyponyms")
pprint(second_order_accident_hyphonym_words)