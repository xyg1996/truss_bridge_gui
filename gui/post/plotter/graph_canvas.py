

"""
Matplotlib based graph canvas used in the postprocessing functionality
of asterstudy
"""

import os.path as osp

from PyQt5 import Qt

# Imports for embedded graph/tables
import matplotlib
from matplotlib.backends.backend_qt5agg import (
    FigureCanvasQTAgg as FigureCanvas)
from matplotlib.figure import Figure
matplotlib.use('Qt5Agg')


class GraphCanvas(FigureCanvas):
    """
    Class represents the basic parameters for graph canvas.
    """

    # pragma pylint: disable=invalid-name
    def __init__(self,
                 parent=None,
                 dpi=100):
        """
        Create graph canvas.

        Arguments:
            parent (QWidget): Parent widget.
            width (int): Horizontal dimension of the graph.
            height (int): Vertical dimension of the graph.
            dpi (int): DPI of the graph.
        """
        width = 4.5
        height = 3.5

        fig = Figure(
            figsize=(width, height),
            dpi=dpi,
            facecolor='white',
            edgecolor='none')
        self.axes = fig.add_subplot(111)
        self.axes.tick_params(labelsize=7)

        FigureCanvas.__init__(self, fig)
        fig.subplots_adjust(bottom=0.15)
        self.setParent(parent)
        self.setFont(self.parent().font())

        FigureCanvas.setSizePolicy(self,
                                   Qt.QSizePolicy.Expanding,
                                   Qt.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

        self.setStyleSheet("background-color:transparent;")
        fig.patch.set_facecolor("None")

        self.installEventFilter(self)
        self.update_axes(([0., 1.]), ([0., 2.]))

    # pragma pylint: disable=invalid-name, unused-argument
    def eventFilter(self, QObject, event):
        """
        Function called based on the event filter installed on the
        current class (self), allows to handle context menu events
        """
        if event.type() == Qt.QEvent.MouseButtonPress:
            if event.button() == Qt.Qt.RightButton:
                self._context_menu()
        return False

    def _context_menu(self):
        """
        Add a savefigure context menu
        """
        menu = Qt.QMenu(self.parent())
        menu.setFont(self.parent().font())

        menu.setMaximumWidth(120)

        menu.addAction("Save &PNG", lambda: self._save_fig('png'))
        menu.addAction("Save &SVG", lambda: self._save_fig('svg'))

        menu.popup(Qt.QCursor.pos())

    # pragma pylint: disable=invalid-name
    def _save_fig(self, ext):
        """
        Saves the plot to a png file
        """
        dotext = '.' + ext
        docont = True
        fpath = ""
        while docont:
            fpath, _ = Qt.QFileDialog.getSaveFileName(
                caption='Export plot to %s file' % (ext),
                directory=fpath, filter='*%s' % (dotext))

            docont = False
            if fpath:
                if dotext != osp.splitext(fpath)[-1]:
                    fpath = fpath + dotext
                    docont = osp.isfile(fpath)

        if fpath:
            self.axes.get_figure().savefig(fpath)

    def update_axes(self, xvals, yvals, xlabel=None, ylabel=None):
        """
        Update (redraw) the graph.
        """
        self.axes.cla()
        if not isinstance(xvals, tuple):
            xvals = (xvals,)
            yvals = (yvals,)

        isvalid = False
        for xval, yval in zip(xvals, yvals):
            # pragma pylint: disable=len-as-condition
            if len(xval):
                marker = 's' if len(xval) < 12 else None
                self.axes.plot(xval, yval, marker=marker)
                self.axes.grid(b=True, which='major',
                               color='#aaaaaa', linestyle='--')
                if abs(xval[-1] - xval[0]) < 1.e-8:
                    self.axes.set_xlim(xval[0] - 1.e-5,
                                       xval[0] + 1.e-5)
                isvalid = True

        if isvalid:
            xlabel = xlabel if xlabel else 'X'
            ylabel = ylabel if ylabel else 'Y'
            self.axes.set_xlabel(xlabel, size=9)
            if isinstance(ylabel, (tuple, list)):
                self.axes.legend(ylabel)
            else:
                self.axes.set_ylabel(ylabel, size=9)

            self.draw()
