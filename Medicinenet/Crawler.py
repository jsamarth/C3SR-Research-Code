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
	char = 'a'
	for i in range(0, 26):
		urls.append("http://www.medicinenet.com/diseases_and_conditions/alpha_" + char + ".html")
		char = chr(ord(char) + 1)
	return urls

def saveToFile(links):
	file = open("urls.txt", "w")
	urls = []
	for link in links:
		# print "============ " + link + " ==============\n"
		soup = url_to_soup(link)
		main = soup.find(id="AZ_container")
		uls = main.find_all("ul")
		for ul in uls:
			for li in ul.contents:
				if type(li) is bs4.element.NavigableString:
					continue
				urls.append("http://www.medicinenet.com" + li.find("a")['href'])
	print len(urls)
	urls = list(set(urls))
	for url in urls:
		file.write(url + "\n")
		# print url + "\n"
	print len(urls)
	file.close()

links = returnAllPages()
saveToFile(links)

