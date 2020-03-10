--------------------------------------------------------------------

# import packages
from strawberryfields.apps import data, plot, sample, clique
import numpy as np
import networkx as nx
import plotly

---------------------------------------------------------------------

# plot graph (randomly generated)
PH = data.PHat()  
A = PH.adj
PH_graph = nx.Graph(A)
plot_graph = plot.graph(PH_graph)
plot_graph.show()

# Complete GBS (the mean density of the subgraphs samples by GBS > the uniform mean density! This means less searching for the classical algorithms)
GBS_dens = []
u_dens = []

for s in samples:
    uniform = list(np.random.choice(16, 20))  
    GBS_dens.append(nx.density(PH_graph.subgraph(s)))
    u_dens.append(nx.density(PH_graph.subgraph(uniform)))

print("GBS mean density = {:.4f}".format(np.mean(GBS_dens)))
print("Uniform mean density = {:.4f}".format(np.mean(u_dens)))
# GBS mean density = 0.3714
# Uniform mean density = 0.1673

---------------------------------------------------------------------

# Perform greedy shrinking until the subgraph is a maxclique
shrunk = [clique.shrink(s, PH_graph) for s in samples]
print(clique.is_clique(PH_graph.subgraph(shrunk[0])))

# Find the average clique size
searched = [clique.search(s, PH_graph, 10) for s in shrunk]
clique_sizes = [len(s) for s in searched]
print("Average clique size = {:.3f}".format(np.mean(clique_sizes)))
# Average clique size = 6.664

---------------------------------------------------------------------

# Plot one of the samples of the average sized cliques
clique_fig = plot.graph(PH_graph, searched[0])
clique_fig.show()

# Find the largest clique (aka the maxclique) and plot it!
largest_clique = searched[np.argmax(clique_sizes)]  
print("Largest clique subgraph is = ", largest_clique)
# Largest clique subgraph is =  [48, 90, 104, 109, 159, 196, 263, 295]

largest_fig = plot.graph(phat_graph, largest_clique)
largest_fig.show()

---------------------------------------------------------------------

## Credits
# This code is modified from Xanadu's Strawberry Fields apps package 
