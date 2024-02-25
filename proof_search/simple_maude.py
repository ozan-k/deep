#!/usr/bin/env python3
# coding: utf-8

import numpy as np
import time
import os
import sys
import maude

try:
	maude_file = sys.argv[1]
	folder_and_file_path = sys.argv[2]
except:
	print("Enter the maude file path as the first argument.")
	print("Enter the formula file path as the second argument.")

if maude_file in ["MLL.maude","MLLi.maude","MLLmix_i.maude","MLLmix_i.maude", "MLLmix.maude"]:
	di = False
else:
	di = True

lengths = []
sizes = []
steps = []
times = []

refute = True

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

def get_proof(path):
	proof = []
	for k,item in enumerate(path):
		if k % 2 == 1:
			struct = str(item).split('[')[1].split(']')[0]
			proof.append(struct)
		else:
			rule = str(item)
			proof.append(rule)
	proof.reverse()
	return proof

def proof_printer(proof):
	for i,item in enumerate(proof):
		if i % 2 == 1:
			print(" "*(9-len(item)),item, end=" ")
			print("---------------")
		else:
			print(" "*10,item)	

def get_size(proof):
	size = 0
	for k,line in enumerate(proof):
		if k % 2==0:
			size +=len(line)
	return size
		
def prove(formula_string,printProof):
	# The search space is stored in a stack.
	# Take the formula on top of the stack.  
	if di:
		formula = module.parseTerm(formula_string)
	else:
		formula = module.parseTerm("|~ " + formula_string)
	k = 0
	start_time = time.time()
	result = formula.search(maude.ANY_STEPS,axiom_pattern)
	time_v = time.time() - start_time
	for _,_,path,rewrite in result:
		proof = get_proof(path())
		size = get_size(proof)
		# ~~~~~~~~~~~~~~~~~~~
		lengths.append((len(proof) +1)/2)	
		sizes.append(size)
		times.append(time_v)
		steps.append(rewrite)
		if printProof:
			proof_printer(proof)
		return True	
	# ~~~~~~~~~~~~~~~~~~~~~~~
	lengths.append(0)	
	sizes.append(0)
	times.append(time_v)
	steps.append(0)
	return False	
			
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def get_formulae_in(folder_file_path):
	file1 = open(folder_file_path, 'r')
	Lines = file1.readlines()
	Lines = [ l.replace("\n","") for l in Lines ]
	return Lines

def prove_all(folder_file,printProof):
	lst = []
	# reading the file content and assign each line to a list element
	formulae = get_formulae_in(folder_file)
	length = str(len(formulae)) 
	print()
	print(length,"formulas in",folder_file)
	print()
	start_time = time.time()
	result = {}
	for k,f in enumerate(formulae):
		print(k+1,"/",length)
		proven = prove(f,printProof)
		if refute and proven: 
			lst.append(k)
		elif not refute and not proven:
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

def prove_main():	
	result = {}
	lengths = []
	sizes = []
	steps = []	
	this = prove_all(folder_and_file_path,False)
	this['system'] = maude_file
	this['formulae'] = folder_and_file_path
	result[folder_and_file_path] = this
	print(result)
	f_type =  "_maude_search_" + folder_and_file_path.split("/")[-1]
	f_type = f_type + ("_refute" if refute else  "")
	write_to_file(str(result),maude_file + "_search_on" +  f_type )


prove_main()
	
# ./simple_maude.py MSdli.maude ../../Formulae/MLL/formulae_02.tx

# ./simple_maude.py MLLi.maude ../../Formulae/MLL/formulae_02.txt