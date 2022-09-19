#!/usr/bin/env -S python3 -B
from tk_drawer import TkDrawer
from r2point import R2Point
from convex import Void, Point, Segment, Polygon


def void_draw(self, tk):
    pass


def point_draw(self, tk):
    tk.draw_point(self.p)


def segment_draw(self, tk):
    tk.draw_line(self.p, self.q)


def polygon_draw(self, tk):
    for n in range(self.points.size()):
        tk.draw_line(self.points.last(), self.points.first())
        self.points.push_last(self.points.pop_first())


setattr(Void, 'draw', void_draw)
setattr(Point, 'draw', point_draw)
setattr(Segment, 'draw', segment_draw)
setattr(Polygon, 'draw', polygon_draw)

tk = TkDrawer()
f = Void()
tk.clean()
print("Введите координаты отрезка")
segment = Segment(R2Point(), R2Point())
try:

    while True:
        tk.draw_seg(segment.p, segment.q)
        f = f.add(R2Point())
        tk.clean()
        f.draw(tk)
        print(f"S = {f.area()}, P = {f.perimeter()}, Dist = {f.min_dist(segment)}\n")
        if isinstance(f, Polygon):
            print(f.adj_matrix)
            print(Segment(f.points.first(), f.points.last()))
except(EOFError, KeyboardInterrupt):
    print("\nStop")
    tk.close()
