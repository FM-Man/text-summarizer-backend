def vectorizer(dataset,sentences):
    vectors ={}
    total_sentence = 0

    for sentence in sentences:
        word_in_the_sentence=0
        # list of vectors of each word in the sentence
        vectors_of_words_in_sentence=[]
        for word in sentence:
            try:
                vector = dataset[word]
                vectors_of_words_in_sentence.append(vector)
                word_in_the_sentence += 1    
            except KeyError:
                # print(f'{word} not found in the model, skipping...')
                x=1
        
        
        if word_in_the_sentence != 0:
            # size is 300
            average_vector = [0]*300
            for single_word_vector in vectors_of_words_in_sentence:
                index_of_dimension = 0
                for dimension in single_word_vector:
                    average_vector [index_of_dimension] += (1/word_in_the_sentence)*dimension
                    index_of_dimension += 1
            # adding positional data
            average_vector.append(total_sentence/len(sentences))
            vectors[total_sentence] = vectors_of_words_in_sentence
        
        total_sentence+=1
    
    return vectors