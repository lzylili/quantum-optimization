#import all necessary packages
from typing import List, Tuple

import networkx as nx
import numpy as np
import random
from itertools import combinations

from pyquil.api import get_qc
from pyquil.paulis import PauliTerm, PauliSum
from scipy.optimize import minimize
from pyquil import get_qc, Program
from grove.pyqaoa.qaoa import QAOA

# %matplotlib inline

#create the graph
n = 4
G = nx.Graph()

for node in range(n):
    G.add_node(node)

for node in range(n):
    G.add_node(node)

#list of nodes with weighted edges
elist = [(0, 1, 2), (0, 2, 5), (0, 3, 0.25), (1, 2, 3), (2, 3, 1.0), (1,3, 0.30)]
G.add_weighted_edges_from(elist)


#creates random graph every time you run it!
for (u,v,w) in G.edges(data=True):
    w['weight'] = random.randint(0,10)

#plot maxcut problem
pos = nx.spring_layout(G)
nx.draw_networkx_edge_labels(G, pos, edge_labels={(0,1):2,
(0, 2):5, (0,3):0.25, (1,2):3, (2,3):1.0, (1,3):0.3},font_color='red')

nx.draw(G, with_labels = True, node_color = 'pink')

#find largest weight in list
largest_weight = 0
for edge in elist:
    for i in range(len(elist)):
        weight = elist[i][2]
        if weight > largest_weight:
            largest_weight = weight

def maxcut_qaoa(graph, steps=1, rand_seed=None, connection=None, samples=None,
                initial_beta=None, initial_gamma=None, minimizer_kwargs=None,
                vqe_option=None):
    
    if not isinstance(graph, nx.Graph) and isinstance(graph, list):
        maxcut_graph = nx.Graph()
        for edge in graph:
            maxcut_graph.add_edge(*edge)
        graph = maxcut_graph.copy()
        nx.draw(graph)
    
    cost_operators = []
    driver_operators = []
    
    #Creates cost hamiltonian from weights + nodes, adds accountability for weights from original rigetti QAOA code 
    for i, j in graph.edges():
        weight = graph.get_edge_data(i,j)['weight']/largest_weight
        cost_operators.append(PauliTerm("Z", i, weight)*PauliTerm("Z", j) + PauliTerm("I", 0, -weight))
    
    #creates driver hamiltonian
    for i in graph.nodes():
        driver_operators.append(PauliSum([PauliTerm("X", i, -1.0)]))

    if connection is None:
        connection = get_qc(f"{len(graph.nodes)}q-qvm")

    if minimizer_kwargs is None:
        minimizer_kwargs = {'method': 'Nelder-Mead',
                            'options': {'ftol': 1.0e-2, 'xtol': 1.0e-2,
                                        'disp': False}}
    if vqe_option is None:
        vqe_option = {'disp': print, 'return_all': True,
                      'samples': samples}
    
    qaoa_inst = QAOA(connection, list(graph.nodes()), steps=steps, cost_ham=cost_operators,
                     ref_ham=driver_operators, store_basis=True,
                     rand_seed=rand_seed,
                     init_betas=initial_beta,
                     init_gammas=initial_gamma,
                     minimizer=minimize,
                     minimizer_kwargs=minimizer_kwargs,
                     vqe_options=vqe_option)

    return qaoa_inst

import numpy as np
from pyquil import *
import pyquil.api as QVMConnection

qvm = api.QVMConnection()

inst = maxcut_qaoa(G, steps=10, connection=qvm, rand_seed=None, samples=None, initial_beta=None, initial_gamma=None, minimizer_kwargs=None, vqe_option=None)

get_ipython().run_cell_magic('time', '', '\nbetas, gammas = inst.get_angles()\nprobs = inst.probabilities(np.hstack((betas, gammas)))\nfor state, prob in zip(inst.states, probs):\n    print(state, prob)\n\nprint("Most frequent bitstring from sampling")\nmost_freq_string, sampling_results = inst.get_string(betas, gammas)')

print(most_freq_string)

#turn 0s into pink nodes and 1s into blue nodes
colours = []
for i in range(n):
    if most_freq_string[i] == 0:
        colours.append('pink')
    elif most_freq_string[i] == 1:
        colours.append('blue')

nx.draw(G, with_labels = True, node_color = colours)
