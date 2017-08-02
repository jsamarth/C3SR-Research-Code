# Total links for NIA: 

import urllib2
import bs4


def url_to_soup(url):
    # bgp.he.net filters based on user-agent.
    req = urllib2.Request(url, headers={ 'User-Agent': 'Mozilla/5.0' })
    html = urllib2.urlopen(req).read() 
    return bs4.BeautifulSoup(html, "html.parser")

def getTopLevelPages():
	link = "https://www.nia.nih.gov/health/topics/"
	soup = url_to_soup(link)

	urls = []
	spans = soup.find_all("span", class_="field-content")
	for span in spans:
		urls.append("https://www.nia.nih.gov" + span.contents[0]['href'])
		
	return urls

def getAllArticleLinks(topLevelLinks):

	urls = []
	for link in topLevelLinks:
		soup = url_to_soup(link)

		tag = soup.find_all("ul", class_="no-style")
		if len(tag) != 0:
			for a in tag[0].find_all("a"):
				urls.append("https://www.nia.nih.gov" + a['href'])
				print "https://www.nia.nih.gov" + a['href']
	
	print "==== Done getting all the urls! ===="
	return list(set(urls))

# print getTopLevelPages().index("https://www.nia.nih.gov/health/topics/diagnosis")
# print getTopLevelPages()[36:37]
urls = getAllArticleLinks(getTopLevelPages())

print "==== Writing to the file ===="
file = open("links.txt", "w")
for url in urls:
	print url
	file.write(url + "\n")
file.close()
print "==== Done writing to the file ===="


