#https://dl.fbaipublicfiles.com/fasttext/vectors-crawl/cc.bn.300.bin.gz

import nltk
nltk.download('punkt')
import re
from nltk.tokenize import RegexpTokenizer

def split_text_by_dividers(text, dividers):
    # Create a regular expression pattern to match the dividers
    divider_pattern = '|'.join(map(re.escape, dividers))
    
    # Use the RegexpTokenizer to split the text based on the dividers
    tokenizer = RegexpTokenizer(f'[^{divider_pattern}]+|[{divider_pattern}]')
    sentences = tokenizer.tokenize(text)
    
    # Remove any empty strings from the list of tokens
    sentences = [sentence.strip() for sentence in sentences if (sentence.strip() and sentence not in dividers)]
    
    return sentences

def stopword_removal(words):
    stop_word_file = open("datasets\\stopwords.txt","r",encoding="utf8")
    stop_words = stop_word_file.readlines()
    stop_words = [stop_word.split('\n')[0] for stop_word in stop_words]
    
    preprocessed_word_list = []
    for sentence in words:
        preprocessed_word_list.append([word for word in sentence if word not in stop_words])
    # print(preprocessed_word_list)

    return preprocessed_word_list

def word_divider(text):
    sentenceDividers = ['।', '|', '!', '\n', '?',":"]
    sentences = split_text_by_dividers(text=text,dividers=sentenceDividers)
    
    # for idx, sentence in enumerate(sentences):
    #     print(f"Sentence {idx + 1}: {sentence}")
    
    wordDividers = [' ', ',', '.', ';', '"', "'", '`','(',')','[',']','-','‘','’‌','%','/','\\']
    words=[]
    for sentence in sentences:
        words.append(split_text_by_dividers(sentence,wordDividers))

    preprocessed_word_list = stopword_removal(words)
    # print(preprocessed_word_list)
    return sentences, preprocessed_word_list

