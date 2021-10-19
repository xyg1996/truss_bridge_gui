import os
import time
import _thread
from PyQt5 import QtWidgets
from ResidualplotUi import Ui_Residual_plot
from PyQt5.QtWidgets import QWidget,QApplication,QFrame,QGridLayout,QLabel,QPushButton,QVBoxLayout
class dialog(QWidget):
    def __init__(self):
        super(dialog, self).__init__()
        self.lay =QtWidgets.QVBoxLayout(self)
        self.frame =QtWidgets.QFrame(self)
        self.lay.addWidget(self.frame)
        self.residual_plot = Ui_Residual_plot()
        self.residual_plot.setupUi(self.frame) 
        self.pushButton = QtWidgets.QPushButton(self)
        self.pushButton.setText('start')
        self.lay.addWidget(self.pushButton)
        self.pushButton.clicked.connect(self.start_plotting)
    def start_plotting(self):
        try:
            _thread.start_new_thread(self.plotting, ("Thread-1", 2, ))
        except:
            print ("Error: 无法启动线程")   
    def plotting(self,threadName, delay):
        os.chdir('/usr/sw-cluster/simforge/PFsalome/SALOME-9.4.0-CO7-SRC/BINARIES-CO7/ASTERSTUDY/lib/python3.6/site-packages/asterstudy/workingdirectory')
        command1 = "cat log.pimpleFoam | grep 'Solving for Ux' | cut -d' ' -f9 | tr -d ','"
        command2 = "cat log.pimpleFoam | grep 'Solving for Uy' | cut -d' ' -f9 | tr -d ','"

        while True:
            try:
                # sleep for the remaining seconds of interval
                time_remaining = delay-time.time()%delay
                time.sleep(time_remaining)
                # execute the command
                content1 = os.popen(command1)
                Ux=content1.read().strip().split('\n')
                content1.close()
                content2 = os.popen(command2)
                Uy=content2.read().strip().split('\n')
                content2.close()
                Ux = list(map(float, Ux))[-100:]
                Uy = list(map(float, Uy))[-100:]
                self.residual_plot.curve1.setData(Ux) 
                self.residual_plot.curve2.setData(Uy)  
                                
            except:
                pass


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    ex = dialog()
    ex.show()
    sys.exit(app.exec_())