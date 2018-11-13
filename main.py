import sys

from error import error
from check import findLine, getRules, checkLines
from parsing import parsing

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

if __name__ == "__main__":
	if (len(sys.argv) != 2):
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
	query = findLine(content, '?')
	rules = getRules(content)
	parsing(rules)
