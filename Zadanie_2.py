#funkcje 
class MyCustomClass:

    def __init__(self):
        self._value = None

    def getValue(self):
        print("getting the value", self._value)
        return self._value

    def setValue(self, value):
        print("setting the value", value)
        self._value = value

    value = property(getValue, setValue)


obj = MyCustomClass()

a = obj.value       # Access the value
print(a)            # Print the value
obj.value = 'hello' # Set the value
b = obj.value       # Access the value
print(b)            # Print the value