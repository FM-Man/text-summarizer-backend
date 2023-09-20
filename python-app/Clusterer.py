from sklearn.cluster import SpectralClustering
from sklearn.metrics import pairwise_distances
from numpy import exp
from math import ceil
from collections import defaultdict

def spectral_clustering(sent_vecors):
    sigma = 10
    vectors=[value[0] for value in sent_vecors.values()]
    # print(vectors[3])
    keys =[key for key in sent_vecors.keys()]
    
    affinity_matrix = exp(- pairwise_distances(vectors, squared=True) / ( sigma ** 2))

    n_clusters = ceil(len(sent_vecors)/4)
    
    model = SpectralClustering(n_clusters=n_clusters, affinity='precomputed')
    # Fit the model to the data
    model.fit(affinity_matrix)

    cluster_indices = defaultdict(list)
    cluster_org_indices = defaultdict(list)
    for idx, label in enumerate(model.labels_):
        cluster_indices[label].append(idx)
        cluster_org_indices[label].append(keys[idx])

    return cluster_org_indices