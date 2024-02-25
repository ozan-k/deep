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

maude_file = "./BV_seed_generator.maude"

maude.init(advise=False)
maude.load('./'+maude_file)
s_build = maude.getModule('S')
target = s_build.parseTerm('R')
start = s_build.parseTerm("[ a , - a ]")    

def one_step(formula):
    result = []  
    for f, subs, path, nsols in formula.search(maude.ONE_STEP,target):
        result.append(f)
    return result


def generate_all(n):
    stack = [start]
    newStack = []
    for i in range(n-1):
        for formula in stack:
            newStack = newStack + one_step(formula)
        stack = newStack
        newStack = []
    return stack


def generate(n):
    lst = generate_all(n)
    write_to_file("\n".join([str(k) for k in lst]),"seeds_BV_0"+ str(n))

for i in range(2,6):
    generate(i)
    


