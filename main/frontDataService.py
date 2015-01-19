#!/usr/bin/python

import yaml, os, common
from jinja2 import Environment, FileSystemLoader

class XSeriveItem:
#               :entity_name, :read_all_service, :save_service, :update_service,:delete_service, 
#               :mass_delete_service, :read_all_url, :save_url, :update_url,:delete_url, 
#               :no_filter_url, :filter_url, :select_url, :client_variable, :client_variable_list
    def lowerCaseEntityName(self):
        return common.lowerCaseString(self.entity_name)
    
class XDataSerive:
#    entity_list
    def __init__(self):
        pass
    
# ------------------------------------------------------------------------------
# Code Generator

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
env = Environment(loader=FileSystemLoader(THIS_DIR), trim_blocks=True, lstrip_blocks=True)

stream = open('conf/frontDataService.yaml')
doc = yaml.load(stream)
template = env.get_template('template/frontDataService.js')
outFile = open(THIS_DIR + '/output/js/DataService.js', "w")
outFile.writelines(template.render(xc = doc))
outFile.close()

stream.close()

print '----END----Test'






            