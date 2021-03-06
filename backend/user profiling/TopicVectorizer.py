# from newspaper import Article
import nltk
import pandas as pd
from tqdm import tqdm
import numpy as np
import pickle as pkl
import re
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import gensim
from gensim.utils import simple_preprocess
import gensim.corpora as corpora
from sklearn.feature_extraction.text import TfidfVectorizer  
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.utils import shuffle
wordnet_lemmatizer = WordNetLemmatizer()

class TopicVectorizer:

    def __init__(self, model, label_encoder, tfid):
        self.model = model
        self.label_encoder = label_encoder
        self.tfid = tfid
        self.stop_words = stopwords.words('english')

    @staticmethod
    def load(loc):
        return pkl.load(open(loc, 'rb'))

    def sent_to_words(self, sentence):
        return gensim.utils.simple_preprocess(str(sentence), deacc=True)

    def remove_stopwords(self, text):
        return [word for word in text if (word not in self.stop_words)]

    def lemmatize_stemming(self, text):
        return ' '.join([WordNetLemmatizer().lemmatize(word, pos='v') for word in text])

    def urls_to_text(self, urls):
        texts = []
        for url in tqdm(urls, total=len(urls)):
            article = Article(url)
            article.download()
            article.parse()
            texts.append(article.text)
        return ' '.join(texts)

    def id_to_labels(self, ids):
        return self.label_encoder.inverse_transform(ids)

    def transform_urls(self, series):
        text = ' '.join(series)
        series = pd.Series([text])
        return self.transform(series)
    
    def getPreferences(self, series):
        result = self.transform_urls(series)
        labels = self.id_to_labels(range(len(result[0])))
        result_list = list()
        result_dict = dict()
        color_dict = {20:"#A8E6CE", 40:"#DCEDC2", 60:"#FFD3B5", 80:"#FFAA66", 100: "#FF8C94"}
        nodes = 0
        for i in range(len(labels)):
            percentage = result[0,i]/max(result[0])*100
            color = ""
            for k in color_dict: 
                if k - percentage >= 0 and k - percentage <= 20:
                    color = color_dict[k]
                    break
            result_list.append([labels[i],result[0,i], int(percentage),color])
            result_dict[nodes] = {"label":labels[i], "value":result[0,i], "radius":int(percentage),"color":color}
            # result_dict["label"] = labels[i]
            # result_dict["value"] = result[0,i]
            # result_dict["radius"] = int(percentage)
            # result_dict["color"] = color
            nodes += 1

        return result_list

    def transform(self, series):
        processed = series.map(self.sent_to_words)
        processed = processed.map(self.remove_stopwords)
        processed = processed.map(self.lemmatize_stemming)
        X = self.tfid.transform(processed).toarray()
        y = self.model.predict_proba(X)
        return y
