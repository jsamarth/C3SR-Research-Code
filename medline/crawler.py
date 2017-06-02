import urllib2
import bs4

# this gets all the links to the 27 pages
def getMainLinks():
	links = []
	char = 'A'
	for i in range(0, 26):
		links.append("https://medlineplus.gov/druginfo/drug_" + char + "a.html")
		char = chr(ord(char) + 1)
	links.append("https://medlineplus.gov/druginfo/drug_00.html")
	return links

# this gets the soup for a particular url
def url_to_soup(url):
    # bgp.he.net filters based on user-agent.
    req = urllib2.Request(url, headers={ 'User-Agent': 'Mozilla/5.0' })
    html = urllib2.urlopen(req).read()
    soup = bs4.BeautifulSoup(html, "html.parser")
    return soup

# this gets all the links on a particular page
def storeAllDrugsLinks(links):
	fileToSaveData = open("drug-links.txt", "w")

	for link in links:
		print "\n==== page=" + link + "====\n"
		soup = url_to_soup(link)
		allLists = soup.find_all(id="index")[0].find_all("li")
		
		# for every list item, find the 'a' tag and then the corresponding 'href'
		for i in allLists:
			print "https://medlineplus.gov/druginfo" + i.a['href'][1:]
			fileToSaveData.write("https://medlineplus.gov/druginfo" + i.a['href'][1:] + "\n")

	fileToSaveData.close()



# MAIN CODE
links = getMainLinks()
storeAllDrugsLinks(links)

