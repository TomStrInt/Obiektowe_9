import sys
from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QPushButton,
    QLabel,
    QGraphicsOpacityEffect
)
from PyQt6.QtCore import (
    Qt,
    QPropertyAnimation,
    QPoint,
    QEasingCurve,
    pyqtSignal,
    pyqtProperty
)
from PyQt6.QtGui import QPainter, QColor
from PyQt6.QtCore import QRectF


class ToggleSwitch(QWidget):        #TOGGLE
    toggled = pyqtSignal(bool)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(60, 30)
        self._checked = False
        self._offset = 0.0

        # przesunięcia kółeczka toggle'a
        self._anim = QPropertyAnimation(self, b"offset", self)
        self._anim.setDuration(200)
        self._anim.setEasingCurve(QEasingCurve.Type.InOutCubic)

    def mouseReleaseEvent(self, event):
        # uruchamianie animacji
        self._checked = not self._checked
        self._anim.stop()
        start = self._offset
        end = 1.0 if self._checked else 0.0
        self._anim.setStartValue(start)
        self._anim.setEndValue(end)
        self._anim.start()
        self.toggled.emit(self._checked)
        super().mouseReleaseEvent(event)

    def paintEvent(self, event):
        radius = self.height() / 2
        knob_d = self.height() - 4
        bg_color = QColor("#4cd137") if self._checked else QColor("lightblue")  

        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        p.setBrush(bg_color)
        p.setPen(Qt.PenStyle.NoPen)
        p.drawRoundedRect(self.rect(), radius, radius)

        # rysujemy kółeczko
        margin = 2
        x = margin + self._offset * (self.width() - knob_d - 2 * margin)
        knob_rect = QRectF(x, margin, knob_d, knob_d)
        p.setBrush(QColor("white"))
        p.drawEllipse(knob_rect)
        p.end()

    @pyqtProperty(float)
    def offset(self):
        return self._offset

    @offset.setter
    def offset(self, value):
        self._offset = value
        self.update()


class AnimatedWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Mój projekt -animowane widgety")
        self.resize(400, 200)

        #przycisk głowny
        self.button = QPushButton("Kliknij mnie", self)
        self.button.resize(120, 30)
        start_x = (self.width() - self.button.width()) // 2
        self.button.move(start_x, 0)
        self.button.clicked.connect(self.on_button_clicked)


        #LABEL
        self.label = QLabel("", self)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setGeometry(0, self.height() // 2, self.width(), 30)
        effect = QGraphicsOpacityEffect(self.label)
        self.label.setGraphicsEffect(effect)

        # animacje przyciku i etykiety
        self.btn_anim = QPropertyAnimation(self.button, b"pos", self)
        self.btn_anim.setDuration(1000)
        self.btn_anim.setEasingCurve(QEasingCurve.Type.InOutCubic)

        self.lbl_anim = QPropertyAnimation(effect, b"opacity", self)
        self.lbl_anim.setStartValue(0.0)
        self.lbl_anim.setEndValue(1.0)
        self.lbl_anim.setDuration(1500)
        self.lbl_anim.setEasingCurve(QEasingCurve.Type.Linear)

        #toggle
        self.toggle = ToggleSwitch(self)
        self.toggle.move(10, self.height() - self.toggle.height() - 10)
        self.toggle.toggled.connect(self.on_toggle_switched)

    def on_button_clicked(self):
        if self.button.text() == "Kliknij mnie":
                #przesuwanie przycisku w dół 
            start_pos = self.button.pos()
            end_y = self.height() - self.button.height() - 10
            end_pos = QPoint(start_pos.x(), end_y)
            self.btn_anim.setStartValue(start_pos)
            self.btn_anim.setEndValue(end_pos)
            self.btn_anim.start()

                #pojawianie się etykiety
            self.label.setText("Witaj w Moim Projekcie!")
            self.lbl_anim.start()

                #zmiana tekstu i tła przycisku
            self.button.setText("Zamknij")
            self.button.setStyleSheet("background-color: orange;")
        else:
            self.close()


    def on_toggle_switched(self, checked: bool):
        if checked:
            self.setStyleSheet("background-color: grey;")
        else:
            self.setStyleSheet("")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = AnimatedWindow()
    win.show()
    sys.exit(app.exec())
