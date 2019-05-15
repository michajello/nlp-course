from pprint import pprint
import networkx as nx
import matplotlib.pyplot as plt

import requests
import point7

API = "http://api.slowosiec.clarin-pl.eu/plwordnet-api/"


def search_meanings(word):
    return requests.get(API + "/senses/search", {"lemma": word}).json()['content']


def get_synsetid_by_sense_id(sense_id):
    return requests.get(API + "/senses/{}/synset".format(sense_id)).json()['id']


def get_synset_by_id(synset_id):
    return requests.get(API + "/synsets/{}/senses".format(synset_id)).json()


def get_synonyms(sense_id):
    return [map_meaning_result(x) for x in get_synset_by_id(get_synsetid_by_sense_id(sense_id))]


def get_all_synset_relations(synset_id):
    return requests.get(API + "/synsets/{}/relations".format(synset_id)).json()


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


def get_synsets_relation(synsets):
    result = []
    synset_ids = set([s["synset_id"] for s in  synsets])
    for synset in synsets:
        s_id = synset["synset_id"]
        rel_data = get_all_synset_relations(s_id)
        result.append(
            flat_list([{"src": r['synsetFrom']['id'], 'dst': r['synsetTo']['id'], 'id': r['relation']['id']}] for r in rel_data if r['synsetTo']['id'] in synset_ids and r['synsetFrom']['id'] in synset_ids))
    return result


# def filter_relations(relations):
def remove_duplicates_from_list(l):
    return [i for n, i in enumerate(l) if i not in l[n + 1:]]


def get_senses_for_word_with_sense_number(words: dict) -> list:
    result = []
    for word in words:
        sense_data = search_meanings(word['word'])
        sense_data_filter = [{"word": word['word'], "id": s['id']} for s in sense_data if
                             s["senseNumber"] == word["senseNumber"] and s['lemma']["word"] == word['word']]
        result.extend(sense_data_filter)
    return result

#{'sense': {'id': 8771, 'word': 'szkoda'}, 'synset_id': 3675},
def join_words_by_synset_id(synsets):
    result={}
    for synset in synsets:
        if not synset['synset_id'] in result :
            result[synset['synset_id']] = synset['sense']['word']
        else:
            result[synset['synset_id']] = result[synset['synset_id']] + ", " + synset['sense']['word']
    return result


#{'dst': 3675, 'id': 10, 'src': 46769}
#{3675: 'szkoda, strata, uszczerbek', 46769: 'uszczerbek na zdrowiu'},
def draph_graph(relation, synsets_by_id):
    graph = [(synsets_by_id[r['src']], synsets_by_id[r['dst']]) for r in relation]
    relations = point7.all_relations()
    edges = [relations[r['id']] for r in relation if r['id'] != 10]
    edge_labes = dict(zip(graph, edges))
    # create directed networkx graph
    G=nx.DiGraph()

    # add edges
    G.add_edges_from(graph)
    plt.figure(figsize=(20, 20))
    graph_pos = nx.shell_layout(G)
    nx.draw(
        G,graph_pos,edge_color='black',width=1,linewidths=1,
        node_size=3000,node_color='pink',alpha=0.9,
        labels={node:node for node in G.nodes()}
    )
    # draw nodes, edges and labels
    # nx.draw_networkx_nodes(G, graph_pos, node_size=1000, node_color='blue', alpha=0.3)
    # we can now added edge thickness and edge color
    # nx.draw_networkx_edges(G, graph_pos, widthz=2, alpha=0.3, edge_color='black')
    # nx.draw_networkx_labels(G, graph_pos, font_size=12, font_family='sans-serif')

    # nx.draw_networkx_edge_labels(G, graph_pos, edge_labels=edge_labes, font_color='blue')

    # show graph
    plt.show()

def draw_closure_words(closure_words):
    graph = list(zip(closure_words, closure_words[1:]))

    edge_labels =dict(zip(graph, ["hiperonimia"] * (len(closure_words)-1)))
    G = nx.DiGraph()

    # {('uszczerbek na zdrowiu', 'szkoda, strata, uszczerbek'): 'hiperonimia',
    #  ('szkoda, strata, uszczerbek', 'uszczerbek na zdrowiu'): 'hiperonimia',
    #  ('krzywda, niesprawiedliwość', 'szkoda, strata, uszczerbek'): 'hiperonimia'}
    # add edges
    G.add_edges_from(graph)
    plt.figure(figsize=(20, 20))
    graph_pos = nx.shell_layout(G)
    nx.draw(
        G, graph_pos, edge_color='black', width=1, linewidths=1,
        node_size=3000, node_color='pink', alpha=0.9,
        labels={node: node for node in G.nodes()}
    )
    # draw nodes, edges and labels
    # nx.draw_networkx_nodes(G, graph_pos, node_size=1000, node_color='blue', alpha=0.3)
    # we can now added edge thickness and edge color
    # nx.draw_networkx_edges(G, graph_pos, width=2, alpha=0.3, edge_color='black')
    # nx.draw_networkx_labels(G, graph_pos, font_size=12, font_family='sans-serif')

    # nx.draw_networkx_edge_labels(G, graph_pos, edge_labels=edge_labels, font_color='blue')

    # show graph
    plt.show()


3
print("TASK 3")
meanings = search_meanings("szkoda")
meanings = [map_meaning_result(x) for x in meanings]

print(meanings)

synonyms = [get_synonyms(x["id"]) for x in meanings]
pprint(synonyms)

# 4
print("TASK 4")
traffic_accident_meaning = [map_meaning_result(x) for x in search_meanings("wypadek drogowy")]
# pprint(traffic_accident_meaning)
#
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




draw_closure_words(closure_words)

print("TASK 5")
accident_meaning = [map_meaning_result(x) for x in search_meanings("wypadek") if
                    x['lemma']['word'] == "wypadek" and x['senseNumber'] == 1]
hyponym_id = 10

accident_synset_id = get_synsetid_by_sense_id(accident_meaning[0]['id'])
accident_hyphonym = get_synset_relations(accident_synset_id, hyponym_id)

accident_hyphonym_synsets = flat_list([get_synset_by_id(x['synsetFrom']['id']) for x in accident_hyphonym])
accident_hyphonym_words = [map_meaning_result(x) for x in accident_hyphonym_synsets]

pprint(accident_hyphonym_words)

# 6
second_order_accident_hyphonym = flat_list(
    [get_synset_relations(get_synsetid_by_sense_id(x['id']), hyponym_id) for x in accident_hyphonym_synsets])
second_order_accident_hyphonym_synsets = flat_list(
    [get_synset_by_id(x['synsetFrom']['id']) for x in second_order_accident_hyphonym if x])
second_order_accident_hyphonym_words = [map_meaning_result(x) for x in second_order_accident_hyphonym_synsets]
print("TASK 6 Find second-order hyponyms")
pprint(second_order_accident_hyphonym_words)

7
senses1 = get_senses_for_word_with_sense_number(point7.words_7_1())
pprint(senses1)
synset1 = [{"sense": s, "synset_id": (get_synsetid_by_sense_id(s['id']))} for s in senses1]
pprint(synset1)
relations1 = remove_duplicates_from_list(flat_list(get_synsets_relation(synset1)))
pprint(relations1)
draph_graph(relations1, join_words_by_synset_id(synset1))

senses2 = get_senses_for_word_with_sense_number(point7.words_7_2())
synset2 = [{"sense": s, "synset_id": (get_synsetid_by_sense_id(s['id']))} for s in senses2]
relations2 = remove_duplicates_from_list(flat_list(get_synsets_relation(synset2)))
print(relations2)
draph_graph(relations2, join_words_by_synset_id(synset2))
