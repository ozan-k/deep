#!/usr/bin/env python3
# coding: utf-8

import numpy as np
import time
import os
import sys
import maude

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

def get_formulae_in(folder_path,filename):
	file1 = open(folder_path + "/" + filename, 'r')
	Lines = file1.readlines()
	Lines = [ l.replace("\n","") for l in Lines ]
	return Lines

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

maude_file = "./BV_generator.maude"

maude.init(advise=False)
maude.load('./'+maude_file)
s_build = maude.getModule('S')
target = s_build.parseTerm('R')


seeds = ["{ [ a , - a ], [ a , - a ] }",
		"{ [ a , - a ], { [ a , - a ], [ a , - a ] } }",
		"{ [ a , - a ], { [ a , - a ], { [ a , - a ], [ a , - a ] } } }",
		"{ [ a , - a ], { [ a , - a ], { [ a , - a ], { [ a , - a ], [ a , - a ] } } } }",
		"{ [ a , - a ], { [ a , - a ], { [ a , - a ], { [ a , - a ], { [ a , - a ], [ a , - a ] } } } } }",
		"{ [ a , - a ], { [ a , - a ], { [ a , - a ], { [ a , - a ], { [ a , - a ], { [ a , - a ], [ a , - a ] } } } } } }",
        "{ [ a , - a ], { [ a , - a ], { [ a , - a ], { [ a , - a ], { [ a , - a ], { [ a , - a ], { [ a , - a ], [ a , - a ] } } } } } } }"]

def transitive(formula):
    start = s_build.parseTerm(formula)
    result = []  
    for f, subs, path, nsols in start.search(maude.ANY_STEPS,target):
        result.append(str(f))
    return result
    

def generate_and_write(atom_count=2,file_name="formulae_0"):
    to_write = transitive(seeds[atom_count-2])
    write_to_file("\n".join(to_write),file_name+ str(atom_count)) 

def simple_generate():
    for i in range(2,8):
        print(i)
        generate_and_write(i)


def generate_and_write_from_file_seed(seed_folder,seed_file,file_name="formulae_0"):
    n = 1
    result = []
    all_seeds = get_formulae_in(seed_folder,seed_file)
    for item in all_seeds:
        result = result + transitive(item)
        if len(result) > 500000:
            write_to_file("\n".join(result),seed_file + "_" +file_name + str(n))
            result = []
            n +=1 
    write_to_file("\n".join(result),seed_file + "_" +file_name + str(n))

simple_generate()

# generate_and_write_from_file_seed("./BV_seeds","seeds_BV_02.txt")
# generate_and_write_from_file_seed("./BV_seeds","seeds_BV_03.txt")
# generate_and_write_from_file_seed("./BV_seeds","seeds_BV_04.txt")    
# generate_and_write_from_file_seed("./BV_seeds","seeds_BV_05.txt")