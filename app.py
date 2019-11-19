import os
from flask import Flask, jsonify, request, send_from_directory
from werkzeug.utils import secure_filename  
from flask_cors import CORS    

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
STATIC_FOLDER  = os.path.join(BASE_DIR, 'static')
UPLOAD_FOLDER = os.path.join(STATIC_FOLDER, 'uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask ('__name__', static_url_path='/static')
app.config['DEBUG'] = True
app.config['ENV']= 'developmnet'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

CORS(app)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET'])
def home():
    return"Upload App"

@app.route('/upload/<path:filename>', methods=['GET'])
@app.route('/upload', methods=['POST'])
def upload_file(filename=None):
    if request.method == 'GET':
        return send_from_directory(app.config ['UPLOAD_FOLDER'], filename)
   
    if request.method == 'POST':
        if 'photo' not in request.files:
            return jsonify({"error":"please upload photo"}), 422

    
        file = request.files['photo']

        if file.filename == '':
            return jsonify({"error":"please upload photo"}), 422

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return jsonify ({"status":"photo uploaded"}), 201
        else:    
            return jsonify({"error":"photo uploaded"}), 422  


if __name__ == '__main__':
    app.run()


