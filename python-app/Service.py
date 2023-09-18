from Preprocessor import word_divider

def getSummary(text):
    words = word_divider(text)
    
    print(words)
    return text