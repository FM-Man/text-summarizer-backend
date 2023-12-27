from common_utils.Preprocessor import word_divider
from common_utils.DatasetReader import read_vector
from common_utils.WordVectorizer import vectorizer
from common_utils.Clusterer import spectral_clustering
from functools import lru_cache
from common_utils.SentenceExtraction import get_most_connected_sentence

def getSummary(text):
    sentences,splited_sentences = word_divider(text)
    vector_space = get_resource()
    vectors_with_sentence_index = vectorizer(vector_space , splited_sentences)
    
    clustered_indeces = spectral_clustering(vectors_with_sentence_index)
    summary_indices=[]

    for cluster_idx, indices in clustered_indeces.items():
        
        picked_indx = get_most_connected_sentence(indices,vectors_with_sentence_index)
        
        summary_indices.append(picked_indx)
        
        
    # summary_indices.sort()
    for i in range(len(summary_indices)):
        for j in range(i+1,len(summary_indices)):
            if summary_indices[i]>summary_indices[j]:
                summary_indices[i],summary_indices[j] = summary_indices[j],summary_indices[i]

    summary = ''
    for indx in summary_indices:
        summary+=sentences[indx]+'। '
    
    return summary_indices,summary

# caching the dataset reading
@lru_cache(maxsize=1)
def get_resource():
    return read_vector()