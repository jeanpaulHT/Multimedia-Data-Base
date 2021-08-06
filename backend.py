from flask import Flask, jsonify, request, redirect
from matchers import *
import os

# You can change this to any folder on your system
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
idx = read_index(labels, pca_data, index_name)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def upload_image():
    # Check if a valid image file was uploaded
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)

        file = request.files['file']

        if file.filename == '':
            return redirect(request.url)

        if file and allowed_file(file.filename):
            # The image file seems valid! Detect faces and return the result.
            return jsonify(closest_matches_rtree(file, K, idx))

    # If no valid image file was uploaded, show the file upload form:
    return '''
    <!doctype html>
    <title>Es la foto de Vizcarra?</title>
    <h1>Cargar una foto y ver si corresponde al presidente Vizcarra!</h1>
    <form method="POST" enctype="multipart/form-data">
      <input type="file" name="file">
      <input type="submit" value="Cargar">
    </form>
    '''



if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)
