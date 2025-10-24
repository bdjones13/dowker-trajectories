import numpy as np
import networkx as nx


class Digraph(nx.DiGraph):
    """
    A wrapper for networkx.DiGraph with 
    custom edge weighting and distance matrix methods.

    Each node stores two attributes:
    
    - bin: the corresponding bin/vertex label
    - count: an integer count associated with that bin
    """

    def __init__(self, adjacency_matrix, vertices, counts, loops: bool):
        """
        Initialize a directed graph from an adjacency matrix.

        Parameters
        ----------
        adjacency_matrix : ndarray of shape (n, n)
            Binary or weighted adjacency matrix describing directed edges.
        vertices : list of length n
            Labels for the vertices (e.g., bin indices).
        counts : list of length n
            Associated counts for each vertex.
        loops : bool
            Whether to keep self-loops (True) or remove them (False).

        Notes
        -----
        - If 'loops' is False, the diagonal of the adjacency matrix is
          zeroed out before graph construction.
        - Node attributes 'bin' and 'count' are set from 'vertices'
          and 'counts' respectively.
        """
        
        if loops == False:
            np.fill_diagonal(adjacency_matrix,0)
            super().__init__(adjacency_matrix)
        elif loops == True:
            super().__init__(adjacency_matrix)
        for i in range(len(self.nodes)):
            self.nodes[i]['bin'] = vertices[i]
            self.nodes[i]['count'] = counts[i]


    def distance_matrix(self, method = 'unweighted_shortest_path'):
        """
        Compute a pairwise distance matrix between all nodes.

        Parameters
        ----------
        method : {`unweighted_shortest_path`, `weighted_shortest_path`, `probabilistic`}

        Returns
        -------
        D : ndarray of shape (n, n)
            Distance matrix, where `D[i, j]` is the distance from node `i` to
            node `j`. Unreachable pairs are assigned a large value (1000).

        Notes
        -----
        - The distance matrix is also stored as self.D.
        """
        
        if method == 'unweighted_shortest_path':
            lengths = dict(nx.all_pairs_shortest_path_length(self))
            D = np.full((len(lengths),len(lengths)),1000,dtype=float) # was -1 default
            for key in lengths:
                for item in lengths[key]:
                        D[key,item] = lengths[key][item]
        
        if method == 'probabilistic': #since I doubt we are doing this in this paper, I haven't checked exactly if this is right
            w = nx.get_edge_attributes(self,'weight')
            for key in w:
                w[key] = 1/w[key]
            nx.set_edge_attributes(self,w,name='weight')
            lengths = dict(nx.all_pairs_dijkstra_path_length(self))
            D = np.full((len(lengths),len(lengths)),1000,dtype=float) # was -1 default
            for key in lengths:
                for item in lengths[key]:
                    if lengths[key][item] != 0:
                        D[key,item] = lengths[key][item]
                    elif lengths[key][item] == 0:
                        D[key,item] = 0

        if method == 'weighted_shortest_path':
            lengths = dict(nx.all_pairs_dijkstra_path_length(self))
            D = np.full((len(lengths),len(lengths)),1000,dtype=float) # was -1 default
            for key in lengths:
                for item in lengths[key]:
                    if lengths[key][item] != 0:
                        D[key,item] = lengths[key][item]
                    elif lengths[key][item] == 0:
                        D[key,item] = 0
        self.D = D
        return D


    def weight_graph(self, weights, smallest, biggest):
        """
        Assign edge weights to the graph.

        Parameters
        ----------
        weights : callable
            Function of the form weights(smallest, biggest) that returns
            a weight for an edge. This is applied to every edge. For example, numpy.random.randint
        smallest : number
            Smallest number in the weight range
        biggest : number
            Biggest number in the weight range

        """
        for e in self.edges:
            source = e[0]
            target = e[1]
            self[source][target]['weight'] = weights(smallest, biggest)

    def get_weights(self):
        """
        Retrieve all edge weights.

        Returns
        -------
        weights : dict
            Dictionary mapping edges '(u, v)' to their 'weight' attribute.
        """
        return nx.get_edge_attributes(self, "weight")



