from common_utils.Preprocessor import word_divider
from common_utils.DatasetReader import read_vector
from common_utils.WordVectorizer import exp_vectorizer
from common_utils.Clusterer import exp_spectral_clustering
from functools import lru_cache
from exp_modules.expSentenceRanking import rank_sentence

def getSummary(text):
    sentences,splited_sentences = word_divider(text)
    vector_space = get_resource()
    
    vectors_with_position = exp_vectorizer(vector_space , splited_sentences)
    
    # print(words)
    clustered_indeces = exp_spectral_clustering(vectors_with_position)
    summary_indices=[]
    # Print the cluster indices
    # and pick the best from the clusters
    for cluster_idx, indices in clustered_indeces.items():
        
        picked_indx = rank_sentence(indices,vectors_with_position)
        
        summary_indices.append(picked_indx)
        
    summary_indices.sort()
    summary = ''
    for indx in summary_indices:
        summary+=sentences[indx]+'। '
    
    return summary

# caching the dataset reading
@lru_cache(maxsize=1)
def get_resource():
    return read_vector()



