#decorator 
class MyCustomClass:

    def __init__(self):
        self._value = None

    @property
    def value(self):
        print("getting the value", self._value)
        return self._value

    @value.setter
    def value(self, value):
        print("setting the value", value)
        self._value = value


obj = MyCustomClass()

a = obj.value       # Access the value
print(a)            # Print the value
obj.value = 'hello' # Set the value
b = obj.value       # Access the value
print(b)  