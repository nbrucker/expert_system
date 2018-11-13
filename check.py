from error import error

def findLine(content, c):
	x = 0
	letters = []
	for key in content:
		if (key[0] == c):
			if (x != 0):
				error('More than one line starting with ' + c)
			i = 1
			while (i < len(key)):
				if (key[i] not in letters and key[i].isupper()):
					letters.append(key[i])
				elif (key[i] in letters):
					error('More than one ' + key[i] + ' in line starting with ' + c)
				else:
					error('Unexpected ' + key[i] + ' in line starting with ' + c)
				i += 1
			x += 1
	if (x != 1):
		error('No line starting with ' + c)
	return letters

def getRules(content):
	rules = []
	for key in content:
		if (key[0].isupper() or key[0] == '!' or key[0] == '('):
			rules.append(key)
	return rules

def checkLines(content):
	i = 1
	for key in content:
		if (not key[0].isupper() and key[0] != '!' and key[0] != '?' and key[0] != '=' and key[0] != '('):
			error('Unexpected syntax line ' + str(i))
		i += 1
