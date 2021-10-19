


#


"""
Popup Frame
-----------

Implementation of class *PopupFrame* for AsterStudy application.
"""


from PyQt5 import Qt as Q, QtCore

# note: the following pragma is added to prevent pylint complaining
#       about functions that follow Qt naming conventions;
#       it should go after all global functions
# pragma pylint: disable=invalid-name


class PopupFrame(Q.QWidget):
    """Popup frame shown during the initialization."""
    closed = Q.pyqtSignal()

    def __init__(self, parent=None, size=None, msg="Popup message", closable=True):
        super().__init__(parent)

        # make the window frameless
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)

        self.fillColor = Q.QColor(30, 30, 30, 120)
        self.penColor = Q.QColor("#333333")

        self.popup_fillColor = Q.QColor(240, 240, 240, 255)
        self.popup_penColor = Q.QColor(200, 200, 200, 255)

        self.close_btn = None
        if closable:
            self.close_btn = Q.QPushButton(self)
            self.close_btn.setText("x")
            font = Q.QFont()
            font.setPixelSize(18)
            font.setBold(True)
            self.close_btn.setFont(font)
            self.close_btn.setStyleSheet("background-color: rgb(240, 240, 240, 0)")
            self.close_btn.setFixedSize(30, 30)
            self.close_btn.clicked.connect(self._onclose)

        msg = msg.strip()
        lines = 1
        cols = len(msg)

        self.msg = msg
        if not size:
            size = (min(800, 50+cols*10), 100+lines*12)

        self.popupSize = size

    def resizeEvent(self, _):
        """Resize the widget."""
        s = self.size()
        ow = int(s.width() / 2 - self.popupSize[0] / 2)
        oh = int(s.height() / 2 - self.popupSize[1] / 2)
        if self.close_btn:
            self.close_btn.move(ow + self.popupSize[0]-35, oh + 5)

    def paintEvent(self, _):
        """Draws the content of the popup."""
        # get current window size
        s = self.size()
        qp = Q.QPainter()
        qp.begin(self)
        qp.setRenderHint(Q.QPainter.Antialiasing, True)
        qp.setPen(self.penColor)
        qp.setBrush(self.fillColor)
        qp.drawRect(0, 0, s.width(), s.height())

        # drawpopup
        qp.setPen(self.popup_penColor)
        qp.setBrush(self.popup_fillColor)
        ow = int(s.width()/2-self.popupSize[0]/2)
        oh = int(s.height()/2-self.popupSize[1]/2)
        qp.drawRoundedRect(ow, oh, self.popupSize[0], self.popupSize[1], 5, 5)

        font = Q.QFont()
        font.setPixelSize(18)
        font.setBold(True)
        qp.setFont(font)
        qp.setPen(Q.QColor(70, 70, 70))
        qp.drawText(ow + 25, oh + self.popupSize[1]/2 + 5, self.msg)
        qp.end()

    def _onclose(self):
        self.closed.emit()
