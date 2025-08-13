from PyQt6.QtCore import pyqtProperty

class CustomObject(QObject):
    def __init__(self):
        super().__init__()
        self._value = 0        # the default value

    @pyqtProperty(int)
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value