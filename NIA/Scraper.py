

import urllib2
import bs4
import json
import os.path


# #################### Helper functions ###########################
def replaceAllOccurences(string, string1, string2):
	while string.find(string1) != -1:
		string = string.replace(string1, string2)
	return string

def removeTagFromString(string, tagToRemove):
	first = string.find("<" + tagToRemove)
	while first != -1:	
		last = string.find(">", first+1)
		string = string[:first] + string[last+1:]
		first = string.find("<" + tagToRemove)
	string = replaceAllOccurences(string, "</" + tagToRemove + ">", "")
	return string

def removeCharactersFromString(string):
	temp = string
	temp = replaceAllOccurences(temp, "   ", " ")
	temp = replaceAllOccurences(temp, "  ", " ")
	temp = replaceAllOccurences(temp, "\n", "")
	temp = replaceAllOccurences(temp, "\r", "")
	temp = replaceAllOccurences(temp, "\t", "")
	temp = replaceAllOccurences(temp, "..", ".")
	temp = replaceAllOccurences(temp, "<em>", "")
	temp = replaceAllOccurences(temp, "</em>", "")
	temp = replaceAllOccurences(temp, "<ul>", "")
	# temp = replaceAllOccurences(temp, "</ul>", "")
	temp = replaceAllOccurences(temp, "<li>", "")
	temp = replaceAllOccurences(temp, "</li>", ".")
	temp = replaceAllOccurences(temp, "<p>", "")
	temp = replaceAllOccurences(temp, "</p>", " ")
	temp = replaceAllOccurences(temp, "<br>", "")
	temp = replaceAllOccurences(temp, "<br/>", "")
	# temp = replaceAllOccurences(temp, "</ol>", "")
	temp = replaceAllOccurences(temp, "<h3>", "")
	temp = replaceAllOccurences(temp, "</h3>", " ")
	temp = replaceAllOccurences(temp, "<h2>", "")
	temp = replaceAllOccurences(temp, "</h2>", " ")
	temp = replaceAllOccurences(temp, "<h4>", "")
	temp = replaceAllOccurences(temp, "</h4>", " ")
	# temp = replaceAllOccurences(temp, "</div>", "")
	
	temp = removeTagFromString(temp, "div")
	temp = removeTagFromString(temp, "a")
	temp = removeTagFromString(temp, "ol")
	temp = removeTagFromString(temp, "ul")

	return temp

def url_to_soup(url):
    # bgp.he.net filters based on user-agent.
    req = urllib2.Request(url, headers={ 'User-Agent': 'Mozilla/5.0' })
    html = urllib2.urlopen(req).read() 
    return bs4.BeautifulSoup(html, "html.parser")


# ================== Get all the links from the file ==================
def getAllLinks():
	file = open("links.txt", "r")
	urls = []
	for i in file:
		temp = i
		temp = temp.replace("\n", "")
		urls.append(temp)
	file.close()
	return urls


# =================== Scrape all the data ==========================
def createFiles(links):

	filenum = 1
	for link in links:

		print "\n\n===== url number " + str(filenum) + " ====="
		print link

		soup = url_to_soup(link)
		div = soup.find("div", class_="field-item even")

		greybox = soup.find("div", class_="greybox")

		string = ""
		for child in div.children:
			if child is greybox:
				continue
			tempString = str(child)
			if tempString.find("<h2") != -1:
				continue
			string += removeCharactersFromString(tempString)


		jsonData = {}
		jsonData['url'] = link
		jsonData['text'] = removeCharactersFromString(string)

		fileToSaveData = open("files/" + str(filenum) + ".json", "w")
		fileToSaveData.write(json.dumps(jsonData))
		fileToSaveData.close()
		print "done with file " + str(filenum)
		filenum += 1

createFiles(getAllLinks())
	