#!/usr/bin/python

import yaml, os
from jinja2 import Environment, FileSystemLoader

class Person:
    
    def getSex(self):
        return self.sex
    
# class end

THIS_DIR = os.path.dirname(os.path.abspath(__file__))

env = Environment(loader=FileSystemLoader(THIS_DIR), trim_blocks=True)
template = env.get_template('template/hello.html')

stream = open('conf/hello.yaml')
docs = yaml.load_all(stream)
for doc in docs:
    outFile = open(THIS_DIR + '/output/js/' + doc.name + '.js', "w")
    outFile.writelines(template.render(person=doc))
    print doc.addr
    outFile.close()
stream.close()
print '----END----'