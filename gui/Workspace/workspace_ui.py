# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'H:\NSCC\UI\workspace\workspace.ui'
#
# Created by: PyQt5 UI code generator 5.15.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import sys

class Ui_Workspace(QWidget):
    def __init__(self, parent=None):
        super(Ui_Workspace,self).__init__()
        self.setupUi
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(235, 826)
        self.horizontalLayout = QtWidgets.QHBoxLayout(Form)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.tabWidget = QtWidgets.QTabWidget(Form)
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.tab)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        # self.splitter_2 = QtWidgets.QSplitter(self.tab)
        # sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        # sizePolicy.setHorizontalStretch(0)
        # sizePolicy.setVerticalStretch(0)
        # sizePolicy.setHeightForWidth(self.splitter_2.sizePolicy().hasHeightForWidth())
        # self.splitter_2.setSizePolicy(sizePolicy)
        # self.splitter_2.setOrientation(QtCore.Qt.Horizontal)
        # self.splitter_2.setObjectName("splitter_2")
        self.lwidget = QtWidgets.QWidget(self.tab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lwidget.sizePolicy().hasHeightForWidth())
        self.lwidget.setSizePolicy(sizePolicy)
        self.lwidget.setObjectName("lwidget")
        # self.dockWidgetContents = QtWidgets.QWidget()
        # self.dockWidgetContents.setObjectName("dockWidgetContents")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.lwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.groupBox_6 = QtWidgets.QGroupBox(self.lwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.groupBox_6.sizePolicy().hasHeightForWidth())
        self.groupBox_6.setSizePolicy(sizePolicy)
        self.groupBox_6.setObjectName("groupBox_6")
        #self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.groupBox_6)
        #self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.f_layout = QFormLayout(self.groupBox_6)
        # Button
        self.width_label = QtWidgets.QLabel('宽度:',self.groupBox_6)
        self.length_label = QtWidgets.QLabel('长度:',self.groupBox_6)
        self.height_label = QtWidgets.QLabel('高度:',self.groupBox_6)
        self.sections_label = QtWidgets.QLabel('桁架节点数:',self.groupBox_6)
        self.spacing_label = QtWidgets.QLabel('间距:',self.groupBox_6)
        #self.label.setObjectName("label")
        #self.verticalLayout_7.addWidget(self.label)
        self.width_lineEdit = QtWidgets.QLineEdit('7',self.groupBox_6)
        self.length_lineEdit = QtWidgets.QLineEdit('40',self.groupBox_6)
        self.height_lineEdit = QtWidgets.QLineEdit('5',self.groupBox_6)
        self.sections_lineEdit = QtWidgets.QLineEdit('8',self.groupBox_6)
        self.spacing_lineEdit = QtWidgets.QLineEdit('5',self.groupBox_6)

        self.spacing_lineEdit.setEnabled(False)
        #self.width = int(self.width_lineEdit.text())
        #print(self.width)


        self.pushButton_ok = QtWidgets.QPushButton('确认',self.groupBox_6)
        self.pushButton_reset = QtWidgets.QPushButton('还原',self.groupBox_6)
        self.f_layout.addRow(self.width_label, self.width_lineEdit)
        self.f_layout.addRow(self.length_label, self.length_lineEdit)
        self.f_layout.addRow(self.height_label, self.height_lineEdit)
        self.f_layout.addRow(self.sections_label, self.sections_lineEdit)
        self.f_layout.addRow(self.spacing_label, self.spacing_lineEdit)
        self.f_layout.addRow(self.pushButton_ok, self.pushButton_reset)
        #self.lineEdit.setObjectName("lineEdit")
        #self.verticalLayout_7.addWidget(self.lineEdit)
        #self.pushButton_15 = QtWidgets.QPushButton(self.groupBox_6)
        #icon = QtGui.QIcon()
        #icon.addPixmap(QtGui.QPixmap("/usr/sw-cluster/simforge/PFsalome/SALOME-9.4.0-CO7-SRC/BINARIES-CO7/ASTERSTUDY/lib/python3.6/site-packages/asterstudy/gui/Workspace/创建.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        #self.pushButton_15.setIcon(icon)
        #self.pushButton_15.setObjectName("pushButton_15")
        #self.verticalLayout_7.addWidget(self.pushButton_15)
        #self.pushButton_16 = QtWidgets.QPushButton(self.groupBox_6)
        #icon1 = QtGui.QIcon()
        #icon1.addPixmap(QtGui.QPixmap("/usr/sw-cluster/simforge/PFsalome/SALOME-9.4.0-CO7-SRC/BINARIES-CO7/ASTERSTUDY/lib/python3.6/site-packages/asterstudy/gui/Workspace/打开.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        #self.pushButton_16.setIcon(icon1)
        #self.pushButton_16.setObjectName("pushButton_16")
        #self.verticalLayout_7.addWidget(self.pushButton_16)
        self.verticalLayout.addWidget(self.groupBox_6)
        self.groupBox = QtWidgets.QGroupBox(self.lwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(3)
        sizePolicy.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.pushButton = QtWidgets.QPushButton(self.groupBox)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("/usr/sw-cluster/simforge/PFsalome/SALOME-9.4.0-CO7-SRC/BINARIES-CO7/ASTERSTUDY/lib/python3.6/site-packages/asterstudy/gui/Workspace/转化.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton.setIcon(icon2)
        self.pushButton.setObjectName("pushButton")
        self.verticalLayout_2.addWidget(self.pushButton)
        self.pushButton_2 = QtWidgets.QPushButton(self.groupBox)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("/usr/sw-cluster/simforge/PFsalome/SALOME-9.4.0-CO7-SRC/BINARIES-CO7/ASTERSTUDY/lib/python3.6/site-packages/asterstudy/gui/Workspace/导入.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_2.setIcon(icon3)
        self.pushButton_2.setObjectName("pushButton_2")
        self.verticalLayout_2.addWidget(self.pushButton_2)
        self.pushButton_3 = QtWidgets.QPushButton(self.groupBox)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap("/usr/sw-cluster/simforge/PFsalome/SALOME-9.4.0-CO7-SRC/BINARIES-CO7/ASTERSTUDY/lib/python3.6/site-packages/asterstudy/gui/Workspace/生成.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_3.setIcon(icon4)
        self.pushButton_3.setObjectName("pushButton_3")
        self.verticalLayout_2.addWidget(self.pushButton_3)
        self.verticalLayout.addWidget(self.groupBox)
        self.groupBox_2 = QtWidgets.QGroupBox(self.lwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(5)
        sizePolicy.setHeightForWidth(self.groupBox_2.sizePolicy().hasHeightForWidth())
        self.groupBox_2.setSizePolicy(sizePolicy)
        self.groupBox_2.setObjectName("groupBox_2")
        self.verticalLayout_8 = QtWidgets.QVBoxLayout(self.groupBox_2)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.scrollArea = QtWidgets.QScrollArea(self.groupBox_2)
        self.scrollArea.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 155, 277))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.verticalLayout_9 = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_9.setObjectName("verticalLayout_9")

        #增加展示方式下拉框
        self.represent_combo = QtWidgets.QComboBox()
        self.represent_combo.addItem('3D Glyphs')
        self.represent_combo.addItem('Feature Edges')
        self.represent_combo.addItem('Outline')
        self.represent_combo.addItem('Point Gaussian')
        self.represent_combo.addItem('Points')
        self.represent_combo.addItem('Surface')
        self.represent_combo.addItem('Surface With Edges')
        self.represent_combo.addItem('Volume')
        self.represent_combo.addItem('Wireframe')
        self.verticalLayout_9.addWidget(self.represent_combo)


        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setObjectName("formLayout")
        self.verticalLayout_9.addLayout(self.formLayout)
        self.verticalLayout_9.addStretch()
        #增加应用按钮
        self.apply = QtWidgets.QPushButton()
        self.apply.setText('应用')
        self.verticalLayout_9.addWidget(self.apply)
        
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout_8.addWidget(self.scrollArea)
        self.verticalLayout.addWidget(self.groupBox_2)
        self.groupBox_3 = QtWidgets.QGroupBox(self.lwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.groupBox_3.sizePolicy().hasHeightForWidth())
        self.groupBox_3.setSizePolicy(sizePolicy)
        self.groupBox_3.setObjectName("groupBox_3")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.groupBox_3)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.pushButton_4 = QtWidgets.QPushButton(self.groupBox_3)
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap("/usr/sw-cluster/simforge/PFsalome/SALOME-9.4.0-CO7-SRC/BINARIES-CO7/ASTERSTUDY/lib/python3.6/site-packages/asterstudy/gui/Workspace/检查 (1).png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_4.setIcon(icon5)
        self.pushButton_4.setObjectName("pushButton_4")
        self.verticalLayout_3.addWidget(self.pushButton_4)
        self.verticalLayout.addWidget(self.groupBox_3)
        # self.lwidget.setWidget(self.dockWidgetContents)
        # self.splitter = QtWidgets.QSplitter(self.splitter_2)
        # sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        # sizePolicy.setHorizontalStretch(8)
        # sizePolicy.setVerticalStretch(0)
        # sizePolicy.setHeightForWidth(self.splitter.sizePolicy().hasHeightForWidth())
        # self.splitter.setSizePolicy(sizePolicy)
        # self.splitter.setOrientation(QtCore.Qt.Vertical)
        # self.splitter.setObjectName("splitter")
        # self.openGLWidget = QtWidgets.QOpenGLWidget(self.splitter)
        # sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        # sizePolicy.setHorizontalStretch(0)
        # sizePolicy.setVerticalStretch(4)
        # sizePolicy.setHeightForWidth(self.openGLWidget.sizePolicy().hasHeightForWidth())
        # self.openGLWidget.setSizePolicy(sizePolicy)
        # self.openGLWidget.setObjectName("openGLWidget")
        # self.dockWidget_2 = QtWidgets.QDockWidget(self.splitter)
        # sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        # sizePolicy.setHorizontalStretch(0)
        # sizePolicy.setVerticalStretch(1)
        # sizePolicy.setHeightForWidth(self.dockWidget_2.sizePolicy().hasHeightForWidth())
        # self.dockWidget_2.setSizePolicy(sizePolicy)
        # self.dockWidget_2.setObjectName("dockWidget_2")
        # self.dockWidgetContents_2 = QtWidgets.QWidget()
        # self.dockWidgetContents_2.setObjectName("dockWidgetContents_2")
        # self.dockWidget_2.setWidget(self.dockWidgetContents_2)
        self.horizontalLayout_2.addWidget(self.lwidget)
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap("/usr/sw-cluster/simforge/PFsalome/SALOME-9.4.0-CO7-SRC/BINARIES-CO7/ASTERSTUDY/lib/python3.6/site-packages/asterstudy/gui/Workspace/执行.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.tabWidget.addTab(self.tab, icon6, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout(self.tab_2)
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        # self.splitter_4 = QtWidgets.QSplitter(self.tab_2)
        # self.splitter_4.setOrientation(QtCore.Qt.Horizontal)
        # self.splitter_4.setObjectName("splitter_4")
        self.lwidget_2 = QtWidgets.QWidget(self.tab_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lwidget_2.sizePolicy().hasHeightForWidth())
        self.lwidget_2.setSizePolicy(sizePolicy)
        self.lwidget_2.setObjectName("lwidget_2")
        # self.dockWidgetContents_3 = QtWidgets.QWidget()
        # self.dockWidgetContents_3.setObjectName("dockWidgetContents_3")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.lwidget_2)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.groupBox_4 = QtWidgets.QGroupBox(self.lwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(2)
        sizePolicy.setHeightForWidth(self.groupBox_4.sizePolicy().hasHeightForWidth())
        self.groupBox_4.setSizePolicy(sizePolicy)
        self.groupBox_4.setObjectName("groupBox_4")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.groupBox_4)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.pushButton_5 = QtWidgets.QPushButton(self.groupBox_4)
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap("/usr/sw-cluster/simforge/PFsalome/SALOME-9.4.0-CO7-SRC/BINARIES-CO7/ASTERSTUDY/lib/python3.6/site-packages/asterstudy/gui/Workspace/材料 (1).png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_5.setIcon(icon7)
        self.pushButton_5.setObjectName("pushButton_5")
        self.verticalLayout_5.addWidget(self.pushButton_5)
        self.pushButton_6 = QtWidgets.QPushButton(self.groupBox_4)
        icon8 = QtGui.QIcon()
        icon8.addPixmap(QtGui.QPixmap("/usr/sw-cluster/simforge/PFsalome/SALOME-9.4.0-CO7-SRC/BINARIES-CO7/ASTERSTUDY/lib/python3.6/site-packages/asterstudy/gui/Workspace/模型 (1).png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_6.setIcon(icon8)
        self.pushButton_6.setObjectName("pushButton_6")
        self.verticalLayout_5.addWidget(self.pushButton_6)
        self.pushButton_7 = QtWidgets.QPushButton(self.groupBox_4)
        icon9 = QtGui.QIcon()
        icon9.addPixmap(QtGui.QPixmap("/usr/sw-cluster/simforge/PFsalome/SALOME-9.4.0-CO7-SRC/BINARIES-CO7/ASTERSTUDY/lib/python3.6/site-packages/asterstudy/gui/Workspace/边界条件.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_7.setIcon(icon9)
        self.pushButton_7.setObjectName("pushButton_7")
        self.verticalLayout_5.addWidget(self.pushButton_7)
        self.pushButton_8 = QtWidgets.QPushButton(self.groupBox_4)
        icon10 = QtGui.QIcon()
        icon10.addPixmap(QtGui.QPixmap("/usr/sw-cluster/simforge/PFsalome/SALOME-9.4.0-CO7-SRC/BINARIES-CO7/ASTERSTUDY/lib/python3.6/site-packages/asterstudy/gui/Workspace/物理.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_8.setIcon(icon10)
        self.pushButton_8.setObjectName("pushButton_8")
        self.verticalLayout_5.addWidget(self.pushButton_8)
        self.pushButton_9 = QtWidgets.QPushButton(self.groupBox_4)
        icon11 = QtGui.QIcon()
        icon11.addPixmap(QtGui.QPixmap("/usr/sw-cluster/simforge/PFsalome/SALOME-9.4.0-CO7-SRC/BINARIES-CO7/ASTERSTUDY/lib/python3.6/site-packages/asterstudy/gui/Workspace/方案.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_9.setIcon(icon11)
        self.pushButton_9.setObjectName("pushButton_9")
        self.verticalLayout_5.addWidget(self.pushButton_9)
        self.pushButton_10 = QtWidgets.QPushButton(self.groupBox_4)
        icon12 = QtGui.QIcon()
        icon12.addPixmap(QtGui.QPixmap("/usr/sw-cluster/simforge/PFsalome/SALOME-9.4.0-CO7-SRC/BINARIES-CO7/ASTERSTUDY/lib/python3.6/site-packages/asterstudy/gui/Workspace/计算器.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_10.setIcon(icon12)
        self.pushButton_10.setObjectName("pushButton_10")
        self.verticalLayout_5.addWidget(self.pushButton_10)
        self.pushButton_14 = QtWidgets.QPushButton(self.groupBox_4)
        icon13 = QtGui.QIcon()
        icon13.addPixmap(QtGui.QPixmap("/usr/sw-cluster/simforge/PFsalome/SALOME-9.4.0-CO7-SRC/BINARIES-CO7/ASTERSTUDY/lib/python3.6/site-packages/asterstudy/gui/Workspace/控制.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_14.setIcon(icon13)
        self.pushButton_14.setObjectName("pushButton_14")
        self.verticalLayout_5.addWidget(self.pushButton_14)
        self.verticalLayout_4.addWidget(self.groupBox_4)
        self.groupBox_5 = QtWidgets.QGroupBox(self.lwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.groupBox_5.sizePolicy().hasHeightForWidth())
        self.groupBox_5.setSizePolicy(sizePolicy)
        self.groupBox_5.setObjectName("groupBox_5")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.groupBox_5)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.pushButton_11 = QtWidgets.QPushButton(self.groupBox_5)
        icon14 = QtGui.QIcon()
        icon14.addPixmap(QtGui.QPixmap("/usr/sw-cluster/simforge/PFsalome/SALOME-9.4.0-CO7-SRC/BINARIES-CO7/ASTERSTUDY/lib/python3.6/site-packages/asterstudy/gui/Workspace/开始.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_11.setIcon(icon14)
        self.pushButton_11.setObjectName("pushButton_11")
        self.verticalLayout_6.addWidget(self.pushButton_11)
        self.pushButton_12 = QtWidgets.QPushButton(self.groupBox_5)
        icon15 = QtGui.QIcon()
        icon15.addPixmap(QtGui.QPixmap("/usr/sw-cluster/simforge/PFsalome/SALOME-9.4.0-CO7-SRC/BINARIES-CO7/ASTERSTUDY/lib/python3.6/site-packages/asterstudy/gui/Workspace/终止.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_12.setIcon(icon15)
        self.pushButton_12.setObjectName("pushButton_12")
        self.verticalLayout_6.addWidget(self.pushButton_12)
        self.pushButton_13 = QtWidgets.QPushButton(self.groupBox_5)
        icon16 = QtGui.QIcon()
        icon16.addPixmap(QtGui.QPixmap("/usr/sw-cluster/simforge/PFsalome/SALOME-9.4.0-CO7-SRC/BINARIES-CO7/ASTERSTUDY/lib/python3.6/site-packages/asterstudy/gui/Workspace/继续.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_13.setIcon(icon16)
        self.pushButton_13.setObjectName("pushButton_13")
        self.verticalLayout_6.addWidget(self.pushButton_13)
        self.verticalLayout_4.addWidget(self.groupBox_5)
        # self.lwidget_2.setWidget(self.dockWidgetContents_3)
        # self.splitter_3 = QtWidgets.QSplitter(self.splitter_4)
        # sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        # sizePolicy.setHorizontalStretch(7)
        # sizePolicy.setVerticalStretch(0)
        # sizePolicy.setHeightForWidth(self.splitter_3.sizePolicy().hasHeightForWidth())
        # self.splitter_3.setSizePolicy(sizePolicy)
        # self.splitter_3.setOrientation(QtCore.Qt.Vertical)
        # self.splitter_3.setObjectName("splitter_3")
        # self.openGLWidget_2 = QtWidgets.QOpenGLWidget(self.splitter_3)
        # sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        # sizePolicy.setHorizontalStretch(0)
        # sizePolicy.setVerticalStretch(5)
        # sizePolicy.setHeightForWidth(self.openGLWidget_2.sizePolicy().hasHeightForWidth())
        # self.openGLWidget_2.setSizePolicy(sizePolicy)
        # self.openGLWidget_2.setObjectName("openGLWidget_2")
        # self.dockWidget_4 = QtWidgets.QDockWidget(self.splitter_3)
        # sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        # sizePolicy.setHorizontalStretch(0)
        # sizePolicy.setVerticalStretch(2)
        # sizePolicy.setHeightForWidth(self.dockWidget_4.sizePolicy().hasHeightForWidth())
        # self.dockWidget_4.setSizePolicy(sizePolicy)
        # self.dockWidget_4.setObjectName("dockWidget_4")
        # self.dockWidgetContents_4 = QtWidgets.QWidget()
        # self.dockWidgetContents_4.setObjectName("dockWidgetContents_4")
        # self.dockWidget_4.setWidget(self.dockWidgetContents_4)
        self.verticalLayout_10.addWidget(self.lwidget_2)
        icon17 = QtGui.QIcon()
        icon17.addPixmap(QtGui.QPixmap("/usr/sw-cluster/simforge/PFsalome/SALOME-9.4.0-CO7-SRC/BINARIES-CO7/ASTERSTUDY/lib/python3.6/site-packages/asterstudy/gui/Workspace/计算机 算数.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.tabWidget.addTab(self.tab_2, icon17, "")
        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.tab_3)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.frame = QtWidgets.QFrame(self.tab_3)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.horizontalLayout_4.addWidget(self.frame)
        icon18 = QtGui.QIcon()
        icon18.addPixmap(QtGui.QPixmap("/usr/sw-cluster/simforge/PFsalome/SALOME-9.4.0-CO7-SRC/BINARIES-CO7/ASTERSTUDY/lib/python3.6/site-packages/asterstudy/gui/Workspace/执行反馈.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.tabWidget.addTab(self.tab_3, icon18, "")
        self.horizontalLayout.addWidget(self.tabWidget)
        self.retranslateUi(Form)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.groupBox_6.setTitle(_translate("Form", "总体设计"))
        #self.label.setText(_translate("Form", "宽度："))
        #self.pushButton_15.setText(_translate("Form", "创建工程"))
        #self.pushButton_16.setText(_translate("Form", "打开工程"))
        self.groupBox.setTitle(_translate("Form", "网格生成"))
        self.pushButton.setText(_translate("Form", "Salome 网格转化 "))
        self.pushButton_2.setText(_translate("Form", "OpenFoam导入网格"))
        self.pushButton_3.setText(_translate("Form", "OpenFoam生成网格"))
        self.groupBox_2.setTitle(_translate("Form", "网格显示"))
        self.groupBox_3.setTitle(_translate("Form", "网格评估"))
        self.pushButton_4.setText(_translate("Form", "网格检查"))
        # self.dockWidget_2.setWindowTitle(_translate("Form", "Log"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("Form", "前处理"))
        self.groupBox_4.setTitle(_translate("Form", "参数设置"))
        self.pushButton_5.setText(_translate("Form", "材料设置"))
        self.pushButton_6.setText(_translate("Form", "模型选择"))
        self.pushButton_7.setText(_translate("Form", "边界条件"))
        self.pushButton_8.setText(_translate("Form", "场设置"))
        self.pushButton_9.setText(_translate("Form", "离散方案"))
        self.pushButton_10.setText(_translate("Form", "求解器设置"))
        self.pushButton_14.setText(_translate("Form", "计算控制"))
        self.groupBox_5.setTitle(_translate("Form", "计算"))
        self.pushButton_11.setText(_translate("Form", "开始"))
        self.pushButton_12.setText(_translate("Form", "中止"))
        self.pushButton_13.setText(_translate("Form", "续算"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("Form", "计算"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), _translate("Form", "后处理"))

if __name__ == '__main__':  
    app = QApplication(sys.argv) 
    MainDialog = QDialog() 
    myDialog = Ui_Workspace()
    myDialog.setupUi(MainDialog)
    MainDialog.show()
    sys.exit(app.exec_()) 
