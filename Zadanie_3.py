import sys
import math
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import Qt, QTimer, QTime, QPointF, QRectF
from PyQt6.QtGui import QPainter, QColor
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTimeEdit


# RYSOWANIE CYFR 7-segmentowych
class SevenSegCountdown(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        # stan minutnika
        self.remaining = 0     
        self.is_finished = False
        self.near_end = False

        # animacja figury (kąt i prędkość)
        self.angle = 0.0
        self.shape_timer = QTimer(self)
        self.shape_timer.timeout.connect(self.rotate_shape)
        self.shape_timer.setInterval(200)  # początkow a prędkość
        self.shape_timer.start()

        # pulsowanie cyfr po zakończeniu
        self.pulse_scale = 1.0
        self.pulse_timer = QTimer(self)
        self.pulse_timer.timeout.connect(self.toggle_pulse)

        # mapa segmentów:
        self.SEGMENTS = {
            0: [1,1,1,1,1,1,0],
            1: [0,1,1,0,0,0,0],
            2: [1,1,0,1,1,0,1],
            3: [1,1,1,1,0,0,1],
            4: [0,1,1,0,0,1,1],
            5: [1,0,1,1,0,1,1],
            6: [1,0,1,1,1,1,1],
            7: [1,1,1,0,0,0,0],
            8: [1,1,1,1,1,1,1],
            9: [1,1,1,1,0,1,1],
        }

    def rotate_shape(self):  # obrót figury; przyspiesza gdy zostało <=7s
        delta = 7 if not self.near_end else 20
        self.angle = (self.angle + delta) % 360
        self.update()


    def toggle_pulse(self):# zmiana skali cyfr
        self.pulse_scale = 1.2 if self.pulse_scale == 1.0 else 1.0
        self.update()

    def update_time(self, secs: int):# wywołane co sekundę z CountdownTimer
        prev = self.remaining
        self.remaining = max(0, secs)

        # przspieszanie kwadratu, gdy zostało <=7s 
        if self.remaining <= 7 and not self.near_end:
            self.near_end = True
            self.shape_timer.setInterval(50)

        # po dojściu do zera-- pulsowanie
        if self.remaining == 0 and not self.is_finished:
            self.is_finished = True
            self.pulse_timer.start(300)

        self.update()

    def paintEvent(self, ev):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        w, h = self.width(), self.height()
        # obszar cyfr - górne 2/3 widgetu
        digit_area = QRectF(0, 0, w, h * 2/3)

        # obliczanie minut isekund
        m = self.remaining // 60
        s = self.remaining % 60
        text = f"{m:02d}{s:02d}"

        n_digits = 4
        margin = w * 0.02
        dig_w = (digit_area.width() - margin * (n_digits + 1)) / n_digits
        dig_h = digit_area.height() - 2 * margin
        seg_th = dig_w * 0.15


        fg = QColor("red") if self.is_finished else QColor("black")
        painter.setBrush(fg)
        painter.setPen(Qt.PenStyle.NoPen)

        # rysowanie  cyfr
        for i, ch in enumerate(text):
            d = int(ch)
            seg_on = self.SEGMENTS[d]
            x0 = margin + i * (dig_w + margin)
            y0 = margin

            #pulsowanie
            painter.save()
            if self.is_finished:
                cx = x0 + dig_w/2
                cy = y0 + dig_h/2
                painter.translate(cx, cy)
                painter.scale(self.pulse_scale, self.pulse_scale)
                painter.translate(-cx, -cy)
            # segmenty:
            # a: góra
            if seg_on[0]:
                painter.fillRect(QRectF(x0+seg_th, y0,
                                        dig_w-2*seg_th, seg_th), fg)
            # b: prawa góra
            if seg_on[1]:
                painter.fillRect(QRectF(x0+dig_w-seg_th, y0+seg_th,
                                        seg_th, dig_h/2-seg_th), fg)
            # c: prawa dół
            if seg_on[2]:
                painter.fillRect(QRectF(x0+dig_w-seg_th, y0+dig_h/2,
                                        seg_th, dig_h/2-seg_th), fg)
            # d: dół
            if seg_on[3]:
                painter.fillRect(QRectF(x0+seg_th, y0+dig_h-seg_th,
                                        dig_w-2*seg_th, seg_th), fg)
            # e: lewa dół
            if seg_on[4]:
                painter.fillRect(QRectF(x0, y0+dig_h/2,
                                        seg_th, dig_h/2-seg_th), fg)
            # f: lewa góra
            if seg_on[5]:
                painter.fillRect(QRectF(x0, y0+seg_th,
                                        seg_th, dig_h/2-seg_th), fg)
            # g: środek
            if seg_on[6]:
                painter.fillRect(QRectF(x0+seg_th, y0+dig_h/2-seg_th/2,
                                        dig_w-2*seg_th, seg_th), fg)
            painter.restore()

        #obracający się kwadrat 
        size = min(w, h/3) * 0.5
        cx, cy = w/2, h * 5/6
        painter.save()
        painter.translate(cx, cy)
        painter.rotate(self.angle)
        painter.setBrush(QColor("blue") if not self.is_finished else QColor("magenta"))
        painter.drawRect(QRectF(-size/2, -size/2, size, size))
        painter.restore()

        painter.end()


#INPUT I PRZYCISKI
class CountdownTimer(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Minutnik 7-segmentowy")
        self.resize(400, 300)

        #kontrolki wejściowe
        self.time_edit = QTimeEdit(self)
        self.time_edit.setDisplayFormat("mm:ss")
        self.time_edit.setTime(QTime(0, 1, 0))

        self.start_btn = QPushButton("Start", self)
        self.reset_btn = QPushButton("Reset", self)

        # wyświetlacz
        self.display = SevenSegCountdown(self)

        # timer odliczający
        self.timer = QTimer(self)
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self._tick)

        # layout
        top = QHBoxLayout()
        top.addWidget(self.time_edit)
        top.addWidget(self.start_btn)
        top.addWidget(self.reset_btn)

        main = QVBoxLayout(self)
        main.addLayout(top)
        main.addWidget(self.display)
        self.setLayout(main)

        # połączenia
        self.start_btn.clicked.connect(self.start)
        self.reset_btn.clicked.connect(self.reset)
        self.initial_time = self.time_edit.time()
        self.initial_remaining = 0
        self.remaining = 0

    def start(self):
        t = self.time_edit.time()
        self.initial_time = t
        self.remaining = t.minute() * 60 + t.second()
        self.initial_remaining = self.remaining


        if self.remaining > 0:
            self.time_edit.setEnabled(False)
            self.start_btn.setEnabled(False)
            self.display.is_finished = False
            self.display.near_end = False
            self.display.pulse_timer.stop()
            self.timer.start()

    def _tick(self):
        self.remaining -= 1
        self.display.update_time(self.remaining)
        if self.remaining <= 0:
            self.timer.stop()
            self.reset_btn.setEnabled(True)

    def reset(self):
        self.timer.stop()
        self.remaining = self.initial_remaining
        #self.display.update_time(0)
        #self.time_edit.setEnabled(True)
        #self.start_btn.setEnabled(True)
        # Zatrzymaj odliczanie
        #self.timer.stop()
       # Przywróć stan „00:00” bez wywoływania update_time,
        # żeby nie odpalić efektu zakończenia
         #self.remaining = 0
       # Reset flag animacji w wyświetlaczu
        self.display.update_time(self.remaining)
        self.display.is_finished = False
        self.display.near_end = False
        self.display.pulse_timer.stop()
        self.display.pulse_scale = 1.0
       #self.display.update()
       # Przywracanie kontrolek wejsviowych
        self.time_edit.setEnabled(True)
        self.time_edit.setTime(self.initial_time)

        self.start_btn.setEnabled(True)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    w = CountdownTimer()
    w.show()
    sys.exit(app.exec())
