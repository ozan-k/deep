#!/usr/bin/env python3
# coding: utf-8


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def write_to_file(content,filename):
    f = open(filename+'.txt', "w")
    f.write(content)
    f.close()

def str_of(s):
	if len(s)>1:
		return s
	else:
		return "0" + s 

def dump_to_file(result,size,file_counter):
	name = "formulae_0" + str(size)+"_" + str_of(str(file_counter))
	write_to_file("\n".join(result),"formulae_0" + str(size)+"_" + str_of(str(file_counter)))
	print(name, flush=True)

def get_current_items_in(this_path):
    item_list = os.listdir(this_path)
    item_list.sort()
    if '.DS_Store' in item_list:
        item_list.remove('.DS_Store')
    return item_list

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def get_formulae_in(folder_path,filename):
	file1 = open(folder_path + "/" + filename, 'r')
	Lines = file1.readlines()
	Lines = [ l.replace("\n","") for l in Lines ]
	return Lines

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

f =  ["[{- a, - a}, [{[a, a], [a, {a, a}]}, {[a, a], [{- a, - a}, {- a, [- a, - a]}]}]]",
		"[{- a, - a}, [{[a, a], [a, a]}, {[{- a, - a}, {- a, - a}], [a, [a, {a, - a}]]}]]",
		"[{[a, a], [a, a]}, [{- a, [- a, - a]}, {[{- a, - a}, {- a, - a}], [a, {a, a}]}]]",
		"[a, [{[a, {- a, - a}], [a, {- a, - a}]}, {- a, [{- a, [a, a]}, {- a, [a, a]}]}]]",
		"[a, [{- a, [{- a, - a}, {[a, a], [a, a]}]}, {[a, a], [{- a, - a}, {- a, - a}]}]]",
		"[{- a, - a}, [{- a, [{- a, - a}, {- a, - a}]}, {[a, a], [a, {[a, a], [a, a]}]}]]",
		"[{[a, a], [a, a]}, [{- a, [a, a]}, {[{- a, - a}, {- a, - a}], [a, {- a, - a}]}]]"]

allf = 0
equal =0
wrong = 0
x = "fff"

def change_one(formula,size):
    result = []
    for i in range(1,size+1):
        f = formula.replace("- a", "b", i)
        f = f.replace("b","- a",i-1)
        result.append(f)
    return result
         	 
def change_all(formulae):
	result = []
	file_counter = 1
	formula_counter = 1  
	size = formulae[0].count("- a")
	iterator_max = int(1000000 /size) + 1
	print(iterator_max)
	for f in formulae:
		result = result + change_one(f,size)
		if formula_counter % 10000 == 0:
			print(".",end="",flush=True)
		if formula_counter % 100000 == 0:
			print()
			print(formula_counter)	
		if formula_counter == iterator_max:
			dump_to_file(result,size,file_counter)
			result = []
			file_counter +=1
			formula_counter = 0
		formula_counter += 1
	if formula_counter > 1:        
		dump_to_file(result,size,file_counter)
              
	

formulae = get_formulae_in("../../Formulae/FBV","formulae_07.txt")
change_all(formulae)
