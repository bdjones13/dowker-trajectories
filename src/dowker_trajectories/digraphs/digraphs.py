import numpy as np
import networkx as nx


class Digraph(nx.DiGraph):
        # inputs: A - the adjacency matrix
    # vertices - the list of vertices, which are the bin numbers
    # loops - whether or not to keep the self-loops in the graph, I am going to do something with this eventually when I include some sort of markovian random walk diffusion distance 
    #Output: G - a networkx digraph
    def __init__(self, adjacency_matrix, vertices, counts, loops: bool):
        if loops == False:
            np.fill_diagonal(adjacency_matrix,0)
            super().__init__(adjacency_matrix)
        elif loops == True:
            super().__init__(adjacency_matrix)
        for i in range(len(self.nodes)):
            self.nodes[i]['bin'] = vertices[i]
            self.nodes[i]['count'] = counts[i]

    #Inputs: G - a networkx graph
    # method - the way you want to measure distance on the graph
    # Outputs: D - a distance matrix
    def distance_matrix(self, method = 'unweighted_shortest_path'):
        if method == 'unweighted_shortest_path':
            lengths = dict(nx.all_pairs_shortest_path_length(self))
            D = np.full((len(lengths),len(lengths)),1000,dtype=float) # was -1 default
            for key in lengths:
                for item in lengths[key]:
                        D[key,item] = lengths[key][item]
        
        if method == 'probabilistic': #since I doubt we are doing this in this paper, I haven't checked exactly if this is right
            w = nx.get_edge_attributes(self.G,'weight')
            for key in w:
                w[key] = 1/w[key]
            nx.set_edge_attributes(self.G,w,name='weight')
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
        for e in self.edges:
            source = e[0]
            target = e[1]
            self[source][target]['weight'] = weights(smallest, biggest)

    def get_weights(self):
        return nx.get_edge_attributes(self, "weight")



        return nx.get_edge_attributes(self.G, "weight")