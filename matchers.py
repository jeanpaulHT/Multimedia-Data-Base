import face_recognition
from index_generator import *
from sklearn import decomposition

import numpy as np
import pandas as pd
import os
import heapq as hq


index_path = 'indexes/index'

K = 8
n = None

index_name = 'indexes/index'
data_file = 'lfw.csv'

print('loading df')
df = pd.read_csv(data_file)
labels, data_matrix = df.iloc[:, :2].to_numpy(), df.iloc[:, 2:].to_numpy()

pca = decomposition.PCA(0.90).fit(data_matrix)    
pca_data = pca.transform(data_matrix)


def filter_matches(file_stream, filter_function, params, idx):
    img = face_recognition.load_image_file(file_stream)
    # Get face encodings for any faces in the uploaded image

    unknown_face_encodings = face_recognition.face_encodings(img)
    face_encoding = unknown_face_encodings[0].reshape(1, -1)

    reduced_face_encoding = pca.transform(face_encoding)

    paths, points = filter_function(reduced_face_encoding, params, idx)

    distances = face_recognition.face_distance(points, reduced_face_encoding)
    result = {
        'matches': [
            {
                'path': file, 
                'distance': distance
            } for file, distance in zip(paths, distances)
        ]
    }
    result['matches'].sort(key=lambda x: x['distance'])
    return result

def range_filter(encoding, d, idx):
    max_encoding = encoding + d
    min_encoding = encoding - d

    bounding_box = np.concatenate((min_encoding, max_encoding),axis=1)
    candidate_matches = list(idx.intersection(tuple(bounding_box[0]), objects=True))

    c_paths = [i.object for i in candidate_matches]
    c_enc = [pca_data[i.id] for i in candidate_matches]

    distances = face_recognition.face_distance(c_enc, encoding)

    matches = ((c_paths[i], c_enc[i]) for i, d_ in enumerate(distances) if d_ <= d)

    paths, points = zip(*matches)
    return paths, points

def rtree_knn_search(encoding, k, idx):
    bounding_box = np.concatenate((encoding, encoding),axis=1)

    closest_matches = (idx.nearest(tuple(bounding_box[0]), k, objects=True))

    paths = [i.object for i in closest_matches]
    points = [pca_data[i.id] for i in closest_matches]

    return paths, points

def seq_knn_search(encoding, k, idx):
    queue = []
    distances = face_recognition.face_distance(pca_data, encoding)

    iterator = zip(labels, pca_data, distances)
    for (i, path), point, distance in iterator:
        if not i < k:
            break
        hq.heappush(queue, (-distance, path, point))

    for (_, path), point, distance in iterator:
        hq.heappushpop(queue, (-distance, path, point))

    _, paths, points = zip(*queue)
    
    return paths, points

def range_matches_search(file_stream, d, idx):
    return filter_matches(file_stream, range_filter, d, idx)

def closest_matches_rtree(file_stream, k, idx):
    return filter_matches(file_stream, rtree_knn_search, k, idx)

def closest_matches_sequential(file_stream, k, idx):
    return filter_matches(file_stream, seq_knn_search, k, idx)






# if __name__ == "__main__":
#     app.run(host='0.0.0.0', port=5001, debug=True)


if __name__ == '__main__':
    import json
    print('reading index')
    idx = read_index(labels, pca_data, index_name)
    
    print(json.dumps(
        range_matches_search('./Paul-Henri_Mathieu_0003.jpg', 0.5, idx), indent=4))