import math
import unittest

from Point import Point


class Polygon:
    def __init__(self, points):
        self.points = points
        pass

    def range_measurement(self, bot, azimuth, min_range=5, max_range=100):
        """ Algorithm from http://stackoverflow.com/a/565282/679647"""

        min_range_measurement = max_range

        for i in xrange(len(self.points)):
            first = self.points[i]
            j = (i + 1) % len(self.points)
            second = self.points[j]

            p = first
            r = second - first
            q = bot
            s = bot.with_azimuth_and_range(azimuth, max_range) - q

            if r.cross_mag(s) == 0:
                continue

            t = (q - p).cross_mag(s) / r.cross_mag(s)
            u = (q - p).cross_mag(r) / r.cross_mag(s)

            print self.points
            print "First", first, "Second", second
            print p, r, q, s
            print t, u

            if 0 <= t <= 1 and 0 <= u <= 1:
                print "Hit point", p + r * t
                range_measurement = (p + r * t - bot).length()
                min_range_measurement = min(min_range_measurement, range_measurement)

        return max(min_range, min_range_measurement)


class TestRangeMeasurement(unittest.TestCase):
    def test_easy_hit(self):
        wall = Polygon([Point(0, 0), Point(0, 2)])
        expected = 1
        result = wall.range_measurement(Point(1, 1), math.pi, 0, 100)
        self.assertEqual(result, expected)

    def test_miss(self):
        wall = Polygon([Point(0, 0), Point(0, 2)])
        expected = 100
        result = wall.range_measurement(Point(1, 1), 0, 0, 100)
        self.assertEqual(result, expected)

    def test_too_close(self):
        wall = Polygon([Point(0, 0), Point(0, 2)])
        expected = 5
        result = wall.range_measurement(Point(1, 1), math.pi, 5, 100)
        self.assertEqual(result, expected)

    def test_too_far(self):
        wall = Polygon([Point(0, 0), Point(0, 2)])
        expected = 100
        result = wall.range_measurement(Point(500, 1), math.pi, 5, 100)
        self.assertEqual(result, expected)

    def test_triangle(self):
        triangle = Polygon([Point(2, 0), Point(0, 2), Point(2, 2)])
        expected = math.sqrt(2)
        result = triangle.range_measurement(Point(0, 0), math.pi / 4, 0, 100)
        self.assertAlmostEqual(result, expected)


if __name__ == "__main__":
    unittest.main()
