from sklearn.cluster import SpectralClustering
from math import ceil
from collections import defaultdict
from exp_modules.expDistance import get_exp_distance_sigma


def exp_spectral_clustering_sigma(sent_vectors_position,sigma):
    total_sentence = len(sent_vectors_position)
    affinity_matrix = []
    for i in range(0,total_sentence):
        row = [0]*total_sentence
        affinity_matrix.append(row)

    for i in range(0,total_sentence):
        for j in range(i+1,total_sentence):
            affinity_matrix[i][j] = affinity_matrix[j][i] = get_exp_distance_sigma(sent_vectors_position[i],sent_vectors_position[j],sigma)
    

    cluster_number = ceil(total_sentence/4)

    if len(affinity_matrix) > 1:
        model = SpectralClustering(n_clusters=cluster_number, affinity='precomputed')
        model.fit(affinity_matrix)
    
        cluster_indices = defaultdict(list)
        for idx, label in enumerate(model.labels_):
            cluster_indices[label].append(idx)
    
        return cluster_indices
    
    else:
        return {}




