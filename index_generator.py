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



def create_rtree_index_lfw  (n = 13234):
    p = index.Property()
    p.dimension = 128
    p.dat_extension = 'data'
    p.idx_extension = 'index'
    idx = index.Index('rtree_index_lfw', properties=p)
    i = 0
    for dir in listdir('lfw/'):
        print(f'direcory: {dir}')
        dir_path = f'lfw/{dir}'
        for img in listdir(dir_path):
            img_path = f'lfw/{dir}/{img}'
            print(f'{i} : {img_path}')
            ef = encode_file(img_path)
            if ef is not None:
                idx.insert(i, tuple(ef))
            i += 1

        if( i > n):
            break

    idx.close()


def create_rtree_index(n = 13234):
    p = index.Property()
    p.dimension = 128
    p.dat_extension = 'data'
    p.idx_extension = 'index'
    idx = index.Index('rtree_index', properties=p)
    i = 0
    for img in listdir('test/fotos_bd/'):
        print(i)
        print(img)

        ef = encode_file(f'test/fotos_bd/{img}')
        if ef is not None:
            idx.insert(i, tuple(ef) )
        i += 1

    idx.close()


def build_index_and_get_pca(filename: str, index_name: str, n=None):
    df = pd.read_csv(filename)
    labels = df.iloc[:, :2].to_numpy()
    data_matrix = df.iloc[:, 2:].to_numpy()
    
    pca = decomposition.PCA(0.90)
    fit_pca = pca.fit(data_matrix)    

    pca_data = fit_pca.transform(data_matrix)
    
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
    
    return fit_pca, idx

if __name__ == '__main__':
    index_name = 'indexes/index'
    n = None
    pca, idx = build_index_and_get_pca('lfw.csv', index_name, n)
    idx.close()

    os.remove(f"{index_name}_{n}.data")
    os.remove(f"{index_name}_{n}.index")




# if __name__ == '__main__':
#     start = time.time()
#     create_csv_lfw()
#     end = time.time()

#     print(end - start)
