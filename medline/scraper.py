import urllib2
import bs4
import json
import os.path
# import zlib
# zlib can be used for compressing or decompressing


# this gets the soup for a particular url
def url_to_soup(url):
    # bgp.he.net filters based on user-agent.
    req = urllib2.Request(url, headers={ 'User-Agent': 'Mozilla/5.0' })
    html = urllib2.urlopen(req).read()
    soup = bs4.BeautifulSoup(html, "html.parser")
    return soup

# this gets all the links from the file
def returnAllLinks():
	fileToReadData = open("drug-links.txt", "r")
	links = list(fileToReadData)
	fileToReadData.close()
	return links

# parse the given list and replace every html tag and return a single string with all the elements concatenated
def parseForHTML(htmlList):
	returnString = ""
	for element in htmlList:
		temp = str(element)
		temp = temp.replace("<h3>", "")
		temp = temp.replace("</h3>", "")
		temp = temp.replace("<ul>", "")
		temp = temp.replace("</ul>", "")
		temp = temp.replace("<li>", "")
		temp = temp.replace("</li>", "")
		temp = temp.replace("<p>", "")
		temp = temp.replace("</p>", "")
		temp = temp.replace("\n", " ")

		sindex = temp.find("<a ")
		lindex = temp.find(">", sindex)
		if(sindex != -1):
			temp = temp[:(sindex)] + temp[(lindex+1):]
		temp = temp.replace("</a>", "")

		returnString = returnString + temp

	return returnString
	
# return a list with only the links after the given links
def returnList(links, linkToBeginAfter):
	index = links.index(linkToBeginAfter)
	print index
	return links[index: ]

# Parse the data from every link and store in separate files
def parseLinks(links):

	i = 1
	for link in links:
		soup = url_to_soup(link)

		# title of the page / name of the drug
		title = soup.find_all("div", "page-title")[0].h1.contents[0]
		print "=== " + str(i) + " -> " + title + " ===\n"
		i = i + 1
		# checks if the file already exists. If it does then skip it
		if os.path.exists("drug-info/" + title + ".json"):
			print "(exists)\n"
			continue
 

		# why this medication section
		why = soup.find_all(id="why")
		if why:
			why = parseForHTML(why[0].find_all("div", "section-body")[0].contents)

		# how this medication section
		how = soup.find_all(id="how")
		if how:
			how = parseForHTML(how[0].find_all("div", "section-body")[0].contents) # this gets all the paragraphs in the list
		
		# Other uses section
		other_uses = soup.find_all(id="other-uses")
		if other_uses:
			other_uses = parseForHTML(other_uses[0].find_all("div", "section-body")[0].contents[0]) # this gets the other uses
		
		# Precautions section
		precautions = soup.find_all(id="precautions") 
		if precautions:
			precautions = parseForHTML(precautions[0].find_all("div", "section-body")[0].contents)

		# Special Dietary notes section
		special_dietary = soup.find_all(id="special-dietary")
		if special_dietary:
			special_dietary = parseForHTML(special_dietary[0].find_all("div", "section-body")[0].contents) # this gets the other uses

		# if I forget section
		if_i_forget = soup.find_all(id="if-i-forget")
		if if_i_forget:
			if_i_forget = parseForHTML(if_i_forget[0].find_all("div", "section-body")[0].contents) # this gets the other uses

		# Side Effects section
		side_effects = soup.find_all(id="side-effects")
		if side_effects:
			side_effects = parseForHTML(side_effects[0].find_all("div", "section-body")[0].contents) # this gets the other uses

		# Storage conditions section
		storage_conditions = soup.find_all(id="storage-conditions")
		if storage_conditions:
			storage_conditions = parseForHTML(storage_conditions[0].find_all("div", "section-body")[0].contents) # this gets the other uses

		# Overdose section
		overdose = soup.find_all(id="overdose")
		if overdose:
			overdose = parseForHTML(overdose[0].find_all("div", "section-body")[0].contents) # this gets the other uses

		# Other information section
		other_information = soup.find_all(id="other-information")
		if other_information:
			other_information = parseForHTML(other_information[0].find_all("div", "section-body")[0].contents) # this gets the other uses

		jsonData = {"title": title,
					"why": why,
					"how": how,
					"other_uses": other_uses,
					"precautions": precautions,
					"special_dietary": special_dietary,
					"if_i_forget": if_i_forget,
					"side_effects": side_effects,
					"storage_conditions": storage_conditions,
					"overdose": overdose,
					"other_information": other_information}
		fileToSaveData = open("drug-info/" + title + ".json", "w")
		fileToSaveData.write(json.dumps(jsonData))
		fileToSaveData.close()

# MAIN CODE
links = returnAllLinks()
print len(links)
links = list(set(links))
print len(links)
parseLinks(links)

