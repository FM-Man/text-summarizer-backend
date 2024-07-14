from functools import lru_cache
import nltk
import re
from nltk.tokenize import RegexpTokenizer
from gensim.models import KeyedVectors
import pickle
import os
from sklearn.cluster import SpectralClustering
from math import ceil, exp
from collections import defaultdict
import numpy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import AgglomerativeClustering
from sklearn.metrics import silhouette_score
from sklearn.manifold import MDS

nltk.download('punkt')
__all__ = ['get_summary']

"""================================== step 1 =======================================
This part preprocesses the  input document. The preprocessing involves at first
tokenizing the input document and then removing the stop words. the tokenization is
done using the 'custom_tokenizer' function and stop word removal using the 
'stopword_removal' function.
================================================================================="""


def _preprocessor(text):
    sentence_dividers = ['।', '|', '!', '\n', '?', ":"]
    sentences = _custom_tokenizer(text, sentence_dividers)  # each sentences as intact and in a list

    word_dividers = [' ', ',', '.', ';', '"', "'", '`', '(', ')', '[', ']', '-', '‘', '’‌', '%', '/', '\\']
    words = []
    for sentence in sentences:
        words.append(_custom_tokenizer(sentence, word_dividers))  # each word as a separate token now

    preprocessed_word_list = _stopword_removal(words)

    # the returning variables are two list.
    # sentences = [sent1, sent2, sent3, ...]
    # preprocessed_word_list = [[word11, word12, ...], [word21, word22, ...], ...]
    return sentences, preprocessed_word_list


def _custom_tokenizer(text, dividers):
    # idk what this regex part is doing. got it from stack overflow.
    divider_pattern = '|'.join(map(re.escape, dividers))
    tokenizer = RegexpTokenizer(f'[^{divider_pattern}]+|[{divider_pattern}]')
    tokens = tokenizer.tokenize(text)

    # removes the divider tokens and also strips them
    processed_tokens = []
    for token in tokens:
        if token.strip() and token not in dividers:
            processed_tokens.append(token.strip())

    return processed_tokens


def _stopword_removal(sentences):
    stop_words = open("../datasets/stopwords.txt", "r", encoding="utf8").readlines()
    stop_words = [stop_word.split('\n')[0] for stop_word in stop_words]

    preprocessed_word_list = []
    for sentence in sentences:
        preprocessed_word_list.append([word for word in sentence if word not in stop_words])

    return preprocessed_word_list


"""====================================step 2=======================================
Now the vector field consisting of over 1.4M bengali words are read. This function 
is cached to save time in future. 'pydic.dic' is a python dictionary written in
binary to save time reading. 'read_vectors_from_object_file' is used to read from
this file. 'cc.bn.300.vec' is a plain text file. 'read_vectors_from_plaintext' is 
used to read from here. These set of functions return a 2d list. it looks like this
[[d1,d2,d3,...,d300],[d1,d2,d3,...,d300]...total 1.4M...]
================================================================================="""


@lru_cache(maxsize=1)
def _read_vector():
    if not os.path.exists('../datasets/pydic.dic'):
        if not os.path.exists('datasets\\cc.bn.300.vec'):
            print('dataset doesnot exist. download text '
                  'from https://drive.google.com/file/d/1qSjqzygv8_T7LC_S21nCvv_x_Rt-BkK5/view?usp=sharing . download '
                  'binary from https://drive.google.com/file/d/1Iga8DB-AbUMHZvVc07byzIyPRmWkrAgn/view?usp=drive_link')
        else:
            data = _read_vectors_from_plaintext('datasets\\cc.bn.300.vec')
            return data
    else:
        data = _read_vectors_from_object_file()
        return data


def _read_vectors_from_plaintext(vec_file_path):
    # loading the plaintext model from file
    model = KeyedVectors.load_word2vec_format(vec_file_path, binary=False)
    print('dictionary done')

    # saving the binary model as a binary file so that it could be read faster in the future
    file_path = '../datasets/pydic.dic'
    with open(file_path, "wb") as file:
        pickle.dump(model, file)
    print('saving done')

    return model


def _read_vectors_from_object_file():
    # loading the binary model from the binary file
    file_path = '../datasets/pydic.dic'
    with open(file_path, "rb") as file:
        data = pickle.load(file)
    print('reading done')
    return data


"""====================================step 3================================================
replaces all the words with corresponding vectors
=========================================================================================="""


def _vectorizer(dataset, sentences):
    set_of_vectors = []

    for sentence in sentences:
        vectors_of_words_in_sentence = []
        for word in sentence:
            try:
                vector = dataset[word]
                vectors_of_words_in_sentence.append(vector)
            except KeyError:
                pass
        set_of_vectors.append(vectors_of_words_in_sentence)

    # returns a 3d list
    # [[vect1,vec2...],[vect3,vect4,...],...]
    return set_of_vectors


"""======================================step 4==============================================
This part clusters the set of vectors into related groups of sentences. the 'spectral_clustering'
function takes a 3d vector as input. along with a sigma for the similarity calculation. it
also takes a size input ranging from 0-1 indicating the size of the summary to be generated.
the function prepares the affinity matrix using the 'similarity' function. the function
takes two sets of vectors as input and a sigma value to calculate gaussian similarity. sigma can
be any number which indicates the standard daviation of the gaussian curve. but it works best 
when sigma is greater than 0.5. through experimentation it is found to work best if its 2. the 
function returns a value ranging from 0 to 1. indicating their similarity. the more similar two 
set are, the closer the value will get to 1.
=========================================================================================="""


def _spectral_clustering(set_of_vectors, sigma, size):
    # making an empty 2d array for an affinity matrix
    total_sentence = len(set_of_vectors)
    affinity_matrix = []
    for i in range(0, total_sentence):
        row = [0] * total_sentence
        affinity_matrix.append(row)

    # calculating similarity for affinity matrix
    for i in range(0, total_sentence):
        for j in range(i+1, total_sentence):
            affinity_matrix[i][j] = _similarity(set_of_vectors[i], set_of_vectors[j], sigma)
            affinity_matrix[j][i] = affinity_matrix[i][j] #_similarity(set_of_vectors[i], set_of_vectors[j], sigma)

            # number of clusters which is the size of the summary as the number of sentences
    n_clusters = max(min(2, total_sentence), ceil(total_sentence * size))
    """---------------------------------------------------------------------------------------"""
    # key = 0
    # k = []
    # my_dict = dict()
    # silhouette_scores = []
    # for n in range(2, total_sentence):
    #     # model = SpectralClustering(n_clusters=n, affinity='precomputed')
    #     # model.fit(affinity_matrix)
    #     cluster1 = AgglomerativeClustering(n_clusters=n, metric='euclidean', linkage='ward')
    #     y1 = cluster1.fit_predict(affinity_matrix)
    #     # Calculate Silhouette Scores
    #     silhouette_scores.append(silhouette_score(affinity_matrix, y1))
    #     k.append(n)
    #     my_dict[key] = n
    #     key = key + 1
    # # Find the maximum Silhouette Score
    # maxx = silhouette_scores.index(max(silhouette_scores))
    #
    # val = list(my_dict.values())
    # n_clusters = val[maxx]
    """--------------------------------------------------------------------------------------"""

    # clustering
    if len(affinity_matrix) > 1:
        model = SpectralClustering(n_clusters=n_clusters, affinity='precomputed')
        model.fit(affinity_matrix)

        # a dictionary containing the labels and a list of sentence index in that cluster is produced
        cluster_indices = defaultdict(list)
        for idx, label in enumerate(model.labels_):
            cluster_indices[label].append(idx)

        # cluster_indices = { "1" : [0,2,4...], "2":[1,3,5...],...}
        return cluster_indices

    else:
        return {}


def _similarity(sentence_x, sentence_y, sigma):
    most_similar_distances = []

    # finding the distance of the closest word from sentence y for every word in sentence x
    for word_x in sentence_x:
        msd = float('inf')
        for word_y in sentence_y:
            dist = _euclidean_distance(word_x, word_y)
            msd = min(dist, msd)
        most_similar_distances.append(msd)

    # finding the distance of the closest word from sentence x for every word in sentence y
    for word_y in sentence_y:
        msd = float('inf')
        for word_x in sentence_x:
            dist = _euclidean_distance(word_x, word_y)
            msd = min(dist, msd)
        most_similar_distances.append(msd)

    # to avoid zero divide by chance
    if len(most_similar_distances) == 0:
        return 0

    most_similar_distances = sorted(most_similar_distances)
    # avg_msd = sum(most_similar_distances) / len(most_similar_distances)
    length = ceil(len(most_similar_distances) * 1)
    # length = ceil(len(most_similar_distances)*.75)
    squared_average = 0
    for i in range(length):
        squared_average += (most_similar_distances[i] ** 2)
    squared_average /= length

    # gaussian similarity
    # return 0.3
    return exp(- squared_average / (2 * sigma ** 2))


def _euclidean_distance(vect1, vect2):
    return numpy.linalg.norm(vect1 - vect2)


"""============================Entry Point==================================
this method is called from the outside to generate summary. to generate the
summary, a text, a sigma value, a size value is inputted. size and sigma is
used in step 4 to cluster the sentences. both of these values have default
values so none of them are mandatory parameters. the function returns the
sentence indices of the summary and the summary itself.
========================================================================="""


def rank_using_tfidf(sentence_cluster):
    sentences = [s for _, s in sentence_cluster]

    tfidf_vectorizer = TfidfVectorizer()

    try:
        # Fit the vectorizer to the Bengali sentences
        tfidf_matrix = tfidf_vectorizer.fit_transform(sentences)
    except ValueError:
        return 0
    # Get feature names
    feature_names = tfidf_vectorizer.get_feature_names_out()
    # Create a dictionary to store the TF-IDF scores for each word in each sentence
    tfidf_scores = {}

    for i in range(len(sentences)):
        feature_index = tfidf_matrix[i, :].nonzero()[1]
        original_index, _ = sentence_cluster[i]
        tfidf_scores[original_index] = {feature_names[index]: tfidf_matrix[i, index] for index in feature_index}
        # print(tfidf_scores[original_index])

    # Sort sentences based on their average TF-IDF scores
    sorted_sentences = sorted(tfidf_scores.items(), key=lambda x: sum(x[1].values()), reverse=True)

    # Print the sorted sentences
    # for idx, _ in sorted_sentences:
    #     print(sentences[idx])
    return sorted_sentences[0][0]


def get_summary(text, sigma=2, size=.1):
    sentences, split_sentences = _preprocessor(text)  # step 1
    vector_space = _read_vector()  # step 2
    set_of_vectors = _vectorizer(vector_space, split_sentences)  # step 3
    set_of_clusters = _spectral_clustering(set_of_vectors, sigma, size)  # step 4

    how_many_index_different = 0

    # step 5: here each of the first sentences from a cluster is picked for the summary
    indices_in_summary = []
    for cluster in set_of_clusters.items():
        picked_index = cluster[1][0]

        #tf-idf
        sentence_in_this_cluster = []
        for sentence_index in cluster[1]:
            sentence_in_this_cluster.append((sentence_index, sentences[sentence_index]))
        if len(sentence_in_this_cluster) != 1:
            picked_index = rank_using_tfidf(sentence_in_this_cluster)

        if picked_index != cluster[1][0]:
            how_many_index_different += 1
        indices_in_summary.append(picked_index)

    print("diff:", how_many_index_different, "/", len(indices_in_summary))

    # step 6: these indices are then sorted in their order of appearance in the original document.
    for i in range(len(indices_in_summary)):
        for j in range(i + 1, len(indices_in_summary)):
            if indices_in_summary[i] > indices_in_summary[j]:
                indices_in_summary[i], indices_in_summary[j] = indices_in_summary[j], indices_in_summary[i]

    # step 7: the sentences are then extracted to generate the summary
    summary = ''
    for index in indices_in_summary:
        summary += sentences[index] + '। '

    # returns the indices and the summary. the indices are there for testing purposes only.
    return indices_in_summary, summary
