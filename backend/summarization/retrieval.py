import nltk
import itertools
import os
import math
import spacy
from nltk.corpus import stopwords  
from nltk.tokenize import word_tokenize
from collections import defaultdict
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer, util
from sentence_transformers.cross_encoder import CrossEncoder
from gensim.summarization.bm25 import BM25

class bm25:

	def __init__(self, nlp):
		self.tokenize = lambda text: [token.lemma_ for token in nlp(text)]
		self.bm25 = None
		self.passages = None

	def preprocess(self, doc):
		passages = [p for p in doc.split('\n') if p and not p.startswith('=')]
		return passages

	def fit(self, docs):
			# passages = list(itertools.chain(*map(self.preprocess, docs)))
		corpus = [self.tokenize(p) for p in docs]
		self.bm25 = BM25(corpus)
		self.passages = docs

	def most_similar(self, question, topn=10):
		tokens = self.tokenize(question)
		# average_idf = sum(map(lambda k: float(self.bm25.idf[k]), self.bm25.idf.keys())) / len(self.bm25.idf.keys())
		scores = self.bm25.get_scores(tokens)
		pairs = [(s, i) for i, s in enumerate(scores)]
		pairs.sort(reverse=True)
		passages = [self.passages[i] for _, i in pairs[:topn]]
		return passages
	
	def rankDocuments(self, query):
		tokens = self.tokenize(query)
		# average_idf = sum(map(lambda k: float(self.bm25.idf[k]), self.bm25.idf.keys())) / len(self.bm25.idf.keys())
		scores = self.bm25.get_scores(tokens)
		return np.array([s for i,s in enumerate(scores)]).reshape((1,len(self.passages)))

class tfidf:

	def __init__(self, nlp):
		self.nlp = nlp
		self.tfidf_model = None
		self.documents = None

	def processSentence(self, sentence):
		sentence = sentence.lower() #Lowering sentences

		#Removing punctuations
		symbols = "!\"#$%&()*+-./:;<=>?@[\]^_`{|}~\n"
		sentence = sentence.translate(str.maketrans(symbols,' '*len(symbols)))

		#removing stopwords
		stop_words = set(stopwords.words('english')) 
		word_tokens = word_tokenize(sentence)  
		filtered_sentence = " ".join([w for w in word_tokens if w not in stop_words and len(w) > 1])

		#lemmatization
		doc = self.nlp(filtered_sentence)
		lemmatized_sentence = [t.lemma_ for t in doc]
		
		return lemmatized_sentence

	def preprocessDocument(self, passages):
		vocabulary = set()
		processed_passages = list()

		for p in range(len(passages)):
			lemmatized_sentence = self.processSentence(passages[p])
			processed_passages.append(" ".join(lemmatized_sentence))
			vocabulary.update(set(lemmatized_sentence))
		
		self.tfidf_model = TfidfVectorizer(vocabulary = list(vocabulary))
		self.documents = self.tfidf_model.fit_transform(processed_passages)
	
	def rankDocuments(self, query):
		query = " ".join(self.processSentence(query))
		queryVector = self.tfidf_model.transform([query])
		return np.transpose(cosine_similarity(self.documents, queryVector))

class sbert:

	def __init__(self):
		self.model = SentenceTransformer('msmarco-distilroberta-base-v2')
		self.document = None

	def fit(self, docs):
		self.document = self.model.encode(docs)
	
	def rankDocuments(self, query):
		query_encoded = self.model.encode(query)
		return util.pytorch_cos_sim(query_encoded, self.document).numpy()

class rerankPassages:

	def __init__(self):
		SPACY_MODEL = os.environ.get("SPACY_MODEL", "en_core_web_sm")
		nlp = spacy.load(SPACY_MODEL, disable = ["ner","parser","textcat"])
		self.tfidf_ranking = tfidf(nlp)
		self.bm25_ranking = bm25(nlp)
		# self.sbert_ranking = sbert()

		self.cross_encoder = CrossEncoder("cross-encoder/ms-marco-TinyBERT-L-6")
		self.document = None
	
	def fit(self, document):
		self.document = document
		self.tfidf_ranking.preprocessDocument(document)
		# self.sbert_ranking.fit(document)
		self.bm25_ranking.fit(document)

	def matchParaSent(self, s, p):
		
		sList = s.split()
		if len(sList) < 1:
			return False
		count = 0
		for i in sList:
			if i in p:count += 1
	
		if count/len(sList) > 0.9: return True
		else: 
			return False

	def getSentences(self, query, n):
		return self.kg.retrieveSentences(query, n)

	def withKg(self, query, paras, t):
			sentences = self.kg.retrieveSentences(query, 10)

			for i in paras:
				avgScore = 0
				sentencesMatched = 0
				for s in sentences:
					sentence = s['sentence']
					score = s['score']
					if self.matchParaSent(sentence, i[0]):
						if sentence not in i[0]: print(sentence, i[0])
						# print(sentence, i[0])
						sentencesMatched += 1
						avgScore += score
				# if sentencesMatched == 0: sentencesMatched = 1
				i[1] = 1/(t + i[1]) + 1/(t + sentencesMatched)

			paras.sort(key = lambda x : x[1])
			return [i[0] for i in paras]

	def withCrossEncoder(self, query, paras):
		para_combination = [[query, p] for p in paras]

		score = self.cross_encoder.predict(para_combination)
		sim_scores_argsort = reversed(np.argsort(score))
		
		reranked_passages = list()
		for idx in sim_scores_argsort:
			reranked_passages.append(paras[idx])
		return reranked_passages

	def rankDocuments(self, query, mu):
		bm25_scores = self.bm25_ranking.rankDocuments(query)
		tfidf_scores = self.tfidf_ranking.rankDocuments(query)
		# sbert_scores = self.sbert_ranking.rankDocuments(query)
		#Combined scoring
		# mu = 0.7
		# k = 10
		rrf = mu*bm25_scores + (1-mu)*tfidf_scores
		# rrf = 1/(k+c) + 1/(k + bm25_scores)
		# print(rrf)
		# print(np.shape(rrf))
		#retrive top k passages
		scores = rrf.tolist()
		score_passage = [(s,i) for i, s in enumerate(scores[0])]
		score_passage.sort(reverse = True)
		# return self.withKg(query, [[self.document[i[1]], i[0]] for i in score_passage[:4]], k)
		return self.withCrossEncoder(query, [self.document[i[1]] for i in score_passage[:5]])

		# return [self.document[i[1]] for i in score_passage[:4]]
