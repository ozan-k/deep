#!/usr/bin/env python3
# coding: utf-8

import maude
import os.path
import time
import sys
import numpy as np

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def write_to_file(content,filename):
    f = open(filename+'.txt', "w")
    f.write(content)
    f.close()

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def get_current_items_in(this_path):
    item_list = os.listdir(this_path)
    item_list.sort()
    if '.DS_Store' in item_list:
        item_list.remove('.DS_Store')
    return item_list

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def get_formulae_in(folder_path,filename):
	file1 = open(folder_path + "/" + filename, 'r')
	Lines = file1.readlines()
	Lines = [ l.replace("\n","") for l in Lines ]
	return Lines

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

lengths = []
sizes = []
steps = []
times = []

breadthfirst = False

maude.init(advise=False)
maude.load(os.path.join(os.path.dirname(__file__), '.', 'FBVi.maude'))
m = maude.getCurrentModule()

# ---------------

dummy = m.parseTerm('H:Structure')
axiom_pattern = m.parseTerm('[A:Atom, - A:Atom]')

deepest_rules = ["rule-1","rule-bot","ai","ai-par","switch-3c"]
rules = deepest_rules + ["switch-3d","switch-4c","switch-4d"]

score = { "rule-1"    : 1000000000,
	      "rule-bot"  : 100000000,
	      "ai"        : 11000000,
		  "ai-par"    : 10000000,
          "switch-3c" : 1000000,
	      "switch-3d" : 100000,
	      "switch-4c" : 10000,
	      "switch-4d" : 1000 }

# ---------------------------

def deepestRQ(substitution):
	return [m.parseTerm("[ " + str(substitution.find("R")) + " , " + str(substitution.find("Q")) + " ]")]
	
def deepestUV(substitution):
	return [substitution.find('U'),substitution.find('V')]

# ---------------------------
	
def deepest(rule,substitution):
	lst = []
	if rule == "switch-3d":
		lst = deepestRQ(substitution)
	elif rule == "switch-4c":
		lst = deepestUV(substitution)
	elif rule == "switch-4d" or rule == "switch-4d":
		lst =  deepestUV(substitution) + deepestRQ(substitution)
	for formula in lst:
		#check if one step rewrite exists for the formula's subformula
		for solution in formula.search(maude.ONE_STEP,dummy):	
			return False	
	return True	

# ---------------------------

def applyRule(rule,formula):
	dct = {}
	for formula, sb, ctx, rl in formula.apply(rule):
		if rule in deepest_rules or deepest(rule,sb):
			dct[formula] = score[rule] + 1000/len(str(formula))
	return dct

# ---------------------------

def applyAllRules(formula):
	dct = {}
	for rule in rules:
		dct = dct | applyRule(rule,formula)
	return [ i[0] for i in sorted(dct.items(), key=lambda x:x[1]) ]	
	
# ---------------------------

def not_a_proof(formula):
	for match, _ in formula.match(axiom_pattern):
		return False
	return True


def prove(stack,printProof):
	# The search space is stored in a stack.
	# Take the formula on top of the stack.  
	derivation = stack[0]
	formula = derivation[0]
	k = 0
	start_time = time.time()
	#for i in range(2):
	while not_a_proof(formula):
		# Apply all the rule instances to the formula and collect the results in a list. 
		# Each result is a derivation.
		results = [ derivation + [f] for f in applyAllRules(formula) ]    
		if results != []:
			# Depth-first search
			end = results.pop() 
			stack = results + stack + [end]
		if stack:
			derivation = stack.pop()
			formula = derivation[-1]
		else:
			print("No!")
			return False	
			
		# Stop after 30000 iterations.
		if k == 250000:   ## time-out number of steps
			return False
		if k % 10000 == 0:
			print(".",end="")	 	
		k+=1	
	# ~~~~~~~~~~~~~~~~~~~~~~~
	time_s = '\n\nSearch completed in\n'
	time_v = time.time() - start_time
	#print() 
	proof = derivation
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
	initial1 = m.parseTerm(formula)
	success = prove([[initial1]],printProof)
	#time_s = '\n\nSearch completed in\n'
	#time_s = time_s + '--- '+str(time.time() - start_time) + 'secs. ---\n'
	#print(time_s)
	return success

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def prove_all(folder,number,printProof):
	lst = []
	current_list = get_current_items_in(folder+"/")
	file = current_list[number]
	# reading the file content and assign each line to a list element
	formulae = get_formulae_in(folder,file)
	length = str(len(formulae)) 
	print()
	print(length,"formulas in",file)
	print()
	start_time = time.time()
	result = {}
	for k,f in enumerate(formulae):
		print()
		print(k+1,"/",length)
		print(f)
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
	print(duration)
	write_to_file(str(result),"FBVi_deepest_search_on_formulae_0" + str(number+2) )
	return file,result,duration 

# prove_main("[{[a, [a, - a]], [a, [a, - a]]}, [{a, [- a, - a]}, {a, [- a, - a]}]]",False)
# prove_all("../../Formulae/FBV",0,False) 
# prove_all("../../Formulae/FBV",1,False) 
# prove_all("../../Formulae/FBV",2,False) 
# prove_all("../../Formulae/FBV",3,False) 
prove_all("../../Formulae/FBV",4,False) 
prove_all("../../Formulae/FBV",5,False) 
# prove_all("../../Formulae/FBV",6,False) 	