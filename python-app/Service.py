from Preprocessor import word_divider
from DatasetReader import read_vector
from WordVectorizer import vectorizer
from Clusterer import spectral_clustering
from functools import lru_cache
from SentenceExtraction import get_most_connected_sentence

def getSummary(text):
    sentences,splited_sentences = word_divider(text)
    vector_space = get_resource()
    print(vector_space['বাংলা'])
    vectors_with_sentence_index = vectorizer(vector_space , splited_sentences)
    
    # print(words)
    clustered_indeces = spectral_clustering(vectors_with_sentence_index)
    summary_indices=[]
    # Print the cluster indices
    # and pick the best from the clusters
    for cluster_idx, indices in clustered_indeces.items():
        print(f"Cluster {cluster_idx}: {indices}")
        for index in indices:
            print(sentences[index])
        print('=================picked========================')
        picked_indx = get_most_connected_sentence(indices,vectors_with_sentence_index)
        # print(picked_indx)
        print(sentences[picked_indx])
        summary_indices.append(picked_indx)
        print('===============================================')
        
    summary_indices.sort()
    summary = ''
    for indx in summary_indices:
        summary+=sentences[indx]+'। '
    
    return summary

# caching the dataset reading
@lru_cache(maxsize=1)
def get_resource():
    return read_vector()