# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'H:\NSCC\UI\field\SolvereditUi.ui'
#
# Created by: PyQt5 UI code generator 5.15.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_solver_form(object):
    def __init__(self):  
        super(Ui_solver_form, self).__init__()
        self.setupUi
    def setupUi(self, Ui_solver_edit):
        Ui_solver_edit.setObjectName("Ui_solver_edit")
        Ui_solver_edit.resize(450, 244)
        Ui_solver_edit.setWindowTitle("求解器编辑")
        self.verticalLayout = QtWidgets.QVBoxLayout(Ui_solver_edit)
        self.verticalLayout.setObjectName("verticalLayout")
        self.GridLayout = QtWidgets.QGridLayout()
        self.GridLayout.setObjectName("GridLayout")
        self.verticalLayout.addLayout(self.GridLayout)
        self.lay1 = self.create_label_combocox_lay('solver:',['请选择',
        'smoothSolver','GAMG',"diagonal","PCG","PBiCG","PBiCGStab"],1,3)
        self.lay2 = self.create_label_combocox_lay('smoother:',['请选择'],1,3)
        self.lay3 = self.create_label_lineedit_lay('tolerance:','1.0E-6',1,3)
        self.lay4 = self.create_label_lineedit_lay('retol:','0.1',1,3)
        self.lay5 = self.create_label_combocox_lay('cacheAgglomeration:',['true','false'],1,3)
        self.lay6 = self.create_label_combocox_lay('agglomerator:',['faceAreaPair'],1,3)
        self.lay7 = self.create_label_lineedit_lay('nCellsInCoarsestLevel:','0',1,3)
        self.lay8 = self.create_label_lineedit_lay('mergeLevels:','2',1,3)
        self.lay9 = self.create_label_combocox_lay('directSolveCoarset:',['False','True'],1,3)
        self.lay10 = self.create_label_combocox_lay('preconditioner:',['DIC','DILU','FDIC','GAMG','Diagonal','None'],1,3)
        self.lay11 = self.create_label_combocox_lay('Final:',['off','on'],1,3)
        self.lay12 = self.create_label_lineedit_lay('tolerance_Final:','1.0E-6',1,3)
        self.lay13 = self.create_label_lineedit_lay('retol_Final:','0',1,3)
        
        self.buttonBox = QtWidgets.QDialogButtonBox(Ui_solver_edit)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.verticalLayout.addWidget(self.buttonBox)
        self.buttonBox.accepted.connect(Ui_solver_edit.accept)
        self.buttonBox.rejected.connect(Ui_solver_edit.reject)

        self.GridLayout.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)

        self.lay_list = [self.lay1,self.lay2,self.lay10,self.lay3,self.lay4,self.lay5,self.lay6,
            self.lay7,self.lay8,self.lay9,self.lay11,self.lay12,self.lay13]
       
        self.lay1.children()[0].itemAt(1).widget().currentIndexChanged['int'].connect(self.refresh_form)
        self.lay1.children()[0].itemAt(1).widget().currentIndexChanged.connect(lambda:self.adj_form_size(Ui_solver_edit))
        self.lay11.children()[0].itemAt(1).widget().currentIndexChanged['int'].connect(self.add_final)
        self.lay11.children()[0].itemAt(1).widget().currentIndexChanged.connect(lambda:self.adj_form_size(Ui_solver_edit))
        
        for index, items in enumerate(self.lay_list):
            self.GridLayout.addWidget(items,index,0,1,1)
        self.refresh_form(0)

    def refresh_form(self,index):
        for i in range(len(self.lay_list)):
            self.GridLayout.itemAt(i).widget().hide()
        if index == 0:
            show_list = [0,1]
            self.lay2.children()[-1].clear()
            self.lay2.children()[-1].addItems(['请选择'])
        elif index == 1:
            show_list = [0,1,3,4,10]
            self.lay2.children()[-1].clear()
            self.lay2.children()[-1].addItems(['请选择','gaussSeidel','symGaussSeidel','DIC','DILU','DICGaussSeidel'])
        elif index == 2:
            show_list = [0,1,3,4,5,6,7,8,9,10] 
            self.lay2.children()[-1].clear()
            self.lay2.children()[-1].addItems(['请选择','gaussSeidel','symGaussSeidel','DIC','DILU','DICGaussSeidel'])
        elif index == 3:
            show_list = [0,10]
        else:
            show_list = [0,2,3,4,10]
            self.lay2 = self.create_label_combocox_lay('smoother:',['请选择','DIC','DILU','FDIC','GAMG','Diagonal','None'],1,3)
        for i in show_list:
            self.GridLayout.itemAt(i).widget().show()
        self.lay11.children()[0].itemAt(1).widget().setCurrentIndex(0)

    def add_final(self,index):
        if index == 0:
            self.GridLayout.itemAt(11).widget().hide()
            self.GridLayout.itemAt(12).widget().hide()
        else:
            self.GridLayout.itemAt(11).widget().show()
            self.GridLayout.itemAt(12).widget().show()

    def adj_form_size(self,form):
        row = len(self.get_visiable_row())
        form.resize(form.geometry().width(),row*41+40)
    
    def get_visiable_row(self):
        visiable_list = []
        for i in range(self.GridLayout.rowCount()):
            if not self.GridLayout.itemAt(i).widget().isHidden():
                visiable_list.append(i)
        
        return visiable_list

    def create_label_lineedit_lay(self,label,default_val = None,label_ratio = None,lineedit_ratio = None):
        self.label = QtWidgets.QLabel(label)
        self.label.setFixedHeight(40)
        self.lineedit = QtWidgets.QLineEdit()
        self.lineedit.setPlaceholderText(default_val)
        self.lineedit.setFixedHeight(40)
        self.frame = QtWidgets.QFrame()
        self.hlay = QtWidgets.QHBoxLayout(self.frame)
        self.hlay.addWidget(self.label)
        self.hlay.addWidget(self.lineedit)
        if label_ratio:
            self.hlay.setStretch(0,label_ratio)
            self.hlay.setStretch(1,lineedit_ratio)
        return self.frame

    def create_label_combocox_lay(self,label,default_val = None,label_ratio = None,combobox_ratio = None):
        self.label = QtWidgets.QLabel(label)
        self.label.setFixedHeight(40)
        self.combobox = QtWidgets.QComboBox()
        self.combobox.addItems(default_val)
        self.combobox.setFixedHeight(40)
        self.frame = QtWidgets.QFrame()
        self.hlay = QtWidgets.QHBoxLayout(self.frame)
        self.hlay.addWidget(self.label)
        self.hlay.addWidget(self.combobox)
        if label_ratio:
            self.hlay.setStretch(0,label_ratio)
            self.hlay.setStretch(1,combobox_ratio)
        return self.frame

if __name__ == '__main__':  
    import sys  
    app = QApplication(sys.argv)  
    MainDialog = QDialog() 
    myWindow = Ui_solver_form()  
    myWindow.setupUi(MainDialog) 
    MainDialog.show()
    sys.exit(app.exec_()) 
