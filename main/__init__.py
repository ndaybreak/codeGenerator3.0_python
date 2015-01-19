# from frontPopup import generatePopup
# 
# __main__.XDetail  should changed to frontPopup.XDetail
# generatePopup()



# import yaml, os, common
# from jinja2 import Environment, FileSystemLoader
# 
# THIS_DIR = os.path.dirname(os.path.abspath(__file__))
# env = Environment(loader=FileSystemLoader(THIS_DIR), trim_blocks=True)
# 
# def generatePopup():
#     template = env.get_template('template/frontPopup.js')
#     stream = open('conf/frontPopup.yaml')
#     docs = yaml.load_all(stream)
# #     print '----START----'
#     for doc in docs:
#         outFile = open(THIS_DIR + '/output/js/' + doc.entity_name + 'EditController.js', "w")
#         outFile.writelines(template.render(xc = doc))
#         outFile.close()
#     stream.close()
# #     print '----END----'
#     return
# 
# generatePopup()