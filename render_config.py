#!/usr/bin/python3

from jinja2 import Template
from jinja2 import Environment, FileSystemLoader, select_autoescape
import os 
import glob

dir_path = os.path.dirname(os.path.realpath(__file__))
config_path = dir_path
templates_path = dir_path
rendered_path = dir_path
templates_filter = templates_path + "/*.j2"

config_file = config_path + '/' + 'config'

"""
Parse config files with syntax key=value
"""
def parse_config():
  v = {}
  parse_config_file(v,config_file)
  return v

def parse_config_file(v,config_file):
  try:
    with open(config_file) as myfile:
        for line in myfile:
            name, var = line.partition("=")[::2]
            v[name.strip()] = var.strip()
  except:
    pass

cfg = parse_config()

env = Environment(
    loader = FileSystemLoader(templates_path)
)

templates = glob.glob(templates_filter)
for template in templates:
    basename = os.path.basename(template)
    destination_file_name = rendered_path + "/" + re.sub("\.j2$", "", basename)
    t = env.get_template(basename)
    destination_file = open(destination_file_name,"w") 
    destination_file.write(t.render(cfg))
    destination_file.close()
