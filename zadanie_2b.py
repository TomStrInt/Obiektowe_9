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
    QEasingCurve
)



class AnimatedWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Mój widget")
        self.resize(400, 200)

        self.button = QPushButton("Kliknij mnie!", self)
        self.button.resize(120, 30)

        #startowa pozycja przycisku na górze
        start_x = (self.width() - self.button.width()) // 2
        self.button.move(start_x, 0)

        self.label = QLabel("", self)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        #pozycja i rozmiar etykiety
        self.label.setGeometry(0, self.height() // 2, self.width(), 30)


        #efekt przezroczystości dla etykiety
        effect = QGraphicsOpacityEffect(self.label)
        self.label.setGraphicsEffect(effect)

        #animacja ruchu przycisku
        self.btn_anim = QPropertyAnimation(self.button, b"pos", self)
        self.btn_anim.setDuration(1000)
        self.btn_anim.setEasingCurve(QEasingCurve.Type.InOutCubic)

        #animacja przezroczystości
        self.lbl_anim = QPropertyAnimation(effect, b"opacity", self)
        self.lbl_anim.setStartValue(0.0)
        self.lbl_anim.setEndValue(1.0)
        self.lbl_anim.setDuration(1500)
        self.lbl_anim.setEasingCurve(QEasingCurve.Type.Linear)


        # Połączenie sygnału kliknięcia przycisku do metody obsługi
        self.button.clicked.connect(self.on_button_clicked)

    def on_button_clicked(self):
    
        start_pos = self.button.pos()
        end_y = self.height() - self.button.height() - 10
        end_pos = QPoint(start_pos.x(), end_y)

        self.btn_anim.setStartValue(start_pos)
        self.btn_anim.setEndValue(end_pos)
        self.btn_anim.start()

       
        self.label.setText("Hello World!! ! !!!!")
        self.lbl_anim.start()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = AnimatedWindow()
    win.show()
    sys.exit(app.exec())
