The first step to run the scripts is generating the benchmark. Alternatively, you can download the benchmark from the following URL:

https://www.inf.unibz.it/~okahramanogullari/Formulae/

The second step is running the prover scripts.

# Formula generation

## Provable formula

Run the script <generate_maude.py> after assigning the variable "maude_file" to the desired generator Maude file.

There are two main functions. 

- The function <simple_generate> uses the seeds listed in the "seeds" one by one and writes the generated formulae to a file for each seed.

- The function <generate_and_write_from_file_seed> is used to generate formulae from seeds in a seperate file. 
This option is useful, for example, for BV as there are many more seed files due the combinatoric wealth in this logic.

## Non-provable formula

There are two options here. 
For the simple option, run the script <generate_nonprovable_maude.py> after assigning the variable "maude_file" to the desired generator Maude file. 
This option is better for MLL formulae.

The second option is better for BV formulae because of the combinatoric explosion. 
In this case, we use the provable formulae to generate the non-provable ones by replacing atoms.
The script <edit_generate_nonprovable.py> does this task.

# Running proof scripts

There are two options here.

- Use the built in Maude breadth-first search via the Python scripts. Maude is highly optimised and efficient. 
For exploring the complete search space, this is the beeter option. 
Simply run the script <simple_maude> with the desired options as presented in the example.

Example:

./simple_maude.py MSdli.maude ../../Formulae/MLL/formulae_02.tx

./simple_maude.py MLLi.maude ../../Formulae/MLL/formulae_02.txt 

- Use the script for running strategies. 

The search stack is stored and managed as a Python object without any optimisation. 

This option is useful running experiments for comparing systems and strategies.

# ./strategy_maude.py MLLi.maude ../../Formulae/MLL/formulae_02.txt

# ./strategy_maude.py MSdli.maude ../../Formulae/MLL/formulae_02.txt

# Counter example

The script <deepest.py> generates the counter-example.
