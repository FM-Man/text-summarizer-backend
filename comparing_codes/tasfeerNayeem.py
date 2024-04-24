from __future__ import print_function
import collections
import re
import os
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


def sentTokenize(gettingText):
        dataToReSize=[]
        data=[]
        cleanText=''
        for i in gettingText:
            if i=='।' or i=='!' or i=='?':
                cleanText+=i
                dataToReSize.append(''.join(cleanText))
                cleanText=''
            else:
                if i=='\n' or i=='\r' or i=='”' or i=='“' or i=='"':
                    continue
                else:
                    cleanText+=i
        #print (dataToReSize)
        for i in dataToReSize:
            withoutAheadSpace=''
            flag=1
            for j in i:
                if j==' ' and flag:
                    continue
                else:
                    flag=0
                    withoutAheadSpace+=j
            data.append(''.join(withoutAheadSpace))
        #print(data)
                
        return data

#1.2
def startF(document):

    tfidf_vectorizer = TfidfVectorizer(max_df=10, min_df=2, use_idf=True, tokenizer=tokenize_only, ngram_range=(1,3))    
    tfidf_matrix = tfidf_vectorizer.fit_transform(document)
    
    similarity_distance = 1 - cosine_similarity(tfidf_matrix)
    
    mds = MDS(n_components=2, dissimilarity="precomputed", random_state=1)
    pos = mds.fit_transform(similarity_distance) 

    n_clusters = int(np.ceil(len(document)/5))
    
    cluster1 = AgglomerativeClustering(n_clusters=n_clusters, affinity='euclidean', linkage='ward')
    cluster1.fit_predict(pos)
    
    #Create file    
    p = str(n_clusters)
    f = open("tmp/cluster"+p+".txt","w",encoding="utf8")
    f.truncate(0)
    f = open("tmp/cluster"+p+".txt","a+",encoding="utf8")
    
    clusters = collections.defaultdict(list)

    for i, label in enumerate(cluster1.labels_):
        clusters[label].append(i)
    dict(clusters)
        
    for cluster in range(n_clusters):
        for i,sentence in enumerate(clusters[cluster]):
            f.write(document[sentence])
            f.write(" ")
        f.write('\n\n')
    f.close()

    p = str(n_clusters)
    cluster_sentence1 = open("tmp/cluster"+p+".txt","r",encoding="utf8").read().split('\n\n')
    print(cluster_sentence1)
    cluster_sentence1.pop((len(cluster_sentence1))-1)
    filenamee1 = []
    print(n_clusters)
    for j in range(n_clusters):
        ab = str(j)
        namee = "tmp/Cluster"+p+"."+ab+".txt"
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


#create folder
def createFolder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print ('Error: Creating directory. ' +  directory)


#Get Summary
def getSummary(filename):  
    summary = []
    for k in range(n):
        with open(filename[k],"r",encoding="utf8") as f:
            text=f.read()
            
            summary_length=40
            
            sentence_tokens = sentTokenize(text)
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
            if  dot_indices:
                last_dot = max(dot_indices) + 1
                summary_lines = ' '.join(summary_words[0:last_dot])
            else:
                summary_lines = ' '.join(summary_words)

        summary.append(summary_lines)

    full_summary =[]
    for x in summary:
        left_text = x.partition("।")[0]
        left_text = left_text.partition("?")[0]
        left_text = left_text.partition("!")[0]
        full_summary.append(left_text+"।")  
    s = " ".join(full_summary)
    unordered_summary = sentTokenize(s)


    unordered_summary = [x[:(len(x)-1)].strip(' ') for x in unordered_summary]
    docs = [x[:(len(x)-1)].strip(' ') for x in doc]
    both = set(docs).intersection(unordered_summary)
    indices_A = [docs.index(x) for x in both]
    indices_B = [unordered_summary.index(x) for x in both]    
    dictionary = {}
    for x in range(len(indices_A)):
        dictionary[indices_A[x]] = indices_B[x]    
    ordered_summary = []
    for i in sorted (dictionary) : 
        ordered_summary.append(dictionary[i])
    st =""
    for i in ordered_summary:
        st = st +(unordered_summary[i])+'। '
    
    
    return st







serial_no = str(1)
document = open('f',encoding="utf8").read()
doc = sentTokenize(document)
filenamee, n = startF(doc)
summary = getSummary(filenamee)

print(summary)
