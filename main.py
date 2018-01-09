#!/usr/bin/python3
# -*-coding: utf-8 -*

import random
import networkx as nx


def generate_sites(n: int, m: int):
    g = nx.gnm_random_graph(n, m)
    for e in list(g.edges()):
        x = e[0]
        y = e[1]
        g[x][y]['weight'] = random.randint(1, 10)

    return g


# enchères séquentielles : protocole :
# chaque agent fait une offre pour le sommet de coût minimum pour chaque sommet contôllé par l'agent
# un commissaire octroi l'offre de coût minimum à l'agent qui l'a faite
# et on recommence jusqu'à que tous les sommets soient distribués
def sequential_auctions(agents: [int], sites: nx.Graph, ) -> {int: [int]}:
    res = {int: [int]}
    nodes = list(sites.nodes())
    for a in agents:
        s_len = len(nodes)
        node = nodes.pop(random.randint(0, s_len))
        res.update({a: [node]})

    pass


g = generate_sites(5, 8)
sequential_auctions([0, 1], g)












