# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'H:\NSCC\UI\field\FieldsettingUi.ui'
#
# Created by: PyQt5 UI code generator 5.15.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.

from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui, QtWidgets
from .CollapsibleBox import CollapsibleBox
from ..commonfunction import *

# working_dir_name = '/usr/sw-cluster/simforge/PFsalome/SALOME-9.4.0-CO7-SRC/BINARIES-CO7/ASTERSTUDY/lib/python3.6/site-packages/asterstudy/workingdirectory'
Sim_mod = "laminar"
Tur_mod = "laminar" 
wall_func = 'on'

para_dirt = {
    "laminar":
    {
        "laminar":["U:","p:"]
    },
    "RAS":
    {
        'kEpsilon':["U:","p:","k:","epsilon:","nut:"],
        'kOmegaSST':["U:","p:","k:","omega:","nut:"],
        'SpalartAllmaras':["U:","p:","nuTilda:","nut:"],
        'LaunderSharmaKE':["U:","p:","k:","epsilon:","nut:"],
    },
    "LES":
    {
        'kEqn':["U:","p:","k:","epsilon:","nut:"],
        'SpalartAllmarasDDES':["U:","p:","k:","nut:"],
        'Smagorinsky':["U:","p:","k:","nut:"],
    }
}


class Ui_Schemesetting(QDialog):
    def __init__(self):
        super(Ui_Schemesetting, self).__init__()
        self.setupUi(self)
    def setupUi(self, Fieldsetting,working_dir_name=None,model="laminar",turbulence_model="laminar",wall_function='off'):
        Fieldsetting.setObjectName("Fieldsetting")
        Fieldsetting.resize(552, 401)
        Sim_mod = model
        Tur_mod = turbulence_model
        wall_func = wall_function
        self.working_dir_name = working_dir_name
        self.verticalLayout = QtWidgets.QVBoxLayout(Fieldsetting)
        self.verticalLayout.setObjectName("verticalLayout")
        self.scroll = QtWidgets.QScrollArea(Fieldsetting)
        self.verticalLayout.addWidget(self.scroll)
        self.buttonBox = QtWidgets.QDialogButtonBox(Fieldsetting)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)
        self.buttonBox.accepted.connect(Fieldsetting.accept)
        self.buttonBox.rejected.connect(Fieldsetting.reject)
        self.buttonBox.accepted.connect(self.col_scheme_setting)
        self.content = QtWidgets.QWidget()
        self.content.resize(self.width(),self.height())

        self.scroll.setWidget(self.content)
        self.scroll.setWidgetResizable(True)
        self.vlay = QtWidgets.QVBoxLayout(self.content)
        self.hlay = QtWidgets.QHBoxLayout()
        self.vlay.addLayout(self.hlay)
        self.label_1 = QtWidgets.QLabel('时间离散')
        self.label_2 = QtWidgets.QLabel('空间离散')
        self.hlay.addWidget(self.label_1)
        self.vlay.addWidget(self.label_2)
        self.comboBox = QtWidgets.QComboBox()
        self.comboBox.addItem('steadyState')
        self.comboBox.addItem('Euler')
        self.hlay.addWidget(self.comboBox)
        self.hlay.setSpacing(100)

        list_1 = [' Grad Scheme',' Div Scheme']
        para_list = para_dirt[Sim_mod][Tur_mod]
        if wall_func == 'on':
            if Sim_mod != 'laminar':
                para_list.append('yPsi')
        self.Grad_list = ['default']
        self.Div_list = ['default']
        for items in para_list:
            self.Grad_list.append('grad(' + items.rstrip(':') + ')')
            self.Div_list.append('div(phi,' + items.rstrip(':') + ')')
        self.Div_list.append('div((nuEff*dev2(T(grad(U)))))')
        for i in range(len(list_1)):
            box = CollapsibleBox(str(list_1[i]))
            self.vlay.addWidget(box)
            self.lay = QtWidgets.QVBoxLayout()
            if i == 0:
                target_list = self.Grad_list
            if i == 1:
                target_list = self.Div_list
            for j in range(len(target_list)):
                self.comboBox_6 = QtWidgets.QComboBox()
                self.comboBox_6.addItem('none')
                self.comboBox_6.addItem('Gauss linear')
                self.comboBox_6.addItem('leastSquares')
                self.comboBox_6.addItem('cellLimited Gauss linear 1')
                self.comboBox_6.addItem('Gauss linearUpwind grad(U)')
                self.comboBox_6.addItem('bounded Gauss linearUpwind grad(U)')
                self.comboBox_6.addItem('bounded Gauss upwind')
                self.hlay_6 = QtWidgets.QHBoxLayout() 
                self.lay.setContentsMargins(50,-1,-1,-1)
                self.lay.addLayout(self.hlay_6)
                label = QtWidgets.QLabel("{}".format(target_list[j]))
                self.hlay_6.addWidget(label)
                self.hlay_6.addWidget(self.comboBox_6)
            box.setContentLayout(self.lay)

        self.hlay_2 = QtWidgets.QHBoxLayout()
        self.hlay_3 = QtWidgets.QHBoxLayout()
        self.hlay_4 = QtWidgets.QHBoxLayout()
        self.hlay_5 = QtWidgets.QHBoxLayout() 
        self.hlay_2.setContentsMargins(20,-1,-1,-1)
        self.hlay_3.setContentsMargins(20,-1,-1,-1)
        self.hlay_4.setContentsMargins(20,-1,-1,-1)
        self.hlay_5.setContentsMargins(20,-1,-1,-1)  
        self.vlay.addLayout(self.hlay_2)
        self.vlay.addLayout(self.hlay_3)
        self.vlay.addLayout(self.hlay_4)


        if wall_func == 'on':
            if Sim_mod != 'laminar':
                self.vlay.addLayout(self.hlay_5)
        self.label_2 = QtWidgets.QLabel(' Interpolation Scheme:')
        self.hlay_2.addWidget(self.label_2)
        self.comboBox_2 = QtWidgets.QComboBox()
        self.comboBox_2.addItems(['linear','vanLeer','cubic'])
        self.hlay_2.addWidget(self.label_2)
        self.hlay_2.addWidget(self.comboBox_2)


        
        self.label_3 = QtWidgets.QLabel(' Laplacian Scheme：')
        self.hlay_3.addWidget(self.label_3)
        self.comboBox_3 = QtWidgets.QComboBox()
        self.comboBox_3.addItems(['Gauss linear corrected','Gauss linear uncorrected','Gauss linear limited corrected'])
        self.hlay_3.addWidget(self.label_3)
        self.hlay_3.addWidget(self.comboBox_3)


        self.label_4 = QtWidgets.QLabel(' Surface-normal gradient Scheme：')
        self.hlay_4.addWidget(self.label_4)
        self.comboBox_4 = QtWidgets.QComboBox()
        self.comboBox_4.addItems(['corrected','uncorrected','orthogonal'])
        self.hlay_4.addWidget(self.label_4)
        self.hlay_4.addWidget(self.comboBox_4)


        self.label_5 = QtWidgets.QLabel(' Wall distance calculation method：')
        self.hlay_5.addWidget(self.label_5)
        self.comboBox_5 = QtWidgets.QComboBox()
        self.comboBox_5.addItems(['Poisson','meshWave'])
        self.hlay_5.addWidget(self.label_5)
        self.hlay_5.addWidget(self.comboBox_5)

        self.vlay.addStretch()

    def col_scheme_setting(self):
        key_list = []
        value_list = []
        target_file = self.working_dir_name + '/system/fvSchemes'
        label_list = ['ddtSchemes','','','','interpolationSchemes','laplacianSchemes','snGradSchemes']

        delifexist3(target_file, 'wallDist')
        if wall_func == 'on':
            if Sim_mod != 'laminar':
                label_list.append('wallDist')
                addfile4(target_file , 'wallDist')
        target_value_list = []
        result_list = []
        for i in range(self.vlay.count()-1):

            item_list = self.vlay.itemAt(i)
            widget_or_layout = item_list.__class__.__name__
            if widget_or_layout == 'QHBoxLayout':
 
                for j in range(item_list.count()):
                    item_in_layout = item_list.itemAt(j)
                    label_or_combo = item_in_layout.widget().__class__.__name__
                    if label_or_combo == 'QComboBox':
                        value = item_in_layout.widget().currentText()
                        target_value_list.append(value)
                        changefile3(target_file, label_list[i] ,'    default         ' + value + ';')               

            else:
                is_Collapbox = item_list.widget().__class__.__name__
                if is_Collapbox == 'CollapsibleBox':
                    for items in item_list.widget().children():
                        if items.__class__.__name__=='QVBoxLayout':
                            for k in range(items.count()):
                                if items.itemAt(k).widget().__class__.__name__=='QScrollArea':
                                    for items2 in items.itemAt(k).widget().children():
                                        if items2.__class__.__name__ == 'QComboBox':
                                            result_list.append(items2.currentText())
        
        delifexist2(target_file,'gradSchemes')
        delifexist2(target_file,'divSchemes')
        self.Grad_list_reverse = self.Grad_list[::-1]
        self.Div_list_reverse = self.Div_list[::-1]
        self.Grad_result_list =result_list[0:len(self.Grad_list)]
        self.Grad_result_list_reverse =self.Grad_result_list[::-1]
        self.Div_result_list =result_list[len(self.Grad_list):]
        self.Div_result_list_reverse =self.Div_result_list[::-1]
        for x in range(len(self.Grad_list)):
            addfile2(target_file, 'gradSchemes', '    ' + self.Grad_list_reverse[x] + '         ', self.Grad_result_list_reverse[x])
        for x in range(len(self.Div_list)):
            addfile2(target_file, 'divSchemes', '    ' + self.Div_list_reverse[x] + '         ', self.Div_result_list_reverse[x])

        # save_to_json  
        value_list = target_value_list
        value_list[1:1] = result_list
        key_list = list(range(len(value_list)))
        key_list = [i + 100 for i in key_list]
        key_list[0] = len(self.Grad_list)
        key_list[1] = len(self.Div_list)
        if wall_func == 'on':
            if Sim_mod != 'laminar':
                key_list[2] = 'True'

        save_to_json(self.working_dir_name,'scheme',key_list,value_list)


    def reload(self,dictionary):        
        key_list = list(dictionary['scheme'].keys())
        value_list = list(dictionary['scheme'].values())

        self.comboBox.setCurrentText(value_list[0])

        value_index = 1
        for i in range(self.vlay.count()):
            if self.vlay.itemAt(i).widget().__class__.__name__ == 'CollapsibleBox':
                for items in self.vlay.itemAt(i).widget().children():
                    if items.__class__.__name__=='QVBoxLayout':
                        for k in range(items.count()):
                            if items.itemAt(k).widget().__class__.__name__=='QScrollArea':
                                for items2 in items.itemAt(k).widget().children():
                                    if items2.__class__.__name__ == 'QComboBox':
                                        items2.setCurrentText(value_list[value_index])
                                        value_index+=1

        if key_list[2] == 'True':
            self.comboBox_2.setCurrentText(value_list[-4])
            self.comboBox_3.setCurrentText(value_list[-3])
            self.comboBox_4.setCurrentText(value_list[-2])
            self.comboBox_5.setCurrentText(value_list[-1])
        else:

            self.comboBox_2.setCurrentText(value_list[-3])
            self.comboBox_3.setCurrentText(value_list[-2])
            self.comboBox_4.setCurrentText(value_list[-1])

if __name__ == '__main__':  
    import sys  
    app = QApplication(sys.argv)  
    myWindow = Ui_Schemesetting()  
    myWindow.show()  
    sys.exit(app.exec_()) 