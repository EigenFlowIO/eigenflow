from __future__ import annotations
import numpy as np
import networkx as nx
from scipy.sparse.csgraph import connected_components

def component_labels(snapshot): return connected_components(snapshot.adjacency,directed=False,return_labels=True)
def component_sizes(snapshot):
    n,labels=component_labels(snapshot); return np.bincount(labels,minlength=n)
def graph_nx(snapshot): return nx.from_scipy_sparse_array(snapshot.adjacency)
def degree_array(snapshot): return np.asarray(snapshot.adjacency.sum(axis=1)).ravel()
def bridge_edges(snapshot): return list(nx.bridges(graph_nx(snapshot)))
def articulation_points(snapshot): return list(nx.articulation_points(graph_nx(snapshot)))
def kcore_nodes(snapshot,k=2): return list(nx.k_core(graph_nx(snapshot),k=k).nodes())
def communities(snapshot):
    g=graph_nx(snapshot)
    return [sorted(c) for c in nx.algorithms.community.greedy_modularity_communities(g)] if g.number_of_edges() else [[i] for i in g.nodes]
