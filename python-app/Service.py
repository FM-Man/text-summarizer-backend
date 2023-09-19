from Preprocessor import word_divider
from DatasetReader import read_vector
from WordVectorizer import vectorizer
from Clusterer import spectral_clustering
from functools import lru_cache

def getSummary(text):
    sentences,splited_sentences = word_divider(text)
    vector_space = get_resource()
    print(vector_space['বাংলা'])
    vectors_with_sentence_index = vectorizer(vector_space , splited_sentences)
    # for (i,v) in vectors_with_sentence_index:
    #     print(f's-{i}: {sentences[i]}\n{v}')
    
    # print(words)
    clustered_indeces = spectral_clustering(vectors_with_sentence_index)
    # Print the cluster indices
    for cluster_idx, indices in clustered_indeces.items():
        print(f"Cluster {cluster_idx}: {indices}")
        for index in indices:
            print(sentences[index])
        print('==============================================')
    
    return text

# caching the dataset reading
@lru_cache(maxsize=1)
def get_resource():
    return read_vector()