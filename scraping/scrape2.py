from bs4 import BeautifulSoup
from urllib.request import urlopen
import csv

def scraper(domain):
	html = urlopen("https://in.udacity.com/courses/"+domain)

	soup = BeautifulSoup(html,'lxml')
	soup = soup.select("h3 > a")

	description = []
	courseList = []

	for i in soup:

		try:
			html1 = urlopen("https://in.udacity.com" + i["href"])
			soup1 = BeautifulSoup(html1,'lxml')
			allCourses = soup1.select("h1")
			allDescNano = soup1.find("div",attrs={"class":"mb-0","_ngcontent-c16":""})
			allDesc = soup1.find("div",attrs={"_ngcontent-c13":"","class":"summary-text"})
			
			for title,desc in zip(allCourses,allDescNano):
				# print ()
				# print ()
				x = title.string
				y = desc.string
				#print ()
				#print ()
			courseList.append([domain, x, y])	

		except Exception as e:
			for title,desc in zip(allCourses,allDesc):
				# print (title.string)
				# print (desc.string)
				# print ()
				# print ()
				x = title.string
				y = desc.string
				#print ()
				#print ()
			courseList.append([domain, x, y])


			#print('Oh no: ',e)
	with open ('udacity.csv','a') as file:
		writer=csv.writer(file)
		for row in courseList:
			writer.writerow(row)

# domains = ["android","deep-learning","Developer%20Essentials","digital-marketing","georgia-tech-masters-in-cs","ios","machine-learning",
# "mobile-app-development","non-tech","self-driving-car","software-engineering","virtual-reality","web-development"]

# for each in domains:
scraper("deep-learning")