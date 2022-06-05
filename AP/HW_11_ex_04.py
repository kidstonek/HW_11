"""
Реализуйте класс Vector. Свойство coordinates определяет координаты вектора и является экземпляром класса Point.
Напомним, что вектором называют направленный отрезок с началом и концом. Начало у нас будет в точке (0, 0),
а конец вектора мы будем задавать атрибутом coordinates.

Реализуйте возможность обращаться к координатам экземпляра класса Vector через квадратные скобки:

vector = Vector(Point(1, 10))

Чтобы получить значение, используя квадратные скобки у объекта print(vector[0]),
реализуйте метод __getitem__ у класса Vector.

Для записи значения координат вектора через индекс, как vector[0] = 10, реализуйте метод __setitem__ у класса Vector.

Обращение к координате x производится по индексу 0, а обращение к координате y — по индексу 1.
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
        else:
            return self.coordinates.y


def main():
    vector = Vector(Point(1, 10))

    print(vector.coordinates.x)  # 1
    print(vector.coordinates.y)  # 10

    vector[0] = 1  # Устанавливаем координату x вектора в 10

    print(vector[0])  # 10
    print(vector[1])  # 10


if '__main__' == __name__:
    main()

