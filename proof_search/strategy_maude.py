#!/usr/bin/env python3
# coding: utf-8

import numpy as np
import time
import os
import sys
import maude

try:
	maude_file = sys.argv[1]
	folder_and_file = sys.argv[2]
except:
	print("Example:") 
	print("The following command will prove all the formulae in the file '../Formulae/formulae_01.txt'.")
	print("./strategy_maude.py MS.maude ../Formulae/formulae_01.txt depthfirst shallow")
	print()
	exit()

if maude_file in ["MLL.maude","MLLi.maude","MLLmix_i.maude","MLLmix_i.maude", "MLLmix.maude"]:
	di = False
else:
	di = True


try:
	breadthfirst = sys.argv[5] == "breadth"
except:
	breadthfirst = False

try:
	shallow = sys.argv[6] == "shallow"
except:
	shallow = False 

lengths = []
sizes = []
steps = []
times = []

def decide(last,current):
	if (last == "}" and current == "[") or (last == "]" and current == "{"):
		return False
	else:
		return True	 

def pretty(s):
	new = ""
	last =""
	for current in s:
		if current != last and current != " " and decide(last,current):
			new = new + current		
		if current  == "{" or current == "[" or current  == "}" or current == "]":
			last = current
	return new.replace("{","(").replace("}",")")

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def write_to_file(content,filename):
    f = open(filename+'.txt', "w")
    f.write(content)
    f.close()

def get_current_items_in(this_path):
    item_list = os.listdir(this_path)
    item_list.sort()
    if '.DS_Store' in item_list:
        item_list.remove('.DS_Store')
    return item_list

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

maude.init(advise=False)
maude.load(os.path.join(os.path.dirname(__file__), '.', maude_file))

module = maude.getCurrentModule()
if di:
	axiom_pattern =module.parseTerm('[A:Atom, - A:Atom]')
	dummy = module.parseTerm('H:Structure')
else:
	axiom_pattern=module.parseTerm('|~ 1')
	dummy = module.parseTerm('X')

deepest_rules = ["switch-3d","switch-4c", "switch-4d"]

score = { "rule-1"    : 1000000000,
	      "rule-bot"  : 100000000,
	      "ai"        : 10000000,
		  "ai-par"    : 10000000,
          "switch-3c" : 1000000,
	      "switch-3d" : 100000,
	      "switch-4c" : 10000,
	      "switch-4d" : 1000 }

score_sc ={ "bot"  : 100000000,
		 "tens" : 50000000, 
	     "mix0" : 40000000,
		 "ai"   : 11000000,
		 "mix"  : 10000000,
		 "par1" : 1000000,
		 "par2" : 1000000,
		 "par3" : 1000000,
		 "collapse": 100000}

def difference(c,s,label):
	def get_diverge_index(s1,s2):
		for k,i in enumerate(s1):
			if i != s2[k]:
				return k
		return 0
	a = get_diverge_index(c,s)
	b = get_diverge_index(c[::-1],s[::-1])
	return len(s[a:-1*b]) +  score[label] 

def one_step(formula):
	pretty_c = pretty(str(formula))
	results = []
	for f, subs, path, nsols in formula.search(maude.ONE_STEP,dummy):
		pretty_p = pretty(str(f))
		label = str(path()[1]).split("[")[1].split("]")[0]
		if di:
			dif = difference(pretty_c,pretty_p,label)
		else:
			dif = score_sc[label]
		results.append((dif,f))		
	if shallow:
		results.sort(key=lambda x:x[0])
	else:
		results.sort(reverse=True, key=lambda x:x[0])
	return [ r[1] for r in results ]

def not_a_proof(formula):
	for match, _ in formula.match(axiom_pattern):
		return False
	return True

def prove(stack,printProof):
	# The search space is stored in a stack.
	# Take the formula on top of the stack.  
	formula = stack[0][-1]
	k = 0
	start_time = time.time()
	while not_a_proof(formula):
		# Apply all the rule instances to the formula and collect the results in a list. 
		# Each result is a derivation.
		results = [ stack[0] + [f] for f in one_step(formula) ]    
		if results == []:
			stack = stack[1:]
		else:
			if breadthfirst:
				# Breadth-first search
				stack = stack[1:] + results 
			else:	
				# Depth-first search
				stack = [results[0]] + stack[1:] + results[1:]
		if stack:
			formula = stack[0][-1]
		else:
			return False
		# Stop after 30000 iterations.
		if k == 50000:   ## time-out number of steps
			return False
		if k % 10000 == 0:
			print(".",end="")	 	
		k+=1
	# ~~~~~~~~~~~~~~~~~~~~~~~
	#time_s = '\n\nSearch completed in\n'
	time_v = time.time() - start_time
	print() 
	proof = stack[0]
	lengths.append(len(proof))
	size = 0
	for f in proof:
		size+=str(f).count("-") * 2  
	sizes.append(size)
	steps.append(k)
	times.append(time_v)
	if printProof:
		for p in proof[::-1]:
			print(p)
	return True		
			
def prove_main(formula,printProof):
	#start_time = time.time()
	if di:
		initial = module.parseTerm(formula)
	else:
		initial = module.parseTerm("|~ " + formula)
	print(initial)
	success = prove([[initial]],printProof)
	#time_s = '\n\nSearch completed in\n'
	#time_s = time_s + '--- '+str(time.time() - start_time) + 'secs. ---\n'
	#print(time_s)
	return success

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def get_formulae_in(folder_path_and_filename):
	file1 = open(folder_path_and_filename, 'r')
	Lines = file1.readlines()
	Lines = [ l.replace("\n","") for l in Lines ]
	return Lines

def prove_all(folder_and_file,printProof):
	lst = []
	formulae = get_formulae_in(folder_and_file)
	length = str(len(formulae)) 
	print()
	print(length,"formulas in",folder_and_file)
	print()
	start_time = time.time()
	result = {}
	for k,f in enumerate(formulae):
		print(k+1,"/",length)
		if not prove_main(f,printProof):
			lst.append(k)
			# break
	time_s = '\n\nSearch completed in\n'
	duration = time.time() - start_time
	time_s = time_s + '--- '+str(duration) + 'secs. ---\n'
	print(time_s)
	print(lst)
	result["mean length"] = np.mean(lengths)
	result["sd length"] = np.std(lengths)
	result["mean size"] = np.mean(sizes)
	result["sd size"] = np.std(sizes)
	result["mean steps"] = np.mean(steps)
	result["sd steps"] = np.std(steps)
	result["length"] = length
	result["failed"] = lst
	result["duration"] = duration
	result["mean time"] = np.mean(times)
	result["sd time"] = np.std(times)
	return result 
	
result = {}
lengths = []
sizes = []
steps = []	
this = prove_all(folder_and_file,False)
this['system'] = maude_file
this['formulae'] = folder_and_file
result[folder_and_file] = this
print(result)
f_type =  folder_and_file.split("/")[-1] 
if breadthfirst:
	f_type = f_type + "_breadthfirst"
if shallow:
	f_type = f_type  + "_shallow"
write_to_file(str(result),"strategy_" + maude_file + "_search_on_" +  f_type )


# ./strategy_maude.py MLLi.maude ../../Formulae/MLL/formulae_02.txt
# ./strategy_maude.py MSdli.maude ../../Formulae/MLL/formulae_02.txt
