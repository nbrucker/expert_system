import sys

from error import error
from check import findLine, getRules, checkLines
from parsing import parsing
from solve import solve, setFacts, getFacts, resolveModified

def initFacts():
	facts = []
	i = 0
	while (i < 26):
		facts.append(0)
		i += 1
	return facts

def cleanContent(content):
	valid = []
	content = content.split('\n')
	for key in content:
		tmp = key.split('#')
		tmp = tmp[0].strip()
		if (len(tmp) > 0 and tmp[0] != '#'):
			valid.append(tmp)
	return valid

def displayResult(query, facts):
	if (len(sys.argv) == 3 and sys.argv[2] == 'test'):
		output = ''
		for key in query:
			output += str(getFacts(key, facts))
		print(output)
	else:
		for key in query:
			value = 'false'
			color = '\033[91m'
			if (getFacts(key, facts) == 1):
				value = 'true'
				color = '\033[92m'
			elif (getFacts(key, facts) == -1):
				value = 'undetermined'
				color = '\033[95m'
			print(color + key + ' is ' + value)

if __name__ == "__main__":
	if (len(sys.argv) != 2 and len(sys.argv) != 3):
		error('python main.py [file]')
	filename = sys.argv[1]
	content = ''
	try:
		f = open(filename, 'r')
		content = f.read()
		f.close()
	except:
		error('error opening file')
	facts = initFacts()
	content = cleanContent(content)
	checkLines(content)
	initial = findLine(content, '=')
	for key in initial:
		setFacts(key, facts, 1)
	query = findLine(content, '?')
	rules = getRules(content)
	rules = parsing(rules)
	resolveModified(rules, facts)
	displayResult(query, facts)
