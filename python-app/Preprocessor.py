#https://dl.fbaipublicfiles.com/fasttext/vectors-crawl/cc.bn.300.bin.gz
import nltk
from nltk.tokenize import sent_tokenize

def tokenize_sentences(text):
    # Remove line breaks and other unwanted whitespace characters
    text = text.replace('\n', ' ').strip()
    
    # Tokenize the text into sentences using NLTK's sent_tokenize
    sentences = sent_tokenize(text)
    
    return sentences