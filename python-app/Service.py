from Preprocessor import sent_tokenize

def getSummary(text):
    sentences = sent_tokenize(text)
    for idx, sentence in enumerate(sentences):
        print(f"Sentence {idx + 1}: {sentence}")
    return text