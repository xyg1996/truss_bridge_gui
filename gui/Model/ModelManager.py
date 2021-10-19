# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'H:\NSCC\UI\Material\MaterialEdit.ui'
#
# Created by: PyQt5 UI code generator 5.15.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.

import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from ..commonfunction import *

# working_dir_name = '/usr/sw-cluster/simforge/PFsalome/SALOME-9.4.0-CO7-SRC/BINARIES-CO7/ASTERSTUDY/lib/python3.6/site-packages/asterstudy/workingdirectory'
# pimplefoam_root = '/usr/sw-cluster/simforge/PFsalome/SALOME-9.4.0-CO7-SRC/BINARIES-CO7/ASTERSTUDY/lib/python3.6/site-packages/asterstudy'

class Ui_Mod_Edi(QObject):
    Model_selecting = pyqtSignal(str,str,str)
    def __init__(self):
        super(Ui_Mod_Edi, self).__init__()
        self.setupUi
    def setupUi(self, Dialog,working_dir_name = None,pimplefoam_root = None):
        Dialog.setObjectName("Dialog")
        Dialog.resize(454, 160)
        self.pimplefoam_root = pimplefoam_root
        self.working_dir_name = working_dir_name
        self.main_layout = QtWidgets.QVBoxLayout(Dialog)
        self.formLayoutWidget = QtWidgets.QWidget(Dialog)
        self.main_layout.addWidget(self.formLayoutWidget)
        self.formLayoutWidget.setGeometry(QtCore.QRect(69, 39, 351, 250))
        self.formLayoutWidget.setObjectName("formLayoutWidget")
        self.formLayout = QtWidgets.QFormLayout(self.formLayoutWidget)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.formLayout.setHorizontalSpacing(10)
        self.formLayout.setVerticalSpacing(20)
        self.formLayout.setObjectName("formLayout")
        self.Label = QtWidgets.QLabel(self.formLayoutWidget)
        self.Label.setMinimumSize(QtCore.QSize(0, 40))
        self.Label.setObjectName("Label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.Label)
        self.comboBox = QtWidgets.QComboBox(self.formLayoutWidget)
        self.comboBox.setMinimumSize(QtCore.QSize(0, 40))
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem('laminar')
        self.comboBox.addItem('RAS')
        self.comboBox.addItem('LES')
        # self.comboBox.setFixedWidth(200)
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.comboBox)
        self.radioButton_2 = QtWidgets.QRadioButton(self.formLayoutWidget)
        self.radioButton_2.setMinimumSize(QtCore.QSize(0, 40))
        self.radioButton_2.setObjectName("Label_2")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.radioButton_2)
        self.lineEdit_2 = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.lineEdit_2.setMinimumSize(QtCore.QSize(0, 40))
        self.lineEdit_2.setObjectName("comboBox")
        self.lineEdit_2.setText('0 -9.8 0')
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.lineEdit_2)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")

        self.main_layout.addWidget(self.buttonBox)
        self.retranslateUi(Dialog)        
        self.comboBox.currentIndexChanged['int'].connect(self.rm_item)
        self.comboBox.currentIndexChanged['int'].connect(lambda:self.add_item(Dialog))
        self.buttonBox.accepted.connect(self.collect_model_res)
        self.buttonBox.accepted.connect(self.emit_model_para)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        self.radioButton_2.setChecked(False)
        self.lineEdit_2.setEnabled(False)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        self.radioButton_2.clicked['bool'].connect(self.lineEdit_2.setEnabled)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "模型选择"))
        self.Label.setText(_translate("Dialog", "  仿真类型：  "))
        self.radioButton_2.setText(_translate("Dialog", "重力模型：  "))

    def rm_item(self):
        while self.formLayout.count() != 4:
            self.formLayout.removeRow(1)

    def add_item(self, Dialog):
        if self.comboBox.currentIndex() == 1:
            # Dialog.resize(494, 334)
            # self.buttonBox.setGeometry(190,Dialog.geometry().height()-80,200,100)            
            self.addcombobox = QtWidgets.QComboBox()
            self.addcombobox.setMinimumSize(QtCore.QSize(0, 40))
            self.addcombobox.addItems(['kEpsilon','kOmegaSST','SpalartAllmaras','LaunderSharmaKE']) 
            self.formLayout.insertRow(1,'  湍流模型：',self.addcombobox)

            self.addcombobox_2 = QtWidgets.QComboBox()
            self.addcombobox_2.setMinimumSize(QtCore.QSize(0, 40))
            self.addcombobox_2.addItems(['off','on']) 
            self.formLayout.insertRow(2,'  壁函数：',self.addcombobox_2)

        if self.comboBox.currentIndex() == 2:
            # Dialog.resize(494, 334)
            # self.buttonBox.setGeometry(190,Dialog.geometry().height()-80,200,100)            
            self.addcombobox = QtWidgets.QComboBox()
            self.addcombobox.setMinimumSize(QtCore.QSize(0, 40))
            self.addcombobox.addItems(['kEqn','SpalartAllmarasDDES','Smagorinsky']) 
            self.formLayout.insertRow(1,'  湍流模型：',self.addcombobox)

            self.addcombobox_2 = QtWidgets.QComboBox()
            self.addcombobox_2.setMinimumSize(QtCore.QSize(0, 40))
            self.addcombobox_2.addItems(['off','on']) 
            self.formLayout.insertRow(2,'  壁函数：',self.addcombobox_2)


    # collect material data 
    def collect_model_res(self):
        key_list = ['model']
        value_list = [self.comboBox.currentText()]
        if self.comboBox.currentText() == 'laminar':
            # initfile(self.working_dir_name + '/constant/turbulenceProperties', self.pimplefoam_root + '/alternativefile/constant/transportProperties')
            initfile(self.working_dir_name + '/constant/turbulenceProperties', self.pimplefoam_root + '/alternativefile/constant/laminar/turbulenceProperties')
            # changefile(self.working_dir_name + '/constant/transportProperties', "simulationType",'laminar')

        elif self.comboBox.currentText() == 'RAS':
            initfile(self.working_dir_name + '/constant/turbulenceProperties', self.pimplefoam_root + '/alternativefile/constant/RAS/turbulenceProperties')
            changefile(self.working_dir_name + '/constant/turbulenceProperties','    ' + "RASModel",
                self.formLayout.itemAt(1,1).widget().currentText())
            key_list.append('turbulence_model')
            value_list.append(self.formLayout.itemAt(1,1).widget().currentText())

            key_list.append('wallfuction')
            value_list.append(self.addcombobox_2.currentText())

        elif self.comboBox.currentText() == 'LES':
            initfile(self.working_dir_name + '/constant/turbulenceProperties',self.pimplefoam_root + '/alternativefile/constant/LES/turbulenceProperties')
            changefile(self.working_dir_name + '/constant/turbulenceProperties', '    ' + "LESModel",
                self.formLayout.itemAt(1,1).widget().currentText())
            key_list.append('turbulence_model')
            value_list.append(self.formLayout.itemAt(1,1).widget().currentText())
        
            key_list.append('wallfuction')
            value_list.append(self.addcombobox_2.currentText())

        if self.radioButton_2.isChecked() == True:
            initfile(self.working_dir_name + '/constant/g',self.pimplefoam_root + '/defaultfile/constant/g')
            changefile(self.working_dir_name + '/constant/g', "value",'           '+'(' +
                self.formLayout.itemAt(self.formLayout.count()/2-1,1).widget().text()+')')

            key_list.append('is_g')
            value_list.append(str(self.radioButton_2.isChecked()))
            key_list.append('g')
            value_list.append(self.formLayout.itemAt(self.formLayout.count()/2-1,1).widget().text())
        else:
            if os.path.exists(self.working_dir_name + '/constant/g'):
                os.remove(self.working_dir_name + '/constant/g')
        
        #save to json
        save_to_json(self.working_dir_name,'model',key_list,value_list)

    def emit_model_para(self):

        model = self.comboBox.currentText()
        wall_function = ''
        if model == 'laminar':
            turbulence_model = 'laminar' 
  
        else:
            turbulence_model = self.formLayout.itemAt(1,1).widget().currentText()
            wall_function = self.addcombobox_2.currentText()
        self.Model_selecting.emit(model,turbulence_model,wall_function)

    def reload(self,dictionary,form):
        value_list = list(dictionary['model'].values())
        self.comboBox.setCurrentText(value_list[0])
        if value_list[0] == 'laminar':
            pass
        elif value_list[0] == 'RAS':
            self.addcombobox.setCurrentText(value_list[1])
            self.addcombobox_2.setCurrentText(value_list[2])
        elif value_list[0] == 'LES':
            self.addcombobox.setCurrentText(value_list[1])
            self.addcombobox_2.setCurrentText(value_list[2])
            
        if "True" in value_list:
            self.radioButton_2.setChecked(True)
            self.lineEdit_2.setEnabled(True)
            self.lineEdit_2.setText(value_list[-1])

        
if __name__ == '__main__':  
    import sys  
    app = QApplication(sys.argv) 
    MainDialog = QDialog() 
    myWindow = Ui_Mod_Edi()  
    myWindow.setupUi(MainDialog) 
    MainDialog.show()
    sys.exit(app.exec_()) 

