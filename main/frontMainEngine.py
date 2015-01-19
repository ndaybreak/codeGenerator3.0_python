#!/usr/bin/python

import yaml, os, common
from jinja2 import Environment, FileSystemLoader

class XGrid:
    
    two_columns = False
    show_scroll = False
    def lowerCaseEntityName(self):
        return common.lowerCaseString(self.entity_name)
    def lowerCaseVisible(self,visible):
        return common.lowerCaseString(str(visible))
    def getHtmlContainer(self):
        container_scrollable ='<section class="container left minWidth1800" style="width:100%;">'
        container_normal     ='<section class="container left" style="width:100%;">'
        return container_scrollable if self.show_scroll else container_normal
    
    def getHtmlTableHeaders(self):
        threshold_headers = '''<tr class="TableHeaderRow"> 
                                     <th ng-if="$index < 8" class="left filterMultiColumn ui-state-default"  ng-click="orderTableBy(header.value,header.cd)" ng-repeat="header in headers" ng-show="header.visible"> 
                                           <div class="DataTables_sort_wrapper"> 
                                                      <input ng-if="$index == 0" type="checkbox" id="item-all" ng-click="checkAllSelection(data)" title="Check All">
                                                      {{header.title}}<span ng-if="$index != 0" ng-class="{'icon-sort-up':header.value == orderHeader && orderDirection == false, 'icon-sort-down':header.value == orderHeader && orderDirection == true}" class="DataTables_sort_icon css_right icon-sort"></span>
                                            </div> 
                                      </th> 
                                      <th ng-if="$index > 7 && $index < 11" dg-tip tip-content="{{T1_title}}" tip-target="topMiddle" tip-tooltip="bottomMiddle" class="left filterMultiColumn ui-state-default"  ng-click="orderTableBy(header.value,header.cd)" ng-repeat="header in headers" ng-show="header.visible">
                                              <div class="DataTables_sort_wrapper"> 
                                                      {{header.title}}<span ng-class="{'icon-sort-up':header.value == orderHeader && orderDirection == false, 'icon-sort-down':header.value == orderHeader && orderDirection == true}" class="DataTables_sort_icon css_right icon-sort"></span>
                                              </div> 
                                      </th> 
                                      <th ng-if="$index > 10" class="left filterMultiColumn ui-state-default"  ng-click="orderTableBy(header.value,header.cd)" ng-repeat="header in headers" ng-show="header.visible">
                                          <div class="DataTables_sort_wrapper"> 
                                                  {{header.title}}<span ng-class="{'icon-sort-up':header.value == orderHeader && orderDirection == false, 'icon-sort-down':header.value == orderHeader && orderDirection == true}" class="DataTables_sort_icon css_right icon-sort"></span>
                                          </div> 
                                      </th> 
                                </tr>'''
        common_headers = '''<tr class="TableHeaderRow">
                                <th class="left filterMultiColumn ui-state-default" ng-click="orderTableBy(header.value,header.cd)" ng-repeat="header in headers" ng-show="header.visible" filter-data="names($column)">
                                    <div class="DataTables_sort_wrapper">
                                        <input ng-if="$index == 0" type="checkbox" id="item-all" ng-click="checkAllSelection(data)" title="Check All">{{header.title}} <span ng-if="$index != 0" ng-class="{'icon-sort-up':header.value == orderHeader && orderDirection == false, 'icon-sort-down':header.value == orderHeader && orderDirection == true}" class="DataTables_sort_icon css_right icon-sort"></span>
                                    </div>
                                </th>
                            </tr>'''
        if self.entity_name == 'OptThreshold':
            return threshold_headers
        else:
            return common_headers
        
    def getHtmlButtons(self):
        add_edit = '<a class="btn btn-Primary {{btn}}" ng-click="btn || addOrEdit()"><i class="icon-edit"></i>Add/Edit</a>'
        save = '<a class="btn btn-Primary {{btn}}" ng-click="save()"><i class="icon-pencil icon-white"></i>Save</a>'
        add = '<a class="btn btn-Primary btn-add {{btn}}" ng-click="add()"><i class="icon-plus"></i>Add New Record</a>'
        del_inactive = '<a class="btn btn-Primary btn-delete {{btn}}" ng-click="del();"><i class="icon-trash"></i>Inactive</a>'
        delete = '<a class="btn btn-Primary btn-delete {{btn}}" ng-click="del();"><i class="icon-trash"></i>Delete</a>'
        update = '<a class="btn btn-Primary {{btn}}" ng-click="update()"><i class="icon-pencil icon-white"></i>Edit</a>'
        
        if self.entity_name == 'OptPriceQualityBand':
            retval = add_edit
        elif self.entity_name == 'OptDefaultRevenueBucket':
            retval = save
        else:
            retval = add + "\n\t\t\t"
            if self.entity_name == 'OptUser':
                retval += del_inactive
            else:
                retval += delete
            retval += ( "\n\t\t\t" + update)
        return retval
    
    def jsCoulmnStyle(self):
        two_col_style = """"windowClass: 'twoCols',
                                size: 'lg'"""
        one_col_style = "windowClass : 'oneCol',"
        return two_col_style if self.two_columns else one_col_style
    
    def jsUseTwoCols(self):
        two_col_style = """windowClass: 'twoCols',
                                size: 'lg',"""
        if self.two_columns:
            return two_col_style
        else:
            return ''
    
#     def jsElseifAuthRole(self):
#         sales_comp_admin = '}else if(authList.role === "Sales Comp Admin"){'
#         admin = '}else if(authList.role === "Admin"){'
#         if self.entity_name in ['OptPriceQualityBand', 'OptSqMccExcp', 'OptSqPricebookExcp']:
#             return sales_comp_admin
#         else:
#             return admin
        
#     def isUseRightTargets(self):
#         if self.right_targets != '0':
#             return ',{ "sClass": "right filterMultiColumn", aTargets: [ <%= xc.right_targets %> ] }'
#         else:
#             return ''
    
    def getAttrList(self):
        attrList = []
        for colm in self.colms_info:
            attrList.append(colm[2])
        del attrList[0]
        return attrList
    
    def getValueList(self):
        valueList = []
        for colm in self.colms_info:
            valueList.append(colm[1])
        del valueList[0]
        return valueList
    
    def getDollerFields(self):
        return self.doller_fields if self.doller_fields else []
    def getPercentFields(self):
        return self.percent_fields if self.percent_fields else []
#     def getNumStrFields(self):
#         return self.num_str_fields if self.num_str_fields else []
    def getInputDateFields(self):
        return self.input_date_fields if self.input_date_fields else []
# ------------------------------------------------------------------------------
# Code Generator

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
env = Environment(loader=FileSystemLoader(THIS_DIR), trim_blocks=True, lstrip_blocks=True)

stream = open('conf/frontMain.yaml')
docs = yaml.load_all(stream)
for doc in docs:
    # grid - html
    template = env.get_template('template/frontMain.html')
    outFile = open(THIS_DIR + '/output/html/' + doc.entity_name + 'Management.html', "w")
    outFile.writelines(template.render(xc = doc))
    outFile.close()
    
    # grid - js
    template = env.get_template('template/frontMain.js')
    outFile = open(THIS_DIR + '/output/js/' + doc.entity_name + 'Management.js', "w")
    outFile.writelines(template.render(xc = doc))
    outFile.close()
stream.close()

print '----END----'






            