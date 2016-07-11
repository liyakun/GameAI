import csv
import numpy as np
import random
import math
import sys
import time

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

count = 0
with open('q3dm1-path1.csv', 'rb') as f:
    reader = csv.reader(f)
    for row in reader:
        count += 1

data = np.zeros((count, 3), dtype=np.float)

with open('q3dm1-path1.csv', 'rb') as f:
    reader = csv.reader(f)
    for r_idx, row in enumerate(reader):
        for c_idx, col in enumerate(row):
            data[r_idx, c_idx] = float(col)


def distance(point1, point2):
    dist = 0
    for i in range(len(point1)):
        dist += (point1[i] - point2[i]) * (point1[i] - point2[i])
    return math.sqrt(dist)


def SOM(X, k, dim, tmax):
    weights = np.zeros((k,3), dtype=np.float)   
    # initializing weights
    for i in range(k):
        point = np.random.randint(0, dim)
        for j in range(3):
            weights[i,j] = X[point,j]

    D = np.zeros((k,k), dtype=np.float)
    for i in range(k):
        for j in range(k):
            if( abs(i-j) <= (k//2) ):
                D[i,j] = abs(i-j)
            else:
                D[i,j] = abs(abs(i-j) - k)


    plt.ion()
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    sc_data = ax.scatter(X[:,0], X[:,1], X[:,2], zorder=1, c='r', alpha=1)
    ax.plot(weights[:,0], weights[:,1], weights[:,2], c='b')
    sc_neurons = ax.scatter(weights[:,0], weights[:,1], weights[:,2], zorder=4, s=100, marker='o',c='b', alpha=1)
    ax.set_xlabel('X Label')
    ax.set_ylabel('Y Label')
    ax.set_zlabel('Z Label')
    fig.show()

    
    for t in range(tmax):
        plt.pause(0.001)
        # randomly sample a point
        random_point = X[np.random.randint(0, dim),:]
        
        # determine a winning neuron
        winning_neuron = weights[0,:]
        winning_neuron_index = 0
        dist = distance(winning_neuron, random_point)
        for i in range(1,k):
            dist_temp = distance(weights[i,:], random_point)
            if( dist_temp < dist):
                winning_neuron = weights[i,:]
                winning_neuron_index = i
                dist = dist_temp

        learn_rate = (1.0-float(t)/float(tmax))
        sigma = math.exp(-float(t)/float(tmax))
        for i in range(0,k):

            dd = distance(winning_neuron, weights[i,:])
            for j in range(3):
                weights[i,j] += learn_rate*math.exp(-( D[winning_neuron_index,i] )/ (2.0*sigma) )*(random_point[j]-weights[i,j])

        sc_neurons._offsets3d = (weights[:,0], weights[:,1], weights[:,2])
        plt.draw()

SOM(data, 10, count, 100)