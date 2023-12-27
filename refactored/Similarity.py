import numpy
from math import exp


def euclidean_distance(vect1, vect2):
    return numpy.linalg.norm(vect1 - vect2)


def similarity(tuple1, tuple2, sigma):
    distances = []
    pos1, cluster1 = tuple1
    pos2, cluster2 = tuple2

    for vect1 in cluster1:
        min_dist = float('inf')
        for vect2 in cluster2:
            dist = euclidean_distance(vect1, vect2)
            min_dist = min(dist, min_dist)
        distances.append(min_dist)

    for vect1 in cluster2:
        min_dist = float('inf')
        for vect2 in cluster1:
            dist = euclidean_distance(vect1, vect2)
            min_dist = min(dist, min_dist)
        distances.append(min_dist)

    if len(distances) == 0:
        return 0

    average = sum(distances) / len(distances)

    return exp(- average ** 2 / (2 * sigma ** 2))
