from error import error
import params

def getIndex(x, tab):
	try:
		return tab.index(x)
	except:
		return -1

def handleNot(tab):
	index = getIndex('!', tab)
	value = tab[index + 1]
	if (str(value).isupper()):
		value = params.getFacts(value)
	if (value == 0):
		value = 1
	elif (value == 1):
		value = 0
	return tab[:index] + [value] + tab[index + 2:]

def handleAXO(tab, op):
	index = getIndex(op, tab)
	a = tab[index - 1]
	b = tab[index + 1]
	if (str(a).isupper()):
		a = params.getFacts(a)
	if (str(b).isupper()):
		b = params.getFacts(b)
	value = 0
	if (a == 2 or b == 2):
		value = 2
	elif (op == '+' and (a == 1 and b == 1)):
		value = 1
	elif (op == '|' and (a == 1 or b == 1)):
		value = 1
	elif (op == '^' and (a != b)):
		value = 1
	return tab[:index - 1] + [value] + tab[index + 2:]

def solveParenthesis(tab):
	while (getIndex('!', tab) != -1):
		tab = handleNot(tab)
	while (getIndex('+', tab) != -1):
		tab = handleAXO(tab, '+')
	while (getIndex('|', tab) != -1):
		tab = handleAXO(tab, '|')
	while (getIndex('^', tab) != -1):
		tab = handleAXO(tab, '^')
	if (len(tab) != 1):
		error('Unexpected error')
	if (str(tab[0]).isupper()):
		tab[0] = params.getFacts(tab[0])
	return tab[0]

def solveInner(tab):
	while (getIndex('(', tab) != -1):
		start = 0
		end = 0
		while (tab[end] != ')'):
			if (tab[end] == '('):
				start = end
			end += 1
		x = solveParenthesis(tab[start + 1:end])
		tab = tab[:start] + [x] + tab[end + 1:]
	return tab[0]

def setValues(before, after):
	if (getIndex('!', after) != -1):
		index = getIndex('!', after)
		params.setFact(after[index + 1], 1 if before == 0 else 0)
	elif (getIndex('+', after) != -1):
		index = getIndex('+', after)
		params.setFact(after[index - 1], before)
		params.setFact(after[index + 1], before)
	elif (getIndex('|', after) != -1):
		index = getIndex('|', after)
		if (before == 1):
			params.setFact(after[index - 1], 2)
			params.setFact(after[index + 1], 2)
		else:
			params.setFact(after[index - 1], before)
			params.setFact(after[index + 1], before)
	elif (getIndex('^', after) != -1):
		index = getIndex('^', after)
		if (before == 1):
			if (params.getFacts(after[index - 1]) == params.getFacts(after[index + 1])):
				params.setFact(after[index - 1], 2)
				params.setFact(after[index + 1], 2)
		else:
			params.setFact(after[index - 1], 0)
			params.setFact(after[index + 1], 0)
	else:
		params.setFact(after[1], before)

def solve(rule, line):
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
	before = solveInner(before)
	after_value = 0
	if (equal == 1):
		after_value = solveInner(after)
	if (equal == 0 or (equal == 1 and after_value == 1)):
		setValues(before, after)
