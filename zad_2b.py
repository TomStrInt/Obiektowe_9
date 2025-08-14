import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QPushButton, QLabel, QVBoxLayout,
    QGraphicsOpacityEffect
)

from PyQt6.QtCore import Qt, QPropertyAnimation, QPoint, QEasingCurve

class AnimatedWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Animowane widgety")
        self.resize(400, 200)

        # Przygotowanie widgetów
        #self.label.hide()
        self.button = QPushButton("Kliknij mnie", self)
        self.label = QLabel("Hello World!", self)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Efekt przezroczystości dla etykiety
        effect = QGraphicsOpacityEffect(self.label)
        self.label.setGraphicsEffect(effect)

        # Layout
        layout = QVBoxLayout(self)
        layout.addWidget(self.button)
        layout.addWidget(self.label)

        # Animacja przesunięcia przycisku
        self.btn_anim = QPropertyAnimation(self.button, b"pos", self)
        self.btn_anim.setEndValue(QPoint(10, 170))
        self.btn_anim.setDuration(1000)
        self.btn_anim.setEasingCurve(QEasingCurve.Type.InOutCubic)

        # Animacja przeźroczystości etykiety
        self.lbl_anim = QPropertyAnimation(effect, b"opacity", self)
        self.lbl_anim.setStartValue(0.0)
        self.lbl_anim.setEndValue(1.0)
        self.lbl_anim.setDuration(1500)
        self.lbl_anim.setEasingCurve(QEasingCurve.Type.Linear)

        # Uruchomienie animacji po starcie aplikacji
        self.btn_anim.start()
        self.lbl_anim.start()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = AnimatedWindow()
    win.show()
    sys.exit(app.exec())
