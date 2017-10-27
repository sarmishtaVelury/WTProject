from bs4 import BeautifulSoup
from urllib.request import urlopen
import csv

def scraper(domain,pageNumber):
	html = urlopen("https://www.coursera.org/browse/data-science/"+domain+"?languages=en&page="+pageNumber)

	soup = BeautifulSoup(html,'lxml')
	soup = soup.find_all("a",attrs={"class": "rc-OfferingCard"})

	title = []
	description = []
	courseList = []
	for i in soup:
		try:
			html1 = urlopen("https://www.coursera.org" + i["href"])
			soup1 = BeautifulSoup(html1,'lxml')
			allCourses = soup1.find("title")
			if(i["href"][1]=='s'):
				allDesc = soup1.find("div",attrs={"class":"description"})
			else:
				allDesc = soup1.find("p",attrs={"class":"course-description"})
				allDesc = list(allDesc)
				allDesc = allDesc[2]
			allCourses = (allCourses.string).split('|')[0]
			allDesc = allDesc.string
			print(allCourses)
			print(allDesc)
			print()
			print()
			print()
			print()
			x = allCourses.replace(',','~')
			y = allDesc.replace(',','~')
			courseList.append([domain,x,y])
		except Exception as e:
			print('Oh no: ',e)
	with open ('strictlyProfessional.csv','a') as file:
		writer=csv.writer(file)
		for row in courseList:
			writer.writerow(row)

for n in range(1,4):
	scraper(domain='machine-learning',pageNumber=str(n))