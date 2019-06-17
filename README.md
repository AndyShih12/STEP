# STEP (Symbolic and Tractable Explanation Package)

Generates explanations from a Sentential Decision Diagram (SDD).
The explanation techniques are described in the following paper:

```
A Symbolic Approach to Explaining Bayesian Network
In Proceedings of the 27th International Joint Conference on Artificial Intelligence (IJCAI), 2018.
Andy Shih and Arthur Choi and Adnan Darwiche.
```

### Input Format

The input SDD is specified using "config.json". It should have a JSON object with the following fields:

- "name": the name of the SDD of interest
- "sdd_filename": the filepath for the SDD
- "vtree_filename": the filepath for the vtree accompanying the SDD
- "variable_description_filename": the filepath of the variable description file for the SDD

First, each occurrence of ```%s``` in the configuration paths will be replaced with ```config["name"]```.
Then, the SDD file should be located at ```config["sdd_filename"]```,
the vtree file should be located at ```config["vtree_filename"]```,
the variable description file should be located at ```config["variable_description_filename"]```.


For example, if ```config["name"] = "admission_1"``` and ```config["sdd_filename"] = "sdd/%s/%s.sdd"``` then the SDD file should be located at ```"sdd/admission_1/admission_1.sdd"```.

### Output Format

The explanation output will be printed to stdout.

### Running BNC_SDD

Edit ```src/expl.py``` to play around with the different explanation queries available in ```src/explanation_queies.py```.

Then, run
```
./run
```

### Further Questions

Contact us at 
```
Andy Shih: andyshih@cs.ucla.edu
Arthur Choi: aychoi@cs.ucla.edu
Adnan Darwiche: darwiche@cs.ucla.edu
```

