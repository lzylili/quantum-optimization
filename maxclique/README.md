# Solving the MaxClique Problem using Gaussian Boson Sampling 

The **MaxClique problem** is a graph-theory problem that is relevant for *modelling various types of networks* such as biological networks, economic networks, and even social networks. The common thread between these networks are their interconnectivity, such that the interactions between different nodes in these respective networks indicate some sort of relationship. Examples:

*   In a **PPI network** (protein to protein interaction network), the dense subgraphs indicates a that the proteins may be mutually influential ones in the network or perhaps, can even form protein complexes. Example paper <a href='https://academic.oup.com/bioinformatics/article/25/15/1891/211634'>here</a>
*   In a **social network**, such as one that models the connections between a group of individuals on Twitter, finding connectivity between nodes (which would represent individuals) may be relevant to social network analysis problems such as <a href='https://en.wikipedia.org/wiki/Social_network_analysis'>this one</a>
*   In a **economic network**, a graph with high connectivity could indicate correlated assets in a market, which would be helpful for performing market analysis.

Hopefully, you're now able to see the motivation for finding subgraphs within these graph models! 

### What is the MaxClique?
The maximum clique is a subgraph such that all vertices contained within it are adjacent to all other vertices in the subgraph. In other words, the subgraph is maximally connected.

Since the MaxClique problem is NP-complete, as we scale the problem and increase the number of nodes, it will very difficult (and highly inefficient) for classical algorithms to solve once we hit a certain threshold.

### What is GBS?
Similar to how you would 'sample' using a galton board and marbles, we would sample dense subgraphs using GBS with the graph's adjacency matrix randomly. After each subgraph is sampled, we would perform greedy shrinking and/or expansion with local search (depending on the complexity of the graph) for find the maxcliques that we are looking for. 

While the greedy shrinking/expansion with local search are classical algorithms,the initial step of GBS helps cut down the number of subgraphs that need to be searched because GBS is optimized to sample dense subgraphs in this case (if they are dense, it means they are more likely to be a maxclique)! 

Specifically, the number of optical channels in the interferometer of the photonic quantum computer corresponds to the number of nodes in the graph. 

The process looks a little something like this:

<img src="https://github.com/lzylili/quantum-optimization/blob/master/maxclique/GBS.png" alt="GBS" width="600">

### About the graph
I used sf.apps.data to get a pre-generated GBS dataset. Specifically, I used data.PHat(), which generates a random graph using the p-hat generator. 

The graphs (randomly generated graph and found cliques) are as follows:

<img src ="https://github.com/lzylili/quantum-optimization/blob/master/maxclique/plotly-graphs.png" alt="Results" width="1000">
