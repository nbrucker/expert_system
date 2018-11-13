import string

from error import error

letters = string.ascii_uppercase

def canHave(rule, i, first, last, chars, line, where):
	if (first == False and i == 0):
		error('Error rule ' + line)
	if (last == False and i == len(rule) - 1):
		error('Error rule ' + line)
	if (i == 0 and where == -1):
		return
	if (i == len(rule) - 1 and where == 1):
		return
	if (rule[i + where] in chars):
		return
	else:
		error('Error rule ' + line)

def checkParenthesis(rule, line):
	x = 0
	for key in rule:
		if (key == '('):
			x += 1
		elif (key == ')' and x > 0):
			x -= 1
		elif (key == ')'):
			error('Error rule ' + line)
	if (x != 0):
		error('Error rule ' + line)

def removeSpaces(rule):
	valid = []
	for x in rule:
		x = x.strip()
		if (len(x) > 0):
			valid.append(x)
	return valid

def checkEqual(rule, line):
	x = 0
	for key in rule:
		if (key == '='):
			x += 1
	if (x != 1):
		error('Error rule ' + line)


def parsing(rules):
	line = 0
	while (line < len(rules)):
		rule = rules[line]
		rule = removeSpaces(rule)
		checkParenthesis(rule, str(line + 1))
		checkEqual(rule, str(line + 1))
		i = 0
		for x in rule:
			if (x.isupper()):
				canHave(rule, i, 1, 1, '(!+|^>', str(line + 1), -1)
				canHave(rule, i, 1, 1, ')+|^<=', str(line + 1), 1)
			elif (x == '('):
				canHave(rule, i, 1, 0, '(!+|^>', str(line + 1), -1)
				canHave(rule, i, 1, 0, '(!' + letters, str(line + 1), 1)
			elif (x == ')'):
				canHave(rule, i, 0, 1, ')' + letters, str(line + 1), -1)
				canHave(rule, i, 0, 1, ')+|^<=', str(line + 1), 1)
			elif (x == '!'):
				canHave(rule, i, 1, 0, '+|^(>' + letters, str(line + 1), -1)
				canHave(rule, i, 1, 0, '(' + letters, str(line + 1), 1)
			elif (x == '+' or x == '|' or x == '^'):
				canHave(rule, i, 0, 0, ')' + letters, str(line + 1), -1)
				canHave(rule, i, 0, 0, '(!' + letters, str(line + 1), 1)
			elif (x == '='):
				canHave(rule, i, 0, 0, ')<' + letters, str(line + 1), -1)
				canHave(rule, i, 0, 0, '>', str(line + 1), 1)
			elif (x == '>'):
				canHave(rule, i, 0, 0, '=', str(line + 1), -1)
				canHave(rule, i, 0, 0, '!(' + letters, str(line + 1), 1)
			elif (x == '<'):
				canHave(rule, i, 0, 0, ')' + letters, str(line + 1), -1)
				canHave(rule, i, 0, 0, '=', str(line + 1), 1)
			else:
				error('Unexpected ' + x + ' rule ' + str(line + 1))
			i += 1
		rules[line] = rule
		line += 1
