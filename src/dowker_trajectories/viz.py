import plotly.graph_objects as go
import numpy as np

def graph_graph(G, bin_cents, perc = 0, arrows = False, color_verts = False): 

    fig = go.Figure()

    points_x = []
    points_y = []
    points_z = []

    for node in list(G.nodes):
        points_x.append(bin_cents[int(G.nodes[node]['bin']),0])
        points_y.append(bin_cents[int(G.nodes[node]['bin']),1])
        points_z.append(bin_cents[int(G.nodes[node]['bin']),2])

    fig.add_trace(go.Scatter3d(x=points_x, y=points_y,z=points_z, mode='markers',marker=dict(size=2, color='black',line=dict(width=1, color='white')),showlegend=False))


    if arrows:
        for edge in list(G.edges):
            source = edge[0]
            target = edge[1]
            bin_source = int(G.nodes[source]['bin'])
            bin_target = int(G.nodes[target]['bin'])

            start_x = bin_cents[bin_source,0]
            start_y = bin_cents[bin_source,1]
            start_z = bin_cents[bin_source,2]

            end_x = bin_cents[bin_target,0]
            end_y = bin_cents[bin_target,1]
            end_z = bin_cents[bin_target,2]


            fig.add_trace(go.Scatter3d(x = [start_x,end_x], y = [start_y,end_y], z = [start_z,end_z], marker = dict(size = 3, color = 'black'), showlegend = False))

            dx = end_x - start_x
            dy = end_y - start_y
            dz = end_z - start_z

            fig.add_trace(go.Cone(x = [end_x], y = [end_y], z = [end_z], u = [dx], v = [dy], w = [dz], anchor = 'tip', sizeref = .3, colorscale = [[0,'black'],[1,'black']], showlegend=False, showscale = False))
        
    if color_verts:

        node_x = []
        node_y = []
        node_z = []
        counts = [G.nodes[node]['count'] for node in G.nodes]
        perc = np.percentile(counts, 100-perc)
        dense_points = np.where(counts >= perc)[0]

        for i in dense_points:
            node_x.append(bin_cents[int(G.nodes[i]['bin']),0])
            node_y.append(bin_cents[int(G.nodes[i]['bin']),1])
            node_z.append(bin_cents[int(G.nodes[i]['bin']),2])

        fig.add_trace(go.Scatter3d(x=node_x, y=node_y,z=node_z, mode='markers',marker=dict(size=2, colorscale='Brwnyl',
        colorbar=dict(title="Counts"),line=dict(width=1, color='white')),showlegend=False))

    fig.update_layout(scene=dict(aspectmode='cube'))
    fig.update(layout_showlegend=False)
        
    return fig