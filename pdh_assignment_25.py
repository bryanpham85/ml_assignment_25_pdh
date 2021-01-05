from os import walk
import math


#define Euclid Distance
def euclid_dist(d1, d2):
    if len(d1) != len(d2):
        return None
    
    sum_diff = 0
    for i in range(0, len(d1), 1):
        sum_diff = sum_diff + (d1[i] - d2[i])**2
    return math.sqrt(sum_diff)

#load all data of companies into dict with Company Code as Key and array of 128 days price as values
stock_daily_price = {}
companies_stock_code = []

file_max_count = 500 #try with small number of file
for (dirpath, dirnames, filenames) in walk('./data/'):
    filenames.sort()
    for f in filenames:
        if file_max_count == 0:
            break
        companies_stock_code.append(f.split('.')[0])
        temp_price = []
        #read line
        with open('./data/' + f) as file_content:
            prices = file_content.read().splitlines()
            for j in range(0,245,1):
                temp_price.append(float(prices[j]))
        stock_daily_price[f.split('.')[0]] = temp_price
        file_max_count = file_max_count - 1 #will remove at final version

# the price of stocks are in different range, and we cluster the timeserie data 
# #so that we check the movement of the price over period of 128 days
stock_daily_movement = {}

for key in stock_daily_price.keys():
    #At the first day in serie, we consider the movement as 0 - no move
    temp_movement = [0]
    for j in range(1,128,1):
        temp_movement.append(round(stock_daily_price[key][j]/stock_daily_price[key][j-1] * 100, 2))
    stock_daily_movement[key] = temp_movement

#implementation of K-mean clustering simple
#data elelement comprised: ('name': [data_series])
def k_means(data: dict, num_of_clusters:int, num_of_iterations:int):
    #identify dimension of training set
    dimension = len(data[list(data.keys())[0]])
    ds_size = len(data)
    #pickout centroid according to the rand index
    #we divide the training set into num_of_cluster as initial state 
    #get the starting item of cluster to be the initial centroid
    init_centroid_indexes = []
    centroids = {}
    sample_names = list(data.keys())
    for i in range(0, num_of_clusters, 1):
        current_index = math.floor((ds_size/num_of_clusters)*i)
        init_centroid_indexes.append(current_index)
        centroids[i] = data[sample_names[current_index]]

    # print(init_centroid_indexes)
    # print('\n=============\n')
    # print(centroids)

    # Step 1: assign n-k patterns into closest cluster. 
    # Given that the current centroid of cluster is itself, so that the euclid_dist will be min(0), so that we can go through the list as total n items
    assignments = {}
    last_round_clusters_assignment = {}
    while(True):
        assignments={}
        for sample in sample_names:
            min_dist = float('inf') 
            closest_clust = None
            for j in range(num_of_clusters):
                dist = euclid_dist(data[sample], centroids[j]) 
                if dist < min_dist:
                   min_dist = dist
                   closest_clust = j

            if closest_clust in assignments.keys(): 
                assignments[closest_clust].append(sample)
            else:
                assignments[closest_clust]=[] 
                assignments[closest_clust].append(sample)
        
        #calculate mean of the cluster to get new centroid for cluster in next round
        for key in list(assignments.keys()):
            clust_sum = []
            for d in range(0, dimension, 1):
                temp_cluster_item_sum = 0
                for k in assignments[key]: 
                    temp_cluster_item_sum += data[k][d]
                
                clust_sum.append(temp_cluster_item_sum)
                #print(clust_sum)
            centroids[key] = ([m / len(assignments[key]) for m in clust_sum])

        if last_round_clusters_assignment != assignments:
            last_round_clusters_assignment = assignments
        else:
            break

    return assignments, centroids

def error_function(clusters: dict, data: dict, centroid: dict):
    total_square_deviation = 0
    #calculate euclid distance item in cluster vs. centroid
    for cluster in list(clusters.keys()):
        for pattern in clusters[cluster]:
            total_square_deviation += euclid_dist(centroid[cluster], data[pattern])
    return total_square_deviation

final_clusters, final_centroids = k_means(stock_daily_price, 5, 13)

print('\n square deviation of k=5')
print(error_function(final_clusters, stock_daily_price, final_centroids))

print('\n=========FINAL Cluster')
print(final_clusters)
print('Final centroids')
#print(final_centroids)

final_clusters, final_centroids = k_means(stock_daily_price, 4, 13)

print('\n square deviation of k=4')
print(error_function(final_clusters, stock_daily_price, final_centroids))

print('\n=========FINAL Cluster')
print(final_clusters)
print('Final centroids')
#print(final_centroids)

final_clusters, final_centroids = k_means(stock_daily_price, 6, 13)

print('\n square deviation of k=6')
print(error_function(final_clusters, stock_daily_price, final_centroids))

print('\n=========FINAL Cluster')
print(final_clusters)
print('Final centroids')
#print(final_centroids)

final_clusters, final_centroids = k_means(stock_daily_price, 500, 100)

print('\n square deviation of k=500')
print(error_function(final_clusters, stock_daily_price, final_centroids))

print('\n=========FINAL Cluster')
print(final_clusters)
print('Final centroids')
#print(final_centroids)