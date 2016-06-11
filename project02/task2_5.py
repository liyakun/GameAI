import numpy as np
import scipy.misc as sc
import matplotlib.pyplot as plt
import networkx as nx
import sys

grid = []
with open('simpleMap-1-20x20.txt') as f:
    for line in f: # read rest of lines
        grid.append([int(x) for x in line.split()])

grid = np.array(grid)

G = nx.Graph()

pos = []
counter = 0
previous_in_row = -1

for row_idx, row in enumerate(reversed(grid)):
	for column_idx, point in enumerate(row):
		if( point == 0 ):
			G.add_node(counter)
			if( column_idx > 0 and previous_in_row+1 == counter):
				G.add_edge(counter-1,counter)
			if( row_idx > 0 and G.has_node(counter - grid.shape[1]) ):
				G.add_edge(counter, counter - grid.shape[1])
			previous_in_row = counter
			pos.append([column_idx, row_idx])
		else:
			pos.append([])
		counter += 1

nx.draw(G, pos, node_color='g',node_size=250,with_labels=True,width=6)

plt.show()
