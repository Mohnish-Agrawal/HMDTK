from selenium import webdriver
import os
import random

def link_scraper(wd,broad_topics:list,specific_topics:list,users:int):
	t=15
	for user in range(users):
		for i,item in enumerate(broad_topics):
			history = set()
			for j,topic in enumerate(specific_topics[i]):
				# print(j,topic)
				google_url = "https://www.google.com/search?q={q}&safe=off&tbm=nws"
				wd.get(google_url.format(q=topic))
				link_urls = set()
				link_count=0
				k = random.randint((t//len(specific_topics[i]))-6,(t//(len(specific_topics[i]))+6))
				if j==len(specific_topics[i])-1:
					k=t-len(history)
				page_number=1
				while link_count<k:
					wd.execute_script("window.scrollTo(0,document.body.scrollHeight);")
					link_results = wd.find_elements_by_class_name("dbsr")
					number_results = len(link_results)
					for link in link_results:
						if link.find_element_by_css_selector('a').get_attribute('href'):
							if link.find_element_by_css_selector('a').get_attribute('href') not in link_urls:
								link_urls.add(link.find_element_by_css_selector('a').get_attribute('href'))
								link_count+=1
						if link_count>=k:
							print(f"Found: {link_count} of {topic}, Done!")
							break
					else:
						print(f"Found: {link_count} of {topic}, looking for more...")
						try:
							load_more = wd.find_element_by_link_text(str(page_number+1))
							load_more.click()
							page_number+=1
						except:
							page_number+=1

						if page_number>5:
							break

				history=history.union(link_urls)
				if len(history)>=t:
					print(f"Found: {t} of {item}, Done!")
					history = set(list(history)[:t])
					break
			parse_url(user,item,history)
	return

def parse_url(name:int,label:str,urls:set):
	urls=list(urls)
	random.shuffle(urls)
	target_path = "./history"
	if not os.path.exists(target_path):
		os.makedirs(target_path)
	file_path = os.path.join(target_path,str(name)+".txt")
	with open(file_path,'a') as f:
		for item in urls:
			f.write(str(item)+"\t"+label+"\n")
		f.close()
	return

Driver_path = "/home/ankit/chromedriver"
number_of_user = int(input())
# to_find = []
# for i in range(number_of_user):
# 	to_find.append(list(map(str,input().split(","))))
broad_topics = [ 'Politics', 'Business', 'Education', 'Music',  'Gaming', 'Movies/TV shows', 'Literature', 'Food',
				 'Tourism', 'Smartphones', 'Laptops', 'Automotive', 'Space', 'Nature', 'Football', 'Cricket', 
				 'Tennis', 'Basketball', 'Religion', 'Health/Medicine', 'Other Sports', 'Other Tech', 'Other News']

specific_keywords = [ ['Election', 'Biden','Trump', 'Modi', 'Government'],
['NASDAQ', 'Stocks', 'Oil', 'Gold', 'Crypto'],
['College', 'Universities', 'Exams', 'Research', 'Students'],
['Jazz', 'Artist', 'Opera', 'Spotify', 'HipHop'],
['Minecraft', 'PUBG', 'CSGO', 'COD', 'FIFA'],
['Movies', 'Directors', 'Actors', 'Anime', 'TV shows'],
['Books', 'Shakespeare',  'Drama', 'Poem', 'Stories'],
['Pizza', 'Burgers', 'Tacos', 'Shawarma', 'Biryani'],
['Dubai', 'Eiffel tower', 'Pyramids of Giza', 'Taj Mahal', 'Statue of liberty'],
['Iphone', 'Oneplus', 'Pixel', 'Samsung Galaxy', 'Huawei p series'],
['Macbook', 'Dell', 'HP', 'Lenovo', 'Microsoft Surface'],
['Tesla', 'Mercedes', 'Boeing', 'Ferrari', 'Range Rover'],
['Moon', 'Mars', 'Sun', 'Spacex', 'Galaxies'],
['Biology', 'Flowers', 'Wildlife', 'Forests', 'Volcanos'],
['Ronaldo', 'Messi', 'Champions League', 'Premier league', 'FIFA world cup'],
['IPL', 'Cricket World cup', 'T20', 'Sachin Tendulkar', 'Virat Kohli'],
['Wimbeldon', 'Roger federer', 'Nadal', 'US open', 'Djokovic'],
['NBA', 'Michael Jordan', 'Stephen Curry', 'Kobe bryant', 'Golden State warriors', 'LA Lakers'],
['Hinduism', 'Muslim', 'Christian', 'Jews', 'Buddhism'],
['COVID', 'Hospital', 'Exercise', 'Diet', 'Doctor'],
['Golf', 'Badminton', 'Rugby', 'Olympics', 'Swimming'],
['Facebook', 'Drones', 'Robotics', 'AI', 'VR'],
['Earthquake', 'Weather', 'Hurricanes', 'World records', 'Deaths']]

wd = webdriver.Chrome(executable_path=Driver_path)
link_scraper(wd,broad_topics,specific_keywords,number_of_user)