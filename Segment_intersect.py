from r2point import R2Point


# Находится ли точка на отрезке
def on_segment(m, p, q):
    if min(m.x, p.x) <= q.x <= max(m.x, p.x) and min(m.y, p.y) <= q.y <= max(m.y, p.y):
        return True
    else:
        return False


# Операция векторного произведения
def Direction(a, b, c):
    return (c.x - a.x) * (b.y - a.y) - (b.x - a.x) * (c.y - a.y)


# Пересекаются ли два отрезка
def Segments_intersect(a, b, c, d):
    d1 = Direction(c, d, a)
    d2 = Direction(c, d, b)
    d3 = Direction(a, b, c)
    d4 = Direction(a, b, d)
    if ((d1 > 0 and d2 < 0) or (d1 < 0 and d2 > 0)) and ((d3 > 0 and d4 < 0) or (d3 < 0 and d4 > 0)):
        return True
    elif d1 == 0 and on_segment(c, d, a):
        return True
    elif d2 == 0 and on_segment(c, d, b):
        return True
    elif d3 == 0 and on_segment(a, b, c):
        return True
    elif d4 == 0 and on_segment(a, b, d):
        return True
    else:
        return False

if __name__ == '__main__':
    print(on_segment(R2Point(1,0), R2Point(0,1), R2Point(0.5, 0.5)))
    print(Segments_intersect(R2Point(0,0), R2Point(1,1), R2Point(0, 1), R2Point(1, 0)))