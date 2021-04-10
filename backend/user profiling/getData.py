import json
import csv

names = ["Mohnish", "Abhinav", "prince", "Sitaram", "rajat", "shaunak", "rhythm", "shashikant"]
dataList = list()
userid = 0
for i in names:
	file = i + ".json"
	data = json.load(open(file, encoding = "utf-8"))
	for i in data:
		dList = [userid, i['title'], i['url'], i['lastVisitTimeUTC'], i['visitCount']]
		dataList.append(dList)
	userid += 1

with open("data.csv", 'w', encoding = 'utf-8', newline = "") as f:
	write = csv.writer(f)

	write.writerow(["id",'Title', 'url', 'Time', 'Counts'])
	write.writerows(dataList)