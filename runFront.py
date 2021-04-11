from flask import Flask, render_template, url_for, request
from werkzeug.utils import secure_filename

app = Flask(__name__)

@app.route('/')
def index():
	return render_template("index.html")

@app.route('/left-sidebar')
def left_sidebar():
	return render_template("left-sidebar.html")

@app.route('/right-sidebar')
def right_sidebar():
	return render_template("right-sidebar.html")

@app.route('/no-sidebar')
def no_sidebar():
	return render_template("no-sidebar.html")

@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
   if request.method == 'POST':
      f = request.files['file']
      f.save(secure_filename(f.filename))
      return 'file uploaded successfully'

# @app.route('/upload')
# def upload_file():
#    return render_template('upload.html')
	
# @app.route('/uploader', methods = ['GET', 'POST'])
# def uploadfile():
#    if request.method == 'POST':
#       f = request.files['file']
#       f.save(secure_filename(f.filename))
#       return 'file uploaded successfully'

if __name__ == '__main__':
	app.run(debug = True)