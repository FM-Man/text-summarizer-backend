from Preprocessor import word_divider
from DatasetReader import read_vector
from WordVectorizer import exp_vectorizer
from Clusterer import spectral_clustering
from functools import lru_cache


# caching the dataset reading
@lru_cache(maxsize=1)
def get_resource():
    return read_vector()


def get_summary(text, sigma=2):
    sentences, split_sentences = word_divider(text)
    vector_space = get_resource()

    vectors_with_position = exp_vectorizer(vector_space, split_sentences)

    clustered_indices = spectral_clustering(vectors_with_position, sigma)
    summary_indices = []

    for cluster_idx, indices in clustered_indices.items():
        picked_index = indices[0]
        summary_indices.append(picked_index)

    for i in range(len(summary_indices)):
        for j in range(i + 1, len(summary_indices)):
            if summary_indices[i] > summary_indices[j]:
                summary_indices[i], summary_indices[j] = summary_indices[j], summary_indices[i]

    summary = ''
    for index in summary_indices:
        summary += sentences[index] + '। '

    return summary_indices, summary

