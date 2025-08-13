class MyObject:

    def __init__(self):
        self.my_attribute = 1
        self.my_attribute2 = 2

obj = MyObject()
print(obj.my_attribute)
print(obj.my_attribute2)
obj.my_attribute = 'hello'
print(obj.my_attribute)