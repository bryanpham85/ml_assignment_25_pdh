from os import walk
import pandas as pd
import numpy as np
import math
import matplotlib.pyplot as mpl


#define Euclid Distance
def euclid_dist(d1, d2):
    if len(d1) != len(d2):
        return None
    
    sum_diff = 0
    for i in range(0, len(d1), 1):
        sum_diff = sum_diff + (d1[i] - d2[i])**2
    return math.sqrt(sum_diff)

#load all data of companies into dict with Company Code as Key and array of 128 days price as values
stock_daily_price = []
companies_stock_code = []

for (dirpath, dirnames, filenames) in walk('./data/'):
    filenames.sort()
    for f in filenames:
        companies_stock_code.append(f.split('.')[0])
        temp_price = []
        #read line
        with open('./data/' + f) as file_content:
            prices = file_content.read().splitlines()
            for j in range(0,128,1):
                temp_price.append(float(prices[j]))
        stock_daily_price.append(temp_price)

# the price of stocks are in different range, and we cluster the timeserie data 
# #so that we check the movement of the price over period of 128 days
stock_daily_movement = []

for i in range(0, len(stock_daily_price), 1):
    #At the first day in serie, we consider the movement as 0 - no move
    temp_movement = [0]
    for j in range(1,128,1):
        temp_movement.append(round(stock_daily_price[i][j]/stock_daily_price[i][j-1] * 100, 2))
    
    stock_daily_movement.append(temp_movement)

#implementation of K-mean clustering simple
#data elelement comprised: ('name': [data_series])
def k_means(data, num_of_clusters, num_of_iterations):
    #identify dimension of training set
    dimension = len(data[0])
    #randomly select num_of_clusters centroids
    rand_indexes = np.random.randint(0, len(data), size=(num_of_clusters))
    print(rand_indexes)
    #pickout centroid according to the rand index
    centroids = []
    for i in rand_indexes:
        centroids.append(data[i])
    
    for n in range(num_of_iterations): 
        assignments={}
        for ind, i in enumerate(data):
            min_dist = float('inf') 
            closest_clust = None
            for c_ind, j in enumerate(centroids):
                print(ind)
                dist = euclid_dist(i, j) 
                if dist != None and dist < min_dist:
                   min_dist = dist
                   closest_clust = c_ind

            if closest_clust in assignments: 
                assignments[closest_clust].append(ind)
            else:
                assignments[closest_clust]=[] 
                assignments[closest_clust].append(ind)
        #calculate mean of the cluster to get new centroid for cluster in next round
        for key in assignments:
            clust_sum = []
            for d in range(0, dimension, 1):
                temp_cluster_item_sum = 0
                for k in assignments[key]: 
                    temp_cluster_item_sum = temp_cluster_item_sum + data[k][d]
                    clust_sum.append(temp_cluster_item_sum)
                print(clust_sum)
                centroids[key] = ([m / len(assignments[key]) for m in clust_sum])

    return centroids


print(k_means(stock_daily_movement[:10], 4, 1))