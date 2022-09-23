from pytest import approx
from math import sqrt
from r2point import R2Point
from convex import Figure, Void, Point, Segment, Polygon


class TestVoid:

    # Инициализация (выполняется для каждого из тестов класса)
    def setup_method(self):
        self.f = Void()

    # Нульугольник является фигурой
    def test_figure(self):
        assert isinstance(self.f, Figure)

    # Конструктор порождает экземпляр класса Void (нульугольник)
    def test_void(self):
        assert isinstance(self.f, Void)

    # Периметр нульугольника нулевой
    def test_perimeter(self):
        assert self.f.perimeter() == 0.0

        # Площадь нульугольника нулевая

    def test_аrea(self):
        assert self.f.area() == 0.0

        # При добавлении точки нульугольник
        # превращается в одноугольник

    def test_add(self):
        assert isinstance(self.f.add(R2Point(0.0, 0.0)), Point)


class TestPoint:

    # Инициализация (выполняется для каждого из тестов класса)
    def setup_method(self):
        self.f = Point(R2Point(0.0, 0.0))
        self.g = Point(R2Point(1.0, 1.0))

    # Одноугольник является фигурой
    def test_figure(self):
        assert isinstance(self.f, Figure)

    # Конструктор порождает экземпляр класса
    # Point (одноугольник)
    def test_point(self):
        assert isinstance(self.f, Point)

    # Периметр одноугольника нулевой
    def test_perimeter(self):
        assert self.f.perimeter() == 0.0

    # Площадь одноугольника нулевая
    def test_аrea(self):
        assert self.f.area() == 0.0

    # При добавлении точки одноугольник может не измениться
    def test_add1(self):
        assert self.f.add(R2Point(0.0, 0.0)) is self.f

    # При добавлении точки одноугольник может
    # превратиться в двуугольник
    def test_add2(self):
        assert isinstance(self.f.add(R2Point(1.0, 0.0)), Segment)

    # Тесты для метода нахождения расстояния от
    # точки (0,0) до отрезков
    def test_min_dist1(self):
        assert self.f.min_dist(Segment(R2Point(0.0, 0.0),
                                       R2Point(1.0, 0.0))) == 0

    def test_min_dist2(self):
        assert self.f.min_dist(Segment(R2Point(-1.0, 1.0),
                                       R2Point(1.0, 1.0))) == 1

    def test_min_dist3(self):
        assert self.f.min_dist(Segment(R2Point(1.0, 1.0),
                                       R2Point(2.0, 2.0))) \
               == approx(sqrt(2))

    def test_min_dist4(self):
        assert self.f.min_dist(Segment(R2Point(1.0, -1.0),
                                       R2Point(-1.0, -1.0))) == 1

    # Тесты для метода нахождения расстояния
    # от точки (1,1) до отрезков
    def test_min_dist5(self):
        assert self.g.min_dist(Segment(R2Point(0.0, 0.0),
                                       R2Point(1.0, 0.0))) == 1

    def test_min_dist6(self):
        assert self.g.min_dist(Segment(R2Point(-1.0, 1.0),
                                       R2Point(1.0, 1.0))) == 0

    def test_min_dist7(self):
        assert self.g.min_dist(Segment(R2Point(1.0, 1.0),
                                       R2Point(2.0, 2.0))) == 0

    def test_min_dist8(self):
        assert self.g.min_dist(Segment(R2Point(-1.0, 4.0),
                                       R2Point(3.0, 4.0))) == 3


class TestSegment:

    # Инициализация (выполняется для каждого из тестов класса)
    def setup_method(self):
        self.f = Segment(R2Point(0.0, 0.0), R2Point(1.0, 0.0))
        self.g = Segment(R2Point(0.0, 1.0), R2Point(1.0, 1.0))

    # Двуугольник является фигурой
    def test_figure(self):
        assert isinstance(self.f, Figure)

    # Конструктор порождает экземпляр класса Segment (двуугольник)
    def test_segment(self):
        assert isinstance(self.f, Segment)

    # Периметр двуугольника равен удвоенной длине отрезка
    def test_perimeter(self):
        assert self.f.perimeter() == approx(2.0)

    # Площадь двуугольника нулевая
    def test_аrea(self):
        assert self.f.area() == 0.0

    # При добавлении точки двуугольник может не измениться
    def test_add1(self):
        assert self.f.add(R2Point(0.5, 0.0)) is self.f

    # При добавлении точки двуугольник может
    # превратиться в другой двуугольник
    def test_add2(self):
        assert isinstance(self.f.add(R2Point(2.0, 0.0)), Segment)

    # При добавлении точки двуугольник может
    # превратиться в треугольник
    def test_add3(self):
        assert isinstance(self.f.add(R2Point(0.0, 1.0)), Polygon)

    # Тесты для метода нахождения расстояния от отрезка
    # с координатами (0,0);(1,0) до отрезков
    def test_min_dist(self):
        assert self.f.min_dist(Segment(R2Point(0.0, 0.0),
                                       R2Point(1.0, 0.0))) == 0

    def test_min_dist1(self):
        assert self.f.min_dist(Segment(R2Point(-1.0, 1.0),
                                       R2Point(1.0, 1.0))) == 1

    def test_min_dist2(self):
        assert self.f.min_dist(Segment(R2Point(1.0, 1.0),
                                       R2Point(2.0, 2.0))) == 1

    def test_min_dist3(self):
        assert self.f.min_dist(Segment(R2Point(1.0, -1.0),
                                       R2Point(-1.0, -1.0))) == 1

    # Тесты для метода нахождения расстояния от от отрезка
    # с координатами  (0,1);(1,1) до отрезков
    def test_min_dist4(self):
        assert self.g.min_dist(Segment(R2Point(1.0, 1.0),
                                       R2Point(1.0, 2.0))) == 0

    def test_min_dist5(self):
        assert self.g.min_dist(Segment(R2Point(-1.0, 1.0),
                                       R2Point(1.0, 1.0))) == 0

    def test_min_dist6(self):
        assert self.g.min_dist(Segment(R2Point(2.0, 2.0),
                                       R2Point(3.0, 1.0))) \
               == approx(sqrt(2))

    def test_min_dist7(self):
        assert self.g.min_dist(Segment(R2Point(-1.0, 0.0),
                                       R2Point(1.0, 0.0))) == 1


class TestPolygon:
    Figure.segment = Segment(R2Point(-1.0, 2.0),
                             R2Point(2.0, 2.0))

    # Инициализация (выполняется для каждого из тестов класса)
    def setup_method(self):
        self.f = Polygon(
            R2Point(
                0.0, 0.0), R2Point(
                1.0, 0.0), R2Point(
                0.0, 1.0))

    # Тесты для нахождения расстояния от отрезка
    # с координатами (-1,2);(2,2)
    def test_min_dist1(self):
        self.f.add(R2Point(1.0, 1.0))
        assert self.f.min_dist(Segment(R2Point(-1.0, 2.0),
                                       R2Point(2.0, 2.0))) == 1

    def test_min_dist2(self):
        self.f.add(R2Point(1.0, 1.0))
        self.f.add(R2Point(1.25, 1.25))
        assert self.f.min_dist(Segment(R2Point(-1.0, 2.0),
                                       R2Point(2.0, 2.0))) == 0.75

    def test_min_dist3(self):
        self.f.add(R2Point(1.0, 1.0))
        self.f.add(R2Point(1.25, 1.25))
        self.f.add(R2Point(0.5, 6))
        assert self.f.min_dist(Segment(R2Point(-1.0, 2.0),
                                       R2Point(2.0, 2.0))) == 0

    # Тесты для метода нахождения расстояния от отрезка
    # с координатами  (0,0);(1,0) до отрезков

    def test_min_dist4(self):
        Figure.segment = Segment(R2Point(1.0, 1.0),
                                 R2Point(1.0, 2.0))
        self.f.add(R2Point(0.75, 0.75))
        assert self.f.min_dist(Segment(R2Point(1.0, 1.0),
                                       R2Point(1.0, 2.0))) \
               == approx(0.25 * sqrt(2))

    def test_min_dist5(self):
        Figure.segment = Segment(R2Point(1.0, 1.0),
                                 R2Point(1.0, 2.0))
        self.f.add(R2Point(0.75, 0.75))
        self.f.add(R2Point(1, 1))
        assert self.f.min_dist(Segment(R2Point(1.0, 1.0),
                                       R2Point(1.0, 2.0))) == 0

    def test_min_dist6(self):
        Figure.segment = Segment(R2Point(1.0, 1.0),
                                 R2Point(1.0, 2.0))
        self.f.add(R2Point(0.75, 0.75))
        self.f.add(R2Point(1, 1))
        self.f.add(R2Point(5, 0))
        self.f.add(R2Point(0, 5))
        assert self.f.min_dist(Segment(R2Point(1.0, 1.0),
                                       R2Point(1.0, 2.0))) == 1

    def test_min_dist7(self):
        Figure.segment = Segment(R2Point(1.0, 1.0),
                                 R2Point(1.0, 2.0))
        self.f.add(R2Point(0.75, 0.75))
        self.f.add(R2Point(1, 1))
        self.f.add(R2Point(5, 0))
        self.f.add(R2Point(0, 5))
        self.f.add(R2Point(-2, -2))
        assert self.f.min_dist(Segment(R2Point(1.0, 1.0),
                                       R2Point(1.0, 2.0))) \
               == approx(sqrt(2))
