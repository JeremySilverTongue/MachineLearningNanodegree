import math
import unittest


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def cross_mag(self, other):
        return self.x * other.y - self.y * other.x

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __mul__(self, other):
        return Point(other * self.x, other * self.y)

    def length(self):
        return math.sqrt(self.x ** 2 + self.y ** 2)

    def distance(self, other):
        return (self - other).length()

    def with_azimuth_and_range(self, azimuth, r=0):
        return Point(self.x + r * math.cos(azimuth), self.y + r * math.sin(azimuth))

    def __str__(self):
        return "Point({:.2f}, {:.2f})".format(self.x, self.y)

    def __repr__(self):
        return "Point({}, {})".format(self.x, self.y)


class PointTest(unittest.TestCase):
    pass


    # def test_parallel_cross_magEasyHit(self):
    #     wall = Polygon([Point(0, 0), Point(0, 2)])
    #     expected = 1
    #     result = wall.range_measurement(Point(1, 1), math.pi, 0, 100)
    #     self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main()
