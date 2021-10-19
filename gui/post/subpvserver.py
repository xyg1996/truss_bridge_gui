# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'subpvserver.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Subpvserver(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        # Form.resize(341, 84)
        self.comboBox = QtWidgets.QComboBox(Form)
        self.comboBox.setGeometry(QtCore.QRect(40, 40, 69, 22))
        self.comboBox.setEditable(True)
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(140, 40, 151, 23))
        self.pushButton.setObjectName("pushButton")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.comboBox.setItemText(0, _translate("Form", "12"))
        self.comboBox.setItemText(1, _translate("Form", "24"))
        self.comboBox.setItemText(2, _translate("Form", "48"))
        self.pushButton.setText(_translate("Form", "提交并行后处理作业"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())

