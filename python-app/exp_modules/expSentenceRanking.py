import numpy

def rank_sentence(cluster, word_vectors):
    cluster_vector = []
    for index in cluster:
        (pos,vect) = word_vectors[index]
        cluster_vector.append(vect)
    
    centerity = []
    for index1 in range(len(cluster_vector)):
        sentence1 = cluster_vector[index1]
        word_direction_vector_length = 0
        for word1 in sentence1:
            direction_vectors = []
            for index2 in range(len(cluster_vector)):
                if index1 != index2:
                    sentence2 = cluster_vector[index2]
                    if len(sentence2) != 0:
                        closest_word = min(sentence2, key= lambda word2 : numpy.linalg.norm(word1-word2)) 
                        direction_vectors.append(closest_word-word1)
            
            
            word_direction_vector =  numpy.zeros(300)
            for dirvec in direction_vectors:
                word_direction_vector += dirvec
            
            word_direction_vector_length += numpy.linalg.norm(word_direction_vector)
        
        centerity.append(word_direction_vector_length)
    
    min_index = centerity.index(min(centerity))

    return cluster[min_index]

            

        