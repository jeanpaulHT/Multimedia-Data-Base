import face_recognition
import numpy as np
from sklearn.decomposition import PCA
import os

# Pre-calculated face encoding of Obama generated with face_recognition.face_encodings(img)
path = "test/fotos_bd/"



def lfw_encoder():

    directory = "lfw/"
    for filename in os.listdir(directory):

    return known_face_encoding

if __name__ == '__main__':
    # image_enc = image_encoder("keiko")
    # image_enc_1 = image_encoder("muñoz")
    #
    # pca = PCA(0.95)
    # pca.fit([image_enc,image_enc_1 ])
    lfw_encoder()

    print(pca.n_components_)




