from flask import Flask, jsonify, request, redirect
from flask.helpers import url_for
from flask.templating import render_template
from matchers import *
import json
import os

# You can change this to any folder on your system
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
idx = read_index(labels, pca_data, index_name)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def query():
    # Check if a valid image file was uploaded
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)

        file = request.files['file']

        if file.filename == '':
            return redirect(request.url)

        if file and allowed_file(file.filename):
          # The image file seems valid! Detect faces and return the result.
            try:
              image_list = json.dumps(closest_matches_rtree(file, K, idx))
              to_render = '''
              <!doctype html>
                            <style>
                  div.gallery {
                      margin: 5px;
                      border: 1px solid #ccc;
                      float: left;
                      width: 180px;
                  }

                  div.gallery:hover {
                      border: 1px solid #777;
                  }

                  div.gallery img {
                      width: 100%;
                      height: auto;
                  }

                  div.desc {
                      padding: 15px;
                      text-align: center;
                  }
              </style>
              <title>Image search</title>
              <h1>Encuentre rostos similares a su imagen.</h1>
              <form method="POST" enctype="multipart/form-data">
                <input type="file" name="file" accept="image/* onchange="loadImage(this)">
                <input type="submit" value="Cargar">
              </form>
              <div class="col-sm" id="image_results">
              '''
              image_list = json.loads(image_list)
              for image in image_list['matches']:
                image['path'] = 'static/' + image['path']
                print (image['path'])
                to_add = "<div class='gallery'> <img src ='"
                to_add += str(image['path'])
                to_add += "'>" 
                to_add += "<div class='desc'><p>"
                to_add += os.path.splitext(os.path.basename(image['path']))[0]
                to_add += "</p></div></div>"
                to_render += to_add
              to_render += "</div>"
              #return jsonify(closest_matches_rtree(file, K, idx))
              return to_render
            except IndexError as e:
              return '''
       <!doctype html>
    <title>Image search</title>
    <h1>Encuentre rostos similares a su imagen.</h1>
    <form method="POST" enctype="multipart/form-data">
      <input type="file" name="file" accept="image/* onchange="loadImage(this)">
      <input type="submit" value="Cargar">
      <p>Index error</p>
    </form>
    '''

    # If no valid image file was uploaded, show the file upload form:
    return '''
       <!doctype html>
    <title>Image search</title>
    <h1>Encuentre rostos similares a su imagen.</h1>
    <form method="POST" enctype="multipart/form-data">
      <input type="file" name="file" accept="image/* onchange="loadImage(this)">
      <input type="submit" value="Cargar">
    </form>
    '''


if __name__ == '__main__':
    app.secret_key = ".."
    app.run(port=8080, threaded=True, host=('127.0.0.1'))
