import sys
from PyQt6.QtWidgets import QApplication, QWidget, QHBoxLayout
from PyQt6.QtCore  import QPropertyAnimation, QPoint, QEasingCurve

class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(600, 600)
        self.child = QWidget(self)
        self.child.setStyleSheet("background-color:red;border-radius:15px;")
        self.child.resize(100, 100)
        self.anim = QPropertyAnimation(self.child, b"pos")
        self.anim.setEasingCurve(QEasingCurve.Type.InOutCubic)
        self.anim.setEndValue(QPoint(400, 400))
        self.anim.setDuration(1500)
        self.anim.start()

if __name__ == "__main__":
    app = QApplication(sys.argv)

    #Kontener okienkowy
    window = QWidget()
    window.setWindowTitle(" single inoutcubic animation")
    window.resize(200, 100)
    win = Window()
    win.__init__()
    layout = QHBoxLayout(window)
    
    #layout.addWidget(toggle)

    window.show()
    sys.exit(app.exec())