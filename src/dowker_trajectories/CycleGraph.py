from .Digraph import Digraph
import networkx as nx

class CycleGraph(Digraph):
    """
    Directed cycle graph.

    A subclass of dowker_trajectories.Digraph that constructs a consistently oriented directed
    cycle on n vertices.
    """


    def __init__(self, n):
        """
        Initialize a directed cycle graph with 'n' vertices.

        Parameters
        ----------
        n : int
            Number of vertices in the cycle

        Notes
        -----
        - The cycle is constructed using networkx.cycle_graph.
        """
        G = nx.cycle_graph(n, create_using=nx.DiGraph)
        super().__init__(nx.adjacency_matrix(G).toarray(),vertices=G.nodes,counts = [1 for _ in G.nodes],loops=False)
    
