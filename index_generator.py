import face_recognition
import numpy as np
from rtree import index
from os import listdir
import pandas as pd
import time


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


def pca_of_reduced_rtree(filename: str, index_name: str, n=None):
    df = pd.read_csv(filename)
    labels = df.iloc[:, :2].to_numpy()
    data_matrix = df.iloc[:, 2:].to_numpy()
    print(data_matrix.shape)
    
    pca = decomposition.PCA(0.90)
    fit_pca = pca.fit(data_matrix)

    pca_data = fit_pca.transform(data_matrix)
    print(fit_pca.components_.T.shape)

    print(data_matrix[0].shape)
    print(pca_data[0])
    print(np.dot(data_matrix[0], fit_pca.components_.T))

    
    data_length = pca_data.shape[1] if n is None else n

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

    idx.close()

    
    return fit_pca

if __name__ == '__main__':
    pca = pca_of_reduced_rtree('lfw.csv', 'indexes/index', 100)
#     arr = np.ndarray([-0.04670116, -0.06473108,  0.37089212,  0.11607505, -0.17187698,  0.04956204,
#   0.0852189,  -0.08376594, -0.08885518,  0.03646477,  0.08852634,  0.11392743,
#  -0.07022093, -0.0200064,   0.07731579,  0.01284326, -0.12859442, -0.07765993,
#   0.01505157,  0.03167434,  0.00070232,  0.09785064, -0.08300794, -0.1417194,
#   0.05603394, -0.05141134, -0.05901501,  0.05400739,  0.01704408,  0.02399501,
#   0.03632427,  0.03276507, -0.00752122, -0.0190076,  -0.02536417, -0.1277002,
#   0.04824758,  0.03157686, -0.04801019,  0.02628937, -0.03327496,  0.02359096,
#  -0.00479919, -0.00241983, -0.05425637, -0.02274882,  0.04423013, -0.04051111,
#  -0.07505367])




# if __name__ == '__main__':
#     start = time.time()
#     create_csv_lfw()
#     end = time.time()

#     print(end - start)
