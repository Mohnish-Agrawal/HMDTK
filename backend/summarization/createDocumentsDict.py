import json
from qna import getData, getPolicyData

policyDocument = "Facebook Twitter Google LinkedIn Apple Microsoft Reddit Amazon".split()

policyDocumentDictionary = dict()
for p in policyDocument:
	d = getData(p.lower() + ".txt", False)
	print(d)
	policyDocumentDictionary[p] = d

with open('data.txt', 'w') as outfile:
    json.dump(policyDocumentDictionary, outfile)

# getData("Facebook (1).txt")