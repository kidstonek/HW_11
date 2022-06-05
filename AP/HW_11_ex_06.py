"""
Для экземпляра класса Vector реализуйте функтор. Создайте для класса Vector метод __call__.
Он должен реализовать следующее поведение:
vector = Vector(Point(1, 10))

print(vector())  # (1, 10)

При вызове экземпляра класса как функции, он возвращает кортеж с координатами вектора.

Если при вызове мы передаем параметр число, то мы выполняем произведение вектора на число —
умножаем каждую координату на указанное число и возвращаем кортеж с новыми координатами вектора.

vector = Vector(Point(1, 10))

print(vector(5))  # (5, 50)
"""


class Point:
    def __init__(self, x, y):
        self.__x = None
        self.__y = None
        self.x = x
        self.y = y

    @property
    def x(self):
        return self.__x

    @x.setter
    def x(self, x):
        if (type(x) == int) or (type(x) == float):
            self.__x = x

    @property
    def y(self):
        return self.__y

    @y.setter
    def y(self, y):
        if (type(y) == int) or (type(y) == float):
            self.__y = y

    def __str__(self):
        return f"Point({self.x},{self.y})"


class Vector:
    def __init__(self, coordinates: Point):
        self.coordinates = coordinates

    def __setitem__(self, index, value):
        if index == 0:
            self.coordinates.x = value
        if index == 1:
            self.coordinates.y = value

    def __getitem__(self, index):
        if index == 0:
            return self.coordinates.x
        if index == 1:
            return self.coordinates.y

    def __call__(self, value=None):
        if value is None:
            return self.coordinates.x, self.coordinates.y
        else:
            self.coordinates.x = self.coordinates.x * value
            self.coordinates.y = self.coordinates.y * value
            return self.coordinates.x, self.coordinates.y

    def __str__(self):
        return f"Vector({self.coordinates.x},{self.coordinates.y})"


def main():
    vector = Vector(Point(1, 10))

    print(vector())
    print(vector(5))  # (5, 50)


if '__main__' == __name__:
    main()
