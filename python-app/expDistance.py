import numpy
from math import exp


def get_euclidean_distance(vect1,vect2):
    return numpy.linalg.norm(vect1-vect2)



def get_exp_distance(tuple1, tuple2):
    distances=[]
    pos1,cluster1 = tuple1
    pos2,cluster2 = tuple2

    for vect1 in cluster1:
        min_dist = float('inf')
        for vect2 in cluster2:
            dist = get_euclidean_distance(vect1,vect2)
            min_dist = min(dist,min_dist)
        distances.append(min_dist)
    
    for vect1 in cluster2:
        min_dist = float('inf')
        for vect2 in cluster1:
            dist = get_euclidean_distance(vect1,vect2)
            min_dist = min(dist,min_dist)
        distances.append(min_dist)
    
    if len(cluster1)+len(cluster2)-len(distances) != 0:
        raise Exception(f"Sorry, no numbers {len(cluster1)+len(cluster2) & {len(distances)}}")
    
    if len(distances)==0:
        return 0
    
    average = sum(distances)/len(distances)
    # positional_difference = abs(pos1-pos2)
    

    return exp(-average) #/ abs(pos1-pos2)

    

