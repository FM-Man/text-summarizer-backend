from common_utils.Preprocessor import word_divider
from common_utils.DatasetReader import read_vector
from common_utils.WordVectorizer import exp_vectorizer
from common_utils.Clusterer import exp_spectral_clustering,exp_spectral_clustering_sigma
from functools import lru_cache
from exp_modules.expSentenceRanking import rank_sentence

def getSummary(text):
    # sentences,splited_sentences = word_divider(text)
    # vector_space = get_resource()
    
    # vectors_with_position = exp_vectorizer(vector_space , splited_sentences)
    
    # # print(words)
    # clustered_indeces = exp_spectral_clustering(vectors_with_position)
    # summary_indices=[]
    # # Print the cluster indices
    # # and pick the best from the clusters
    # for cluster_idx, indices in clustered_indeces.items():
        
    #     picked_indx = rank_sentence(indices,vectors_with_position)
        
    #     summary_indices.append(picked_indx)
        
    # summary_indices.sort()
    # summary = ''
    # for indx in summary_indices:
    #     summary+=sentences[indx]+'। '
    
    # return summary
    get_summary_ranked_sigma(text=text,sigma=.5)





# caching the dataset reading
@lru_cache(maxsize=1)
def get_resource():
    return read_vector()



def get_summary_unranked_sigma(text, sigma=2):
    sentences,splited_sentences = word_divider(text)
    vector_space = get_resource()
    
    vectors_with_position = exp_vectorizer(vector_space , splited_sentences)
    
    clustered_indeces = exp_spectral_clustering_sigma(vectors_with_position,sigma)
    summary_indices=[]

    for cluster_idx, indices in clustered_indeces.items():
        
        picked_indx = indices[0]
        
        summary_indices.append(picked_indx)
        

    for i in range(len(summary_indices)):
        for j in range(i+1,len(summary_indices)):
            if summary_indices[i]>summary_indices[j]:
                summary_indices[i],summary_indices[j] = summary_indices[j],summary_indices[i]

    summary = ''
    for indx in summary_indices:
        summary+=sentences[indx]+'। '
    
    return summary_indices,summary




def get_summary_ranked_sigma(text,sigma):
    sentences,splited_sentences = word_divider(text)
    vector_space = get_resource()
    
    vectors_with_position = exp_vectorizer(vector_space , splited_sentences)
    
    # print(words)
    clustered_indeces = exp_spectral_clustering_sigma(vectors_with_position,sigma)
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
