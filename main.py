import sys

from error import error
from check import findLine, getRules, checkLines
from parsing import parsing
import params

def cleanContent(content):
	valid = []
	content = content.split('\n')
	for key in content:
		tmp = key.split('#')
		tmp = tmp[0].strip()
		if (len(tmp) > 0 and tmp[0] != '#'):
			valid.append(tmp)
	return valid

def displayResult(query):
	if (len(sys.argv) == 3 and sys.argv[2] == 'test'):
		output = ''
		for key in query:
			output += str(params.getFacts(key))
		print(output)
	else:
		for key in query:
			value = 'false'
			color = '\033[91m'
			result = params.getFacts(key)
			if (result == 1):
				value = 'true'
				color = '\033[92m'
			elif (result == 2):
				value = 'undetermined'
				color = '\033[95m'
			elif (result == -1):
				value = 'error'
			print(color + key + ' is ' + value)

if __name__ == "__main__":
	global rules
	global initial
	global facts
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
	content = cleanContent(content)
	checkLines(content)
	initial = findLine(content, '=')
	query = findLine(content, '?')
	rules = getRules(content)
	rules = parsing(rules)
	params.initFacts()
	params.setRules(rules)
	params.setInitial(initial)
	displayResult(query)
