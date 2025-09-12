from .digraphs import Digraph
import networkx as nx

class CycleGraph(Digraph):


    # caution: broken, since this was based on old Digraph class that didn't inherit from networkx

    def __init__(self, n):
        G = nx.cycle_graph(n, create_using=nx.DiGraph)
        super().__init__(nx.adjacency_matrix(G).toarray(),vertices=G.nodes,counts = [1 for _ in G.nodes],loops=False)
    
