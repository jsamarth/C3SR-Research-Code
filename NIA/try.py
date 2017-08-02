def removeTagFromString(string, tagToRemove):
	first = string.find("<" + tagToRemove)
	while first != -1:	
		last = string.find(">", first+1)
		string = string[:first] + string[last+1:]
		first = string.find("<" + tagToRemove)
	return string

print removeTagFromString("""<div class="hello">hello world</div> """, "div")