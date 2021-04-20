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

<<<<<<< HEAD
=======
# import nltk
# import pandas as pd
# from tqdm import tqdm
# import numpy as np
# import pickle as pkl
# import re
# from nltk.corpus import stopwords
# from nltk.stem import WordNetLemmatizer
# import gensim
# from gensim.utils import simple_preprocess
# import gensim.corpora as corpora
# from sklearn.feature_extraction.text import TfidfVectorizer  
# from sklearn.preprocessing import LabelEncoder
# from sklearn.model_selection import train_test_split
# from sklearn.utils import shuffle
# wordnet_lemmatizer = WordNetLemmatizer()

# class TopicVectorizer(object):
# 	pass
#     def __init__(self, model, label_encoder, tfid):
#         self.model = model
#         self.label_encoder = label_encoder
#         self.tfid = tfid
#         self.stop_words = stopwords.words('english')

#     @staticmethod
#     def load(loc):
#         return pkl.load(open(loc, 'rb'))

#     def sent_to_words(self, sentence):
#         return gensim.utils.simple_preprocess(str(sentence), deacc=True)

#     def remove_stopwords(self, text):
#         return [word for word in text if (word not in self.stop_words)]

#     def lemmatize_stemming(self, text):
#         return ' '.join([WordNetLemmatizer().lemmatize(word, pos='v') for word in text])

#     def urls_to_text(self, urls):
#         texts = []
#         for url in tqdm(urls, total=len(urls)):
#             article = Article(url)
#             article.download()
#             article.parse()
#             texts.append(article.text)
#         return ' '.join(texts)

#     def id_to_labels(self, ids):
#         return self.label_encoder.inverse_transform(ids)

#     def transform_urls(self, series):
#         text = ' '.join(series)
#         series = pd.Series([text])
#         return self.transform(series)
    
#     def getPreferences(self, series):
#         result = self.transform_urls(series)
#         labels = self.id_to_labels(range(len(result[0])))
#         result_list = list()
#         color_dict = {20:"#A8E6CE", 40:"#DCEDC2", 60:"#FFD3B5", 80:"#FFAA6", 100: "#FF8C94"}
#         for i in range(len(labels)):
#             percentage = result[0,i]/max(result[0])*100
#             color = ""
#             radius = 100
#             for k in color_dict: 
#                 if k - percentage >= 0 and k - percentage <= 20:
#                     color = color_dict[k]
#                     break
#             result_list.append([labels[i],result[0,i], int(percentage),color])
#         return result_list

#     def transform(self, series):
#         processed = series.map(self.sent_to_words)
#         processed = processed.map(self.remove_stopwords)
#         processed = processed.map(self.lemmatize_stemming)
#         X = self.tfid.transform(processed).toarray()
#         y = self.model.predict_proba(X)
#         return y
>>>>>>> d07e52e22688a35792cf94074ae2b6f2b47145a7

app = Flask(__name__)


def getList():
	file = json.load(open(script_path + "/backend/user profiling/Abhinav.json", encoding = "utf-8"))
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

@app.route('/StartProfile')
def profiler():
	l = getList()
<<<<<<< HEAD
	data = pkl.load(open(script_path+"/backend/user profiling/TopicVectorizer.pkl", "rb"))
	# data = TopicVectorizer.load(script_path+"/backend/user profiling/TopicVectorizer.pkl").getPreferences(l)
	print(type(data))
	# with open('static/data.csv', 'w', encoding = "utf-8", newline = "") as f:
	# 	write = csv.writer(f)
	# 	write.writerow(["Field", "Value", "Radius","Color"])
	# 	write.writerows(data)
=======
	model = pkl.load(open(script_path+"/backend/user profiling/TopicVectorizer.pkl", "rb"))
# 	data = TopicVectorizer.load(script_path+"/backend/user profiling/TopicVectorizer.pkl").getPreferences(l)

# 	with open('static/data.csv', 'w', encoding = "utf-8", newline = "") as f:
# 		write = csv.writer(f)
# 		write.writerow(["Field", "Value", "Radius","Color"])
# 		write.writerows(data)
>>>>>>> d07e52e22688a35792cf94074ae2b6f2b47145a7

	return render_template('test.html')

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
