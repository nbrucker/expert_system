import string

from error import error
import solve

rules = []
initial = []
facts = []
already = []

def setRules(tab):
	global rules
	rules = tab

def getRules():
	global rules
	return rules

def initFacts():
	global facts
	i = 0
	while (i < 26):
		facts.append(-1)
		i += 1

def setFact(c, value):
	global facts
	index = string.ascii_uppercase.find(c)
	if (index == -1):
		error('Unexpected error')
	facts[index] = value

def getFacts(c):
	global already
	global initial
	global rules
	global facts
	index = string.ascii_uppercase.find(c)
	if (index == -1):
		error('Unexpected error')
	value = facts[index]
	if (value != -1):
		return value
	found = False
	line = 1
	for rule in rules:
		equal = solve.getIndex('=', rule)
		letter = solve.getIndex(c, rule[equal:])
		if (letter != -1 and equal != -1 and rule not in already):
			already.append(rule)
			solve.solve(rule, line)
			found = True
			if (facts[index] == 1):
				break
		line += 1
	if (found == False):
		if (c in initial):
			setFact(c, 1)
		else:
			setFact(c, 0)
	return facts[index]

def setInitial(tab):
	global initial
	initial = tab

def getInitial():
	global initial
	return initial
