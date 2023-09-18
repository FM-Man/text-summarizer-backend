from gensim.models import KeyedVectors
import pickle
import os

def read_vectors_from_plaintext(vec_file_path):
    # vec_file_path = '/content/drive/MyDrive/cc.bn.300.vec'
    model = KeyedVectors.load_word2vec_format(vec_file_path, binary=False)
    print('dictionary done')

    # saving the data into file
    filePath = 'pydic.dic'
    with open(filePath, "wb") as file:
        pickle.dump(model, file)
    print('saving done')

    return model

def read_vectors_from_objectfile():
    file_path = 'pydic.dic'
    with open(file_path, "rb") as file:
        data = pickle.load(file)
    print('reading done')
    return data

def read_vector():
    if not os.path.exists('pydic.dic'):
        data = read_vectors_from_plaintext('..\\java-app\\cc.bn.300.vec')
        return data
    else:
        data = read_vectors_from_objectfile()
        return data

read_vector()