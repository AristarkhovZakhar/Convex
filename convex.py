from deq import Deq
from r2point import R2Point
import math
from Segment_intersect import Segments_intersect, on_segment


class Figure:
    """ Абстрактная фигура """
    dist = math.inf

    def perimeter(self):
        return 0.0

    def area(self):
        return 0.0

    def min_dist(self, seg):
        return math.inf


class Void(Figure):
    """ "Hульугольник" """

    def add(self, p):
        return Point(p)


class Point(Figure):
    """ "Одноугольник" """

    def __init__(self, p):
        self.p = p

    def add(self, q):
        return self if self.p == q else Segment(self.p, q)

    # Вычисление минимального расстояния от точки до отрезка
    def min_dist(self, seg):
        if seg.p.x == seg.q.x:
            if min(seg.p.y, seg.q.y) <= self.p.y <= max(seg.p.y, seg.q.y):
                return abs(self.p.x - seg.p.x)
            else:
                return min(R2Point.dist(self.p, seg.p), R2Point.dist(self.p, seg.q))

        elif seg.p.y == seg.q.y:
            if min(seg.p.x, seg.q.x) <= self.p.x <= max(seg.p.x, seg.q.x):
                return abs(self.p.y - seg.p.y)
            else:
                return min(R2Point.dist(self.p, seg.p), R2Point.dist(self.p, seg.q))
        else:
            x = (self.p.x * (seg.p.x - seg.q.x) - (seg.p.y - self.p.y) * (seg.p.y - seg.q.y) + seg.p.x * (
                    (seg.p.y - seg.q.y) ** 2 / (seg.p.x - seg.q.x))) \
                / (seg.p.x - seg.q.x + (seg.p.y - seg.q.y) ** 2 / (seg.p.x - seg.q.x))
            y = seg.p.y + (seg.p.y - seg.q.y) * (x - seg.p.x) / (seg.p.x - seg.q.x)
            if on_segment(seg.p, seg.q, R2Point(x, y)):
                return math.sqrt(x ** 2 + y ** 2)
            else:
                return min(R2Point.dist(self.p, seg.p), R2Point.dist(self.p, seg.q))


class Segment(Figure):
    """ "Двуугольник" """

    def __init__(self, p, q):
        self.p, self.q = p, q

    # Задаем хэш для объекта класса Segment
    def __hash__(self):
        return hash((self.p.x, self.q.y))

    def perimeter(self):
        return 2.0 * self.p.dist(self.q)

    def add(self, r):
        if R2Point.is_triangle(self.p, self.q, r):
            return Polygon(self.p, self.q, r)

        elif self.q.is_inside(self.p, r):
            return Segment(self.p, r)
        elif self.p.is_inside(r, self.q):
            return Segment(r, self.q)
        else:
            return self

    # Вычисление минимального расстояния между двумя отрезками
    def min_dist(self, seg):
        if Segments_intersect(self.p, self.q, seg.p, seg.q):
            return 0
        else:
            return min(Point(self.p).min_dist(seg), Point(self.q).min_dist(seg), Point(seg.p).min_dist(self),
                       Point(seg.q).min_dist(self))

    # Определение равенства двух объектов класса Segment
    def __eq__(self, other):
        return (self.p == other.p and self.q == other.q) or (self.p == other.q and self.q == other.p)


class Polygon(Figure):
    """ Многоугольник """
    # Словарь, в котором ключи-ребра многоугольника, а ключи - расстояния от них до заданного отрезка
    adj_matrix = {}

    def __init__(self, a, b, c):
        self.points = Deq()
        self.points.push_first(b)
        if b.is_light(a, c):
            self.points.push_first(a)
            self.points.push_last(c)
        else:
            self.points.push_last(a)
            self.points.push_first(c)
        self._perimeter = a.dist(b) + b.dist(c) + c.dist(a)
        self._area = abs(R2Point.area(a, b, c))

    def perimeter(self):
        return self._perimeter

    def area(self):
        return self._area

    # Вычисление минимального расстояния от многоугольника до отрезка
    def min_dist(self, segment):
        self.seg = segment
        a = Segment(self.points.first(), self.points.last()).min_dist(segment)
        self.adj_matrix[Segment(self.points.first(), self.points.last())] = a
        self.points.push_first(self.points.pop_last())
        b = Segment(self.points.first(), self.points.last()).min_dist(segment)
        self.adj_matrix[Segment(self.points.first(), self.points.last())] = b
        self.points.push_first(self.points.pop_last())
        c = Segment(self.points.first(), self.points.last()).min_dist(segment)
        self.adj_matrix[Segment(self.points.first(), self.points.last())] = c
        self.points.push_first(self.points.pop_last())
        return min(a, b, c)
    # Операция нахождения в словаре adj_matrix ключа со значением seg
    def _search_in_matrix(self, seg):
        for i in self.adj_matrix.keys():
            if i == seg:
                del self.adj_matrix[i]
                break

    # добавление новой точки
    def add(self, t):

        # поиск освещённого ребра
        for n in range(self.points.size()):
            if t.is_light(self.points.last(), self.points.first()):
                break
            self.points.push_last(self.points.pop_first())

        # хотя бы одно освещённое ребро есть
        if t.is_light(self.points.last(), self.points.first()):

            # учёт удаления ребра, соединяющего конец и начало дека
            self._perimeter -= self.points.first().dist(self.points.last())
            self._area += abs(R2Point.area(t,
                                           self.points.last(),
                                           self.points.first()))
            self._search_in_matrix(Segment(self.points.first(), self.points.last()))

            # удаление освещённых рёбер из начала дека
            p = self.points.pop_first()
            while t.is_light(p, self.points.first()):
                self._perimeter -= p.dist(self.points.first())
                self._area += abs(R2Point.area(t, p, self.points.first()))
                self._search_in_matrix(Segment(self.points.first(), p))
                p = self.points.pop_first()
            self.points.push_first(p)

            # удаление освещённых рёбер из конца дека
            p = self.points.pop_last()
            while t.is_light(self.points.last(), p):
                self._perimeter -= p.dist(self.points.last())
                self._area += abs(R2Point.area(t, p, self.points.last()))
                self._search_in_matrix(Segment(p, self.points.last()))
                p = self.points.pop_last()
            self.points.push_last(p)

            # добавление двух новых рёбер
            self._perimeter += t.dist(self.points.first()) + \
                               t.dist(self.points.last())
            self.points.push_first(t)
            Polygon.adj_matrix[Segment(t, self.points.first())] = Segment(t, self.points.first()).min_dist(self.seg)
            Polygon.adj_matrix[Segment(t, self.points.last())] = Segment(t, self.points.last()).min_dist(self.seg)

        return self


if __name__ == "__main__":
    print(Point(R2Point(0, 0)).min_dist(Segment(R2Point(0, 1), R2Point(1, 0))))
