import numpy as np
from ... import pyqtgraph as pg
import sys
from PyQt5.QtWidgets import QWidget,QApplication,QFrame,QGridLayout,QLabel,QPushButton,QVBoxLayout
from PyQt5.QtCore import Qt,QTimer

class Ui_Residual_plot(QWidget):

    def __init__(self):
        super(Ui_Residual_plot, self).__init__()
        # self.setupUi(self)

    def setupUi(self,frame,Ux=[],Uy=[]):
        # frame.resize(150,250)
        verticalLayout = QVBoxLayout(frame)
        win = pg.GraphicsLayoutWidget(frame)
        verticalLayout.addWidget(win)
        p = win.addPlot()
        p.showGrid(x=True,y=True)
        p.setLabel(axis="left",text="残差")
        p.setLabel(axis="bottom",text="迭代次数 / 次")
        p.addLegend()
        self.curve1 = p.plot(pen="r",name="Ux")
        self.curve2 = p.plot(pen="g",name="Uy")
        # p2 = win.addPlot()
        # p2.showGrid(x=True,y=True)
        # p2.setLabel(axis="left",text="残差")
        # p2.setLabel(axis="bottom",text="迭代次数 / 次")
        # p2.addLegend()
        # self.curve3 = p2.plot(pen="r",name="Ux")
        # self.curve4 = p2.plot(pen="g",name="Uy")
        # print(win.children())
        self.curve1.setData(Ux)
        self.curve2.setData(Uy)

        # win.removeItem(p)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Ui_Residual_plot()
    ex.show()
    sys.exit(app.exec_())
