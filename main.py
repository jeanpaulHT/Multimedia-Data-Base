from rtree import index
from flask import Flask, jsonify, request, redirect
import face_recognition
from index_generator import build_index_and_get_pca

import numpy as np
import os

# app = Flask(__name__)

index_path = 'indexes/index'

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
K = 8
n = None

try:
    os.remove(f"{index_path}_{n}.data")
    os.remove(f"{index_path}_{n}.index")
except Exception:
    pass
pca, idx = build_index_and_get_pca('lfw.csv', index_path)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


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


def closest_matches_knn(file_stream):
    # Load the uploaded image file
    img = face_recognition.load_image_file(file_stream)
    # Get face encodings for any faces in the uploaded image

    unknown_face_encodings = face_recognition.face_encodings(img)
    reduced_face_encoding = pca.transform(unknown_face_encodings[0].reshape(1, -1))

    size = reduced_face_encoding.shape[1]
    bounding_box = np.concatenate((reduced_face_encoding, reduced_face_encoding),axis=1)

    closest_matches = list(idx.nearest(tuple(bounding_box[0]), K, objects=True))
    paths = [i.object for i in closest_matches]
    points = [i.bounds[:size] for i in closest_matches]

    distances = face_recognition.face_distance(points, reduced_face_encoding)
    print(distances)

    # hope this is enough
    result = {
        'matches': [
            {
                'path': file, 
                'distance': distance
            } for file, distance in zip(paths, distances)
        ]
    }
    return result

# if __name__ == "__main__":
#     app.run(host='0.0.0.0', port=5001, debug=True)



if __name__ == '__main__':
    import json
    print(json.dumps(closest_matches_knn('./Paul-Henri_Mathieu_0003.jpg'), indent=4))