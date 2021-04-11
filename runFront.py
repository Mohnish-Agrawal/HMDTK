from flask import Flask, render_template, url_for, request
from werkzeug.utils import secure_filename
import sys
import os
script_path = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(1, script_path + "/backend/summarization")
from qna import getData, getPolicyData
# from test import randomout

def loadPolicy(policyName):
	result = getPolicyData(policyName)
	return render_template("summarizedPolicies.html", result = [policyName, result])

app = Flask(__name__)

@app.route('/')
def index():
	return render_template("index.html")

# @app.route('/left-sidebar')
# def left_sidebar():
# 	return render_template("left-sidebar.html")

# @app.route('/right-sidebar')
# def right_sidebar():
# 	return render_template("right-sidebar.html")

# @app.route('/no-sidebar')
# def no_sidebar():
# 	return render_template("no-sidebar.html")

@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
   if request.method == 'POST':
      f = request.files['file']
      # f.save(secure_filename(f.filename))
      print("Going in")
      result = getData(f)
      print(result)
      return render_template("summarizedPolicies.html", result = [f.filename[:f.filename.find(".")], result])

@app.route('/loadPolicyfb')
def loadPolicyfb():
	return loadPolicy("Facebook")

@app.route('/loadPolicytwitter')
def loadPolicyTwitter():
	return loadPolicy("Twitter")

@app.route('/loadPolicygoogle')
def loadPolicyGoogle():
	return loadPolicy("Google")

@app.route('/loadPolicyli')
def loadPolicyli():
	return loadPolicy("LinkedIn")

@app.route('/loadPolicyapple')
def loadPolicyApple():
	return loadPolicy("Apple")

@app.route('/loadPolicymc')
def loadPolicyMC():
	return loadPolicy("Microsoft")

@app.route('/loadPolicyreddit')
def loadPolicyReddit():
	return loadPolicy("Reddit")

@app.route('/loadPolicyamazon')
def loadPolicyAmazon():
	return loadPolicy("Amazon")




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