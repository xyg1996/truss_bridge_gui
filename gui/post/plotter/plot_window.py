

"""
Implementation of a simple window for plotting single point or cell
probes in asterstudy post processor
"""

from PyQt5 import Qt as Q
import numpy as np

from .graph_canvas import GraphCanvas
from .table import (CustomTable, GenericTableModel,
                    TableParams, ok_validator)


class PlotWindow(Q.QWidget):
    """
    Plot window
    """

    def __init__(self, data=None, variable='Function'):
        """
        Create/intialize the representation parameters widget on the
        sidebar of the post-processor page.

        Arguments:
            parent (Optional[QWidget]): Parent widget. Defaults to
                *None*.
            rep: representation for which the parameters are to be
                 modified
        """
        Q.QWidget.__init__(self, None)

        font = Q.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.setFont(font)

        if data is None:
            xvals = np.arange(0., 5., 0.01)
            yvals = np.sin(xvals)
            data = np.vstack((xvals, yvals))
            data = data.transpose()
        elif isinstance(data, (list, tuple)):
            data = np.array(data)

        rows, cols = data.shape
        if rows <= cols:
            data = data.transpose()

        hlmain = Q.QHBoxLayout()
        hlmain.setSpacing(0)
        self.setLayout(hlmain)

        table = CustomTable(self)
        table.setSizePolicy(Q.QSizePolicy.Minimum,
                            Q.QSizePolicy.Expanding)

        params = TableParams()
        params.headers = ('Time', 'Value')
        params.validators = [ok_validator, ok_validator]

        # Special treatment for single data points...
        modeldata = data
        if len(data[:, 0]) == 2 and abs(data[1, 0] - data[0, 0]) < 1.e-8:
            modeldata = [data[0, :]]

        model = GenericTableModel(params, modeldata)
        table.setModel(model)

        graph = GraphCanvas(parent=self)
        graph.update_axes(data[:, 0], data[:, 1], 'Time (s)', variable)

        hlmain.addWidget(table)
        hlmain.addWidget(graph)

        table.resize(400, 0)
        table.setReadOnly(True)
        self.resize(1024, 500)


# def __main__():
#     import sys
#     app = Q.QApplication(sys.argv)
#     w = PlotWindow()
#     w.setWindowTitle('Testing plotter')
#     w.show()

#     sys.exit(app.exec_())


# if __name__ == "__main__":
#     __main__()
