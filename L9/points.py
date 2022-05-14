import math


class Point2D:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def reset(self):
        self.x = 0
        self.y = 0

    def print(self):
        print(F"[{self.x}, {self.y}]")


class Point3D(Point2D):
    def __init__(self, x, y, z):
        super().__init__(x, y)
        self.z = z

    def reset(self):
        super().reset()
        self.z = 0

    def print(self):
        print(F"[{self.x}, {self.y}, {self.z}]")


class Segment2D:
    def __init__(self, a: Point2D, b: Point2D):
        self.a = a
        self.b = b

    def length(self):
        return math.sqrt((self.b.x - self.a.x) ** 2 + (self.b.y - self.a.y) ** 2)
