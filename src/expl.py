#!/usr/bin/env python

import argparse
from utils import readConfig
import sdd
import explanation_queries as explqs

def PI(alpha, mgr, num_features, model_list):
  print "-----Begin PI query-----"
  explqs.run_prime_implicant_query(alpha,mgr,num_features,model_list)
  print "-----End PI query-----\n"

def get_model_list(alpha, vtree, num_models_limit):
  models_generator = sdd.models.models(alpha, vtree)
  model_list = []
  for model_dict in models_generator:
    model_plain = [model_dict[i+1] for i in xrange(len(model_dict))]
    model_list.append(model_plain)
    if len(model_list) == num_models_limit:
      break
  return model_list

def run():
  vtree = sdd.sdd_vtree_read(vtree_filename)
  mgr = sdd.sdd_manager_new(vtree)
  vtree = sdd.sdd_manager_vtree(mgr)
  alpha = sdd.sdd_read(sdd_filename, mgr)

  with open(variable_description_filename) as f:
    variable_description = f.readlines()
  num_features = int(variable_description[0].strip().split(" ")[1])

  # can specify custom instances by doing
  # model_list = [[0,0,0,0],[0,0,0,1],[0,0,1,0],...]
  # enumerate a few positive instances from alpha
  model_list = get_model_list(alpha, vtree, 10)
  

  PI(alpha, mgr, num_features, model_list)


parser = argparse.ArgumentParser('Generates explanations from an SDD.')

parser.add_argument('config_file', type=str, help='The config file.')
args = parser.parse_args()

if __name__== "__main__":
  config_file = args.config_file
  config_json = readConfig.read_json(config_file)

  sdd_filename = config_json["sdd_filename"]
  vtree_filename = config_json["vtree_filename"]
  variable_description_filename = config_json["variable_description_filename"]

  run()
