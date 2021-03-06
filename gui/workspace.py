import sys
import os
import shutil
import time
import pvsimple as pvs
from .commonfunction import LoadingMessage
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QDialog,QFrame
from PyQt5.QtWidgets import QApplication,QFileDialog
from PyQt5 import uic
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QDir
from PyQt5.Qt import *
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QWidget, QApplication, QMainWindow
from .commonfunction import *
from .Workspace.workspace_ui import Ui_Workspace
from .Material.MaterialManager import Ui_Mat_Man
from .Model.ModelManager import Ui_Mod_Edi
from .BC.boundaryform import Ui_boundary_form
from .Field.FieldsettingUi import Ui_Fieldsetting
from .Solver.SolverManUi import Ui_Sol_Man
from .Scheme.SchemesettingUi import Ui_Schemesetting
from .post import (ResultFile, PlotWindow,
            ColorRep, WarpRep, ModesRep, BaseRep,
            pvcontrol, show_min_max, selection_probe, selection_plot,
            get_active_selection, get_pv_mem_use, dbg_print,
            RESULTS_PV_LAYOUT_NAME, RESULTS_PV_VIEW_NAME)
from .post.navigator import OverlayBar
from .Mesh_transfer.salome_mesh_tran import Ui_Mesh_tran
from .Mesh_generation.mesh_generationUi import Ui_Mesh_generate 
from .Computing_control.Computingcontrol import Ui_Computing_control
# from ..pyqtgraph.widgets.GraphicsLayoutWidget import GraphicsLayoutWidget
from .Residual_error.ResidualplotUi import Ui_Residual_plot
# from meshview.baseview import MeshBaseView

class Workspace_tool(QWidget):
    def __init__(self, astergui, parent=None):
        super(Workspace_tool,self).__init__()

        self.astergui = astergui
        model = turbulence_model = wall_function = ''

        self.ui = Ui_Workspace()
        self.ui.setupUi(self)
        v_layout = QtWidgets.QVBoxLayout(self)
        v_layout.setContentsMargins(0, 0, 0, 0)
        v_layout.addWidget(self.ui)

        self.MaterialDialog = QDialog() 
        self.mat_man = Ui_Mat_Man()
        self.mat_man.setupUi(self.MaterialDialog)
        self.MaterialDialog.setWindowModality(Qt.ApplicationModal)
        self.mat_man.subDialog.setWindowModality(Qt.ApplicationModal)

        self.ModelDialog = QDialog()
        self.mod_man = Ui_Mod_Edi()
        self.mod_man.setupUi(self.ModelDialog)
        self.ModelDialog.setWindowModality(Qt.ApplicationModal)

        self.BCDialog = QDialog()
        self.bod_man = Ui_boundary_form()
        self.bod_man.setupUi(self.BCDialog)
        self.BCDialog.setWindowModality(Qt.ApplicationModal)
        self.bod_man.MainDialog.setWindowModality(Qt.ApplicationModal)

        self.FieldDialog = QDialog()
        self.fie_man = Ui_Fieldsetting()
        self.fie_man.setupUi(self.FieldDialog)
        self.FieldDialog.setWindowModality(Qt.ApplicationModal)

        self.SolverDialog = QDialog()
        self.sol_man = Ui_Sol_Man()
        self.sol_man.setupUi(self.SolverDialog)
        self.SolverDialog.setWindowModality(Qt.ApplicationModal)
        self.sol_man.solver_form_Ui.setWindowModality(Qt.ApplicationModal)

        self.SchemeDialog = QDialog()
        self.sch_man = Ui_Schemesetting()
        self.sch_man.setupUi(self.SchemeDialog)
        self.SchemeDialog.setWindowModality(Qt.ApplicationModal)

        self.MeshtranDialog = QDialog()
        self.mesh_tran = Ui_Mesh_tran()
        self.mesh_tran.setupUi(self.MeshtranDialog)
        self.MeshtranDialog.setWindowModality(Qt.ApplicationModal)

        self.MeshgenerateDialog = QDialog()
        self.mesh_generate = Ui_Mesh_generate()
        self.mesh_generate.setupUi(self.MeshgenerateDialog)
        self.MeshgenerateDialog.setWindowModality(Qt.ApplicationModal)

        self.ComputingControlDialog = QDialog()
        self.computing_control = Ui_Computing_control()
        self.computing_control.setupUi(self.ComputingControlDialog)
        self.ComputingControlDialog.setWindowModality(Qt.ApplicationModal)

        ###Signal creation
        # self.ui.pushButton.clicked.connect(self.pop_mesh_tran_man)

        #self.ui.pushButton_12.setEnabled(False)

        #self.ui.pushButton_5.clicked.connect(self.pop_mat_man)
        #self.ui.pushButton_6.clicked.connect(self.pop_mod_man)
        #self.ui.pushButton_7.clicked.connect(self.pop_BC_man)
        #self.ui.pushButton_8.clicked.connect(self.pop_fie_man)
        #self.ui.pushButton_9.clicked.connect(self.pop_sch_man)
        #self.ui.pushButton_10.clicked.connect(self.pop_sol_man)
        # self.ui.pushButton_3.clicked.connect(self.pop_mesh_generate_man)
        #self.ui.pushButton_14.clicked.connect(self.pop_com_control_man)
        



    def pop_com_control_man(self):
        self.ComputingControlDialog.show()

    # def pop_mesh_generate_man(self):
    #     self.MeshgenerateDialog.show()

    # def pop_mesh_tran_man(self):
    #     self.MeshtranDialog.show()
    #     self.mesh_tran.pushButton_3.clicked.connect(self.MeshtranDialog.reject)
        

    def pop_mat_man(self):
        self.MaterialDialog.show()

    def pop_mod_man(self):
        self.ModelDialog.show()
        # self.mod_man.Model_selecting.connect(self.update_dialog_by_model)

    def pop_BC_man(self):
        self.BCDialog.show()

    def pop_fie_man(self):
        self.FieldDialog.show()

    def pop_sol_man(self):
        self.SolverDialog.show()

    def pop_sch_man(self):
        self.SchemeDialog.show()



class Workspace(QWidget):
    '''
    workspace??????????????????salome??????????????????
    '''
    _loader = res_splitter = pv_widget = pv_view = pv_layout = None
    ren_view = pv_overlay = toolbuttons = current = previous = None
    pv_widget_children = play_btn = pause_btn = outline_btn = None
    minmax_btn = infobar_label = shown = filename_label = None
    set_workingdir = pyqtSignal(str)
    openfoam_error = pyqtSignal(str)
    
    def __init__(self, astergui, parent=None):
        super(Workspace,self).__init__()
        self.pv_view = None
        self.workingdirectory = None
        self.res = self.ren_view = self.default_file_root = None
        self.astergui = astergui
        self.previous = {}
        # pimplefoam_root ???default??????alternative??????????????????????????????????????????????????????openfoam???
        #self.pimplefoam_root = '/usr/sw-cluster/simforge/PFsalome/SALOME-9.4.0-CO7-SRC/BINARIES-CO7/ASTERSTUDY/lib/python3.6/site-packages/asterstudy'
        self.pimplefoam_root ='/usr/salome/SALOME-9.4.0-CO7-SRC/BINARIES-CO7/ASTERSTUDY/lib/python3.6/site-packages/asterstudy/'
        #self.curr_dir = os.popen('echo `pwd`').read()[0:-1]
        self.curr_dir = '/amd_share/online1/install/truss_bridge/code_aster_dir'
        self.curr_dir_2 = '/amd_share/online1/install/truss_bridge/SALOME-9.4.0-CO7-SRC/asterstudy/gui'
        self.work_dir = '/amd_share/online1/install/truss_bridge/script'
        #self.work_dir = '/home/export/online3/amd_share/truss_bridge_app'
        print(self.work_dir)
        # ????????????????????????????????????????????????
        self.horizontalLayout = QtWidgets.QHBoxLayout(self) #??????????????????????????????
        self.main_splitter = QtWidgets.QSplitter(QtCore.Qt.Horizontal, self) #??????????????????
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding,
                           QtWidgets.QSizePolicy.Expanding)
        self.main_splitter.setSizePolicy(QtWidgets.QSizePolicy.Expanding,
                                        QtWidgets.QSizePolicy.Expanding)
        self.horizontalLayout.addWidget(self.main_splitter)  #??????addWidget????????????????????????????????????
        # self.work_space_tool?????????????????????????????????
        self.work_space_tool = Workspace_tool(astergui)
        self.work_space_tool.setMinimumSize(QtCore.QSize(250, 0))
        self.main_splitter.addWidget(self.work_space_tool)
        # self.right_container???????????????????????????????????????paraview?????????????????????????????????,???self.pv_splitter??????????????????
        ## ??????paraview??????
        self.right_container = QtWidgets.QWidget()
        self.right_container.setSizePolicy(QtWidgets.QSizePolicy.Expanding,
                                QtWidgets.QSizePolicy.Expanding)
        self.right_container_layout = QtWidgets.QHBoxLayout(self.right_container)
        self.main_splitter.addWidget(self.right_container)
        self.pv_splitter = QtWidgets.QSplitter(QtCore.Qt.Vertical, self.right_container)
        self.pv_splitter.setSizePolicy(QtWidgets.QSizePolicy.Expanding,
                                        QtWidgets.QSizePolicy.Expanding) 
        self.right_container_layout.addWidget(self.pv_splitter)
        ## ?????????paraview??????
        self.init_paraview()
        ## ????????????????????????(????????????????????????????????????????????????????????????tab widget??????)
        self.log_widget = QtWidgets.QDockWidget(self.right_container)
        self.log_widget_Contents = QtWidgets.QWidget()
        self.log_widget_layout = QtWidgets.QHBoxLayout(self.log_widget_Contents)
        self.log_tab_widget = QtWidgets.QTabWidget(self.log_widget_Contents)
        self.log_tab = QtWidgets.QWidget()
        self.progress_tab = QtWidgets.QWidget()
        self.log_tab_Layout = QtWidgets.QHBoxLayout(self.log_tab)
        self.progress_tab_Layout = QtWidgets.QVBoxLayout(self.progress_tab)
        self.log_textBrowser = QtWidgets.QTextBrowser(self.log_widget_Contents)
        self.log_textBrowser.setReadOnly(True)
        self.log_tab_Layout.addWidget(self.log_textBrowser)
        self.log_tab_widget.addTab(self.log_tab,'????????????')
        self.log_tab_widget.addTab(self.progress_tab,'????????????')
        ### ??????????????????(??????????????????????????????????????????)
        self.residual_plot_widget = QtWidgets.QWidget()
        self.residual_plot = Ui_Residual_plot()
        self.residual_plot.setupUi(self.residual_plot_widget)
        self.progress_tab_Layout.addWidget(self.residual_plot_widget)
        self.progress_bar_Layout=QtWidgets.QHBoxLayout()
        self.progress_bar = QtWidgets.QProgressBar()
        self.progress_bar.setProperty("value", 0)
        self.progress_bar_Layout.addWidget(self.progress_bar)
        self.progress_bar_label = QtWidgets.QLabel('????????????: s')
        self.progress_bar_Layout.addWidget(self.progress_bar_label)
        self.progress_tab_Layout.addLayout(self.progress_bar_Layout)
        self.log_widget_layout.addWidget(self.log_tab_widget)
        self.log_widget.setWidget(self.log_widget_Contents)
        self.pv_splitter.addWidget(self.log_widget)
        titleBar=QWidget()
        self.log_widget.setTitleBarWidget(titleBar)
        ## ??????paraview??????????????????????????????????????????
        self.main_splitter.setStretchFactor(0,1)
        self.main_splitter.setStretchFactor(1,8)
        ## ??????*????????????*???????????????????????????????????????
        self.log_tab_widget.setTabEnabled(1,False)
        ## ??????????????????
        self.process = QtCore.QProcess(self)
        self.process1 = QtCore.QProcess(self)
        self.process2 = QtCore.QProcess(self)
        self.process.readyRead.connect(self.dataReady)
        self.process2.readyRead.connect(self.dataReady)
        # self.process.setProcessChannelMode(QtCore.QProcess.MergedChannels)

        self.change_element_pro() # ??????????????????
        # ????????????
        self.work_space_tool.ui.pushButton_ok.clicked.connect(self.cal_spacing)
        # ????????????
        self.work_space_tool.ui.pushButton_reset.clicked.connect(self.reset)
         # ???????????????????????? 
        self.work_space_tool.ui.pushButton_beam.clicked.connect(self.change_element_pro)
        self.work_space_tool.ui.apply.clicked.connect(self.change_element_pro)
        # ????????????
        self.work_space_tool.ui.pushButton_4.clicked.connect(self.submit)
        self.work_space_tool.ui.pushButton_break.clicked.connect(self.show_result)
        # ??????open foam??????
        #self.work_space_tool.ui.pushButton_2.clicked.connect(lambda:self.open_openfoam_file(self.workingdirectory))
        # ??????????????????
        #self.work_space_tool.ui.pushButton_15.clicked.connect(self.create_dir)
        # ????????????
        #self.work_space_tool.ui.pushButton_4.clicked.connect(self.show_mesh_check_res)
        # OpenFoam????????????
        #self.work_space_tool.ui.pushButton_3.clicked.connect(self.check_is_working_dir_gen_mesh)
        # Salome ???????????? 
        #self.work_space_tool.ui.pushButton.clicked.connect(self.check_is_working_dir_mesh_tran)
        # ?????????????????????
        #self.work_space_tool.ui.apply.clicked.connect(lambda:self.change_mesh_display(self.res))
        # ????????????
        #self.work_space_tool.ui.pushButton_11.clicked.connect(self.disable_some_buttons)
        #self.work_space_tool.ui.pushButton_12.clicked.connect(self.enable_some_buttons)

        #self.work_space_tool.ui.pushButton_11.clicked.connect(lambda:self.log_tab_widget.setTabEnabled(1,True)) 
        #self.work_space_tool.ui.pushButton_11.clicked.connect(self.prepare_computing)
        # ????????????????????????????????????
        self.work_space_tool.ui.tabWidget.currentChanged['int'].connect(self.main_tab_change)
        # ????????????
        #self.work_space_tool.ui.pushButton_16.clicked.connect(self.reload)
        # ??????
    #     self.work_space_tool.ui.pushButton_12.clicked.connect(self.terminate_self())
        # ??????
        #self.work_space_tool.ui.pushButton_13.clicked.connect(self.continue_to_calculate)
        
        self.openfoam_error.connect(self.show_openfoam_error)

    def create_static_comm(self,material1,material2,element,curr_dir,pres):
        #file = work_dir + '/static.comm'
        fname = 'static.comm'
        file = os.path.join(curr_dir,fname)
        print('file:',file)
        data = ''
        i = 1
        with open(file,'r+') as f:
            for line in f.readlines():
                if(line.find('steel') == 0):
                    #line = 'width = %s' % (str(self.width1)) + '\n'
                    line = 'steel = DEFI_MATERIAU(ELAS=_F(E=%s, NU=%s, RHO=%s))' % (material1[0],material1[1],material1[2])  + '\n'
                if(line.find('concrete') == 0):
                    line = 'concrete = DEFI_MATERIAU(ELAS=_F(E=%s, NU=%s, RHO=%s))' % (material2[0],material2[1],material2[2])  + '\n'
                '''print(i,len(line))
                if(line.find('CARA',4) == 0):
                    print('ok')'''
                if i == 23:
                    line = '    COQUE=_F(EPAIS=%s, GROUP_MA=(\'road\', )),' % (element[0]) + '\n'
                if i == 30:
                    line = '            VALE=(%s, )' % (element[1]) + '\n'
                if i == 35:
                    line = '            VALE=(%s, )' % (element[2]) + '\n'
                if i == 40:
                    line = '            VALE=(%s, )' % (element[3]) + '\n'
                if i == 45:
                    line = '            VALE=(%s, )' % (element[4]) + '\n'
                if i == 67:
                    line = '    PRES_REP=_F(GROUP_MA=(\'road\', ), PRES=%s)' % (pres) + '\n'
                i+=1
                data += line
        f.close
        #print(data)
        with open(file,'r+') as f:
            f.writelines(data)
        f.close

    def create_modes_comm(self,material1,material2,element,curr_dir,fre):
        fname = 'modes.comm'
        file = os.path.join(curr_dir,fname)
        print('file:',file)
        data = ''
        i = 1
        with open(file,'r+') as f:
            for line in f.readlines():
                if(line.find('steel') == 0):
                    #line = 'width = %s' % (str(self.width1)) + '\n'
                    line = 'steel = DEFI_MATERIAU(ELAS=_F(E=%s, NU=%s, RHO=%s))' % (material1[0],material1[1],material1[2])  + '\n'
                if(line.find('concrete') == 0):
                    line = 'concrete = DEFI_MATERIAU(ELAS=_F(E=%s, NU=%s, RHO=%s))' % (material2[0],material2[1],material2[2])  + '\n'

                if i == 18:
                    line = '    COQUE=_F(EPAIS=%s, GROUP_MA=(\'road\', )),' % (element[0]) + '\n'
                if i == 25:
                    line = '            VALE=(%s, )' % (element[1]) + '\n'
                if i == 30:
                    line = '            VALE=(%s, )' % (element[2]) + '\n'
                if i == 35:
                    line = '            VALE=(%s, )' % (element[3]) + '\n'
                if i == 40:
                    line = '            VALE=(%s, )' % (element[4]) + '\n'
                if i == 78:
                    line = '    CALC_FREQ=_F(NMAX_FREQ=%s),' % (fre) + '\n'

                i+=1
                data += line
        f.close
        with open(file,'r+') as f:
            f.writelines(data)
        f.close

    def change_element_pro(self):
        #from .create_static_comm import create_static_comm
        #fname = 'static.comm' #????????????
        #fdir_curr = os.path.join(self.curr_dir,fname)
        element0 = self.work_space_tool.ui.tab0_H_value.text()
        element1 = self.work_space_tool.ui.tab1_H_value.text()
        element2 = self.work_space_tool.ui.tab2_H_value.text()
        element3 = self.work_space_tool.ui.tab3_H_value.text()
        element4 = self.work_space_tool.ui.tab4_H_value.text()
        self.element = [element0,element1,element2,element3,element4]

        material11 = self.work_space_tool.ui.modulus_value_beams.text()
        material12 = self.work_space_tool.ui.poisson_value_beams.text()
        material13 = self.work_space_tool.ui.rho_value_beams.text()
        self.material1 = [material11,material12,material13]

        material21 = self.work_space_tool.ui.modulus_value_road.text()
        material22 = self.work_space_tool.ui.poisson_value_road.text()
        material23 = self.work_space_tool.ui.rho_value_road.text()
        self.material2 = [material21,material22,material23]
        for i in self.element + self.material1 + self.material2:
            self.check_parameter_isnum(i)
        try:
            self.create_static_comm(self.material1,self.material2,self.element,self.curr_dir,'1e5')
            self.create_modes_comm(self.material1,self.material2,self.element,self.curr_dir,'10')
            #material1=[2e11,0.3,7850]
            #material2=[2.5e10,0.2,2500]
            #element = [0.1,0.2,0.3,0.4,0.5]
            print('curr_dir:',self.curr_dir_2)
            #self.create_static_comm(material1,material2,element,self.curr_dir_2)
            self.process.start('echo ??????comm?????????')

        except:
            self.process.start('echo ??????comm????????????')
        
    def submit(self):
        if self.work_space_tool.ui.modes_button.isChecked():
            self.fre,ok = QtWidgets.QInputDialog.getText(self,'????????????????????????','??????????????????')
            print('set fre = ',self.fre)
            while ok and self.check_parameter_isnum(self.fre) and self.check_parameter_isint(self.fre):
                self.create_modes_comm(self.material1,self.material2,self.element,self.curr_dir,self.fre)
                self.disable_some_buttons()
                self.work_space_tool.ui.pushButton_4.setEnabled(False)
                #cmd = '/amd_share/online1/install/code_aster_14.6/14.6/bin/as_run '
                cmd = 'sh '
                cmd += self.curr_dir
                cmd += '/submit_2.sh'
                print('cmd_modes:',cmd)
                try:
                    self.process2.start('echo ????????????')
                    QApplication.processEvents()
                    self.process.start(cmd)
                    #self.process.waitForFinished()
                    QtWidgets.QMessageBox.information(self, '??????', '???????????????????????????!')
                    self.work_space_tool.ui.pushButton_4.setEnabled(False)
                    time.sleep(8)
                    self.work_space_tool.ui.pushButton_break.setEnabled(True)
                    self.enable_some_buttons()
                    ok = 0
                except:
                    self.process2.start('echo ??????????????????') 
                    ok = 0           
        else:
            self.pres,ok = QtWidgets.QInputDialog.getText(self,'????????????','???????????????/Pa???')
            #cmd = '/amd_share/online1/install/code_aster_14.6/14.6/bin/as_run '
            while ok and self.check_parameter_isnum(self.pres):
                self.disable_some_buttons()
                self.work_space_tool.ui.pushButton_4.setEnabled(False)
                self.create_static_comm(self.material1,self.material2,self.element,self.curr_dir,self.pres)    
                cmd = 'sh '
                cmd += self.curr_dir
                cmd += '/submit.sh'
                print('cmd:',cmd)
                try:
                    self.process2.start('echo ????????????')
                    QApplication.processEvents()
                    self.process.start(cmd)
                    #self.process.waitForFinished()
                    QtWidgets.QMessageBox.information(self, '??????', '???????????????????????????!')
                    self.work_space_tool.ui.pushButton_4.setEnabled(False)
                    time.sleep(8)
                    self.work_space_tool.ui.pushButton_break.setEnabled(True)
                    self.enable_some_buttons()
                    ok = 0
                except:
                    self.process2.start('echo ??????????????????')
                    ok = 0
    
    def check_parameter_isnum(self,num):
        try:
            num = float(num)
            s=str(num).split('.')
            if float(s[1])==0:
                print('??????')
                return True
            else :
                print('??????')
                return True
        except:
            print("?????????????????????!")
            QtWidgets.QMessageBox.information(self, '??????', '???????????????!')
            return False

    def check_parameter_isint(self,num):
        num = float(num)
        s=str(num).split('.')
        if float(s[1])==0:
            print('??????')
            return True
        else :
            print('??????')
            QtWidgets.QMessageBox.information(self, '??????', '???????????????!')
            return False       

    def check_iseven(self,num):
        s=str(float(num)).split('.')
        if float(s[1])==0:
            print('??????')
            if (int(num) % 2 == 0):
                return True
            else:
                QtWidgets.QMessageBox.information(self, '??????', '????????????????????????!')
                return False
        else :
            print('??????')
            QtWidgets.QMessageBox.information(self, '??????', '????????????????????????!')
            return False

    def cal_spacing(self):
        self.width1 = self.work_space_tool.ui.width_lineEdit.text()
        self.length = self.work_space_tool.ui.length_lineEdit.text()
        self.height1 = self.work_space_tool.ui.height_lineEdit.text()
        self.sections = self.work_space_tool.ui.sections_lineEdit.text()
        self.spacing = self.work_space_tool.ui.spacing_lineEdit.text() 
        parameters=[self.width1,self.length,self.height1,self.sections]
        for i in parameters:
            print('i:',i)
            self.check_parameter_isnum(i)
        #self.check_iseven(self.sections)
        #self.width1 = float(self.work_space_tool.ui.width_lineEdit.text())
        self.length = float(self.work_space_tool.ui.length_lineEdit.text())
        #self.height1 = float(self.work_space_tool.ui.height_lineEdit.text())
        self.sections = int(self.work_space_tool.ui.sections_lineEdit.text())
        #self.spacing = float(self.work_space_tool.ui.spacing_lineEdit.text())
        self.spacing = float('%.2f' % (self.length/self.sections))
        self.work_space_tool.ui.spacing_lineEdit.setText(str(self.spacing))

        fname = 'Mesh_1.med' #????????????
        script_name = 'create_geo_mesh_new.py' #???????????????
        fdir = os.path.join(self.work_dir,fname)
        fdir_curr = os.path.join(self.curr_dir,fname)
        script_dir = os.path.join(self.work_dir,script_name)
        script_dir_curr = os.path.join(self.curr_dir,script_name)
        self.change_bridge(script_dir)
        time.sleep(0.25)
        try:
            if(self.check_iseven(self.sections)):
                exec(open(script_dir,"rb").read())
                self.process.start('echo ??????????????????????????????')
        except:
            print("????????????!")
            self.process.start('echo ???????????????')
        #exec(open('/amd_share/online1/install/truss_bridge/script/create_geo_mesh.py').read())
        self.show_mesh_1(fdir_curr)

    def reset(self):
        self.work_space_tool.ui.width_lineEdit.setText('8')
        self.work_space_tool.ui.length_lineEdit.setText('40')
        self.work_space_tool.ui.height_lineEdit.setText('5')
        self.work_space_tool.ui.sections_lineEdit.setText('8')
        self.work_space_tool.ui.spacing_lineEdit.setText('5')
        self.cal_spacing()

    def show_modes_result(self):
        #choice = self.fre[0]
        choice_list = self.fre_all
        #QInputDialog.getItem(self, "select input dialog", '????????????', items, 0, False)
        self.fre_show, ok = QtWidgets.QInputDialog.getItem(self, "select", '??????', choice_list, 0, False)
        index_id = choice_list.index(self.fre_show)
        print('index_id:',index_id)
        if ok:
            try:
                if self.currentdisplay:
                    current_display = pvs.GetActiveSource()
                    pvs.Delete(current_display)
                    print('delete ok')
                    self.process.start('echo ??????????????????')
                    self.process.waitForFinished()
                    
            except Exception as e:
                print('show_modes_result error!')
            try:
                self.warpByVector1Display.SetScalarBarVisibility(self.renderView1, False)
                self.static_resrmedDisplay.SetScalarBarVisibility(self.renderView1, False)
                self.process.start('echo ????????????')
            except:
                self.process.start('echo ???????????????...')
                self.process.waitForFinished()
            finally:
                fname = 'study_modes.rmed'
                fdir = os.path.join(self.curr_dir,fname)
                self.process.start('echo ??????????????????????????????...')
                self.process.waitForFinished()
                self.modes_resrmed = pvs.MEDReader(FileName=fdir)
                animationScene1 = pvs.GetAnimationScene()
                self.modes_resrmed.GenerateVectors = 1
                self.modes_resrmed.ActivateMode = 1
                renderView1 = pvs.GetActiveViewOrCreate('RenderView')
                modes_resrmedDisplay = pvs.Show(self.modes_resrmed, renderView1)
                modes_resrmedDisplay.Representation = 'Surface'
                renderView1.ResetCamera()
                materialLibrary1 = pvs.GetMaterialLibrary()
                animationScene1.UpdateAnimationUsingDataTimeSteps()
                renderView1.Update()

                pvs.Hide(self.modes_resrmed, renderView1)
                self.warpByVector2 = pvs.WarpByVector(Input=self.modes_resrmed)
                self.warpByVector2.ScaleFactor = 3.0
                pvs.SetActiveSource(self.warpByVector2)
                self.warpByVector2Display = pvs.Show(self.warpByVector2, renderView1)
                renderView1.Update()
                self.warpByVector2Display.Representation = 'Surface'
                self.warpByVector2.Vectors = ['POINTS', 'unnamed0DEPL [%s] - %s_Vector' %(index_id,self.fre_show[0:7])]
                pvs.ColorBy(self.warpByVector2Display, ('POINTS', 'unnamed0DEPL [%s] - %s' %(index_id,self.fre_show[0:7]), 'Magnitude'))
                self.warpByVector2Display.RescaleTransferFunctionToDataRange(True, False)
                self.warpByVector2Display.SetScalarBarVisibility(renderView1, False)
                renderView1.Update()
                self.currentdisplay = self.warpByVector2
                # The following two lines insure that the view is refreshed
                self.pv_splitter.setVisible(False)
                self.pv_splitter.setVisible(True)
                self.process.start('echo ???????????????')
                self.process.waitForFinished()
                self.work_space_tool.ui.pushButton_4.setEnabled(True)
        
    def read_fre(self):
        file = self.curr_dir + '/modes.mess'
        num = int(self.fre)
        print('num:',num)
        data = ''
        i = 1
        id_modal = 0
        with open(file,'r+') as f:
            for line in f.readlines():
                if(line.find('     Calcul modal') == 0):
                    #line = 'width = %s' % (str(self.width1)) + '\n'
                    print('modal:',i)
                    id_modal = i
                if i >= (id_modal + 4) and i <= (id_modal + 4 + num -1) and id_modal:
                    data +=line
                i+=1
        f.close
        '''try:
            with open(file,'r+') as f:
                for line in f.readlines():
                    if(line.find('     Calcul modal') == 0):
                        #line = 'width = %s' % (str(self.width1)) + '\n'
                        print('modal:',i)
                        id_modal = i
                    if i >= (id_modal + 4) and i <= (id_modal + 4 + num -1) and id_modal:
                        data +=line
                    i+=1
            f.close
        except:
            print('error! Not find frequency result!')
                #data += line'''
        
        print('id_modal:',id_modal)
        print(data.split())
        fre_data = data.split()
        self.fre_all = []
        for i in range(1,len(fre_data),3):
            #print(fre_data[i])
            self.fre_all.append(fre_data[i])
        print('fre:',self.fre_all)
        self.fre_num = []
        for i in self.fre_all:
            j = i[0:7]
            self.fre_num.append(j)
        print('fre_num:',self.fre_num)

    def select_modes(self):
        #choice = self.fre[0]
        choice_list = self.fre_all
        #QInputDialog.getItem(self, "select input dialog", '????????????', items, 0, False)
        self.fre_show, ok = QtWidgets.QInputDialog.getItem(self, "select", '??????', choice_list, 0, False)

    def show_result(self):
        if self.work_space_tool.ui.modes_button.isChecked():
            try:
                self.read_fre() # ??????????????????
            except:
                QtWidgets.QMessageBox.information(self, '??????', '????????????????????????!')
            time.sleep(0.5)
            self.show_modes_result()
        else:
            self.show_static_result()

    def show_static_result(self):
        choice_list = ['??????','??????']
        self.res_show, ok = QtWidgets.QInputDialog.getItem(self, "select", '????????????', choice_list, 0, False)
        try:
            if self.currentdisplay:
                current_display = pvs.GetActiveSource()
                pvs.Delete(current_display)
                print('delete ok')
                self.process.start('echo ??????????????????')
                self.process.waitForFinished()
        except Exception as e:
                print(e)
        if self.res_show == '??????' and ok:
            fname = 'static_res.rmed'
            fdir = os.path.join(self.curr_dir,fname)
            self.process.start('echo ???????????????????????????...')
            self.process.waitForFinished()
            self.static_resrmed = pvs.MEDReader(FileName=fdir)
            self.static_resrmed.AllArrays = ['TS0/mesh/ComSup0/reslin__DEPL@@][@@P1']
            self.static_resrmed.GenerateVectors = 1
            self.renderView1 = pvs.GetActiveViewOrCreate('RenderView')
            static_resrmedDisplay = pvs.Show(self.static_resrmed, self.renderView1)
            static_resrmedDisplay.Representation = 'Surface'
            self.renderView1.ResetCamera()
            materialLibrary1 = pvs.GetMaterialLibrary()
            self.renderView1.Update()
            # set scalar coloring
            pvs.ColorBy(static_resrmedDisplay, ('POINTS', 'reslin__DEPL_Vector', 'Magnitude'))
            # rescale color and/or opacity maps used to include current data range
            static_resrmedDisplay.RescaleTransferFunctionToDataRange(True, False)
            # show color bar/color legend
            static_resrmedDisplay.SetScalarBarVisibility(self.renderView1, True)
            # get color transfer function/color map for 'reslin__DEPL_Vector'
            reslin__DEPL_VectorLUT = pvs.GetColorTransferFunction('reslin__DEPL_Vector')
            # get opacity transfer function/opacity map for 'reslin__DEPL_Vector'
            reslin__DEPL_VectorPWF = pvs.GetOpacityTransferFunction('reslin__DEPL_Vector')
            # create a new 'Warp By Vector'
            self.warpByVector1 = pvs.WarpByVector(Input=self.static_resrmed)
            # set active source
            pvs.SetActiveSource(self.warpByVector1)
            # show data in view
            self.warpByVector1Display = pvs.Show(self.warpByVector1, self.renderView1)
            # trace defaults for the display properties.
            self.warpByVector1Display.Representation = 'Surface'
            # show color bar/color legend
            self.warpByVector1Display.SetScalarBarVisibility(self.renderView1, True)
            # show data in view
            self.warpByVector1Display = pvs.Show(self.warpByVector1, self.renderView1)
            # hide data in view
            pvs.Hide(self.static_resrmed, self.renderView1)
            # show color bar/color legend
            self.warpByVector1Display.SetScalarBarVisibility(self.renderView1, True)
            # update the view to ensure updated data information
            self.renderView1.Update()
            self.currentdisplay = self.warpByVector1
            # The following two lines insure that the view is refreshed
            self.pv_splitter.setVisible(False)
            self.pv_splitter.setVisible(True)
            self.process.start('echo ???????????????')
            self.process.waitForFinished()
            self.work_space_tool.ui.pushButton_4.setEnabled(True)
        if self.res_show == '??????' and ok:
            fname = 'static_res.rmed'
            fdir = os.path.join(self.curr_dir,fname)
            self.process.start('echo ???????????????????????????...')
            self.process.waitForFinished()
            self.static_resrmed = pvs.MEDReader(FileName=fdir)
            self.renderView1 = pvs.GetActiveViewOrCreate('RenderView')
            self.static_resrmedDisplay = pvs.Show(self.static_resrmed, self.renderView1)
            self.static_resrmedDisplay.Representation = 'Surface'
            pvs.ColorBy(self.static_resrmedDisplay, ('POINTS', 'reslin__EFGE_NOEU', 'Magnitude'))
            self.static_resrmedDisplay.RescaleTransferFunctionToDataRange(True, False)
            self.static_resrmedDisplay.SetScalarBarVisibility(self.renderView1, True)
            self.renderView1.Update()
            self.currentdisplay = self.warpByVector1
            # The following two lines insure that the view is refreshed
            self.pv_splitter.setVisible(False)
            self.pv_splitter.setVisible(True)
            self.process.start('echo ???????????????')
            self.process.waitForFinished()
            self.work_space_tool.ui.pushButton_4.setEnabled(True)

    def show_mesh_1(self,fdir):
        '''
            ????????????
        '''
        #boundary_file = self.workingdirectory + '/constant/polyMesh/boundary'
        try:
            if self.currentdisplay:
                current_display = pvs.GetActiveSource()
                pvs.Delete(current_display)
                print('delete ok')
                self.process.start('echo ??????????????????')
                self.process.waitForFinished()
        except Exception as e:
            print(e)
        try:
            self.warpByVector1Display.SetScalarBarVisibility(self.renderView1, False)
            self.static_resrmedDisplay.SetScalarBarVisibility(self.renderView1, False)
            self.process.start('echo ????????????')
        except:
            self.process.start('echo ???????????????...')
            self.process.waitForFinished()
        finally:
            self.process.start('echo ??????????????????...')
            self.process.waitForFinished()
            #self.show_mesh_display_list(boundary_file)
            self.res = pvs.MEDReader(FileName=fdir)
            self.ren_view = pvs.GetRenderView()
            self.foamDisplay =pvs.Show(self.res, self.ren_view)
            #self.foamDisplay.SetRepresentationType('Surface With Edges')
            self.currentdisplay = self.foamDisplay
            # The following two lines insure that the view is refreshed
            self.pv_splitter.setVisible(False)
            self.pv_splitter.setVisible(True)
            self.process.start('echo ???????????????')
            self.process.waitForFinished()

    def change_bridge(self,fdir):
        data = ''
        with open(fdir, 'r+') as f:
            for line in f.readlines():
                if(line.find('width') == 0):
                    line = 'width = %s' % (str(self.width1)) + '\n'
                if(line.find('height') == 0):
                    line = 'height = %s' % (str(self.height1)) + '\n'
                if(line.find('length') == 0):
                    line = 'length = %s' % (str(self.length)) + '\n'
                if(line.find('sections') == 0):
                    line = 'sections = %s' % (str(self.sections)) + '\n'
                data += line
        with open(fdir, 'r+') as f:
            f.writelines(data)
        #f.close()

    def show_openfoam_error(self,txt):
        self.process.waitForFinished()
        txt_list = txt.split('\n')
        for items in txt_list:
            self.process.waitForFinished()
            self.process.start('echo ' + items)
        self.log_textBrowser.moveCursor(self.log_textBrowser.textCursor().End)
    def continue_to_calculate(self):
        '''
            ??????
        '''
        changefile(self.workingdirectory+'/system/controlDict','startFrom','latestTime')
        self.disable_some_buttons()
        # self.workingdirectory????????????shell???????????????
        with open(self.workingdirectory + '/project_data.json','r') as load_f:
                load_dict = json.load(load_f)
        compute_control_key_list = list(load_dict['compute_control'].keys())
        compute_control_value_list = list(load_dict['compute_control'].values())
        if 'is_parallel' in compute_control_key_list:
            cores = compute_control_value_list[8]
        else:
            cores = '1'
        self.simulation_time = compute_control_value_list[0]
        QApplication.processEvents()
        self.process.start('sh '+ self.workingdirectory + '/run.sh '+ self.workingdirectory + ' '+ cores)
        #self.work_space_tool.ui.pushButton_12.clicked.connect(self.terminate_self)
        # ?????????????????????????????????????????????(?????????????????????)
        import _thread
        try:
            _thread.start_new_thread(self.residual_plotting, ("Thread-1", 2, ))
        except:
            print ("Error: ??????????????????")   
        self.process.finished.connect(self.enable_some_buttons)
        self.log_textBrowser.moveCursor(self.log_textBrowser.textCursor().End)

    def enable_some_buttons(self):
        '''
            ??????????????????????????????????????????????????????
        '''
        self.work_space_tool.ui.pushButton_ok.setEnabled(True)
        self.work_space_tool.ui.pushButton_reset.setEnabled(True)
        self.work_space_tool.ui.pushButton_beam.setEnabled(True)
        self.work_space_tool.ui.apply.setEnabled(True)
        self.work_space_tool.ui.static_button.setEnabled(True)
        self.work_space_tool.ui.modes_button.setEnabled(True)
        self.work_space_tool.ui.pushButton_4.setEnabled(True)
        '''
        self.work_space_tool.ui.pushButton_5.setEnabled(True)
        self.work_space_tool.ui.pushButton_6.setEnabled(True)
        self.work_space_tool.ui.pushButton_7.setEnabled(True)
        self.work_space_tool.ui.pushButton_8.setEnabled(True)
        self.work_space_tool.ui.pushButton_9.setEnabled(True)
        self.work_space_tool.ui.pushButton_10.setEnabled(True)
        self.work_space_tool.ui.pushButton_11.setEnabled(True)
        self.work_space_tool.ui.pushButton_13.setEnabled(True)
        #??????computing_control???????????????????????????????????????????????????????????????????????????????????????groupbox????????????
        #self.work_space_tool.computing_control.groupBox.setEnabled(True)
        self.work_space_tool.ui.pushButton_12.setEnabled(False)
        self.work_space_tool.ui.tabWidget.setTabEnabled(0,True)
        self.work_space_tool.ui.tabWidget.setTabEnabled(2,True)'''

    def disable_some_buttons(self):
        '''
            ??????????????????????????????????????????????????????
        '''

        self.work_space_tool.ui.pushButton_ok.setEnabled(False)
        self.work_space_tool.ui.pushButton_reset.setEnabled(False)
        self.work_space_tool.ui.pushButton_beam.setEnabled(False)
        self.work_space_tool.ui.apply.setEnabled(False)
        self.work_space_tool.ui.static_button.setEnabled(False)
        self.work_space_tool.ui.modes_button.setEnabled(False)
        self.work_space_tool.ui.pushButton_break.setEnabled(False)
        '''
        self.work_space_tool.ui.pushButton_5.setEnabled(False)
        self.work_space_tool.ui.pushButton_6.setEnabled(False)
        self.work_space_tool.ui.pushButton_7.setEnabled(False)
        self.work_space_tool.ui.pushButton_8.setEnabled(False)
        self.work_space_tool.ui.pushButton_9.setEnabled(False)
        self.work_space_tool.ui.pushButton_10.setEnabled(False)
        self.work_space_tool.ui.pushButton_11.setEnabled(False)
        self.work_space_tool.ui.pushButton_13.setEnabled(False)
        #self.work_space_tool.computing_control.groupBox.setEnabled(False)
        self.work_space_tool.ui.pushButton_12.setEnabled(True)
        self.work_space_tool.ui.tabWidget.setTabEnabled(0,False)
        self.work_space_tool.ui.tabWidget.setTabEnabled(2,False)
        #self.work_space_tool.ui.spacing_lineEdit.setEnabled(False)
        '''

    def terminate_self(self):
        '''
        ??????????????????
        '''
        # ??????process.kill??????????????????????????????????????????bkill
        self.process.kill()
        self.jobid = self.getjobid(self.workingdirectory + '/log')
        if self.jobid:
            self.process1.start('env -i /usr/sw-mpp/bin/bkill '+self.jobid)
            self.process.waitForFinished()
    def getjobid(self,logfile):
        '''
            ???????????????id
        '''
        try:
            with open(logfile) as log:
                for i in range(10):
                    firstline = log.readline()
                    jobid = firstline.split()[2]
                    try:
                        return str(int(jobid))
                    except:
                        pass
        except:
            print(logfile,':logfile????????????!')    

    def reload(self):
        '''
            ???????????????
        '''
        import json
        # cwd??????????????????????????????
        home_dir = os.popen('echo $HOME').read()
        self.cwd = home_dir.replace('\n','') + '/'
        # ??????????????????
        filedir = self.get_dir_name()
        if filedir:
            self.workingdirectory = filedir
            #??????????????????????????????project_data.json???????????????
            with open(self.workingdirectory + '/project_data.json','r') as load_f:
                load_dict = json.load(load_f)       
            self.update_workingdir_for_dialogs(self.workingdirectory)
            self.show_mesh(self.workingdirectory + '/.foam')
            self.dialogs_reload(self.workingdirectory,load_dict)
            self.process.start('echo ?????????????????????????????????'+self.workingdirectory)
            self.process.waitForFinished()


    def dialogs_reload(self,workingdirectory,dictionary):
        '''
            ?????????????????????
            workingdirectory???????????????
            dictionary???json?????????????????????????????????
        '''
        if 'material' in dictionary.keys():
            self.work_space_tool.mat_man.reload(dictionary)

        # ?????????model???????????????model??????????????????????????????
        if 'model' in dictionary.keys():
            self.work_space_tool.mod_man.reload(dictionary,self.work_space_tool.mod_man)
            model = self.work_space_tool.mod_man.comboBox.currentText()
            wall_function = ''
            if model == 'laminar':
                turbulence_model = 'laminar' 
            else:
                turbulence_model = self.work_space_tool.mod_man.formLayout.itemAt(1,1).widget().currentText()
                wall_function = self.work_space_tool.mod_man.addcombobox_2.currentText()
            self.update_dialog_by_model(model,turbulence_model,wall_function)
            self.update_dialog_by_model_and_boundary(model,turbulence_model,wall_function)

        if 'boundaryconditions' in dictionary.keys():
            self.work_space_tool.bod_man.reload(dictionary)  

        if 'field' in dictionary.keys():
            self.work_space_tool.fie_man.reload(dictionary,self.work_space_tool.fie_man)  

        if 'scheme' in dictionary.keys():
            self.work_space_tool.sch_man.reload(dictionary) 

        if 'solver' in dictionary.keys():
            self.work_space_tool.sol_man.reload(dictionary) 

        if 'compute_control' in dictionary.keys():
            self.work_space_tool.computing_control.reload(dictionary) 
  
    def prepare_computing(self):
        self.process.start(self.disable_some_buttons())
        self.process.waitForFinished()
        self.process.start(self.start_computing())

    def start_computing(self):
        '''
            ????????????
        '''
        run_sh_default = self.pimplefoam_root + "/gui/Run/run.sh"
        run_sh_working_dir = self.workingdirectory + '/run.sh'
        initfile(run_sh_working_dir,run_sh_default)
        log_root = self.workingdirectory + '/log'
        if os.path.exists(log_root):
            os.remove(log_root)
        # ??????????????????????????????????????????????????????????????????????????????????????????????????????
        with open(self.workingdirectory + '/project_data.json','r') as load_f:
                load_dict = json.load(load_f)
        compute_control_key_list = list(load_dict['compute_control'].keys())
        compute_control_value_list = list(load_dict['compute_control'].values())
        if 'is_parallel' in compute_control_key_list:
            cores = compute_control_value_list[5]
        else:
            cores = '1'
        self.simulation_time = compute_control_value_list[0]
        QApplication.processEvents()
        self.process.start('sh '+ self.workingdirectory + '/run.sh '+ self.workingdirectory + ' '+ cores)
        #self.work_space_tool.ui.pushButton_12.clicked.connect(self.terminate_self)
        # ?????????????????????????????????????????????(?????????????????????)
        import _thread
        try:
            _thread.start_new_thread(self.residual_plotting, ("Thread-1", 2, ))
        except:
            print ("Error: ??????????????????")   
        self.process.finished.connect(self.enable_some_buttons)
        #self.programError()
        self.log_textBrowser.moveCursor(self.log_textBrowser.textCursor().End)

    def residual_plotting(self,threadName, delay):
        import time
        from datetime import datetime, timedelta
        os.chdir(self.workingdirectory)
        # ?????????????????????????????????
        command1 = "cat log | grep 'Solving for Ux' | cut -d' ' -f9 | tr -d ','"
        command2 = "cat log | grep 'Solving for Uy' | cut -d' ' -f9 | tr -d ','"
        # ???????????????????????????????????????????????????
        command3 = "cat log | grep 'ExecutionTime' | cut -d' ' -f3 | tail -n 2"
        command4 = "cat log | grep '^Time' | cut -d' ' -f3 |tail -n 1"
        command5 = "cat log | grep 'deltaT' | cut -d' ' -f3 |tail -n 1"
        # ??????End??????????????????????????????????????????
        command6 = "cat log | grep 'End' | cut -d' ' -f3 |tail -n 1"
        command7 = "cat log | grep 'FOAM FATAL'"
        #command6 = "awk '{print NR}' log|tail -n1"
        command8 = "cat log | grep 'sending Ctrl-C to job' | cut -d' ' -f6"
        log_root = self.workingdirectory + '/log'
        while True:
            if os.path.exists(log_root):
                try:
                    time.sleep(delay)
                    # execute the command
                    content6 = os.popen(command6)
                    is_over_list = content6.read().strip().split('\n')
                    content6.close()
                    content7 = os.popen(command7)
                    is_error_list = content7.read().strip().split('\n')
                    content7.close()
                    content8 = os.popen(command8)
                    is_terminate_list = content8.read().strip().split('\n')
                    content8.close()
                    is_over = is_over_list[0]
                    is_error = is_error_list[0]
                    is_terminate = is_terminate_list[0]
                    #print(is_over_list)
                    if is_over:
                        self.progress_bar.setValue(100)
                        self.progress_bar_label.setText('????????????:0s')
                        break
                    if is_error:
                        self.error_txt = ''
                        self.progress_bar.setValue(100)
                        self.progress_bar_label.setText('????????????:0s')
                        with open(log_root,'r+',encoding='utf-8') as fr:
                            keywordlist = (fr.read().splitlines())
                            for index,text in enumerate(keywordlist):
                              if 'FOAM FATAL' in text:
                                    start_index = index
                            self.error_txt ='\n'.join(keywordlist[start_index:-1])
                        fr.close()
                        #self.process.waitForFinished()
                        #for text in self.error_txt_list:
                        #    newCursor1 = self.log_textBrowser.textCursor()
                        #    newCursor1.movePosition(QtGui.QTextCursor.End)
                        #    self.log_textBrowser.setTextCursor(newCursor1)
                        #self.log_textBrowser.insertText(self.error_txt)
                        #logOutput = self.log_textBrowser
                        #logOutput.append(text + '\n')
                        #QApplication.processEvents()
                        #error_sh_default = self.pimplefoam_root + "/alternativefile/error_txt.sh"
                        #error_sh_working_dir = self.workingdirectory + '/error_txt.sh'
                        #initfile(error_sh_working_dir,error_sh_default)
                        self.error_txt += '\n'
                        self.openfoam_error.emit(self.error_txt)
                        break
                    if is_terminate:
                        self.progress_bar_label.setText('????????????:0s')
                        break
                    content1 = os.popen(command1)
                    Ux=content1.read().strip().split('\n')
                    content1.close()
                    content2 = os.popen(command2)
                    Uy=content2.read().strip().split('\n')
                    content2.close()
                    Ux = list(map(float, Ux))
                    Uy = list(map(float, Uy))
                    if len(Ux) == len(Uy):
                        self.residual_plot.curve1.setData(Ux) 
                        self.residual_plot.curve2.setData(Uy) 

                    content3 = os.popen(command3)
                    delta_exacuate_time_list = content3.read().strip().split('\n')
                    content3.close()
                    content4 = os.popen(command4)
                    computed_time_list = content4.read().strip().split('\n')
                    content4.close()
                    content5 = os.popen(command5)
                    deltaT_list = content5.read().strip().split('\n')
                    content5.close()

                    total_time = float(self.simulation_time)
                    computed_time =  float(computed_time_list[0])
                    deltaT = float(deltaT_list[0])
                    delta_exacuate_time = float(delta_exacuate_time_list[1])-float(delta_exacuate_time_list[0])
                    epxected_remaining_time = int((total_time-computed_time)/deltaT*delta_exacuate_time)
                    prograss_bar_value = int(computed_time/total_time*100)
                    self.progress_bar.setValue(prograss_bar_value)   
                    sec = timedelta(seconds=epxected_remaining_time)
                    d = datetime(1,1,1) + sec
                    if epxected_remaining_time < 60:
                        self.progress_bar_label.setText('????????????:' + "%d???" % d.second)
                    elif epxected_remaining_time < 3600:
                        self.progress_bar_label.setText('????????????:' + "%d???%d???" % ( d.minute, d.second))
                    elif epxected_remaining_time < 86400:
                        self.progress_bar_label.setText('????????????:' + "%d???%d???%d???" % ( d.hour, d.minute, d.second))
                    elif epxected_remaining_time > 86400:
                        self.progress_bar_label.setText('????????????:' + "%d???%d???%d???%d???" % (d.day-1, d.hour, d.minute, d.second))    
                except (Exception, BaseException) as e:
                    print('fail to plot residual error')
                    print(e)
            else:
                pass

    
    def main_tab_change(self,index):
        '''
            ?????????????????????????????????????????????????????????
            index = 1 ????????????
            index = 2 ???????????????
        '''
        '''if index == 1:
            if not self.workingdirectory:
                QtWidgets.QMessageBox.information(self, '??????', '????????????????????????!')'''
        if index == 1:
            import SalomePyQt
            import pvsimple as pvs
            sg = SalomePyQt.SalomePyQt()
            current_view = sg.getViews()
            self.detach()
            sg.activateModule("ParaViS")
            views = sg.getViews()
            sg.setViewTitle(views[-1],'ParaViS')
            self.work_space_tool.ui.tabWidget.setCurrentIndex(0)
            previous_source = pvs.GetActiveSource()
            pvs.Delete(previous_source)
            
            #### disable automatic camera reset on 'Show'
            pvs._DisableFirstRenderCameraReset()

            # create a new 'OpenFOAMReader'
            foam = pvs.OpenFOAMReader(FileName=self.workingdirectory+'/.foam')
            
            # get animation scene
            animationScene1 = pvs.GetAnimationScene()

            # update animation scene based on data timesteps
            animationScene1.UpdateAnimationUsingDataTimeSteps()

            # set active source
            pvs.SetActiveSource(foam)

            # get active view
            renderView1 = pvs.GetActiveViewOrCreate('RenderView')
            # uncomment following to set a specific view size
            # renderView1.ViewSize = [1054, 491]

            # show data in view
            foamDisplay = pvs.Show(foam, renderView1)

            # trace defaults for the display properties.
            foamDisplay.Representation = 'Surface'

            # show color bar/color legend
            foamDisplay.SetScalarBarVisibility(renderView1, True)

            # reset view to fit data
            renderView1.ResetCamera()

            # get color transfer function/color map for 'p'
            pLUT = pvs.GetColorTransferFunction('p')

            # get opacity transfer function/opacity map for 'p'
            pPWF = pvs.GetOpacityTransferFunction('p')
  
            if os.path.exists(self.workingdirectory + '/processor0'):
                print('1111111')
                foam.CaseType = 'Decomposed Case'
                animationScene1.UpdateAnimationUsingDataTimeSteps()
                renderView1.Update()

    def dataReady(self):
        '''
            ??????Qprocess?????????????????????????????????????????????????????????????????????????????????
        '''
        logOutput = self.log_textBrowser.textCursor()
        processStdout = bytearray(self.process.readAllStandardOutput())
        processStdout = processStdout.decode(encoding='UTF-8',errors='strict')
        newCursor1 = self.log_textBrowser.textCursor()
        newCursor1.movePosition(QtGui.QTextCursor.End)
        self.log_textBrowser.setTextCursor(newCursor1)
        logOutput = self.log_textBrowser.textCursor()
        logOutput.insertText(processStdout)
        # self.log_textBrowser.moveCursor(self.log_textBrowser.textCursor().End)

   # def programError(self):
   #     '''
   #         ??????Qprocess?????????????????????????????????????????????????????????????????????????????????
   #     '''
   #     print('111')
   #     processStdout = bytearray(self.process.readAllStandardError())
   #     processStdout2= processStdout.decode(encoding='UTF-8',errors='strict')
   #     print(processStdout2)
   #     newCursor1 = self.log_textBrowser.textCursor()
   #     newCursor1.movePosition(QtGui.QTextCursor.End)
   #     self.log_textBrowser.setTextCursor(newCursor1)
   #     logOutput = self.log_textBrowser.textCursor()
   #     logOutput.insertText(processStdout2)
        # self.log_textBrowser.moveCursor(self.log_textBrowser.textCursor().End)

    def show_mesh_display_list(self,boundary_root):
        '''
            ????????????????????????internal part?????????????????????
            boundary_root?????????????????????constant/polyMesh/boundary
        '''
        self.mesh_list = []
        with open(boundary_root,'r+',encoding='utf-8') as fr:
            keywordlist = fr.read().splitlines()
            for index,text in enumerate(keywordlist):
                if text == '    {':
                    self.mesh_list.append(keywordlist[index-1].lstrip('    '))                 
        fr.close()

        self.internalMesh_region = QtWidgets.QCheckBox()
        self.internalMesh_region.setText('internalMesh')
        self.internalMesh_region.setChecked(True)
        self.work_space_tool.ui.formLayout.addWidget(self.internalMesh_region)
        for items in self.mesh_list:
            self.mesh_region = QtWidgets.QCheckBox()
            self.mesh_region.setText(items)
            self.work_space_tool.ui.formLayout.addWidget(self.mesh_region)

    def change_mesh_display(self, res):
        '''
            ????????????????????????????????????
            res???pvs.OpenFOAMReader??????.foam????????????????????????
        '''
        '''
        res_MeshRegions = []
        if res:
            for i in range(self.work_space_tool.ui.formLayout.rowCount()):
                if self.work_space_tool.ui.formLayout.itemAt(i,1).widget().isChecked():
                    items = self.work_space_tool.ui.formLayout.itemAt(i,1).widget().text()
                    res_MeshRegions.append(items)
            res.MeshRegions = res_MeshRegions
            self.ren_view = pvs.GetRenderView()
            #represent_type = self.work_space_tool.ui.represent_combo.currentText()
            #self.currentdisplay.SetRepresentationType(represent_type)
            self.ren_view.Update()
            # The following two lines insure that the view is refreshed
            self.pv_splitter.setVisible(False)
            self.pv_splitter.setVisible(True)
        else:
            pass'''
        pass

    def check_is_working_dir_mesh_tran(self):
        '''
            ???????????????????????????????????????
        '''
        if self.workingdirectory:
            self.work_space_tool.MeshtranDialog.show()
            #self.work_space_tool.mesh_tran.pushButton_3.clicked.connect(self.work_space_tool.MeshtranDialog.reject)
        else:
            QtWidgets.QMessageBox.information(self, '??????', '????????????????????????!')

    def check_is_working_dir_gen_mesh(self):
        '''
            ???????????????????????????????????????
        '''
        if self.workingdirectory:
            self.work_space_tool.MeshgenerateDialog.show()
        else:
            QtWidgets.QMessageBox.information(self, '??????', '????????????????????????!')

    def show_generated_mesh(self):
        '''
            ??????openfoam??????????????????
        '''

        self.work_space_tool.mesh_generate.ok_button.setEnabled(False)
        self.work_space_tool.mesh_generate.cancel_button.setEnabled(False)
        self.work_space_tool.mesh_generate.import_button.setEnabled(False)
        QApplication.processEvents()
        pros = self.work_space_tool.mesh_generate.addcombo.currentText()
        mesh_generate_sh_default = self.pimplefoam_root + "/gui/Mesh_generation/mesh_generate.sh"
        mesh_generate_sh_working_dir = self.workingdirectory + '/mesh_generate.sh'
        initfile(mesh_generate_sh_working_dir,mesh_generate_sh_default)
        self.process.start('sh '+ mesh_generate_sh_working_dir + ' ' +
            self.workingdirectory + ' ' + pros)
        self.process.finished.connect(self.enable_mesh_generate_button)
        
        fname = self.workingdirectory + '/' + '.foam'
        if not os.path.isfile(fname):
            fd = open(fname,mode = "w",encoding="utf-8")
            fd.close()
        self.work_space_tool.mesh_generate.import_button.clicked.connect(lambda:self.show_mesh(fname))
    def enable_mesh_generate_button(self):
        self.work_space_tool.mesh_generate.ok_button.setEnabled(True)
        self.work_space_tool.mesh_generate.cancel_button.setEnabled(True)
        self.work_space_tool.mesh_generate.import_button.setEnabled(True)
      

    def show_mesh(self,fname):
        '''
            ????????????
        '''
        boundary_file = self.workingdirectory + '/constant/polyMesh/boundary'
        self.process.start('echo ??????????????????...')
        self.process.waitForFinished()
        self.show_mesh_display_list(boundary_file)
        self.res = pvs.OpenFOAMReader(FileName=fname)
        self.ren_view = pvs.GetRenderView()
        self.foamDisplay =pvs.Show(self.res, self.ren_view)
        self.currentdisplay = self.foamDisplay
        # The following two lines insure that the view is refreshed
        self.pv_splitter.setVisible(False)
        self.pv_splitter.setVisible(True)
        self.process.start('echo ???????????????')
        self.process.waitForFinished()
        boundary_file_root = self.workingdirectory + '/constant/polyMesh/boundary'
        self.work_space_tool.BCDialog = QDialog()
        self.work_space_tool.bod_man = Ui_boundary_form()
        self.work_space_tool.bod_man.setupUi(self.work_space_tool.BCDialog,self.workingdirectory,self.pimplefoam_root, boundary_file_root)
        self.work_space_tool.mod_man.Model_selecting.connect(self.update_dialog_by_model_and_boundary)
        self.work_space_tool.BCDialog.setWindowModality(Qt.ApplicationModal)
        self.work_space_tool.bod_man.MainDialog.setWindowModality(Qt.ApplicationModal)

    def show_mesh_check_res(self):
        '''
            ??????????????????
        '''
        '''
        self.mesh_chack_enable(False)
        QApplication.processEvents()
        mesh_check_sh_default = self.pimplefoam_root + "/gui/Checkmesh/mesh_check.sh"
        mesh_check_sh_working_dir = self.workingdirectory + '/mesh_check.sh'
        initfile(mesh_check_sh_working_dir,mesh_check_sh_default)
        self.process.start('sh '+ mesh_check_sh_working_dir + ' ' +
            self.workingdirectory + ' ' + '1')
        #self.process.waitForFinished()
        self.process.finished.connect(lambda:self.mesh_chack_enable(True))
        '''
        pass

    def mesh_chack_enable(self,bool):
        pass
        #self.work_space_tool.ui.pushButton.setEnabled(bool)
        #self.work_space_tool.ui.pushButton_2.setEnabled(bool)
        #self.work_space_tool.ui.pushButton_3.setEnabled(bool)
        #self.work_space_tool.ui.pushButton_4.setEnabled(bool)
        #self.work_space_tool.ui.pushButton_15.setEnabled(bool)
        #self.work_space_tool.ui.pushButton_16.setEnabled(bool)
        
    def return_to_smash(self):
        import SalomePyQt
        sg = SalomePyQt.SalomePyQt()
        sg.activateModule("Mesh")

    def transfer_mash(self, workingdirectory):
        '''
            unv???????????????foam
            workingdirectory???????????????
        '''
        self.cwd = self.workingdirectory
        full_load_pv=True
        # self.shown = None
        unv_file = self.get_file_name('.unv')
        if unv_file:
            unv_fname = os.path.basename(unv_file)
            self.work_space_tool.MeshtranDialog.accept()

            if workingdirectory:
                unv_dir_file = self.workingdirectory + '/' + unv_fname
                initfile(unv_dir_file, unv_file)
                #???????????????????????????
                mesh_tran_sh_default =self.pimplefoam_root + "/gui/Mesh_transfer/mesh_transfer.sh"
                mesh_tran_sh_working_dir = self.workingdirectory + '/mesh_transfer.sh'
                initfile(mesh_tran_sh_working_dir,mesh_tran_sh_default)
                self.process.start('sh '+ mesh_tran_sh_working_dir + ' '+
                    self.workingdirectory + ' ' + unv_fname)
                self.process.waitForFinished()
                fname = workingdirectory + '/' + '.foam'
                if not os.path.isfile(fname):
                    fd = open(fname,mode = "w",encoding="utf-8")
                    fd.close()
                self.show_mesh(fname)
  
            else:
  
                QtWidgets.QMessageBox.information(self, '??????', '????????????????????????!')
        else:
            pass


    def create_dir(self):
        '''
            ??????????????????
        '''
        import salome
        home_dir = os.popen('echo $HOME').read()
        self.default_file_root = self.pimplefoam_root + '/defaultfile'
        self.cwd = home_dir.replace('\n','') + '/'
        filedir = self.get_dir_name()
        if filedir:
            self.set_workingdir.emit(filedir)
            #filedir += '/workingdirectory'
            inittree(filedir,self.default_file_root)
            self.workingdirectory = filedir
            self.update_workingdir_for_dialogs(self.workingdirectory)
            self.process.start('echo ?????????????????????????????????'+self.workingdirectory)
            self.process.waitForFinished()
        else:
            pass
        
    def get_file_name(self,filetype):
        fname, filetype = QFileDialog.getOpenFileName(self,  
                                    "????????????",  
                                    self.cwd, # ???????????? 
                                    "All Files (*);;OpenFoam Files (*" + filetype + ")")
        return fname

    def get_dir_name(self):
        dir_choose = QFileDialog.getExistingDirectory(self,  
                                    "???????????????",  
                                    self.cwd) # ????????????
        return dir_choose

    def open_openfoam_file(self,workingdirectory):
        '''
            ??????foam???????????????????????????
        '''
        if workingdirectory:
            self.cwd = self.workingdirectory
            full_load_pv = True
            filedir = self.get_dir_name()
            fname = workingdirectory + '/' + '.foam'
            if not os.path.isfile(fname):
              fd = open(fname,mode = "w",encoding="utf-8")
              fd.close()
            if filedir:
              inittree(workingdirectory + '/constant/polyMesh',filedir)
              self.show_mesh(fname)

            else:
                pass 
        else:
            QtWidgets.QMessageBox.information(self, '??????', '????????????????????????')

    def update_workingdir_for_dialogs(self, workingdirectory):
        '''
            ??????????????????????????????????????????????????????
        '''
        self.work_space_tool.MaterialDialog = QDialog() 
        self.work_space_tool.mat_man = Ui_Mat_Man(workingdirectory,self.pimplefoam_root)
        self.work_space_tool.mat_man.setupUi(self.work_space_tool.MaterialDialog)
        self.work_space_tool.MaterialDialog.setWindowModality(Qt.ApplicationModal)
        self.work_space_tool.mat_man.subDialog.setWindowModality(Qt.ApplicationModal)

        self.work_space_tool.ModelDialog = QDialog()
        self.work_space_tool.mod_man = Ui_Mod_Edi()
        self.work_space_tool.mod_man.setupUi(self.work_space_tool.ModelDialog,workingdirectory,self.pimplefoam_root)
        self.work_space_tool.mod_man.Model_selecting.connect(self.update_dialog_by_model)
        self.work_space_tool.ModelDialog.setWindowModality(Qt.ApplicationModal)

        self.work_space_tool.BCDialog = QDialog()
        self.work_space_tool.bod_man = Ui_boundary_form()
        self.work_space_tool.bod_man.setupUi(self.work_space_tool.BCDialog,workingdirectory,self.pimplefoam_root)
        self.work_space_tool.BCDialog.setWindowModality(Qt.ApplicationModal)
        self.work_space_tool.bod_man.MainDialog.setWindowModality(Qt.ApplicationModal)

        self.work_space_tool.FieldDialog = QDialog()
        self.work_space_tool.fie_man = Ui_Fieldsetting()
        self.work_space_tool.fie_man.setupUi(self.work_space_tool.FieldDialog,workingdirectory,self.pimplefoam_root)
        self.work_space_tool.FieldDialog.setWindowModality(Qt.ApplicationModal)

        self.work_space_tool.SolverDialog = QDialog()
        self.work_space_tool.sol_man = Ui_Sol_Man()
        self.work_space_tool.sol_man.setupUi(self.work_space_tool.SolverDialog,workingdirectory)
        self.work_space_tool.SolverDialog.setWindowModality(Qt.ApplicationModal)
        self.work_space_tool.sol_man.solver_form_Ui.setWindowModality(Qt.ApplicationModal)

        self.work_space_tool.SchemeDialog = QDialog()
        self.work_space_tool.sch_man = Ui_Schemesetting()
        self.work_space_tool.sch_man.setupUi(self.work_space_tool.SchemeDialog,workingdirectory)
        self.work_space_tool.SchemeDialog.setWindowModality(Qt.ApplicationModal)

        self.work_space_tool.MeshtranDialog = QDialog()
        self.work_space_tool.mesh_tran = Ui_Mesh_tran()
        self.work_space_tool.mesh_tran.setupUi(self.work_space_tool.MeshtranDialog)
        self.work_space_tool.MeshtranDialog.setWindowModality(Qt.ApplicationModal)
        #self.work_space_tool.mesh_tran.pushButton.clicked.connect(self.return_to_smash)
        #self.work_space_tool.mesh_tran.pushButton_2.clicked.connect(lambda:self.transfer_mash(self.workingdirectory))
        self.work_space_tool.MeshtranDialog.setWindowModality(Qt.ApplicationModal)

        self.work_space_tool.MeshgenerateDialog = QDialog()
        self.work_space_tool.mesh_generate = Ui_Mesh_generate()
        self.work_space_tool.mesh_generate.setupUi(self.work_space_tool.MeshgenerateDialog,workingdirectory,self.pimplefoam_root)
        self.work_space_tool.MeshgenerateDialog.setWindowModality(Qt.ApplicationModal)
        self.work_space_tool.mesh_generate.ok_button.clicked.connect(self.show_generated_mesh)
        self.work_space_tool.MeshgenerateDialog.setWindowModality(Qt.ApplicationModal)
        
        self.work_space_tool.ComputingControlDialog = QDialog()
        self.work_space_tool.computing_control = Ui_Computing_control()
        self.work_space_tool.computing_control.setupUi(self.work_space_tool.ComputingControlDialog, workingdirectory,self.pimplefoam_root)
        self.work_space_tool.ComputingControlDialog.setWindowModality(Qt.ApplicationModal)
        # self.work_space_tool.mod_man.Model_selecting.connect(self.get_simulation_time)

    # def get_simulation_time(self,simulation_time):
    #     self.simulation_time = simulation_time

    def update_dialog_by_model_and_boundary(self,model,turbulence_model,wall_function):
        '''
            ?????????????????????????????????????????????????????????boundary??????????????????
            model:laminar,RAS,LES
            turbulence_model: e.g.kEpsilon,kOmegaSST
            wall_function: on or off
        '''
        self.model = model
        self.turbulence_model = turbulence_model
        self.wall_function = wall_function

        boundary_file_root = self.workingdirectory + '/constant/polyMesh/boundary'
        self.work_space_tool.BCDialog = QDialog()
        self.work_space_tool.bod_man = Ui_boundary_form(model = self.model,turbulence_model = self.turbulence_model)
        self.work_space_tool.bod_man.setupUi(self.work_space_tool.BCDialog,self.workingdirectory,self.pimplefoam_root, boundary_file_root)
        self.work_space_tool.BCDialog.setWindowModality(Qt.ApplicationModal)
        self.work_space_tool.bod_man.MainDialog.setWindowModality(Qt.ApplicationModal)
        # self.work_space_tool.FieldDialog = QDialog()
        # self.work_space_tool.fie_man = Ui_Fieldsetting()
        # self.work_space_tool.fie_man.setupUi(self.work_space_tool.FieldDialog,self.workingdirectory,self.pimplefoam_root,
        #                                      model = self.model,turbulence_model = self.turbulence_model)
    
    def update_dialog_by_model(self,model,turbulence_model,wall_function):
        '''
            ????????????????????????????????????????????????????????????
            model:laminar,RAS,LES
            turbulence_model: e.g.kEpsilon,kOmegaSST
            wall_function: on or off
        '''
        self.model = model
        self.turbulence_model = turbulence_model
        self.wall_function = wall_function

        self.work_space_tool.FieldDialog = QDialog()
        self.work_space_tool.fie_man = Ui_Fieldsetting()
        self.work_space_tool.fie_man.setupUi(self.work_space_tool.FieldDialog,self.workingdirectory,self.pimplefoam_root,
                                             model = self.model,turbulence_model = self.turbulence_model)
        self.work_space_tool.FieldDialog.setWindowModality(Qt.ApplicationModal)

        self.work_space_tool.SchemeDialog = QDialog()
        self.work_space_tool.sch_man = Ui_Schemesetting()
        self.work_space_tool.sch_man.setupUi(self.work_space_tool.SchemeDialog,self.workingdirectory,
                                             model = self.model,turbulence_model = self.turbulence_model,
                                             wall_function=self.wall_function)
        self.work_space_tool.SchemeDialog.setWindowModality(Qt.ApplicationModal)

        self.work_space_tool.SolverDialog = QDialog()
        self.work_space_tool.sol_man = Ui_Sol_Man()
        self.work_space_tool.sol_man.setupUi(self.work_space_tool.SolverDialog,self.workingdirectory,
                                             model = self.model,turbulence_model = self.turbulence_model)
        self.work_space_tool.SolverDialog.setWindowModality(Qt.ApplicationModal)
        self.work_space_tool.sol_man.solver_form_Ui.setWindowModality(Qt.ApplicationModal)

        

    def activate(self, enable):
        """
        Activate/deactivate workspace.

        Arguments:
            enable (bool): *True* to activate, *False* to deactivate.
        """
        self.setVisible(enable)



    def detach(self, keep_pipeline=True):
        """
        Function called upon deactivating asterstudy, allows to properly
        remove all layouts and view from the ParaView View (salome View)
        """
        from .salomegui import get_salome_pyqt
        import pvsimple as pvs

        # Clears the PV widget and removes the event filter (right click
        # behavior) from all of its children.
        if self.pv_widget:
            for child in self.pv_widget_children:
                if child:
                    try:
                        child.removeEventFilter(self)
                    except BaseException: # pragma pylint: disable=broad-except
                        pass
            self.pv_widget_children = []
            self.pv_widget = None

        # This forces the creation of new overlay buttons upon restarting
        # the AsterStudy results tab
        self.pv_overlay = None
        self.toolbuttons = None

        # Deletes the active view and layout from paraview
        # Close the (salome) view corresponding to 'ParaView'
        if self.pv_view:
            get_salome_pyqt().closeView(self.pv_view)
        # get_salome_pyqt().closeView(self.ren_view)
        # get_salome_pyqt().closeView(self.ren_view1)
        
        # self.ren_view = None
        # self.ren_view1 = None
            pvs.RemoveLayout(self.pv_layout)
        self.pv_layout = None
        self.pv_view = None

        # Optional: clear all sources and proxies, leaving no trace!
        if not keep_pipeline:
            self.previous = {}
            self.current = None
            self.shown = None
            pxm = pvs.servermanager.ProxyManager()
            pxm.UnRegisterProxies()
            del pxm
            pvs.Disconnect()
            pvs.Connect()

    def init_paraview(self, full_load_pv=True):
        """
        Initializes, if necessary, paraview and creates a dedicated pvsimple
        view in the results tab.
        """
        from .salomegui import (get_salome_pyqt, get_salome_gui)

        if not self.pv_view:
            import time
            dbg_print(">> Initializing PV view for the main tab...")
            start = time.time()
            self.views = get_salome_pyqt().findViews('ParaView')
            self.pv_view = self.views[-1]
            get_salome_pyqt().activateViewManagerAndView(self.pv_view)
            paraview = self.update_pv_layout_view()
            end = time.time()
            dbg_print("  Finished in %d seconds..." % int(end - start))

            self._finalize_pv_widget()
        else:
            self.update_pv_layout_view()
            self._finalize_pv_widget()

        if self.current:
            self.redraw()

    def _finalize_pv_widget(self):
        """
        References toolbuttons (for interactive selection) and updates the
        overlay widget if needed
        """
        if self.pv_widget:
            if not self.toolbuttons:
                self._add_toolbuttons()
            if not self.pv_overlay:
                self._add_overlay()

    def _add_toolbuttons(self):
        """
        Shortcut for referencing the toolbuttons that may need to be
        automatically activated for point and cell selections

        requires : self.pv_widget
        """
        self.toolbuttons = {'Interactive Select Cells On': None,
                            'Interactive Select Points On': None,
                            'Select Points On (d)': None,
                            'Select Cells On (s)': None,
                            }
        to_find = list(self.toolbuttons.keys())

        for tbutt in self.pv_widget.findChildren(QtWidgets.QToolButton)[::-1]:
            if not to_find:
                break
            for tooltip in to_find:
                if tooltip in tbutt.toolTip():
                    self.toolbuttons[tooltip] = tbutt
                    to_find.remove(tooltip)
                    break

    def _add_overlay(self):
        """
        Add an overlay widget to the main pv_widget with a few buttons
        to control the view, save screenshots, etc.

        requires : self.pv_widget
        """

        # START
        # ol_height = 56 # Overlay height in pixels
        ol_height = 50  # Overlay height in pixels
        self.pv_overlay = OverlayBar(self.pv_widget, height=ol_height,
                                     botline=(0, 0, 255, 2)
                                     )

        # >> Buttons toolbar items
        #    Start with an empty shell widget, used for parenting toolbar buttons
        #    and enforcing a simple horizontal layout with a right spacer
        hlayo = QtWidgets.QHBoxLayout()
        hlayo.setContentsMargins(5, 5, 5, 5)
        hlayo.setSpacing(5)
        # add_button(hlayo, tooltip='Refresh view',
        #            icon='PVC Refresh',
        #            callback=self.redraw)
        # add_separator(hlayo)

        # Camera controls
        add_button(hlayo, tooltip='Project view to X (YZ-plane)',
                   icon='PVC XProj',
                   callback=lambda: pvcontrol(self, 'xproj'))
        add_button(hlayo, tooltip='Project view to Y (XZ-plane)',
                   icon='PVC YProj',
                   callback=lambda: pvcontrol(self, 'yproj'))
        add_button(hlayo, tooltip='Project view to Z (XY-plane)',
                   icon='PVC ZProj',
                   callback=lambda: pvcontrol(self, 'zproj'))

        # Display controls
        self.outline_btn = add_button(hlayo, tooltip='Toggle bounding box',
                                      icon='PVC Outline',
                                      callback=lambda: pvcontrol(
                                          self, 'outline'),)
                                    #   checkable=True)

        # >> Information labels bar
        hlayo.addStretch(1)
        self.infobar_label = QtWidgets.QLabel(self.pv_overlay)
        hlayo.addWidget(self.infobar_label)
        self.update_infobar()

        self.pv_overlay.setLayout(hlayo)

    def update_pv_layout_view(self, full_update=True):
        """
        Updates or creates a new PV layout and view for AsterStudy
        post processing in the Results tab
        """
        import pvsimple as pvs
        from .salomegui import get_salome_pyqt

        pv_layout = pvs.GetLayoutByName(RESULTS_PV_LAYOUT_NAME)
        if not pv_layout:
            pv_layout = pvs.CreateLayout(name=RESULTS_PV_LAYOUT_NAME)

            
        self.views = pvs.GetViewsInLayout(pv_layout)
        if not self.views:
            pvs.SetActiveView(None)
            self.ren_view = pvs.CreateRenderView(guiName=RESULTS_PV_VIEW_NAME)

            self.ren_view.UseGradientBackground = 1
            pv_layout.AssignView(0, self.ren_view)

        self.pv_layout = pvs.GetLayoutByName("Layout #1")

        self.pv_widget = get_salome_pyqt().getViewWidget(self.pv_view)
        self.pv_widget.setSizePolicy(QtWidgets.QSizePolicy.Expanding,
                                    QtWidgets.QSizePolicy.Expanding)

        self.pv_splitter.addWidget(self.pv_widget)

        self.pv_splitter.setVisible(False)
        self.pv_splitter.setVisible(True)

        pvs.Render()

        self.pv_widget_children = [self.pv_widget]
        self.pv_widget_children += self.pv_widget.findChildren(QtWidgets.QWidget)

        to_ignore = []
        if self.pv_overlay:
            to_ignore = [self.pv_overlay] + \
                self.pv_overlay.findChildren(QtWidgets.QWidget)

        for child in self.pv_widget_children:
            if not child in to_ignore:
                child.installEventFilter(self)


    def clear_paraview_pipeline(self):
        """
        Clears up intermediate paraview pipeline sources and
        refreshes the current representation
        """
        wait_cursor(True)
        self.shown.clear_sources()
        self.clear_readers()
        self.redraw()
        wait_cursor(False)

    def clear_readers(self):
        """
        Clears readers from the paraview pipeline not relevant
        to the current representation
        """
        import pvsimple as pvs

        to_remove = []
        for path in self.previous:
            if path == self.current.path:
                continue
            prev, _ = self.previous[path]

            for source in ['filter_source', 'extract_source', 'source',
                           'full_source', 'mode_source', 'dup_source']:
                if hasattr(prev, source):
                    src = getattr(prev, source)
                    setattr(prev, source, None)
                    if not src:
                        continue
                    try:
                        pvs.Delete(src)
                    except RuntimeError:
                        pass

            to_remove.append(path)

        for path in to_remove:
            self.previous.pop(path, None)

        for source in ['mode_source', 'dup_source']:
            if hasattr(self.current, source):
                src = getattr(self.current, source)
                setattr(self.current, source, None)
                if not src:
                    continue
                try:
                    pvs.Delete(src)
                except RuntimeError:
                    pass

    def minmax_shown(self):
        """Returns whether the minmax button is checked"""
        return self.minmax_btn.isChecked()

    def set_minmax_shown(self):
        """Checks the minmax button"""
        self.minmax_btn.setChecked(True)

    def outline_shown(self):
        """Returns whether the outline button is checked"""
        return self.outline_btn.isChecked()

    def set_outline_shown(self):
        """Checks the outline button"""
        self.outline_btn.setChecked(True)


    def load_med_result(self, med_fn, loader):
        """
        Load a results file in MED format

        Arguments:
            med_fn (string): full path to the MED filename to be loaded
            loader
        """
        if not med_fn:
            dbg_print("Invalid med file")
            return

        self._loader = loader
        self._loader.start()
        QtCore.QTimer.singleShot(50, lambda: self.load_med_result_call(med_fn))

    def load_med_result_call(self, med_fn, full_load_pv=True):
        """
        Load a results file in MED format

        Arguments:
            med_fn (string): full path to the MED filename to be loaded
        """
        # Initialize paraview widget in asterstudy gui
        # (this can take a few seconds on first load)
        new_load = True

        self.init_paraview(full_load_pv=full_load_pv)
        self.shown = None

        modif_time = os.path.getmtime(med_fn)
        if med_fn in self.previous:
            # This file has already been read, check if the modification date
            # is identifical to the previous load, if so then just set it as current
            new_load = (modif_time != self.previous[med_fn][1])

        if new_load:
            if not self._loader:
                from . salomegui import LoadingMessage
                self._loader = LoadingMessage(self, 'Please wait...', True)
                self._loader.start()

            res = ResultFile(med_fn)

            # Check if there are indeed fields that can be represented
            if res.is_empty():
                if self._loader:
                    self._loader.terminate()
                wait_cursor(False)

                if self.astergui:
                    msg = translate("AsterStudy",
                                    "The provided MED file contains no "
                                    "result concepts or fields.\n")
                    buttons = QtWidgets.QMessageBox.Ok
                    QtWidgets.QMessageBox.warning(self.astergui.mainWindow(), "AsterStudy",
                                          msg, buttons, Qt.QMessageBox.Ok)

                return

            self.current = res
            self.previous.update({self.current.path: (self.current, modif_time)})
        else:
            self.current = self.previous[med_fn][0]

        self.ren_view.ResetCamera()

        # self.refresh_navigator()
        pvcontrol(self, 'first')

        # Show displacement field preferentially by default
        for concept in self.current.concepts:
            for field in concept.fields:
                if 'DEPL' in field.name:
                    self.represent(field, WarpRep)
                    pvcontrol(self, 'resetview')
                    return

        # If not found, show the first field that is found
        for concept in self.current.concepts:
            for field in concept.fields:
                self.represent(field)
                pvcontrol(self, 'resetview')
                return

    def projection(self,ren_view,request):
        if request == 'x':
            refpos = [-1e5, 0., 0.]\
                if ren_view.CameraPosition[0] > 0\
                else [1e5, 0., 0.]
            ren_view.CameraPosition = refpos
            ren_view.CameraFocalPoint = [0.0, 0.0, 0.0]
            ren_view.CameraViewUp = [0.0, 0.0, 1.0]
            ren_view.ResetCamera()
        elif request == 'y':
            refpos = [0., -1e5, 0.] if ren_view.CameraPosition[1] > 0 else [0., 1e5, 0.]
            ren_view.CameraPosition = refpos
            ren_view.CameraFocalPoint = [0.0, 0.0, 0.0]
            ren_view.CameraViewUp = [0.0, 0.0, 1.0]
            ren_view.ResetCamera()
        elif request == 'z':
            refpos = [0., 0., 1e5] if ren_view.CameraPosition[2] < 0 \
                else [0., 0., -1e5]
            ren_view.CameraPosition = refpos
            ren_view.CameraFocalPoint = [0.0, 0.0, 0.0]
            ren_view.CameraViewUp = [0.0, 1.0, 0.0]
            ren_view.ResetCamera()        

    def resetview(self,needreset):
        if not needreset:
            if self.sender() == self.sidebar.groupBox_5:
                pvs.HideAll(self.ren_view)
                pvs.Show(self.solidpvd, self.ren_view)
                self.currentdisplay = self.foamDisplay
            elif self.sender() == self.sidebar.groupBox_6:
                pvs.HideAll(self.ren_view1)
                pvs.Show(self.fluidfoam, self.ren_view1)
                self.currentdisplay1 = self.fluidfoamDisplay

    def cliping(self):
        if self.sender() == self.sidebar.comboBox_9:
            if not self.clip1:
                self.clip1 = pvs.Clip(Input=self.solidpvd)
            pvs.Hide3DWidgets(proxy=self.clip1.ClipType)
            if self.sender().currentText() == 'X??????':
                # self.clip1.ClipType.Origin = [-13184.847264041935, 0.0, 150000.0]
                self.clip1.ClipType.Normal = [1.0, 0.0, 0.0]
            elif self.sender().currentText() == 'Y??????':
                # self.clip1.ClipType.Origin = [-13184.847264041935, 0.0, 150000.0]
                self.clip1.ClipType.Normal = [0.0, 1.0, 0.0]
            elif self.sender().currentText() == 'Z??????':
                # self.clip1.ClipType.Origin = [-13184.847264041935, 0.0, 150000.0]
                self.clip1.ClipType.Normal = [0.0, 0.0, 1.0]

            pvs.HideAll(self.ren_view)
            clip1Display = pvs.Show(self.clip1, self.ren_view)
            clip1Display.Representation = 'Surface'
            self.currentdisplay = clip1Display

        elif self.sender() == self.sidebar.comboBox_10:
            if not self.clip2:
                self.clip2 = pvs.Clip(Input=self.fluidfoam)
            pvs.Hide3DWidgets(proxy=self.clip2.ClipType)
            if self.sender().currentText() == 'X??????':
                # self.clip1.ClipType.Origin = [-13184.847264041935, 0.0, 150000.0]
                self.clip2.ClipType.Normal = [1.0, 0.0, 0.0]
            elif self.sender().currentText() == 'Y??????':
                # self.clip1.ClipType.Origin = [-13184.847264041935, 0.0, 150000.0]
                self.clip2.ClipType.Normal = [0.0, 1.0, 0.0]
            elif self.sender().currentText() == 'Z??????':
                # self.clip1.ClipType.Origin = [-13184.847264041935, 0.0, 150000.0]
                self.clip2.ClipType.Normal = [0.0, 0.0, 1.0]

            pvs.HideAll(self.ren_view1)
            clip2Display = pvs.Show(self.clip2, self.ren_view1)
            clip2Display.Representation = 'Surface'
            self.currentdisplay1 = clip2Display

        self.updateview()

    def updateview(self):
        # if self.sender() == self.sidebar.comboBox:
            # HideUnusedScalarBars ?????????????????????ScalarBars
            pvs.HideUnusedScalarBars(self.ren_view)
            self.currentdisplay.SetScalarBarVisibility(self.ren_view, True)
            self.ren_view.Update()
        # elif self.sender() == self.sidebar.comboBox_3:
            # HideUnusedScalarBars ?????????????????????ScalarBars
            pvs.HideUnusedScalarBars(self.ren_view1)
            self.currentdisplay1.SetScalarBarVisibility(self.ren_view1, True)
            self.ren_view1.Update()

            pvs.Render()

    def renviewchange(self):
        arrayname = self.sidebar.comboBox_5.currentText()
        self.sidebar.comboBox_6.clear()
        if arrayname in ['S','E']:
            directs = ['Magnitude','xx','yy','zz','xy','yz','zx','Mises','Min Principal','Mid Principal','Max Principal',]
        elif arrayname == 'U':
            directs = ['Magnitude','D1','D2','D3']
        else:
            directs = []

        for d in directs:
            self.sidebar.comboBox_6.addItem(d)
        # pvs.ColorBy(self.currentdisplay, ('POINTS', arrayname, 'Mises'))
        pvs.ColorBy(self.currentdisplay, ('POINTS', arrayname))
        self.colorobject[arrayname] = pvs.GetColorTransferFunction(arrayname)
        # pvs.Render()
        self.updateview()


    def apply_params(self):
        """
        Called when the parameters are changed from the parameters
        modification box (and the Apply button clicked)
        """
        rep = self.params.rep
        if rep:
            new_opts = self.params.values()
            self.represent(rep.field, rep.__class__, False, **new_opts)

    def update_infobar(self):
        """
        Method used to update the information bar below the post-processing
        controls based on the shown field (uses self.shown)
        """
        info = 'No data loaded'
        fsuffix = ''
        if self.shown:
            field, opts = self.shown.field, self.shown.opts
            comp = opts['Component'] if 'Component' in opts else ''
            if 'ColorField' in opts:
                cfield = opts['ColorField']
                if cfield != field:
                    fsuffix = ', colored by %s' % (
                        cfield.info['label'].split('(')[0])
                    if len(cfield.info['components']) > 1:
                        fsuffix += ' [%s]' % (comp)

            if not fsuffix:
                if len(field.info['components']) > 1:
                    fsuffix = ' [%s]' % (comp)

            ctime = self.ren_view.ViewTime
            # info = '<B>Concept :</B> %s; '\
            #        '<B>Field :</B> %s%s; '\
            #        '<B>Current time/frequency :</B> %g'\
            #        %(field.concept.name,
            #          field.info['label'], fsuffix, ctime)

            info = '<B><span style="color: #ffffff; background-color: #1d71b8;">'\
                   '&nbsp;Concept&nbsp;</B></span>&nbsp;%s'\
                   '&nbsp;<B><span style="color: #ffffff; background-color: #1d71b8;">'\
                   '&nbsp;Field&nbsp;</B></span>&nbsp;%s%s'\
                   '&nbsp;<B><span style="color: #ffffff; background-color: #1d71b8;">'\
                   '&nbsp;Time/Frequency&nbsp;</B></span>&nbsp;%g'\
                   % (field.concept.name,
                      field.name, fsuffix, ctime)

        if self.infobar_label:
            self.infobar_label.setText(info)

        # if self.mem_bar:
        #     current, available = get_pv_mem_use()
        #     self.mem_bar.setRange(0, int(available / 1024.))
        #     self.mem_bar.setValue(int(current / 1024.))

    def redraw(self):
        """
        Redraws the current field
        """
        pvs.GetActiveView().ResetCamera()
        

    # pragma pylint: disable=invalid-name
    def eventFilter(self, source, event):
        """
        EventFilter for capturing mouse clicks over the ParaView
        widget.
        """
        if not hasattr(self, 'pv_widget_children'):
            return 0

        if source in self.pv_widget_children:
            #????????????paraview??????????????????????????????????????????
            # pass
            if event.type() == QtCore.QEvent.MouseButtonPress:
                # self.on_click_callback()
                if hasattr(event, 'button'):
                    return 1
            elif event.type() == QtCore.QEvent.MouseButtonRelease:
                self.on_click_callback()
                if hasattr(event, 'button'):
                    if event.button() == QtCore.Qt.RightButton:
                        # self.navtree.contextMenuEvent('Representation')
                        pass
                    return 1
            # elif event.type() == Qt.QEvent.MouseButtonDblClick:
            #     pvcontrol(self, 'clear_selection')
            #     return 1

        return QtWidgets.QWidget.eventFilter(self, source, event)

    def on_click_callback(self):
        """
        Callback to launch either a probing or plot operation based
        on the user selection
        """
        if not self.shown:
            return

        if not self.shown.pickable:
            return

        selection, _, _ = get_active_selection(self.shown.source)
        if selection:
            self.probe_plot_callback()
        else:
            QtCore.QTimer.singleShot(100, self.probe_plot_callback)

    def probe_plot_callback(self):
        """
        Delayed probe as to allow selection to be coined
        """
        selection, _, _ = get_active_selection(self.shown.source)
        if selection:
            if self.probing:
                selection_probe(self)
            else:
                selection_plot(self)
                self.probing = True

    def plot(self, data, variable):
        """
        Adds a popup dialog with a plot of the given data
        """
        dialog = QtWidgets.QDialog(self)
        dialog.ui = PlotWindow(data=data, variable=variable)
        dialog.ui.setWindowTitle('AsterStudy - Selection plot over time')
        dialog.ui.show()


def add_button(layout, name='', tooltip='', icon=None,
               callback=None, checkable=False):
    """
    Adds a push button to the given parent widget and layout with some
    user-defined properties
    """
    from . import get_icon
    button = QtWidgets.QPushButton(name)
    button.setFixedWidth(100)
    if tooltip:
        button.setToolTip(tooltip)
    if icon:
        button.setIcon(get_icon(icon))
    button.setCheckable(checkable)
    if checkable:
        button.toggled.connect(callback)
    else:
        button.clicked.connect(callback)

    layout.addWidget(button)
    return button


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    aaa = QMainWindow()
    main = Workspace()
    main.setupUi(aaa)
    aaa.show()
    sys.exit(app.exec_())
