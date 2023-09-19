from sklearn.metrics.pairwise import cosine_similarity
import numpy

# Define your two vectors as numpy arrays
# vector1 = np.array([1, 2, 3])
# vector2 = np.array([4, 5, 6])

# # Reshape the vectors if needed (e.g., if they are 1D arrays)
# vector1 = vector1.reshape(1, -1)  # Reshape to a row vector
# vector2 = vector2.reshape(1, -1)

# # Calculate the cosine similarity
# cosine_sim = cosine_similarity(vector1, vector2)

# print("Cosine Similarity:", cosine_sim[0][0])

def get_most_connected_sentence(cluster,vectors_with_sentence_index):
    cosine_graph=[]
    for indx1 in cluster:
        row=[]
        for indx2 in cluster:
           v1 = numpy.array(vectors_with_sentence_index[indx1]).reshape(1,-1)
           v2 = numpy.array(vectors_with_sentence_index[indx2]).reshape(1,-1)
           cosine_sim = cosine_similarity(v1,v2)
           row.append(cosine_sim)
        cosine_graph.append(row)
    
    

