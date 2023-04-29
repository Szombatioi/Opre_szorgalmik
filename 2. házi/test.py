class XYZ:
    def __init__(self):
        self.bool = True

a = XYZ()
b = XYZ()
c = XYZ()

arr = [a,b,c]
x = arr.pop(1)
x.bool = False
arr.
