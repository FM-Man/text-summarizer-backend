from sklearn.cluster import SpectralClustering
from sklearn.metrics import pairwise_distances
from numpy import exp
from math import ceil
from collections import defaultdict
from exp_modules.expDistance import get_exp_distance

def spectral_clustering(sent_vecors):
    sigma = 10
    vectors=[value[0] for value in sent_vecors.values()]
    # print(vectors[3])
    keys =[key for key in sent_vecors.keys()]
    
    affinity_matrix = exp(- pairwise_distances(vectors, squared=True) / ( sigma ** 2))

    n_clusters = ceil(len(sent_vecors)/5)
    
    model = SpectralClustering(n_clusters=n_clusters, affinity='precomputed')
    # Fit the model to the data
    model.fit(affinity_matrix)

    cluster_indices = defaultdict(list)
    cluster_org_indices = defaultdict(list)
    for idx, label in enumerate(model.labels_):
        cluster_indices[label].append(idx)
        cluster_org_indices[label].append(keys[idx])

    return cluster_org_indices


def exp_spectral_clustering(sent_vectors_position):
    total_sentence = len(sent_vectors_position)
    affinity_matrix = []
    for i in range(0,total_sentence):
        row = [0]*total_sentence
        affinity_matrix.append(row)

    for i in range(0,total_sentence):
        for j in range(i,total_sentence):
            affinity_matrix[i][j] = get_exp_distance(sent_vectors_position[i],sent_vectors_position[j])
            affinity_matrix[j][i] = get_exp_distance(sent_vectors_position[i],sent_vectors_position[j])
    
    model = SpectralClustering(n_clusters=ceil(total_sentence/6), affinity='precomputed')
    model.fit(affinity_matrix)
    cluster_indices = defaultdict(list)
    for idx, label in enumerate(model.labels_):
        cluster_indices[label].append(idx)
    
    return cluster_indices




