#!/usr/bin/env python  
#coding=utf-8  
from PyQt5.QtWidgets import *
###
from ..BC.lookforboundarycondition import *
from ..BC.boundaryUI import *
from PyQt5.QtCore import QObject , pyqtSignal
from ..BC.boundaryUI import *
from ..commonfunction import *

# working_dir_name = '/usr/sw-cluster/simforge/PFsalome/SALOME-9.4.0-CO7-SRC/BINARIES-CO7/ASTERSTUDY/lib/python3.6/site-packages/asterstudy/workingdirectory'
# Sim_mod = "laminar"
# Tur_mod = "laminar"

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
class Ui_boundary_form(QDialog):  
    signal1 = pyqtSignal(int)

    def __init__(self,model="laminar",turbulence_model="laminar"):
        super(Ui_boundary_form, self).__init__()
        self.MainDialog = QDialog() 
        self.Sim_mod = model
        self.Tur_mod = turbulence_model
        self.myDialog = boundary_edit_form()
        self.myDialog.setupUi(self.MainDialog,model = self.Sim_mod,
                              turbulence_model = self.Tur_mod)
        self.setupUi(self)

    def setupUi(self,Form,working_dir_name=None,pimplefoam_root = None,boundary_file_root=None):
        Form.setObjectName("Form")
        Form.resize(500,260)
        self.working_dir_name = working_dir_name
        self.pimplefoam_root = pimplefoam_root
        self.boundary_file_root = boundary_file_root
        self.boundarywidget = QTableWidget(0,3,parent=Form) 
        self.boundarywidget.horizontalHeader().setSectionResizeMode(
                QHeaderView.Stretch)
        self.boundarywidget.resize(500,230)
        self.boundarywidget.setHorizontalHeaderLabels(['名称','参数','参数编辑'])
        self.resize(500,260) 
        if boundary_file_root:
            self.lname = lookforboundaryname(self.boundary_file_root)
            self.boundarywidget.setRowCount(len(self.lname))
            for i in range(len(self.lname)):
                self.boundarywidget.setRowHeight(i, 80)
                boundaryname = QTableWidgetItem(str(self.lname[i]))  
                self.boundarywidget.setItem(i, 0, boundaryname)

                item = QPushButton('Edit')
                item.setObjectName(str(i))
                self.boundarywidget.setCellWidget(i, 2, item) 
                self.signal1.emit(i)
                item.clicked.connect(self.popboundarymenu)   
                Form.resize(Form.width()+60,len(self.lname)*40+60)
        layout = QVBoxLayout(Form)  
        layout.addWidget(self.boundarywidget)    
        self.buttonBox = QtWidgets.QDialogButtonBox(Form)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        layout.addWidget(self.buttonBox) 
        self.buttonBox.accepted.connect(Form.accept)
        self.buttonBox.rejected.connect(Form.reject)
        self.buttonBox.accepted.connect(self.save_info)
 
        #编辑信号
        
    def popboundarymenu(self):
        self.menuindex = int(self.MainDialog.sender().objectName())
        boundaryname = self.boundarywidget.item(self.menuindex,0).text()
        self.MainDialog.show()
        self.MainDialog.setWindowTitle(boundaryname)
        self.myDialog.buttonBox.accepted.connect(self.col_boundary_res)

    def col_boundary_res(self):
        boundaryname = self.boundarywidget.item(self.menuindex,0).text()
        para_list = para_dirt[self.Sim_mod][self.Tur_mod]
        needed_files_list = []
        self.label_list = []
        self.res_list = []
        self.presented_result = ''
        for i,items in enumerate(para_list):
            items = items.replace(':','')
            items = '/'+items
            needed_files_list.append(items)
        #inittree(self.working_dir_name + '/0',self.pimplefoam_root + '/alternativefile/0')
        DeleteFiles(self.working_dir_name+'/0',needed_files_list)
        for i,items in enumerate(para_list):
            items = items.replace(':','')
            boundarytype = self.myDialog.boundarytype.currentText()
            delifexist(self.working_dir_name+'/0/'+items,'    ' + boundaryname)
            addlabel(self.working_dir_name+'/0/'+items, 'boundaryField', boundaryname)
            if self.myDialog.Ui_Form_list[i].formLayout.itemAt(1,1).widget().currentText()=='自定义':
                valuea = self.myDialog.Ui_Form_list[i].formLayout.itemAt(2,1).widget().toPlainText()
                valueb = '        ' + valuea.replace('\n','\n        ')
                addfile2(self.working_dir_name+'/0'+'/'+items,'    ' +boundaryname,valueb,'')
                self.presented_result += 'boundarytype' + '(' +items + '):' +boundarytype+'\n'
                self.presented_result += '自定义('+ items +'):'+ '\n' + valuea + '\n'
            else:
                for j in range(int(self.myDialog.Ui_Form_list[i].formLayout.count()/2-1),0,-1):
                    if j < 2:
                        labela = 'type'
                        
                        valuea = self.myDialog.Ui_Form_list[i].formLayout.itemAt(j,1).widget().currentText()
                    else:
                        labela = self.myDialog.Ui_Form_list[i].formLayout.itemAt(j,0).widget().text().replace(':','') 
                        valuea = 'uniform ' + self.myDialog.Ui_Form_list[i].formLayout.itemAt(j,1).widget().text()+ ''    
                    self.label_list.append(labela+'(' + items +')')
                    self.res_list.append(valuea)
                    addfile2(self.working_dir_name+'/0'+'/'+items,'    ' +boundaryname,'        ' + labela, '            ' + valuea)
                    changefile2(self.working_dir_name + '/constant/polyMesh/boundary','    ' +boundaryname, 'type', boundarytype+';')
        self.label_list.append('boundarytype('+ items +')')
        self.res_list.append(boundarytype)
        
        self.label_list = self.label_list[::-1]
        self.res_list = self.res_list[::-1]
        for index, item in enumerate(self.label_list):
            self.presented_result +=  self.label_list[index] 
            self.presented_result += ': '
            self.presented_result +=  self.res_list[index]
            self.presented_result +=  ';' +'\n'
        self.presented_result.rstrip('\n')

        self.textBrowser = QtWidgets.QTextBrowser()
        self.textBrowser.setText(self.presented_result)
        self.boundarywidget.setCellWidget(self.menuindex, 1, self.textBrowser) 

    #save to json
    def save_info(self):
        key_list = []
        value_list = []
        for i in range(self.boundarywidget.rowCount()):
            

            if self.boundarywidget.cellWidget(i,1).__class__.__name__== 'QTextBrowser':
                key_list.append(i)
                value_list.append(self.boundarywidget.cellWidget(i,1).toPlainText())
            else:
                pass
        save_to_json(self.working_dir_name,'boundaryconditions',key_list,value_list)

    def reload(self,dictionary):
        key_list = list(dictionary['boundaryconditions'].keys())
        value_list = list(dictionary['boundaryconditions'].values())
        for i in range(len(key_list)):
            self.textBrowser = QtWidgets.QTextBrowser()
            self.textBrowser.setText(value_list[i])
            self.boundarywidget.setCellWidget(int(key_list[i]), 1, self.textBrowser) 


if __name__ == '__main__':  
    import sys  
    app = QApplication(sys.argv)  
    myWindow = Ui_boundary_form()  
    myWindow.show()  
    sys.exit(app.exec_()) 
