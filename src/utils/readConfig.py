import json

def read_json(filename):
  with open(filename) as f:
    config_json = json.load(f)

  # add str() to convert from unicode to ascii
  name = config_json["name"]

  config_json["sdd_filename"] = str(config_json["sdd_filename"] % (name, name))
  config_json["vtree_filename"] = str(config_json["vtree_filename"] % (name, name))
  config_json["variable_description_filename"] = str(config_json["variable_description_filename"] % (name, name))

  # json_string = json.dumps(config_json, indent=2, sort_keys=True)
  # json_string += "\n"

  return config_json
