from flask import Flask, render_template, url_for, request, send_from_directory
from werkzeug.utils import secure_filename
import sys
import os
script_path = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(1, script_path + "/backend/summarization")
sys.path.insert(2, script_path + "/backend/user profiling")
from qna import getData, getPolicyData
import csv
import json
import pickle as pkl
from TopicVectorizer import TopicVectorizer

app = Flask(__name__)


def getList(file):
	file = json.load(open(file, encoding = "utf-8"))
	# print("chrome_history.json")
	l = list()
	for i in file:
		l.append(i['title'])
	return l

def loadPolicy(policyName):
	result = getPolicyData(policyName)
	return render_template("summarizedPolicies.html", result = [policyName, result])


# @app.route('/manifest.json')
# def manifest():
# 	return send_from_directory('static','manifest.json')

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

@app.route('/StartProfile', methods = ['GET', 'POST'])
def profiler():
	if request.method == 'POST':
		f = request.files['file']
		f.save(secure_filename(f.filename))
		l = getList(secure_filename(f.filename))
		# data = pkl.load(open(script_path+"/backend/user profiling/TopicVectorizer.pkl", "rb"))
		data = TopicVectorizer.load(script_path+"/backend/user profiling/TopicVectorizer.pkl").getPreferences(l)
		topics = sorted(data, key = lambda x: x[2], reverse = True)[:5]
		# print(type(data))
		# with open('templates/data.csv', 'w', encoding = "utf-8", newline = "") as f:
		# 	write = csv.writer(f)
		# 	write.writerow(["Field", "Value", "Radius","Color"])
		# 	write.writerows(data)

		return render_template('test.html', data = data, topics = topics)

@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
	if request.method == 'POST':
		f = request.files['file']
	  # f.save(secure_filename(f.filename))
		result = getData(f)
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
	# app.run(threaded = True, port = 5000)
	app.run(debug = True)
