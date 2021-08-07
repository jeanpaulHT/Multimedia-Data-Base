from flask import Flask, jsonify, request, redirect
from flask.helpers import url_for
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
                return jsonify(closest_matches_rtree(file, K, idx))
            except IndexError as e:
                return jsonify({ 'matches': [] })

    # If no valid image file was uploaded, show the file upload form:
    return '''
    
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">
    <link rel="stylesheet" href="https://netdna.bootstrapcdn.com/font-awesome/4.0.3/css/font-awesome.css">
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
    <script type="text/javascript" src="../static/js/match.js"></script>
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
    <style class="INLINE_PEN_STYLESHEET_ID">
        html {
            height: 100%;
          }
          
          body {
            background-color: #ffffff;
            height: 100%;
          }
          
          .wrapper {
            width: 100%;
            height: 100%;
            display: flex;
            align-items: center;
            justify-content: center;
          }
          .wrapper .file-upload {
            height: 100px;
            width: 100px;
            border-radius: 100px;
            position: relative;
            display: flex;
            justify-content: center;
            align-items: center;
            border: 4px solid #FFFFFF;
            overflow: hidden;
            background-image: linear-gradient(to bottom, #FFFFFF 50%, #2cbd00 50%);
            background-size: 100% 200%;
            transition: all 1s;
            color: #2cbd00;
            font-size: 50px;
          }
          .wrapper .file-upload input[type='file'] {
            height: 200px;
            width: 200px;
            position: absolute;
            top: 0;
            left: 0;
            opacity: 0;
            cursor: pointer;
          }
          .wrapper .file-upload:hover {
            background-position: 0 -100%;
            color: rgb(255, 255, 255);
          }
    </style>
    <title>Proyecto 2 - Face Recognition</title>
  </head>


<body>

  <div class="container-fluid">
    <div class="container">
        <div class="row">
          <div class="col-sm">
            <div class="mx-auto" style="width: 500px;">
              
                <div style="background:transparent !important" class="jumbotron">
                  <h1 class="display-4">Face Recognition</h1>
                  <p class="lead">Encuentre rostos similares a su imagen.</p>
                  
                  <hr class="my-4" >
                  <p> Adjunte una imagen con un rostro visible.
                  <p class="lead">
                      <form method=POST enctype=multipart/form-data>
                      <div class="wrapper">
                          <div class="file-upload">
                            <input type="file" name=file />                          
                          <i class="fa fa-arrow-up"></i>
                      </div>
                      <input type="file" accept="image/*" name="image" id="imgquery" onchange="loadImage(this)">
                      <input type="submit" value="Cargar">
                      </form>
                      <small id="HelpBlock" class="form-text text-muted">
                          Suba o arrastre una imagen
                      </small>
                  </p>
                </div>
                <hr class="my-4">
                <div class="container">
                  <div class="row">
                    <div class="col-sm">
                      <img id=preview>
                      <img id=mainresult />
                </div></div></div>
            </div>
          </div>
        </div>

          <div class="col-sm" id="image_results">               
          </div>
        </div>
      </div>
    
    </div>     

    <script type="text/javascript">
      function loadResults(response) {
    image_list = response;
    for (i = 0; i < image_list.length; i++) {
      var name = image_list[i].split('/').pop.replace("_", " ").split('.')[0]
      var div = document.createElement('div');
      div.setAttribute('class', 'gallery');

      var a = document.createElement('a');
      a.setAttribute('target', 'blank');
      a.setAttribute('href', image_list[i]);
      
      var img = document.createElement('img');
      img.setAttribute('src', image_list[i]);
      img.setAttribute('height', '600');
      
      a.appendChild(img);
      div.appendChild(a);
      
      var desc = document.createElement('div');
      desc.setAttribute('class', 'desc');
      desc.innerHTML = name;

      div.appendChild(desc);

      $("image_results").append(div);
    }
  }

  function loadImage(input) {
    if (input.files && input.files[0]) {
      var reader = new FileReader();
      reader.onload = function(e) {
        $('#preview')
          .attr('src', e.target.result)
          .attr('height', '400');
      };
      reader.readAsDataURL(input.files[0]);
    }
  }
    </script>
  </body>
    '''


if __name__ == '__main__':
    app.secret_key = ".."
    app.run(port=8080, threaded=True, host=('127.0.0.1'))
