from Preprocessor import word_divider
from DatasetReader import read_vector
from WordVectorizer import vectorizer

def getSummary(text):
    sentences,splited_sentences = word_divider(text)
    vector_space = read_vector()
    print(vector_space['বাংলা'])
    vectors_with_sentence_index = vectorizer(vector_space , splited_sentences)
    for (i,v) in vectors_with_sentence_index:
        print(f's-{i}: {sentences[i]}\n{v}')
    # print(words)
    return text