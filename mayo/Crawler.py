# Total links for Mayo: 7477

import urllib2
import bs4


def url_to_soup(url):
    # bgp.he.net filters based on user-agent.
    req = urllib2.Request(url, headers={ 'User-Agent': 'Mozilla/5.0' })
    html = urllib2.urlopen(req).read() 
    return bs4.BeautifulSoup(html, "html.parser")

def returnAllPages():
	urls = []
	char = 'A'
	for i in range(0, 26):
		urls.append("http://www.mayoclinic.org/drugs-supplements/drug-list?letter=" + char)
		char = chr(ord(char) + 1)
	return urls

def saveToFile(links):
	file = open("urls.txt", "w")
	i = 1
	for link in links:
		print "============ " + link + " ==============\n"
		soup = url_to_soup(link)
		main = soup.find(id="index")
		lists = main.find_all("li")
		for a in lists:
			print " => " + str(i)
			i = i + 1
			file.write("http://www.mayoclinic.org" + a.find("a")['href'] + "\n")
	file.close()

links = returnAllPages()
saveToFile(links)

