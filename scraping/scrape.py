from bs4 import BeautifulSoup
from urllib.request import urlopen

html = urlopen("https://www.coursera.org/browse/computer-science/computer-security-and-networks?languages=en")

soup = BeautifulSoup(html,'lxml')
soup = soup.find_all("a",attrs={"class": "rc-OfferingCard"})

for i in soup:
    #print(i["href"])
    html1 = urlopen("https://www.coursera.org" + i["href"])
    soup1 = BeautifulSoup(html1,'lxml')
    allCourses = soup1.find_all("h2",attrs={"class":"s12n-headline display-6-text"})
    allDesc = soup1.find_all("div",attrs={"class":"description subsection"})  
    
    for name,desc in zip(allCourses,allDesc):
        print (name.string + ":" + " \n " + desc.string)
        print ("\n")
