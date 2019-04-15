#!/usr/bin/env python

import sdd
import explanation_queries as explqs

datasets = [
  ("sdds/digit0vs1.sdd","sdds/digit0vs1.vtree",256)
]

models_list = [
  [
    [
      0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
      0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0,
      0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
      0, 0, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0,
      0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0,
      0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0,
      0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0,
      1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1,
      1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1,
      1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1,
      1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0,
      1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0,
      0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0,
      0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0,
      0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
      0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0
    ]
  ],
]

def PI(sdd_filename, vtree_filename, num_features, model_list):
  vtree = sdd.sdd_vtree_new(num_features,"right")
  mgr = sdd.sdd_manager_new(vtree)
  vtree = sdd.sdd_manager_vtree(mgr)
  alpha = sdd.sdd_read(sdd_filename,mgr)

  sdd.sdd_vtree_save(vtree_filename, vtree)

  print "-----Begin PI query-----"
  explqs.run_prime_implicant_query(alpha,mgr,num_features,model_list)
  print "-----End PI query-----\n"

def main():
  MODEL_INDEX = 0
  (sdd_filename, vtree_filename, num_features) = datasets[MODEL_INDEX]
  model_list = models_list[MODEL_INDEX]
  PI(sdd_filename, vtree_filename, num_features, model_list)

if __name__== "__main__":
  main()
