def exp_vectorizer(dataset,sentences):
    vectors = []
    sentence_index = 0
    total_sentence = len(sentences)

    for sentence in sentences:
        vectors_of_words_in_sentence=[]
        for word in sentence:
            try:
                vector = dataset[word]
                vectors_of_words_in_sentence.append(vector)    
            except KeyError:
                pass
        sentence_index += 1
        vectors.append((sentence_index/total_sentence , vectors_of_words_in_sentence))
    
    return vectors
