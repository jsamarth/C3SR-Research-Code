

import urllib2
import bs4
import json


# #################### Helper functions

# # Function to remove tags from the string
# def simpleText(string):
# 	if string.find("<") != -1:
# 		length = len(string)
# 		openBrackets = []
# 		closeBrackets = []
# 		for i in range(0, length):
# 			if(string[i] == "<"):
# 				openBrackets.append(i)
# 			if(string[i] == ">"):
# 				closeBrackets.append(i)

# 		firstOcc = string[openBrackets[0]:closeBrackets[0] + 1]
# 		secondOcc = string[openBrackets[1]:closeBrackets[1] + 1]

# 		string = string.replace(firstOcc, '')
# 		string = string.replace(secondOcc, '')

# 		return string
# 	else:
# 		return string


# ################# Creating the soup #####################

def removeCharactersFromString(string):
	temp = string
	temp = temp.replace("\n", "")
	temp = temp.replace("\r", "")
	temp = temp.replace("<ul>", "")
	temp = temp.replace("</ul>", "")
	temp = temp.replace("<li>", "")
	temp = temp.replace("</li>", " ")
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

def getAllLinks():
	file = open("urls.txt", "r")
	urls = []
	for i in file:
		temp = i
		temp = temp.replace("\n", "")
		urls.append(temp)
	file.close()
	return urls

def createFiles(links):

	for link in links:

		url = link
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
		providedTag = soup.find("span", class_="provided").parent

		descTag = soup.find_all("h3", text="Descriptions")[0]

		# Title
		title = soup.find("div", class_="headers v2 lg").contents[1].find("a").string
		print title

		# Descriptions
		descString = ""
		if len(descTag) != 0:
			for sibling in descTag.next_siblings:
				if type(sibling) is bs4.element.Comment:
					break
				if sibling is adTag:
					continue
				if sibling is providedTag:
					continue
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

		# tags = []
		# allTag = soup.find_all("h3", text="Allergies ")
		# if len(allTag) != 0:
		# 	tags.append(allTag[0])
		# pedTag = soup.find_all("h3", text="Pediatric ")
		# if len(pedTag) != 0:
		# 	tags.append(pedTag[0])
		# gerTag = soup.find_all("h3", text="Geriatric ")
		# if len(gerTag) != 0:
		# 	tags.append(gerTag[0])
		# pregTag = soup.find_all("h3", text="Pregnancy ")
		# if len(pregTag) != 0:
		# 	tags.append(pregTag[0])
		# bfTag = soup.find_all("h3", text="Breastfeeding ")
		# if len(bfTag) != 0:
		# 	tags.append(bfTag[0])
		# diTag = soup.find_all("h3", text="Drug Interactions ")
		# if len(diTag) != 0:
		# 	tags.append(diTag[0])
		# oiTag = soup.find_all("h3", text="Other Interactions ")
		# if len(oiTag) != 0:
		# 	tags.append(oiTag[0])
		# ompTag = soup.find_all("h3", text="Other Medical Problems ")
		# if len(ompTag) != 0:
		# 	tags.append(ompTag[0])
		
		# i = 0

		# # Allergies
		# allString = ""
		# if len(allTag) != 0 and tags[i] is allTag[0]:
		# 	for sibling in tags[i].next_siblings:
		# 		if sibling is tags[i+1]:
		# 			break
		# 		if sibling is adTag:
		# 			continue
		# 		allString += str(sibling)
		# 	i = i + 1
		# # print removeCharactersFromString(allString)

		# if len(pregTag)!=0 and tags[i] is pregTag[0]:
		# 	i = i + 1

		# # Pediatric
		# pedString = ""
		# if len(pedTag) != 0 and tags[i] is pedTag[0]:
		# 	for sibling in tags[i].next_siblings:
		# 		if sibling is tags[i+1]:
		# 			break
		# 		if sibling is adTag:
		# 			continue
		# 		pedString += str(sibling)
		# 	i = i + 1
		# # print removeCharactersFromString(pedString)

		# if len(pregTag)!=0 and tags[i] is pregTag[0]:
		# 	i = i + 1

		# # Geriatric
		# gerString = ""
		# if len(gerTag) != 0 and tags[i] is gerTag[0]:
		# 	for sibling in tags[i].next_siblings:
		# 		if sibling is tags[i+1]:
		# 				break
		# 		if sibling is adTag:
		# 			continue
		# 		gerString += str(sibling)
		# 	i = i + 1
		# # print removeCharactersFromString(gerString)

		# if len(pregTag)!=0 and tags[i] is pregTag[0]:
		# 	i = i + 1
		
		# # Breastfeeding
		# bfString = ""
		# if len(bfTag) != 0 and tags[i] is bfTag[0]:
		# 	for sibling in tags[i].next_siblings:
		# 		if sibling is tags[i+1]:
		# 			break
		# 		if sibling is adTag:
		# 			continue
		# 		bfString += str(sibling)
		# 	i = i + 1
		# # print removeCharactersFromString(bfString)

		# if len(pregTag)!=0 and tags[i] is pregTag[0]:
		# 	i = i + 1
		
		# # Drug Interactions
		# diString = ""
		# if len(diTag) != 0 and tags[i] is diTag[0]:
		# 	for sibling in tags[i].next_siblings:
		# 		if sibling is tags[i+1]:
		# 			break
		# 		if sibling is adTag:
		# 			continue
		# 		diString += str(sibling)
		# 	i = i + 1
		# # print removeCharactersFromString(diString)

		# if len(pregTag)!=0 and tags[i] is pregTag[0]:
		# 	i = i + 1
		
		# # Other Interactions
		# oiString = ""
		# if len(oiTag) != 0 and tags[i] is oiTag[0]:
		# 	for sibling in tags[i].next_siblings:
		# 		if type(sibling) is bs4.element.Comment or sibling is tags[i+1]:
		# 			break
		# 		if sibling is adTag:
		# 			continue
		# 		oiString += str(sibling)
		# 	i = i + 1
		# # print removeCharactersFromString(oiString)



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

		# tags = []
		# properTag = soup.find_all("h2", text="Proper Use")
		# if len(properTag) != 0:
		# 	tags.append(properTag[0])
		# dosingTag = soup.find_all("h3", text="Dosing ")
		# if len(dosingTag) != 0:
		# 	tags.append(dosingTag[0])
		# mDoseTag = soup.find_all("h3", text="Missed Dose ")
		# if len(mDoseTag) != 0:
		# 	tags.append(mDoseTag[0])
		# storageTag = soup.find_all("h3", text="Storage ")
		# if len(storageTag) != 0:
		# 	tags.append(storageTag[0])
		
		
		# i = 0

		# # Proper Use
		# properString = ""
		# if len(properTag) != 0 and tags[i] is properTag[0]:
		# 	for sibling in tags[i].next_siblings:
		# 		if sibling is tags[i+1]:
		# 			break
		# 		if sibling is adTag:
		# 			continue
		# 		if sibling is providedTag:
		# 			continue
		# 		properString += str(sibling)
		# 	i = i + 1
		# # print removeCharactersFromString(properString)

		# # Dosing
		# dosingString = ""
		# if len(dosingTag) != 0 and tags[i] is dosingTag[0]:
		# 	for sibling in tags[i].next_siblings:
		# 		if sibling is tags[i+1]:
		# 			break
		# 		if sibling is adTag:
		# 			continue
		# 		if sibling is providedTag:
		# 			continue
		# 		dosingString += str(sibling)
		# 	i = i + 1
		# # print removeCharactersFromString(dosingString)

		# # Missed Dose
		# mDoseString = ""
		# if len(mDoseTag) != 0 and tags[i] is mDoseTag[0]:
		# 	for sibling in tags[i].next_siblings:
		# 		if sibling is tags[i+1]:
		# 			break
		# 		if sibling is adTag:
		# 			continue
		# 		if sibling is providedTag:
		# 			continue
		# 		mDoseString += str(sibling)
		# 	i = i + 1
		# # print removeCharactersFromString(mDoseString)

		# # Storage
		# storageString = ""
		# if len(storageTag) != 0 and tags[i] is storageTag[0]:
		# 	for sibling in tags[i].next_siblings:
		# 		if type(sibling) is bs4.element.Comment:
		# 			break
		# 		if sibling is adTag:
		# 			continue
		# 		if sibling is providedTag:
		# 			continue
		# 		storageString += str(sibling)
		# 	i = i + 1
		# # print removeCharactersFromString(storageString)




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

# # 		adTag = soup.find(id="adsmobileBottom")
# # 		providedTag = soup.find("span", class_="provided").parent

# # 		precautionsTag = soup.find_all("h2", text="Precautions")[0]


# # 		# Precautions
# # 		precautionsString = ""
# # 		if len(precautionsTag) != 0:
# # 			for sibling in precautionsTag.next_siblings:
# # 				if type(sibling) is bs4.element.Comment:
# # 					break
# # 				if sibling is adTag:
# # 					continue
# # 				if sibling is providedTag:
# # 					continue
# # 				precautionsString += str(sibling)
# # 		# print removeCharactersFromString(precautionsString)


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

# # 		adTag = soup.find(id="adsmobileBottom")
# # 		providedTag = soup.find("span", class_="provided").parent

# # 		commonTag = soup.find_all("h4", text="More common")[0]
# # 		commonTag2 = soup.find_all("h4", text="More common")[1]
# # 		rareTag = soup.find_all("h4", text="Rare")[0]


# # 		# More Common
# # 		commonString = ""
# # 		if len(commonTag) != 0:
# # 			for sibling in commonTag.next_siblings:
# # 				if sibling is rareTag:
# # 					break
# # 				if sibling is adTag:
# # 					continue
# # 				if sibling is providedTag:
# # 					continue
# # 				commonString += str(sibling)
# # 		# print removeCharactersFromString(commonString)


	

		
createFiles(getAllLinks()[0:7])
