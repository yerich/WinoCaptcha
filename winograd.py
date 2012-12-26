import random
import re
from collections import Counter
from operator import itemgetter

class Winograd:
	def __init__(self, filename):
		self.schema = random_lines(filename, 1)[0]
	
	def generate(self):
		# Switch genders, 50% of the time
		if(random.randint(0,1) == 1):
			self.schema = re.sub("<malename>", "<femalename>", self.schema)
			self.schema = re.sub(r"\bhis\b", "her", self.schema)
			self.schema = re.sub(r"\bhe\b", "she", self.schema)
			self.schema = re.sub(r"\bhim\b", "her", self.schema)
		else:
			self.schema = re.sub("<femalename>", "<malename>", self.schema)
			self.schema = re.sub(r"\bher\b", "his", self.schema)
			self.schema = re.sub(r"\bshe\b", "he", self.schema)
			self.schema = re.sub(r"\bher\b", "him", self.schema)
		
		schemaparts = self.schema.split("=")
		self.question = schemaparts[0]
		self.choices = schemaparts[1].split("/")
		
		# Process the variables that are in the question
		variables = re.findall(r"(\<[^0-9][^>]+\>)", self.question)
		if(variables):
			self.variables = map(lambda s: {'type': s[1:-1], 'value' : None}, variables)
		else:
			self.variables = []
		
		variable_count = Counter(map(lambda s: s['type'], self.variables))
		for name in variable_count:
			if("|" in name):
				choices = name.split("|")
				for j in self.variables:
					if(j['type'] == name and j['value'] == None):
						j['value'] = random.choice(choices)
			else:
				values = random_lines(name+"s.txt", variable_count[name])
				for i in values:
					for j in self.variables:
						if(j['type'] == name and j['value'] == None):
							j['value'] = i
							break
		
		for v in self.variables:
			self.question = self.question.replace("<"+v['type']+">", v['value'], 1)
		
		# Substitute in the variables into the choices and the question
		self.choices = map(lambda n: re.sub("\<([0-9]+)\>", lambda m: self.variables[int(m.group(1))-1]['value'], n), self.choices)
		self.question = re.sub("\<([0-9]+)\>", lambda m: self.variables[int(m.group(1))-1]['value'], self.question)
		
		# Process the schema keyword: switch between two critical words, with the answer changing depending on the word chosen
		choice = random.randint(0, 1)
		if(choice == 0):
			self.question = re.sub("\[([^/]+)/([^\]]+)\]", "\g<1>", self.question)
			self.answer = self.choices[0]
		else:
			self.question = re.sub("\[([^/]+)/([^\]]+)\]", "\g<2>", self.question)
			self.answer = self.choices[1]
		
		self.answer = self.answer.split("|")
		self.choices = map(lambda c: c.split("|"), self.choices)
		
def random_lines(filename, n):
	with open(filename) as f:
		lines = random.sample(f.readlines(), n)
	lines = map(lambda s: s.strip(), lines)
	return lines

w = Winograd("winograd.txt")
w.generate()
print w.question
print w.answer