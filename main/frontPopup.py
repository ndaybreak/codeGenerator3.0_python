#!/usr/bin/python

import yaml, os, common
from jinja2 import Environment, FileSystemLoader

class XDetailItem:
#     :service_name, :return_value, :default_index, :data_source,
#               :control_type, :key, :item_name, :item_value, :item_desc,
#               :desc_for_message, :html_element_id, :html_element_name,
#               :checks, :on_check_fail, :mandatory, :side
    def getControlTitleOne(self):
        if self.control_type in ['dropdown', 'text', 'text2', 'textarea']:
            if self.mandatory:
                titleLable = '<label class="col-lg-3 control-label add_form_label pa-standalone-label popup_table_lable pa-edit-mandatory-label"> ' + self.item_desc + '</label>'
            else:
                titleLable = '<label class="col-lg-3 control-label add_form_label pa-standalone-label popup_table_lable"> ' + self.item_desc + '</label>'
        elif self.control_type == 'checkbox':
            if self.mandatory:
                titleLable = '<label class="col-lg-3 control-label add_form_label pa-standalone-label popup_table_lable pa-edit-mandatory-label" for="' + self.html_element_id + '"> ' + self.item_desc + '</label>'
            else:
                titleLable = '<label class="col-lg-3 control-label add_form_label pa-standalone-label popup_table_lable" for="' + self.html_element_id + '"> ' + self.item_desc + '</label>'
        return titleLable
    
    def getControlTitleTwo(self):
        if self.control_type in ['dropdown', 'text', 'text2', 'textarea']:
            if self.mandatory:
                titleLable = '<label class="col-lg-3 control-label add_form_label pa-standalone-label twoCols-label pa-edit-mandatory-label"> ' + self.item_desc + '</label>'
            else:
                titleLable = '<label class="col-lg-3 control-label add_form_label pa-standalone-label twoCols-label"> ' + self.item_desc + '</label>'
        elif self.control_type == 'checkbox':
            if self.mandatory:
                titleLable = '<label class="col-lg-3 control-label add_form_label twoCols-label pa-edit-mandatory-label" for="' + self.html_element_id + '"> ' + self.item_desc + '</label>'
            else:
                titleLable = '<label class="col-lg-3 control-label add_form_label twoCols-label" for="' + self.html_element_id + '"> ' + self.item_desc + '</label>'
        return titleLable
    
class XDetail:
#     entity_name, :screen_name, :one_column_flag, :items
    def lowerCaseEntityName(self):
        return common.lowerCaseString(self.entity_name)

    def getDropdownSourceData(self):
        sourceStr = ''
        for item in self.items:
            if item.data_source == 'admin':
                sourceStr += ("$scope." + item.return_value + " = AdminService." + item.service_name + "();\n\t")
        return sourceStr
    
    def initFormItemAdd(self):
        itemAddStr = ''
        for item in self.items:
            if item.data_source == 'admin':
                itemAddStr += ("$scope.formItem." + item.item_name + " = $scope." + item.return_value + "[" + str(item.default_index) + "];\n\t\t")
        return itemAddStr
    
    def initFormItemUpdate(self):
        itemUpdateStr = ''
        for item in self.items:
            if item.data_source == 'admin':
                itemUpdateStr += "idx = AdminService.getIndexOf(selected" + self.entity_name + "." + item.item_value + ", $scope." + item.return_value + ", 'cd');\n\t\t"
                itemUpdateStr += "$scope.formItem." + item.item_name + " = $scope." + item.return_value + "[idx];\n\n\t\t";
        for item in self.items:
            if item.data_source == 'bool' and item.return_value == 'Y':
                itemUpdateStr += "$scope.formItem." + item.item_name + " = true;\n\t\t"
        return itemUpdateStr
    
    def getSaveItem(self):
        saveItemStr = ''
        for item in self.items:
            if item.data_source == 'admin':
                saveItemStr += "$scope.item." + item.item_value + " = $scope.formItem." + item.item_name + ".cd;\n\t\t"
        for item in self.items:
            if item.data_source == 'bool':
                saveItemStr += "$scope.item." + item.item_value + " = ($scope.formItem['" + item.item_name + "'] === true) ? 'Y' : 'N';\n\t\t"
        for item in self.items:
            if item.data_source == 'text2':
                saveItemStr += "$scope.item." + item.item_name + " = $scope.item." + item.item_name + ".toUpperCase();\n\t\t"
        return saveItemStr
    
# ------------------------------------------------------------------------------
# Code Generator

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
env = Environment(loader=FileSystemLoader(THIS_DIR), trim_blocks=True, lstrip_blocks=True)

stream = open('conf/frontPopup.yaml')
docs = yaml.load_all(stream)
for doc in docs:
    # popup - html
    if doc.one_column_flag:
        template = env.get_template('template/frontPopupOneColm.html')
    else:
        template = env.get_template('template/frontPopupTwoColm.html')
    outFile = open(THIS_DIR + '/output/html/' + doc.entity_name + 'Edit.html', "w")
    outFile.writelines(template.render(xc = doc))
    outFile.close()
    
    # popup - js
    template = env.get_template('template/frontPopup.js')
    outFile = open(THIS_DIR + '/output/js/' + doc.entity_name + 'EditController.js', "w")
    outFile.writelines(template.render(xc = doc))
    outFile.close()
stream.close()

print '----END----'






            