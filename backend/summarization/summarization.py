from retrieval import rerankPassages

# data = open("whatsapp.txt", encoding = "utf-8")

# sentences = list()
# topics = list()
# lastIndex = 0

# for lines in data:
# 	if len(lines[:-1].split()) > 5:
# 		sentences.append(lines[:-1])
# 	# else:
# 	# 	sentencesUnderTopic = sentences[lastIndex:]
# 	# 	topics.append(lines[:-1])
# 	# 	for s in sentencesUnderTopic:
# 	# 		topics[-1] += s


# print("File imported!")

# getRelevantDocs = rerankPassages()
# getRelevantDocs.fit(sentences)

# print("File fitted")


# answers = getRelevantDocs.rankDocuments("Is my information shared to anyone?", 0.3)
# for a in answers:
# 	print(a)

# questions = [
# 	"Is my Information (camera access, location access, contacts) data being stored collected by this website",
# 	"Is my information data being shared to anyone with without my consent",
# 	"What are some of the new updated changes in these documents policies terms of service"
# 	""


# ]

def init(fileName):
	global getRelevantDocs
	data = open("whatsapp.txt", encoding = "utf-8")

	sentences = list()
	topics = list()
	lastIndex = 0

	for lines in data:
		if len(lines[:-1].split()) > 5:
			sentences.append(lines[:-1])

	print("File imported!")

	getRelevantDocs = rerankPassages()
	getRelevantDocs.fit(sentences)

	print("File fitted")

def getResults(questions, n_ans = 2):
	global getRelevantDocs

	mu = 0.6
	answers = list()
	for q in questions:
		ans = getRelevantDocs.rankDocuments(q, mu)[:n_ans]
		answers.append(ans)

	return answers
