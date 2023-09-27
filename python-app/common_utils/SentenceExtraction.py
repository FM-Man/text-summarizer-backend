from sklearn.metrics.pairwise import cosine_similarity
import numpy

def get_most_connected_sentence(cluster,vectors_with_sentence_index):
    cosine_graph=[]
    sumations = []
    for indx1 in cluster:
        row=[]
        sumation=0.0
        for indx2 in cluster:
           v1 = vectors_with_sentence_index[indx1] #numpy.array(vectors_with_sentence_index[indx1]).reshape(1,-1)
           v2 = vectors_with_sentence_index[indx2] #numpy.array(vectors_with_sentence_index[indx2]).reshape(1,-1)
           cosine_sim = cosine_similarity(v1,v2)[0][0]
        #    print(cosine_sim)
        #    print(type(cosine_sim))
           sumation+=cosine_sim
           row.append(cosine_sim)
        cosine_graph.append(row)
        sumations.append(sumation)
    # print(cosine_graph)
    max_index = sumations.index(max(sumations))

    return cluster[max_index]
    