

# Form implementation generated from reading ui file 'pvsidebar.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class SideBar(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(414, 682)
        self.horizontalLayout = QtWidgets.QHBoxLayout(Form)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.tabWidget = QtWidgets.QTabWidget(Form)
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.tab)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.toolBox = QtWidgets.QToolBox(self.tab)
        self.toolBox.setEnabled(True)
        self.toolBox.setMaximumSize(QtCore.QSize(16777215, 825))
        self.toolBox.setAutoFillBackground(False)
        self.toolBox.setObjectName("toolBox")
        self.page = QtWidgets.QWidget()
        self.page.setGeometry(QtCore.QRect(0, 0, 370, 455))
        self.page.setObjectName("page")
        self.formLayout = QtWidgets.QFormLayout(self.page)
        self.formLayout.setObjectName("formLayout")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.groupBox = QtWidgets.QGroupBox(self.page)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.checkBox = QtWidgets.QCheckBox(self.groupBox)
        self.checkBox.setObjectName("checkBox")
        self.gridLayout_5.addWidget(self.checkBox, 2, 0, 1, 1)
        self.comboBox = QtWidgets.QComboBox(self.groupBox)
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.gridLayout_5.addWidget(self.comboBox, 1, 0, 1, 1)
        self.verticalLayout_2.addWidget(self.groupBox)
        self.groupBox_2 = QtWidgets.QGroupBox(self.page)
        self.groupBox_2.setCheckable(True)
        self.groupBox_2.setChecked(False)
        self.groupBox_2.setObjectName("groupBox_2")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.groupBox_2)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.label_4 = QtWidgets.QLabel(self.groupBox_2)
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 1, 0, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.groupBox_2)
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 3, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.groupBox_2)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 2, 0, 1, 1)
        self.lineEdit = QtWidgets.QLineEdit(self.groupBox_2)
        self.lineEdit.setObjectName("lineEdit")
        self.gridLayout.addWidget(self.lineEdit, 2, 1, 1, 1)
        self.comboBox_2 = QtWidgets.QComboBox(self.groupBox_2)
        self.comboBox_2.setObjectName("comboBox_2")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.gridLayout.addWidget(self.comboBox_2, 1, 1, 1, 1)
        self.lineEdit_2 = QtWidgets.QLineEdit(self.groupBox_2)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.gridLayout.addWidget(self.lineEdit_2, 3, 1, 1, 1)
        self.gridLayout_3.addLayout(self.gridLayout, 0, 0, 1, 1)
        self.verticalLayout_2.addWidget(self.groupBox_2)
        self.formLayout.setLayout(0, QtWidgets.QFormLayout.SpanningRole, self.verticalLayout_2)
        self.groupBox_5 = QtWidgets.QGroupBox(self.page)
        self.groupBox_5.setCheckable(True)
        self.groupBox_5.setChecked(False)
        self.groupBox_5.setObjectName("groupBox_5")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.groupBox_5)
        self.verticalLayout.setObjectName("verticalLayout")
        self.comboBox_9 = QtWidgets.QComboBox(self.groupBox_5)
        self.comboBox_9.setObjectName("comboBox_9")
        self.comboBox_9.addItem("")
        self.comboBox_9.addItem("")
        self.comboBox_9.addItem("")
        self.verticalLayout.addWidget(self.comboBox_9)
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.SpanningRole, self.groupBox_5)
        self.toolBox.addItem(self.page, "")
        self.page_2 = QtWidgets.QWidget()
        self.page_2.setGeometry(QtCore.QRect(0, 0, 370, 455))
        self.page_2.setObjectName("page_2")
        self.toolBox.addItem(self.page_2, "")
        self.gridLayout_2.addWidget(self.toolBox, 3, 0, 1, 1)
        self.pushButton = QtWidgets.QPushButton(self.tab)
        self.pushButton.setObjectName("pushButton")
        self.gridLayout_2.addWidget(self.pushButton, 4, 0, 1, 1)
        self.pushButton_3 = QtWidgets.QPushButton(self.tab)
        self.pushButton_3.setObjectName("pushButton_3")
        self.gridLayout_2.addWidget(self.pushButton_3, 5, 0, 1, 1)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.comboBox_5 = QtWidgets.QComboBox(self.tab)
        self.comboBox_5.setObjectName("comboBox_5")
        self.horizontalLayout_3.addWidget(self.comboBox_5)
        self.comboBox_6 = QtWidgets.QComboBox(self.tab)
        self.comboBox_6.setObjectName("comboBox_6")
        self.horizontalLayout_3.addWidget(self.comboBox_6)
        self.gridLayout_2.addLayout(self.horizontalLayout_3, 1, 0, 1, 1)
        self.groupbox = QtWidgets.QGroupBox(self.tab)
        self.groupbox.setFlat(True)
        self.groupbox.setCheckable(False)
        self.groupbox.setObjectName("groupbox")
        self.gridLayout_2.addWidget(self.groupbox, 0, 0, 1, 1)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.gridLayout_2.addLayout(self.horizontalLayout_2, 2, 0, 1, 1)
        self.verticalLayout_5.addLayout(self.gridLayout_2)
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.tab_2)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.groupbox_2 = QtWidgets.QGroupBox(self.tab_2)
        self.groupbox_2.setFlat(True)
        self.groupbox_2.setCheckable(False)
        self.groupbox_2.setObjectName("groupbox_2")
        self.verticalLayout_3.addWidget(self.groupbox_2)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.comboBox_7 = QtWidgets.QComboBox(self.tab_2)
        self.comboBox_7.setObjectName("comboBox_7")
        self.horizontalLayout_4.addWidget(self.comboBox_7)
        self.comboBox_8 = QtWidgets.QComboBox(self.tab_2)
        self.comboBox_8.setObjectName("comboBox_8")
        self.horizontalLayout_4.addWidget(self.comboBox_8)
        self.verticalLayout_3.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.verticalLayout_3.addLayout(self.horizontalLayout_5)
        self.toolBox_2 = QtWidgets.QToolBox(self.tab_2)
        self.toolBox_2.setEnabled(True)
        self.toolBox_2.setMaximumSize(QtCore.QSize(16777215, 825))
        self.toolBox_2.setAutoFillBackground(False)
        self.toolBox_2.setObjectName("toolBox_2")
        self.page_3 = QtWidgets.QWidget()
        self.page_3.setGeometry(QtCore.QRect(0, 0, 370, 455))
        self.page_3.setObjectName("page_3")
        self.formLayout_2 = QtWidgets.QFormLayout(self.page_3)
        self.formLayout_2.setObjectName("formLayout_2")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.groupBox_3 = QtWidgets.QGroupBox(self.page_3)
        self.groupBox_3.setObjectName("groupBox_3")
        self.gridLayout_6 = QtWidgets.QGridLayout(self.groupBox_3)
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.comboBox_3 = QtWidgets.QComboBox(self.groupBox_3)
        self.comboBox_3.setObjectName("comboBox_3")
        self.comboBox_3.addItem("")
        self.comboBox_3.addItem("")
        self.comboBox_3.addItem("")
        self.comboBox_3.addItem("")
        self.gridLayout_6.addWidget(self.comboBox_3, 0, 0, 1, 1)
        self.checkBox_2 = QtWidgets.QCheckBox(self.groupBox_3)
        self.checkBox_2.setObjectName("checkBox_2")
        self.gridLayout_6.addWidget(self.checkBox_2, 1, 0, 1, 1)
        self.verticalLayout_4.addWidget(self.groupBox_3)
        self.groupBox_4 = QtWidgets.QGroupBox(self.page_3)
        self.groupBox_4.setCheckable(True)
        self.groupBox_4.setChecked(False)
        self.groupBox_4.setObjectName("groupBox_4")
        self.gridLayout_7 = QtWidgets.QGridLayout(self.groupBox_4)
        self.gridLayout_7.setObjectName("gridLayout_7")
        self.gridLayout_8 = QtWidgets.QGridLayout()
        self.gridLayout_8.setObjectName("gridLayout_8")
        self.label_5 = QtWidgets.QLabel(self.groupBox_4)
        self.label_5.setAlignment(QtCore.Qt.AlignCenter)
        self.label_5.setObjectName("label_5")
        self.gridLayout_8.addWidget(self.label_5, 1, 0, 1, 1)
        self.label_6 = QtWidgets.QLabel(self.groupBox_4)
        self.label_6.setAlignment(QtCore.Qt.AlignCenter)
        self.label_6.setObjectName("label_6")
        self.gridLayout_8.addWidget(self.label_6, 3, 0, 1, 1)
        self.label_7 = QtWidgets.QLabel(self.groupBox_4)
        self.label_7.setAlignment(QtCore.Qt.AlignCenter)
        self.label_7.setObjectName("label_7")
        self.gridLayout_8.addWidget(self.label_7, 2, 0, 1, 1)
        self.lineEdit_3 = QtWidgets.QLineEdit(self.groupBox_4)
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.gridLayout_8.addWidget(self.lineEdit_3, 2, 1, 1, 1)
        self.comboBox_4 = QtWidgets.QComboBox(self.groupBox_4)
        self.comboBox_4.setObjectName("comboBox_4")
        self.comboBox_4.addItem("")
        self.comboBox_4.addItem("")
        self.comboBox_4.addItem("")
        self.comboBox_4.addItem("")
        self.comboBox_4.addItem("")
        self.comboBox_4.addItem("")
        self.gridLayout_8.addWidget(self.comboBox_4, 1, 1, 1, 1)
        self.lineEdit_4 = QtWidgets.QLineEdit(self.groupBox_4)
        self.lineEdit_4.setObjectName("lineEdit_4")
        self.gridLayout_8.addWidget(self.lineEdit_4, 3, 1, 1, 1)
        self.gridLayout_7.addLayout(self.gridLayout_8, 0, 0, 1, 1)
        self.verticalLayout_4.addWidget(self.groupBox_4)
        self.formLayout_2.setLayout(0, QtWidgets.QFormLayout.SpanningRole, self.verticalLayout_4)
        self.groupBox_6 = QtWidgets.QGroupBox(self.page_3)
        self.groupBox_6.setCheckable(True)
        self.groupBox_6.setChecked(False)
        self.groupBox_6.setObjectName("groupBox_6")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.groupBox_6)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.comboBox_10 = QtWidgets.QComboBox(self.groupBox_6)
        self.comboBox_10.setObjectName("comboBox_10")
        self.comboBox_10.addItem("")
        self.comboBox_10.addItem("")
        self.comboBox_10.addItem("")
        self.verticalLayout_7.addWidget(self.comboBox_10)
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.SpanningRole, self.groupBox_6)
        self.toolBox_2.addItem(self.page_3, "")
        self.page_4 = QtWidgets.QWidget()
        self.page_4.setGeometry(QtCore.QRect(0, 0, 100, 30))
        self.page_4.setObjectName("page_4")
        self.toolBox_2.addItem(self.page_4, "")
        self.verticalLayout_3.addWidget(self.toolBox_2)
        self.pushButton_2 = QtWidgets.QPushButton(self.tab_2)
        self.pushButton_2.setObjectName("pushButton_2")
        self.verticalLayout_3.addWidget(self.pushButton_2)
        self.pushButton_4 = QtWidgets.QPushButton(self.tab_2)
        self.pushButton_4.setObjectName("pushButton_4")
        self.verticalLayout_3.addWidget(self.pushButton_4)
        self.verticalLayout_6.addLayout(self.verticalLayout_3)
        self.tabWidget.addTab(self.tab_2, "")
        self.horizontalLayout.addWidget(self.tabWidget)

        self.retranslateUi(Form)
        self.tabWidget.setCurrentIndex(1)
        self.toolBox.setCurrentIndex(0)
        self.toolBox_2.setCurrentIndex(0)
        self.groupBox_4.clicked.connect(self.label_4.clear)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.groupBox.setTitle(_translate("Form", "??????????????????"))
        self.checkBox.setText(_translate("Form", "??????????????????"))
        self.comboBox.setItemText(0, _translate("Form", "??????"))
        self.comboBox.setItemText(1, _translate("Form", "??????"))
        self.comboBox.setItemText(2, _translate("Form", "??????"))
        self.comboBox.setItemText(3, _translate("Form", "Jet"))
        self.groupBox_2.setTitle(_translate("Form", "???????????????????????????"))
        self.label_4.setText(_translate("Form", "??????"))
        self.label_3.setText(_translate("Form", "?????????"))
        self.label_2.setText(_translate("Form", "?????????"))
        self.comboBox_2.setItemText(0, _translate("Form", "???"))
        self.comboBox_2.setItemText(1, _translate("Form", "???"))
        self.comboBox_2.setItemText(2, _translate("Form", "?????????"))
        self.comboBox_2.setItemText(3, _translate("Form", "??????"))
        self.comboBox_2.setItemText(4, _translate("Form", "??????"))
        self.comboBox_2.setItemText(5, _translate("Form", "???????????????"))
        self.groupBox_5.setTitle(_translate("Form", "??????"))
        self.comboBox_9.setItemText(0, _translate("Form", "X??????"))
        self.comboBox_9.setItemText(1, _translate("Form", "Y??????"))
        self.comboBox_9.setItemText(2, _translate("Form", "Z??????"))
        self.toolBox.setItemText(self.toolBox.indexOf(self.page), _translate("Form", "????????????"))
        self.toolBox.setItemText(self.toolBox.indexOf(self.page_2), _translate("Form", "????????????"))
        self.pushButton.setText(_translate("Form", "??????"))
        self.pushButton_3.setText(_translate("Form", "?????????????????????"))
        self.groupbox.setTitle(_translate("Form", "??????"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("Form", "??????1"))
        self.groupbox_2.setTitle(_translate("Form", "??????"))
        self.groupBox_3.setTitle(_translate("Form", "??????????????????"))
        self.comboBox_3.setItemText(0, _translate("Form", "??????"))
        self.comboBox_3.setItemText(1, _translate("Form", "??????"))
        self.comboBox_3.setItemText(2, _translate("Form", "??????"))
        self.comboBox_3.setItemText(3, _translate("Form", "Jet"))
        self.checkBox_2.setText(_translate("Form", "??????????????????"))
        self.groupBox_4.setTitle(_translate("Form", "???????????????????????????"))
        self.label_5.setText(_translate("Form", "??????"))
        self.label_6.setText(_translate("Form", "?????????"))
        self.label_7.setText(_translate("Form", "?????????"))
        self.comboBox_4.setItemText(0, _translate("Form", "???"))
        self.comboBox_4.setItemText(1, _translate("Form", "???"))
        self.comboBox_4.setItemText(2, _translate("Form", "?????????"))
        self.comboBox_4.setItemText(3, _translate("Form", "??????"))
        self.comboBox_4.setItemText(4, _translate("Form", "??????"))
        self.comboBox_4.setItemText(5, _translate("Form", "???????????????"))
        self.groupBox_6.setTitle(_translate("Form", "??????"))
        self.comboBox_10.setItemText(0, _translate("Form", "X??????"))
        self.comboBox_10.setItemText(1, _translate("Form", "Y??????"))
        self.comboBox_10.setItemText(2, _translate("Form", "Z??????"))
        self.toolBox_2.setItemText(self.toolBox_2.indexOf(self.page_3), _translate("Form", "????????????"))
        self.toolBox_2.setItemText(self.toolBox_2.indexOf(self.page_4), _translate("Form", "????????????"))
        self.pushButton_2.setText(_translate("Form", "??????"))
        self.pushButton_4.setText(_translate("Form", "?????????????????????"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("Form", "??????2"))