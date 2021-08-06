import face_recognition
import numpy as np
from rtree import index
from os import listdir
import pandas as pd
import time
import os

from sklearn import decomposition


def encode_file(file):
    faces_vect = face_recognition.load_image_file(file)

    try:
        known_face_encoding = face_recognition.face_encodings(faces_vect)[0]
        return known_face_encoding

    except IndexError as e:
        print(e, "face was not recognized")
        return  None


def create_csv_lfw  (n = 13234):
    dimension = 128

    col_name  = ["name"]
    for num in range(dimension):
        col_name.append(str(num + 1))

    df = pd.DataFrame(columns= col_name)
    i = 0
    row = 0
    for dir in listdir('lfw/'):
        print(f'direcory: {dir}')
        dir_path = f'lfw/{dir}'
        for img in listdir(dir_path):
            img_path = f'lfw/{dir}/{img}'
            ef = encode_file(img_path)
            if ef is not None:
                df.loc[row] = [img_path] + list(ef)
                row += 1
            i += 1
            print(f'file {i} done')
        if(i > n):
            break

    df.to_csv("lfw.csv")




def build_index(labels, pca_data, index_name: str, n=None):
    data_length = pca_data.shape[0] if n is None else n

    p = index.Property()
    p.dimension = pca_data.shape[1]
    p.dat_extension = 'data'
    p.idx_extension = 'index'

    idx = index.Index(f"{index_name}_{n}", properties=p, interleaved=True)

    for (i, path), vector in zip(labels, pca_data):
        if not i < data_length:
            break
        bounding_box = np.concatenate([vector, vector])
        idx.insert(i, tuple(bounding_box), obj=path)
    
    return idx


def read_index(_, pca_data, index_name: str, n=None):
    p = index.Property()
    p.dimension = pca_data.shape[1]
    p.dat_extension = 'data'
    p.idx_extension = 'index'

    idx = index.Index(f"{index_name}_{n}", properties=p, interleaved=True)
    return idx

if __name__ == '__main__':
    index_name = 'indexes/index'
    n = None
    
    df = pd.read_csv('lfw.csv')

    labels, data_matrix = df.iloc[:, :2].to_numpy(), df.iloc[:, 2:].to_numpy()
    
    pca = decomposition.PCA(0.90).fit(data_matrix)    
    pca_data = pca.transform(data_matrix)
    

    idx = build_index(labels, pca_data, index_name, n)
    idx.close()

    os.remove(f"{index_name}_{n}.data")
    os.remove(f"{index_name}_{n}.index")




# if __name__ == '__main__':
#     start = time.time()
#     create_csv_lfw()
#     end = time.time()

#     print(end - start)
