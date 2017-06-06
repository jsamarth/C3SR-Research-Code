

import urllib2
import bs4
import json
import os.path


# #################### Helper functions


def removeCharactersFromString(string):
	temp = string
	temp = temp.replace("\n", "")
	temp = temp.replace("\r", "")
	temp = temp.replace("<ul>", "")
	temp = temp.replace("</ul>", "")
	temp = temp.replace("<li>", "")
	temp = temp.replace("</li>", ".")
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

	temp = temp.replace("Description and Brand Names", "")
	temp = temp.replace("Descriptions", "")

	temp = temp.replace("Before Using", "")
	temp = temp.replace("Allergies", "")
	temp = temp.replace("Pediatric", "")
	temp = temp.replace("Geriatric", "")
	temp = temp.replace("Pregnancy", "")
	temp = temp.replace("Breastfeeding", "")
	temp = temp.replace("Drug Interactions", "")
	temp = temp.replace("Other Interactions", "")
	temp = temp.replace("Other Medical Problems", "")

	temp = temp.replace("Proper Use", "")
	temp = temp.replace("Dosing", "")
	temp = temp.replace("Missed Dose", "")
	temp = temp.replace("Storage", "")

	temp = temp.replace("Precautions", "")

	temp = temp.replace("Side Effects", "")
	temp = temp.replace("More common", "")
	temp = temp.replace("Rare", "")
	temp = temp.replace("More common", "")
	temp = temp.replace("Less common", "")

	first = temp.find("<ol")
	while first != -1:	
		last = temp.find(">", first+1)
		temp = temp[:first] + temp[last+1:]
		first = temp.find("<ol")

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
	i = 1
	for link in links:

		url = link
		print url
		soup = url_to_soup(url)

		# Check if pages are there or not
		descCheck = soup.find_all("a", text="Description and Brand Names")
		if len(descCheck) == 0:
			descCheck = 0
		else:
			descCheck = 1

		buCheck = soup.find_all("a", text="Before Using")
		if len(buCheck) == 0:
			buCheck = 0
		else:
			buCheck = 1

		puCheck = soup.find_all("a", text="Proper Use")
		if len(puCheck) == 0:
			puCheck = 0
		else:
			puCheck = 1

		precCheck = soup.find_all("a", text="Precautions")
		if len(precCheck) == 0:
			precCheck = 0
		else:
			precCheck = 1

		sideCheck = soup.find_all("a", text="Side Effects")
		if len(sideCheck) == 0:
			sideCheck = 0
		else:
			sideCheck = 1


		# =============== Descriptions Page ==================

		adTag = soup.find(id="adsmobileBottom")
		# providedTag = soup.find("span", class_="provided").parent

		descTag = soup.find_all("h3", text="Descriptions")[0]

		# Title
		title = soup.find("div", class_="headers v2 lg").contents[1].find("a").string
		title = title.replace("/", "-")
		# print title

		print "=== " + str(i) + " -> " + title + " ===\n"
		i = i + 1
		# checks if the file already exists. If it does then skip it
		if os.path.exists("drug-info/" + title + ".json"):
			print "(exists)\n"
			continue

		# Descriptions
		descString = ""
		if len(descTag) != 0:
			for sibling in descTag.next_siblings:
				if type(sibling) is bs4.element.Comment:
					break
				if sibling is adTag:
					continue
				# if sibling is providedTag:
				# 	continue
				descString += str(sibling)
		# print removeCharactersFromString(descString)



		# =============== Before Using Page ==================
		buString = ""
		if buCheck == 1:
			url = link.replace("description", "before-using")
			soup = url_to_soup(url)

			adTag = soup.find(id="adsmobileBottom")
			providedTag = soup.find("span", class_="provided").parent
			pageContent = soup.find("ul", class_="page content")
			tableTag = soup.find("table", class_="standard article")

			parentTag = soup.find(id="main-content")
			for child in parentTag.children:
				if child.next_sibling is tableTag:
					continue
				if child is tableTag:
					continue
				if child is adTag:
					continue
				if type(child) is bs4.element.Comment:
					continue
				if child is providedTag:
					continue
				if child is pageContent:
					break
				buString += str(child)
			# print removeCharactersFromString(buString)

		



		# =============== Proper Use Page ==================
		puString = ""
		if puCheck == 1:
			url = link.replace("description", "proper-use")
			soup = url_to_soup(url)

			adTag = soup.find(id="adsmobileBottom")
			providedTag = soup.find("span", class_="provided").parent
			pageContent = soup.find("ul", class_="page content")
			tableTag = soup.find("table", class_="standard article")

			parentTag = soup.find(id="main-content")
			for child in parentTag.children:
				if child.next_sibling is tableTag:
					continue
				if child is tableTag:
					continue
				if child is adTag:
					continue
				if type(child) is bs4.element.Comment:
					continue
				if child is providedTag:
					continue
				if child is pageContent:
					break
				puString += str(child)
			# print removeCharactersFromString(puString)



		# =============== Precautions Page ==================
		precString = ""
		if precCheck == 1:
			url = link.replace("description", "precautions")
			soup = url_to_soup(url)

			adTag = soup.find(id="adsmobileBottom")
			providedTag = soup.find("span", class_="provided").parent
			pageContent = soup.find("ul", class_="page content")
			tableTag = soup.find("table", class_="standard article")

			parentTag = soup.find(id="main-content")
			for child in parentTag.children:
				if child.next_sibling is tableTag:
					continue
				if child is tableTag:
					continue
				if child is adTag:
					continue
				if type(child) is bs4.element.Comment:
					continue
				if child is providedTag:
					continue
				if child is pageContent:
					break
				precString += str(child)
			# print removeCharactersFromString(precString)



		# =============== Side Effects page ==================

		sideString = ""
		if sideCheck == 1:
			url = link.replace("description", "side-effects")
			soup = url_to_soup(url)

			adTag = soup.find(id="adsmobileBottom")
			providedTag = soup.find("span", class_="provided").parent
			pageContent = soup.find("ul", class_="page content")
			tableTag = soup.find("table", class_="standard article")

			parentTag = soup.find(id="main-content")
			for child in parentTag.children:
				if child.next_sibling is tableTag:
					continue
				if child is tableTag:
					continue
				if child is adTag:
					continue
				if type(child) is bs4.element.Comment:
					continue
				if child is providedTag:
					continue
				if child is pageContent:
					break
				sideString += str(child)
			# print removeCharactersFromString(sideString)

		jsonData = {}
		jsonData['title'] = title
		jsonData['descriptions'] = removeCharactersFromString(descString)
		jsonData['before using'] = removeCharactersFromString(buString)
		jsonData['proper use'] = removeCharactersFromString(puString)
		jsonData['precautions'] = removeCharactersFromString(precString)
		jsonData['side effects'] = removeCharactersFromString(sideString)

		fileToSaveData = open("drug-info/" + title + ".json", "w")
		fileToSaveData.write(json.dumps(jsonData))
		fileToSaveData.close()
		
createFiles(list(set(getAllLinks())))
