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

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

maude_file = "./FBV_generator.maude"

maude.init(advise=False)
maude.load('./'+maude_file)
s_build = maude.getModule('S')
target = s_build.parseTerm('R')


seeds = ["{ [ b , - a ], [ a , - a ] }",
		 "{ [ b , - a ], { [ a , - a ], [ a , - a ] } }",
		 "{ [ b , - a ], { [ a , - a ], { [ a , - a ], [ a , - a ] } } }",
		 "{ [ b , - a ], { [ a , - a ], { [ a , - a ], { [ a , - a ], [ a , - a ] } } } }",
		 "{ [ b , - a ], { [ a , - a ], { [ a , - a ], { [ a , - a ], { [ a , - a ], [ a , - a ] } } } } }",
		 "{ [ b , - a ], { [ a , - a ], { [ a , - a ], { [ a , - a ], { [ a , - a ], { [ a , - a ], [ a , - a ] } } } } } }",
         "{ [ b , - a ], { [ a , - a ], { [ a , - a ], { [ a , - a ], { [ a , - a ], { [ a , - a ], { [ a , - a ], [ a , - a ] } } } } } } }"]

def transitive(formula):
    start = s_build.parseTerm(formula)
    result = []  
    for f, subs, path, nsols in start.search(maude.ANY_STEPS,target):
        result.append(str(f))
    return "\n".join(result)
    

def generate_and_write(atom_count=2,file_name="formulae_0"):
    write_to_file(transitive(seeds[atom_count-2]),file_name+ str(atom_count)) 

def main():
    for i in range(2,8):
        print(i)
        generate_and_write(i)

main()
