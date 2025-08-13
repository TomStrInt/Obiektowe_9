from PyQt6.QtCore import pyqtProperty, pyqtSignal

class CustomObject(QObject):

    valueChanged = pyqtSignal(int)

    def __init__(self):
        super().__init__()
        self._value = 0        # the default value

    # change the setter function to be as:
    @value.setter
    def value(self, value):
        # here, the check is very important..
        # to prevent unneeded signal being propagated.
        if value != self._value:
            self._value = value
            self.valueChanged.emit(value)