
import math
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import Qt, QPointF
from PyQt6.QtGui import QPainter, QColor
from PyQt6.QtWidgets import QDial

class _Bar(QtWidgets.QWidget):
    clickedValue = QtCore.pyqtSignal(int)

    def __init__(self, steps, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding
        )

        if isinstance(steps, list):
            self.n_steps = len(steps)
            self.steps = steps
        elif isinstance(steps, int):
            self.n_steps = steps
            self.steps = ['red'] * steps
        else:
            raise TypeError('steps must be a list or int')

        self._bar_solid_percent = 0.8
        self._background_color = QtGui.QColor('black')
        self._padding = 4.0

    def paintEvent(self, e):
        painter = QtGui.QPainter(self)
        brush = QtGui.QBrush()
        brush.setColor(self._background_color)
        brush.setStyle(Qt.BrushStyle.SolidPattern)
        rect = QtCore.QRect(0, 0, painter.device().width(), painter.device().height())
        painter.fillRect(rect, brush)

        parent = self.parent()
        vmin, vmax = parent.minimum(), parent.maximum()
        value = parent.value()

        d_height = painter.device().height() - (self._padding * 2)
        d_width = painter.device().width() - (self._padding * 2)

        step_size = d_height / self.n_steps
        bar_height = step_size * self._bar_solid_percent
        bar_spacer = step_size * (1 - self._bar_solid_percent) / 2

        pc = (value - vmin) / (vmax - vmin)
        n_steps_to_draw = int(pc * self.n_steps)
        for n in range(n_steps_to_draw):
            brush.setColor(QtGui.QColor(self.steps[n]))

            x = int(self._padding)
            y = int(self._padding + d_height - ((n + 1) * step_size) + bar_spacer)
            w = int(d_width)
            h = int(bar_height)

            rect = QtCore.QRect(x, y, w, h)
            painter.fillRect(rect, brush)


        painter.end()

    def sizeHint(self):
        return QtCore.QSize(140, 200)

    def _trigger_refresh(self):
        self.update()

    def _calculate_clicked_value(self, e):
        parent = self.parent()
        vmin, vmax = parent.minimum(), parent.maximum()
        d_height = self.size().height() + (self._padding * 2)
        step_size = d_height / self.n_steps

        click_y = e.y() - self._padding - step_size / 2
        pc = (d_height - click_y) / d_height
        value = vmin + pc * (vmax - vmin)
        self.clickedValue.emit(int(value))

    def mouseMoveEvent(self, e):
        self._calculate_clicked_value(e)

    def mousePressEvent(self, e):
        self._calculate_clicked_value(e)


class PowerBar(QtWidgets.QWidget):
    colorChanged = QtCore.pyqtSignal()

    def __init__(self, steps=5, *args, **kwargs):
        super().__init__(*args, **kwargs)
        layout = QtWidgets.QHBoxLayout()        #ustawienie poziomego layoutu

        self._bar = _Bar(steps)
        self._dial = DotDial(dot_radius=3, dot_color='green')   #zmiiana kresek na kropki
        self._dial.valueChanged.connect(self._bar._trigger_refresh)
        self._bar.clickedValue.connect(self._dial.setValue)
        self._dial.setRange(0, 15)          #zmiana liczby kropek
        layout.addWidget(self._bar)
        layout.addWidget(self._dial)
        #self._dial = DotDial(dot_radius=4, dot_color='green')
        #self._dial = QtWidgets.QDial()
        #self._dial.setNotchesVisible(True)
        #self._dial.setWrapping(False)
        #self._dial.valueChanged.connect(self._bar._trigger_refresh)
        
        layout.setStretch(0, 1)
        layout.setStretch(1, 0)

        self._bar.clickedValue.connect(self._dial.setValue)

        self.setLayout(layout)

    def __getattr__(self, name):
        if name in self.__dict__:
            return self.__dict__[name]
        try:
            return getattr(self._dial, name)
        except AttributeError:
            raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")


    def setColor(self, color):
        self._bar.steps = [color] * self._bar.n_steps
        self._bar.update()

    def setColors(self, colors):
        self._bar.n_steps = len(colors)
        self._bar.steps = colors
        self._bar.update()

    def setBarPadding(self, i):
        self._bar._padding = int(i)
        self._bar.update()

    def setBarSolidPercent(self, f):
        self._bar._bar_solid_percent = float(f)
        self._bar.update()

    def setBackgroundColor(self, color):
        self._bar._background_color = QtGui.QColor(color)
        self._bar.update()

#dodatkowa klasa zamieniająca (nadpisująca) kropki nad kreski
class DotDial(QDial):           
    def __init__(self, *args, dot_radius=3, dot_color='black', dot_margin=6, **kwargs):
        super().__init__(*args, **kwargs)
        self.setNotchesVisible(False)
        self.dot_radius = dot_radius
        self.dot_color = QColor(dot_color)
        #self.dot_count = dot_count
        self.dot_margin = dot_margin
        self.setNotchesVisible(False)

    def paintEvent(self, ev):
        # 1) narysuj oryginalne pokrętło (bez kresek)
        super().paintEvent(ev)

        # 2) dopisz własne kropki
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        p.setBrush(self.dot_color)
        p.setPen(Qt.PenStyle.NoPen)


        rect = self.rect()
        center = rect.center()


        r = min(self.width(), self.height())/2 - 5          # promień okręgu kropkowego
        center = self.rect().center()
        steps = self.maximum() - self.minimum()            # ile kropek

        start, span = 0, 360                   # kąty w stopniach
        for i in range(steps+1):
            ang = math.radians(start + span * i/steps)
            x = center.x() + r * math.cos(math.pi/2 - ang)
            y = center.y() - r * math.sin(math.pi/2 - ang)
            p.drawEllipse(QPointF(x, y), self.dot_radius, self.dot_radius)

        p.end()


if __name__ == '__main__':
    app = QtWidgets.QApplication([])

    #bar = PowerBar(7)
    bar = PowerBar(["#ff1000", "#07ff00", "#8000ff", "#ffff02", "#0cffff","#ff6200"])
    bar.setBarPadding(4)
    bar.setBarSolidPercent(0.8)
    bar.setBackgroundColor('orange')
    

    bar.show()
    app.exec()
