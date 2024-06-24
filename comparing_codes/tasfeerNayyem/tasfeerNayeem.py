from __future__ import print_function
import collections
import re
import json
import os
import nltk
import itertools
import editdistance
import networkx as nx
import nltk
import numpy as np
from sklearn.manifold import MDS
from sklearn.cluster import AgglomerativeClustering
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import silhouette_score


# 1---- divides the document into array of sentences
def sent_tokenize(gettingText):
    dataToReSize = []
    data = []
    cleanText = ''
    for i in gettingText:
        if i == '।' or i == '!' or i == '?':
            cleanText += i
            dataToReSize.append(''.join(cleanText))
            cleanText = ''
        else:
            if i == '\n' or i == '\r' or i == '”' or i == '“' or i == '"':
                continue
            else:
                cleanText += i

    for i in dataToReSize:
        withoutAheadSpace = ''
        flag = 1
        for j in i:
            if j == ' ' and flag:
                continue
            else:
                flag = 0
                withoutAheadSpace += j
        data.append(''.join(withoutAheadSpace))

    return data


def start_f(document):
    tfidf_vectorizer = TfidfVectorizer(max_df=10, min_df=2, use_idf=True, tokenizer=tokenize_only, ngram_range=(1, 3))
    tfidf_matrix = tfidf_vectorizer.fit_transform(document)

    similarity_distance = 1 - cosine_similarity(tfidf_matrix)

    mds = MDS(n_components=2, dissimilarity="precomputed", random_state=1)
    pos = mds.fit_transform(similarity_distance)

    # n_clusters = int(np.ceil(len(document)/5))
    """---------------------------------------------------------------------------------------"""
    key = 0
    k = []
    my_dict = dict()
    silhouette_scores = []
    for n in range(2, len(document)):
        cluster1 = AgglomerativeClustering(n_clusters=n, metric='euclidean', linkage='ward')
        y1 = cluster1.fit_predict(pos)
        # Calculate Silhouette Scores
        silhouette_scores.append(silhouette_score(pos, y1))
        k.append(n)
        my_dict[key] = n
        key = key + 1
    # Find the maximum Silhouette Score
    maxx = silhouette_scores.index(max(silhouette_scores))

    val = list(my_dict.values())
    n_clusters = val[maxx]
    size_writing_file = open("size.txt", "a")
    size_writing_file.write(str(n_clusters/len(document)*100) + "\n")
    size_writing_file.close()
    """---------------------------------------------------------------------------------------"""

    cluster1 = AgglomerativeClustering(n_clusters=n_clusters, metric='euclidean', linkage='ward')
    cluster1.fit_predict(pos)

    #Create file    
    p = str(n_clusters)
    f = open("tmp/cluster" + p + ".txt", "w", encoding="utf8")
    f.truncate(0)
    f = open("tmp/cluster" + p + ".txt", "a+", encoding="utf8")

    clusters = collections.defaultdict(list)

    for i, label in enumerate(cluster1.labels_):
        clusters[label].append(i)
    dict(clusters)

    for cluster in range(n_clusters):
        for i, sentence in enumerate(clusters[cluster]):
            f.write(document[sentence])
            f.write(" ")
        f.write('\n\n')
    f.close()

    p = str(n_clusters)
    cluster_sentence1 = open("tmp/cluster" + p + ".txt", "r", encoding="utf8").read().split('\n\n')

    cluster_sentence1.pop((len(cluster_sentence1)) - 1)
    filenamee1 = []

    for j in range(n_clusters):
        ab = str(j)
        namee = "tmp/Cluster" + p + "." + ab + ".txt"
        filenamee1.append(namee)
        with open(namee, 'w', encoding="utf8") as f:
            for item in cluster_sentence1[j]:
                f.write(item)

    return filenamee1, n_clusters


def tokenize_only(text):
    # first tokenize by sentence, then by word to ensure that punctuation is caught as it's own token
    tokens = [word.lower() for sent in nltk.sent_tokenize(text) for word in nltk.word_tokenize(sent)]
    filtered_tokens = []
    # filter out any tokens not containing letters (e.g., numeric tokens, raw punctuation)
    for token in tokens:
        if re.search('[a-zA-Zঅ-ঔং ৎ  ক-‍ঁ ]', token):
            filtered_tokens.append(token)
    return filtered_tokens


def create_folder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print('Error: Creating directory. ' + directory)


def get_summary(filename):
    summary = []
    for k in range(n):
        with open(filename[k], "r", encoding="utf8") as f:
            text = f.read()

            summary_length = 40

            sentence_tokens = sent_tokenize(text)
            graph = nx.Graph()  # initialize an undirected graph
            graph.add_nodes_from(sentence_tokens)
            nodePairs = list(itertools.combinations(sentence_tokens, 2))

            # add edges to the graph (weighted by Levenshtein distance)
            for pair in nodePairs:
                firstString = pair[0]
                secondString = pair[1]
                levDistance = editdistance.eval(firstString, secondString)
                graph.add_edge(firstString, secondString, weight=levDistance)

            calculated_page_rank = nx.pagerank(graph, weight='weight')

            # most important sentences in ascending order of importance
            sentences = sorted(calculated_page_rank, key=calculated_page_rank.get, reverse=True)

            # return a 100 word summary
            summary_lines = ' '.join(sentences)
            summary_words = summary_lines.split()
            summary_words = summary_words[0:summary_length]
            dot_indices = [idx for idx, word in enumerate(summary_words) if word.find('।') != -1]
            #if clean_sentences and dot_indices:
            if dot_indices:
                last_dot = max(dot_indices) + 1
                summary_lines = ' '.join(summary_words[0:last_dot])
            else:
                summary_lines = ' '.join(summary_words)

        summary.append(summary_lines)

    full_summary = []
    for x in summary:
        left_text = x.partition("।")[0]
        left_text = left_text.partition("?")[0]
        left_text = left_text.partition("!")[0]
        full_summary.append(left_text + "।")
    s = " ".join(full_summary)
    unordered_summary = sent_tokenize(s)

    unordered_summary = [x[:(len(x) - 1)].strip(' ') for x in unordered_summary]
    docs = [x[:(len(x) - 1)].strip(' ') for x in doc]
    both = set(docs).intersection(unordered_summary)
    indices_A = [docs.index(x) for x in both]
    indices_B = [unordered_summary.index(x) for x in both]
    dictionary = {}
    for x in range(len(indices_A)):
        dictionary[indices_A[x]] = indices_B[x]
    ordered_summary = []
    for i in sorted(dictionary):
        ordered_summary.append(dictionary[i])
    st = ""
    for i in ordered_summary:
        st = st + (unordered_summary[i]) + '। '

    return st


import pandas as pd
import json
from rouge import Rouge
import numpy

documents_summaries = json.load(open("document_summaries.json", "r", encoding="utf-8"))
rouge = Rouge()

tasfeer = []

for serial_no in range(250):
    print(serial_no)
    row = {}

    document = documents_summaries[serial_no]["document"]
    row["document"] = document
    row["summary"] = documents_summaries[serial_no]['summary-1']

    # print(document)
    doc = sent_tokenize(document)
    # print(doc)
    file_name, n = start_f(doc)
    # print(file_name, "-->", n)
    machine_summary = get_summary(file_name)
    row["machine-summary"] = machine_summary

    rouge_score = rouge.get_scores(machine_summary, documents_summaries[serial_no]['summary-1'])[0]
    row["rouge-1-r"] = rouge_score['rouge-1']['r']
    row["rouge-1-p"] = rouge_score['rouge-1']['p']
    row["rouge-1-f"] = rouge_score['rouge-1']['f']
    row["rouge-2-r"] = rouge_score['rouge-2']['r']
    row["rouge-2-p"] = rouge_score['rouge-2']['p']
    row["rouge-2-f"] = rouge_score['rouge-2']['f']
    row["rouge-l-r"] = rouge_score['rouge-l']['r']
    row["rouge-l-p"] = rouge_score['rouge-l']['p']
    row["rouge-l-f"] = rouge_score['rouge-l']['f']

    tasfeer.append(row)

    row = {}
    row["document"] = document
    row["summary"] = documents_summaries[serial_no]['summary-2']
    doc = sent_tokenize(document)
    file_name, n = start_f(doc)
    machine_summary = get_summary(file_name)
    row["machine-summary"] = machine_summary

    rouge_score = rouge.get_scores(machine_summary, documents_summaries[serial_no]['summary-2'])[0]
    row["rouge-1-r"] = rouge_score['rouge-1']['r']
    row["rouge-1-p"] = rouge_score['rouge-1']['p']
    row["rouge-1-f"] = rouge_score['rouge-1']['f']
    row["rouge-2-r"] = rouge_score['rouge-2']['r']
    row["rouge-2-p"] = rouge_score['rouge-2']['p']
    row["rouge-2-f"] = rouge_score['rouge-2']['f']
    row["rouge-l-r"] = rouge_score['rouge-l']['r']
    row["rouge-l-p"] = rouge_score['rouge-l']['p']
    row["rouge-l-f"] = rouge_score['rouge-l']['f']

    tasfeer.append(row)
    # print(rouge_score)

sum_r1_p = 0
sum_r1_r = 0
sum_r1_f = 0
sum_r2_p = 0
sum_r2_r = 0
sum_r2_f = 0
sum_rl_p = 0
sum_rl_r = 0
sum_rl_f = 0

for row in tasfeer:
    sum_r1_p += row["rouge-1-p"]
    sum_r1_r += row["rouge-1-r"]
    sum_r1_f += row["rouge-1-f"]
    sum_r2_p += row["rouge-2-p"]
    sum_r2_r += row["rouge-2-r"]
    sum_r2_f += row["rouge-2-f"]
    sum_rl_p += row["rouge-l-p"]
    sum_rl_r += row["rouge-l-r"]
    sum_rl_f += row["rouge-l-f"]

tasfeer.append(
    [sum_r1_r / 500, sum_r1_p / 500, sum_r1_f / 500, sum_r2_r / 500, sum_r2_p / 500, sum_r2_f / 500, sum_rl_r / 500,
     sum_rl_p / 500, sum_rl_f / 500])

json.dump(tasfeer, open("tasfeerResult.json", "w", encoding="utf-8"), ensure_ascii=False, indent=4)
