from flask import Flask, jsonify, request, redirect
from flask.templating import render_template
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
    return render_template('index.html')



if __name__ == '__main__':
    app.secret_key = ".."
    app.run(port=8080, threaded=True, host=('127.0.0.1'))
