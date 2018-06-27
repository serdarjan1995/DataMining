import numpy as np
import csv
import random
import math

att_first = 1
att_last = 8

def nearest_centroid(instance,centroids,cluster_count):
    dist = []
    for centroid in centroids:
        summ = 0
        for i in range (att_first,att_last):
            summ += (float(centroid[i])-float(instance[i]))**2
        dist.append(math.sqrt(summ))
    return np.argmin(dist)

def new_centroids(clusters,centroids,cluster_count):
    for cluster in range(0,cluster_count):
        for feature in range (att_first,att_last):
            summ = 0
            for row in clusters[cluster]:
                summ += float(row[feature])
            summ = float(summ / len(clusters[cluster]))
            centroids[cluster][feature] = summ

print("K-Means")
file = open("abalone_data_clustering.csv","r")
rows = csv.reader(file, delimiter=',')
data = []
for row in rows:
    data.append(row)
row_count = len(data)
file.close()
print("Dataset imported successfully...")

cluster_count = 11#int(input("Enter cluster count:"))
cluster_centroids = []
for i in range(0,cluster_count):
    random_centroid = random.randint(0,row_count)
    cluster_centroids.append(data[random_centroid])
print('Initial centroids:')
for cluster in cluster_centroids:
    print(cluster)

MaxIter = 100
for itera in range(0,MaxIter):
    clusters = []
    for i in range(0,cluster_count):
        clusters.append([])
        
    for row in data:
        nearest_c = nearest_centroid(row,cluster_centroids,cluster_count)
        clusters[nearest_c].append(row)
        
    new_centroids(clusters,cluster_centroids,cluster_count)

## final centroids
    
print('\nFinal centroids:')
for cluster in cluster_centroids:
    print(cluster)

## confusing matrix
print('\nConfusion Matrix:')
classLabelIndex = 8
minClassLabel = int(data[0][classLabelIndex])
for row in data:
    if( int(row[classLabelIndex])< minClassLabel ):
        minClassLabel = int(row[classLabelIndex])
    
#for i in range(1,cluster_count+1):
#    print(repr('c'+str(i)).rjust(2), end=" | ")
#print('\n')
confusion_matrix = np.zeros((cluster_count,cluster_count+1), dtype='int')
for i in range(0,cluster_count):
    counts = np.zeros((cluster_count,), dtype=int)
    for row in clusters[i]:
        indx = int(row[classLabelIndex]) - minClassLabel
        counts[indx] += 1
    for j in range(0,cluster_count):
        confusion_matrix[i][j] = counts[j]
        #print(repr(confusion_matrix[i][j]).rjust(2), end="  |  ")
    confusion_matrix[i][j+1] = minClassLabel+i
    #print('age:'+str(confusion_matrix[i][j+1]))


#accuracy
k = 0
for j in range(0,cluster_count):
    max_value = confusion_matrix[k][j]
    max_index = k
    for i in range(k+1,cluster_count):
        if(max_value < confusion_matrix[i][j]):
            max_value = confusion_matrix[i][j]
            max_index = i
    if(max_index != k):
        temp = np.zeros((0,cluster_count+1), dtype='int')
        temp = np.copy(confusion_matrix[k])
        print('temp',temp)
        print('confusion_matrix[k]',confusion_matrix[k] , 'k:', k)
        confusion_matrix[k] = np.copy(confusion_matrix[max_index])
        print('confusion_matrix[k]',confusion_matrix[k] , 'k:', k)
        print('confusion_matrix[max_index]',confusion_matrix[max_index] , 'max_index:', max_index)
        print(confusion_matrix[k], k)
        confusion_matrix[max_index] = np.copy(temp)
    k += 1


incorrect = 0
for i in range(1,cluster_count+1):
    print(repr('c'+str(i)).rjust(2), end=" | ")
print('\n')
for i in range(0,cluster_count):
    for j in range(0,cluster_count):
        print(repr(confusion_matrix[i][j]).rjust(2), end="  |  ")
        if(i != j):
            incorrect += confusion_matrix[i][j]
    print('age:'+str(confusion_matrix[i][j+1]))
    
print('Incorrectly clustered:',incorrect)
print('Accuracy:', float((row_count-incorrect)/row_count)*100, '%')
