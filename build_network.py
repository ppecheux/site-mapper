import json
import networkx as nx
import matplotlib.pyplot as plt

with open('pages.json') as fp:
    pages = json.load(fp)

DG = nx.DiGraph()
for page in pages:
    # TODO add number of add on the same edge
    DG.add_node(page.get('url', ''), body_length=page.get(
        'body_length', 0), title=page.get('title'))
    DG.add_edges_from([edge for edge in zip(
        [page.get('url', '')]*len(page.get('links', [])), page.get('links', []))])


#print(DG.nodes.data())
# nx.draw(DG, withlabels=True)
# plt.show()

puits = []
for node in DG:
    if not any(True for _ in DG.successors(node)):
        puits.append(node)
DG.remove_nodes_from(puits)

labels={n:d['title'][:25] for n,d in DG.nodes(data=True)}

nx.draw(DG, labels=labels, withlabels=True, node_size=1000)
plt.show()