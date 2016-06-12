import numpy as np
import scipy.misc as sc
import matplotlib.pyplot as plt
import networkx as nx
import sys

import heapq
from collections import deque 



def dijkstra(G , source , target  ):
	"""	Returns a tuple of two dictionaries keyed by node.
	The first dicdtionary stores distance from the source.
	The second stores the path from the source to that node.
	source - node label
	target - node label
	"""
	if source == target: 
		return (0, [source])
	dist = {}  # dictionary of final distances
	paths = {source:[source]}  # dictionary of paths
	seen = {source:0} 
	fringe=[] # use heapq with (distance,label) tuples 
	heapq.heappush(fringe,(0,source))
	while fringe:
		(d,v)=heapq.heappop(fringe)
		if v in dist: 
			continue # already searched this node.
		dist[v] = d
		if v == target: 
			break
		edata = G[v].iteritems()
		for w,edgedata in edata:
			vw_dist = dist[v]+edgedata['weight']
			
			if w not in seen or vw_dist < seen[w]:
				seen[w] = vw_dist
				heapq.heappush(fringe,(vw_dist,w))
				paths[w] = paths[v]+[w]
	return (dist,paths)



grid = []
with open('simpleMap-1-20x20.txt') as f:
	for line in f: # read rest of lines
		grid.append([int(x) for x in line.split()])

grid = np.array(grid)

G = nx.Graph()

counter = 0
previous_in_row = -1

for row_idx, row in enumerate(reversed(grid)):
	for column_idx, point in enumerate(row):
		if( point == 0 ):
			G.add_node(counter, pos=(column_idx,row_idx))
			if( column_idx > 0 and previous_in_row+1 == counter):
				G.add_edge(counter-1,counter, weight=1)
			if( row_idx > 0 and G.has_node(counter - grid.shape[1]) ):
				G.add_edge(counter, counter - grid.shape[1], weight=1)
			previous_in_row = counter
		counter += 1


pos = nx.get_node_attributes(G,'pos')
(length,path) = dijkstra(G, 200 , 35)
print(path[35])


nx.draw(G, pos, node_color='g',node_size=250,with_labels=True,width=6)
nx.draw_networkx_nodes(G,pos, nodelist=path[35], node_color='r', node_size=300, with_labels=True, width=6)
plt.show()