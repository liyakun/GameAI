import numpy as np
import scipy.misc as sc
import matplotlib.pyplot as plt
import networkx as nx
import sys
import heapq
import math


def heuristic(u, v, G):
	return math.sqrt( math.pow(G.node[u]['pos'][0] - G.node[v]['pos'][0],2) +  math.pow(G.node[u]['pos'][1] - G.node[v]['pos'][1],2) )


def reconstruct_a_star_path(curnode, parent, cameFrom):
	path = [curnode]
	node = parent
	while node is not None:
		path.append(node)
		node = cameFrom[node]
		path.reverse()
	return path

def a_star(G, source, target, heuristic ):
	# The set of currently discovered nodes still to be evaluated.
	# Initially, only the start node is known.
	# The queue stores:
	#  - priority, 
	#  - node, 
	#  - cost to reach from source to goal by passing that node, 
	#  - parent
	queue = [(0, source, 0, None)]
	# maps closedSet nodes to distance of discovered paths
	closedSet = {}
	# maps nodes to parent closest to the source.
	cameFrom = {}

	while queue:
		# get item with lowest path cost
		_, curnode, dist, parent = heapq.heappop(queue)

		if curnode == target: # if target reached move back to get the best path
			return reconstruct_a_star_path(curnode, parent, cameFrom)

		cameFrom[curnode] = parent
		for neighbor, w in G[curnode].items(): # for each neighbour of current node
			if neighbor in cameFrom: # ignore the neighbor which is already evaluated
				continue
			ncost = dist + w["weight"] # distance from start to a neighbor

			if neighbor not in closedSet:
				h = heuristic(neighbor, target, G)
			else:
				qcost, h = closedSet[neighbor]
				# a longer path to the neighbor is avoided
				if qcost <= ncost:
					continue
			closedSet[neighbor] = ncost, h
			heapq.heappush(queue, (ncost + h, neighbor, ncost, curnode))



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
	queue = [] # use heapq with (distance,label) 
	heapq.heappush(queue,(0,source)) # initialize priority queue

	while queue: # while queue is not empty
		(d,node) = heapq.heappop(queue) # return and remove best vertex
		if node in dist: 
			continue # already searched this node.
		dist[node] = d
		if node == target:
			break  # target reached

		edata = G[node].iteritems() 
		for neighbour ,edge in edata: # for each neighbour of best vertex
			node_neighbour_dist = dist[node] + edge['weight'] # calculate distance between best vertex and its neighbour
			
			if neighbour not in seen or node_neighbour_dist < seen[neighbour]: 	
										# if neighbour was not seen at all or 
										# distance to the neighbour is lower than some previously 
										# calculated distance
				seen[neighbour] = node_neighbour_dist
				heapq.heappush(queue,(node_neighbour_dist,neighbour))
				paths[neighbour] = paths[node]+[neighbour]
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
(length,path_dijkstra) = dijkstra(G, 200 , 35)
print("dijkstra path")
print(path_dijkstra[35])


nx.draw(G, pos, node_color='g',node_size=250,with_labels=True,width=6)
nx.draw_networkx_nodes(G,pos, nodelist=path_dijkstra[35], node_color='r', node_size=300, with_labels=True, width=6)

path_a_star = a_star(G,200,35, heuristic)
print("A* path")
print(path_a_star)
nx.draw_networkx_nodes(G,pos, nodelist=path_a_star, node_color='b', node_size=300, with_labels=True, width=6)

plt.show()