from rtree import index
from flask import Flask, jsonify, request, redirect
import face_recognition
from index_generator import build_index_and_get_pca

import numpy as np

# app = Flask(__name__)

index_path = 'indexes/index_100'

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
K = 8

pca = build_index_and_get_pca('lfw.csv', index_path)

p = index.Property()
p.dimension = pca.components_.shape[0]
p.dat_extension = 'data'
p.idx_extension = 'index'

idx = index.Index(index_path, properties=p, interleaved=True)




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


def detect_faces_in_image(file_stream):
    # Load the uploaded image file
    img = face_recognition.load_image_file(file_stream)
    # Get face encodings for any faces in the uploaded image

    unknown_face_encodings = face_recognition.face_encodings(img)
    reduced_face_encoding = pca.transform(unknown_face_encodings[0].reshape(1, -1))

    print(reduced_face_encoding)
    print(reduced_face_encoding.shape)
    bounding_box = np.concatenate((reduced_face_encoding,reduced_face_encoding),axis=1)

    closest_matches = [n.object for n in idx.nearest(tuple(bounding_box[0]), K, objects=True)]
    distances = face_recognition.face_distance(closest_matches, reduced_face_encoding)


    
    # if len(unknown_face_encodings) > 0:
    #     face_found = True
    #     # See if the first face in the uploaded image matches the known face of Obama
        
    #     match_results = face_recognition.compare_faces([known_face_encoding], reduced_face_encoding)
    #     # Your can use the distance to return a ranking of faces <face, dist>. 
    #     # face_recognition.face_distance([known_face_encoding], unknown_face_encodings[0])
    #     if match_results[0]:
    #         is_vizcarra = True

    # Return the result as json
    result = {
        "best_matches": closest_matches,
        "distances": distances
    }
    return result

# if __name__ == "__main__":
#     app.run(host='0.0.0.0', port=5001, debug=True)



if __name__ == '__main__':
    print(detect_faces_in_image('./Paul-Henri_Mathieu_0003.jpg'))