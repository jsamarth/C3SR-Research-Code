

import urllib2
import bs4
import json
import os.path
import sys


# #################### Helper functions
def removeTagFromString(tagToRemove, string):
	first = string.find("<" + tagToRemove)
	while first != -1:	
		last = string.find(">", first+1)
		string = string[:first] + string[last+1:]
		first = string.find("<" + tagToRemove)
	string = replaceAllOccurences(string, "</" + tagToRemove + ">", "")
	return string

def replaceAllOccurences(string, string1, string2):
	while string.find(string1) != -1:
		string = string.replace(string1, string2)
	return string

def removeATag(tagname, string):
	first = string.find("<" + tagname)
	while first != -1:	
		last = string.find(tagname + ">", first+1)
		last = string.find(">", last)
		string = string[:first] + string[last+1:]
		first = string.find("<" + tagname)
	return string

def removeCharactersFromString(string):
	temp = string
	temp = temp.replace("<ul>", "")
	temp = temp.replace("</ul>", "")
	temp = temp.replace("<li>", "")
	temp = temp.replace("</li>", "")
	temp = temp.replace("<p>", "")
	temp = temp.replace("</p>", " ")
	temp = temp.replace("<br>", "")
	temp = temp.replace("<br/>", "")
	temp = temp.replace("</ol>", "")
	temp = temp.replace("<h3>", "")
	temp = temp.replace("</h3>", " ")
	temp = temp.replace("<h2>", "")
	temp = temp.replace("</h2>", " ")
	temp = temp.replace("<h4>", "")
	temp = temp.replace("</h4>", " ")
	temp = temp.replace("..", ".")
	temp = temp.replace(".", ". ")

	temp = temp.replace("\n", "")
	temp = temp.replace("\t", " ")
	temp = temp.replace("\r", "")

	temp = removeTagFromString("a", temp)
	temp = removeTagFromString("b", temp)
	temp = removeTagFromString("p", temp)
	temp = removeTagFromString("span", temp)
	temp = removeTagFromString("i", temp)

	temp = temp.replace("  ", " ")
	temp = temp.replace("  ", " ")

	return temp

def url_to_soup(url):
    # bgp.he.net filters based on user-agent.
    req = urllib2.Request(url, headers={ 'User-Agent': 'Mozilla/5.0' })
    html = urllib2.urlopen(req).read() 
    return bs4.BeautifulSoup(html, "html.parser")


# ================== Get all the links from the file ==================
def getAllLinks():
	file = open("urls.txt", "r")
	urls = []
	for i in file:
		temp = i
		temp = temp.replace("\n", "")
		urls.append(temp)
	file.close()
	return urls


# =================== Scrape all the data ==========================
def createFiles(links):
	num = 0
	for link in links:
		num = num + 1
		url = link
		urlHead = url.replace("article.htm", "")
		title = urlHead.replace("http://www.medicinenet.com/", "")
		title = title.replace("/", "")
		title = title.replace("_facts", "")
		title = title.replace("_", " ").title()
		
		print "\n========================================\n\n" + str(num) + ". --> " + title
		pagenum = 2
		string = ""
		while 1:
			try:

				# print url + "\n\n"
				soup = url_to_soup(url)
				pageContent = soup.find(id="pageContainer").find_all("div")[0]
				navUl = soup.find_all(class_ = "nav")
				pCredits = soup.find_all(class_ = "credits")
				
				for i in pageContent.contents:
					if "<script" in str(i):
						continue
					if "<div" in str(i):
						continue
					if "<table" in str(i):
						continue
					if i in navUl:
						continue
					if i in pCredits:
						continue
					if type(i) is bs4.element.Comment:
						continue
					string = string + str(i) + " "

				# print removeCharactersFromString(string)
				print "=========== " + str(pagenum - 1) + ". ============="
				# nextTag = soup.find(string="NEXT").parent
				
				url = urlHead + "page" + str(pagenum) + ".htm"
				pagenum = pagenum + 1

			except (KeyboardInterrupt):
	    			print "\n\n Control: C pressed: keyboard interrupted"
	    			sys.exit()
			except:
					# print "Exception caught"
					break

		jsonData = {}
		jsonData['title'] = title
		jsonData['data'] = removeCharactersFromString(string).replace("  ", " ")

		fileToSaveData = open("drug-info/" + title + ".json", "w")
		fileToSaveData.write(json.dumps(jsonData, sort_keys = True, indent = 4))
		fileToSaveData.close()


		
		# jsonData = {}
		# jsonData['title'] = title
		# jsonData['descriptions'] = removeCharactersFromString(descString)
		# jsonData['before using'] = removeCharactersFromString(buString)
		# jsonData['proper use'] = removeCharactersFromString(puString)
		# jsonData['precautions'] = removeCharactersFromString(precString)
		# jsonData['side effects'] = removeCharactersFromString(sideString)

		# fileToSaveData = open("drug-info/" + title + ".json", "w")
		# fileToSaveData.write(json.dumps(jsonData))
		# fileToSaveData.close()
		
createFiles(getAllLinks()[:])