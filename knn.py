import face_recognition
from index_generator import *
from sklearn import decomposition

import numpy as np
import pandas as pd
import os
import heapq as hq


# app = Flask(__name__)

index_path = 'indexes/index'

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
K = 8
n = None

index_name = 'indexes/index'
data_file = 'lfw.csv'

print('loading df')
df = pd.read_csv(data_file)
labels, data_matrix = df.iloc[:, :2].to_numpy(), df.iloc[:, 2:].to_numpy()

pca = decomposition.PCA(0.90).fit(data_matrix)    
pca_data = pca.transform(data_matrix)

print('reading index')
idx = read_index(labels, pca_data, index_name)


def closest_matches(file_stream, knn_function, k=K):
    img = face_recognition.load_image_file(file_stream)
    # Get face encodings for any faces in the uploaded image

    unknown_face_encodings = face_recognition.face_encodings(img)
    face_encoding = unknown_face_encodings[0].reshape(1, -1)

    reduced_face_encoding = pca.transform(face_encoding)

    paths, points = knn_function(reduced_face_encoding, k)

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

def rtree_knn_search(encoding, k=K):
    bounding_box = np.concatenate((encoding, encoding),axis=1)

    closest_matches = list(idx.nearest(tuple(bounding_box[0]), k, objects=True))

    paths = [i.object for i in closest_matches]
    points = [pca_data[i.id] for i in closest_matches]

    return paths, points

def seq_knn_search(encoding, k=K):
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

def closest_matches_rtree(file_stream):
    return closest_matches(file_stream, rtree_knn_search)

def closest_matches_sequential(file_stream):
    return closest_matches(file_stream, seq_knn_search)



# def allowed_file(filename):
#     return '.' in filename and \
#            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# @app.route('/', methods=['GET', 'POST'])
# def upload_image():
#     # Check if a valid image file was uploaded
#     if request.method == 'POST':
#         if 'file' not in request.files:
#             return redirect(request.url)

#         file = request.files['file']

#         if file.filename == '':
#             return redirect(request.url)

#         if file and allowed_file(file.filename):
#             # The image file seems valid! Detect faces and return the result.
#             return detect_faces_in_image(file)

#     # If no valid image file was uploaded, show the file upload form:
#     return '''
#     <!doctype html>
#     <title>Es la foto de Vizcarra?</title>
#     <h1>Cargar una foto y ver si corresponde al presidente Vizcarra!</h1>
#     <form method="POST" enctype="multipart/form-data">
#       <input type="file" name="file">
#       <input type="submit" value="Cargar">
#     </form>
#     '''




# if __name__ == "__main__":
#     app.run(host='0.0.0.0', port=5001, debug=True)


if __name__ == '__main__':
    import json
    
    print(json.dumps(closest_matches_rtree('./Paul-Henri_Mathieu_0003.jpg'), indent=4))