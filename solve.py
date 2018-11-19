import string

from error import error

modified = []

def setFacts(c, facts, value):
	index = string.ascii_uppercase.find(c)
	if (index == -1):
		error('Unexpected error')
	global modified
	if (c not in modified):
		modified.append(c)
	facts[index] = value

def getFacts(c, facts):
	index = string.ascii_uppercase.find(c)
	if (index == -1):
		error('Unexpected error')
	return facts[index]

def getIndex(x, tab):
	try:
		return tab.index(x)
	except:
		return -1

def handleNot(tab, facts):
	index = getIndex('!', tab)
	value = tab[index + 1]
	if (str(value).isupper()):
		value = getFacts(value, facts)
	if (value == 0):
		value = 1
	elif (value == 1):
		value = 0
	return tab[:index] + [value] + tab[index + 2:]

def handleAXO(tab, facts, op):
	index = getIndex(op, tab)
	a = tab[index - 1]
	b = tab[index + 1]
	if (str(a).isupper()):
		a = getFacts(a, facts)
	if (str(b).isupper()):
		b = getFacts(b, facts)
	value = 0
	if (a == -1 or b == -1):
		value = -1
	elif (op == '+' and (a == 1 and b == 1)):
		value = 1
	elif (op == '|' and (a == 1 or b == 1)):
		value = 1
	elif (op == '^' and (a != b)):
		value = 1
	return tab[:index - 1] + [value] + tab[index + 2:]

def solveParenthesis(tab, facts):
	while (getIndex('!', tab) != -1):
		tab = handleNot(tab, facts)
	while (getIndex('+', tab) != -1):
		tab = handleAXO(tab, facts, '+')
	while (getIndex('|', tab) != -1):
		tab = handleAXO(tab, facts, '|')
	while (getIndex('^', tab) != -1):
		tab = handleAXO(tab, facts, '^')
	if (len(tab) != 1):
		error('Unexpected error')
	if (str(tab[0]).isupper()):
		tab[0] = getFacts(tab[0], facts)
	return tab[0]

def solveInner(tab, facts):
	while (getIndex('(', tab) != -1):
		start = 0
		end = 0
		while (tab[end] != ')'):
			if (tab[end] == '('):
				start = end
			end += 1
		x = solveParenthesis(tab[start + 1:end], facts)
		tab = tab[:start] + [x] + tab[end + 1:]
	return tab[0]

def setValues(before, after, facts):
	if (getIndex('!', after) != -1):
		index = getIndex('!', after)
		setFacts(after[index + 1], facts, 1 if before == 0 else 0)
	elif (getIndex('+', after) != -1):
		index = getIndex('+', after)
		setFacts(after[index - 1], facts, before)
		setFacts(after[index + 1], facts, before)
	elif (getIndex('|', after) != -1):
		index = getIndex('|', after)
		if (before == 1):
			setFacts(after[index - 1], facts, -1)
			setFacts(after[index + 1], facts, -1)
		else:
			setFacts(after[index - 1], facts, before)
			setFacts(after[index + 1], facts, before)
	elif (getIndex('^', after) != -1):
		index = getIndex('^', after)
		if (before == 1):
			if (getFacts(after[index - 1], facts) == getFacts(after[index + 1], facts)):
				setFacts(after[index - 1], facts, -1)
				setFacts(after[index + 1], facts, -1)
		else:
			setFacts(after[index - 1], facts, 0)
			setFacts(after[index + 1], facts, 0)
	else:
		setFacts(after[1], facts, before)

def resolveModified(rules, facts):
	global modified
	while (len(modified) != 0):
		tmp = modified
		modified = []
		i = 0
		for rule in rules:
			e = getIndex('=', rule)
			for c in tmp:
				i = getIndex(c, rule)
				if (i != -1 and i < e):
					solve(rule, facts, i + 1)
			i += 1

def solve(rule, facts, line):
	equal = 0
	index = rule.index('=')
	if (rule[index - 1] == '<'):
		equal = 1
	after = ['('] + rule[index + 2:] + [')']
	if (5 < len(after)):
		error('Too much values on right side rule ' + str(line))
	if (equal == 1):
		index -= 1
	before = ['('] + rule[:index] + [')']
	before = solveInner(before, facts)
	after_value = 0
	if (equal == 1):
		after_value = solveInner(after, facts)
	if (equal == 0 or (equal == 1 and after_value == 1)):
		setValues(before, after, facts)
