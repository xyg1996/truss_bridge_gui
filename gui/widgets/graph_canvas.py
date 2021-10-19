


#


"""
Graph Canvas
------------

Implementation of class *GraphCanvas* for Pi application.
"""


# Special imports for embedded graph/tables
import matplotlib
import numpy
from PyQt5 import Qt

matplotlib.use('Qt5Agg')
# pragma pylint: disable=ungrouped-imports

# Workaround for windows version and calibre9 linux when matplotlib
# gets mixed up with Qt version
try:
    from matplotlib.figure import Figure
    from matplotlib.backends.backend_qt5agg import (
        FigureCanvasQTAgg as FigureCanvas)
except ImportError:
    FigureCanvas = object

# note: the following pragma is added to prevent pylint complaining
#       about functions that follow Qt naming conventions;
#       it should go after all global functions
# pragma pylint: disable=invalid-name


def getModifiedScale(yValues):
    """
    Tests whether autoscaling needs to be overridden for a given set
    of ordinate values. Returns the modified ymin and ymax for the
    plotting
    """
    yvals = [float(y) for y in yValues]
    ymin = min(yvals)
    ymax = max(yvals)

    if abs(ymax) <= 1.e-6:
        return None, None

    dy = (ymax - ymin)
    if abs(dy / ymax) < 1.e-3:
        ymin = 0. if ymin > 1.e-5 else ymin * 1.1
        ymax = 0. if ymax < -1.e-5 else ymax * 1.1
        return ymin, ymax
    return None, None


class GraphCanvas(FigureCanvas):
    """
    Class represents the basic parameters for graph canvas.
    """
    def __init__(self,
                 parent=None,
                 width=5,
                 height=4,
                 dpi=100):
        """
        Create graph canvas.

        Arguments:
            parent (QWidget): Parent widget.
            width (int): Horizontal dimension of the graph.
            height (int): Vertical dimension of the graph.
            dpi (int): DPI of the graph.
        """
        self.fig = Figure(figsize=(width, height),
                          dpi=dpi,
                          facecolor='white',
                          edgecolor='none')
        self.axes = self.fig.add_subplot(111)
        self.axes.tick_params(labelsize=6)

        self.oldXValues = []
        self.oldYValues = []

        FigureCanvas.__init__(self, self.fig)

        self.setParent(parent)

        # pragma pylint: disable=no-member
        FigureCanvas.setSizePolicy(self,
                                   Qt.QSizePolicy.Expanding,
                                   Qt.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    def resizeEvent(self, event):
        """Overridden in order to correct negative size in the event."""
        w = event.size().width()
        h = event.size().height()
        FigureCanvas.resizeEvent(
            self, Qt.QResizeEvent(Qt.QSize(abs(w), abs(h)), event.oldSize()))

    def updateAxes(self, xValues, yValues,
                   color="#616161", grid=True, title=None,
                   xlabel=None, ylabel=None, transparent=True):
        """
        Update (redraw) the graph.
        """
        unchanged = (numpy.array_equal(self.oldXValues, xValues) and
                     numpy.array_equal(self.oldYValues, yValues))
        if unchanged:
            return

        self.oldXValues = xValues
        self.oldYValues = yValues

        self.axes.cla()
        self.axes.plot(xValues, yValues, color=color)

        if xValues.size > 0:
            ymin, ymax = getModifiedScale(yValues)
            if ymin is not None:
                self.axes.set_ylim(bottom=ymin, top=ymax)

        if grid:
            self.axes.grid()

        if title:
            self.axes.set_title(title, fontsize=10)

        if xlabel:
            self.axes.set_xlabel(xlabel, fontsize=9)

        if ylabel:
            self.axes.set_ylabel(ylabel, fontsize=9)

        if transparent:
            self.fig.patch.set_facecolor('None')
            self.fig.patch.set_alpha(0)

        self.draw()
        try:
            self.fig.tight_layout()
        except Exception: # pragma pylint: disable=broad-except
            pass
