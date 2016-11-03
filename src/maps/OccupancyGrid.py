import math

import numpy as np
from PIL import Image
from scipy.ndimage.filters import gaussian_filter


class OccupancyGrid:
    def __init__(self, file_name, danger_variance, detection_variance):
        img = Image.open(file_name)
        self.occupancy = 1 - np.array(img.convert("L")) / 255

        self.danger = gaussian_filter(1. * self.occupancy, sigma=math.sqrt(danger_variance), mode="constant", cval=1)
        # self.detection = gaussian_filter(1.*self.occupancy, sigma=math.sqrt(detection_variance), mode="constant", cval=1)

        self.danger = np.maximum(self.danger, self.occupancy)
        # self.detection = np.maximum(self.danger, self.occupancy)

        # Image.fromarray(self.danger * 255).show()
        # Image.fromarray(self.detection * 255).show()

        self.measure_memo = {}

    def eight_way_measurement(self, position, max_range=500, img=None):
        """
        Gives the result of eight perfect depth sensors, arranged at the compass points, starting with the positive
        x axis and moving counter clockwise. Note that the y-axis is the first coordinate, and points down X_x
        """
        position = int(position[0]), int(position[1])
        if position not in self.measure_memo:
            self.measure_memo[position] = (
                self.simple_range_measurement(position, 0, 1,  img),
                self.simple_range_measurement(position, -1, 1,  img),
                self.simple_range_measurement(position, -1, 0,  img),
                self.simple_range_measurement(position, -1, -1,  img),
                self.simple_range_measurement(position, 0, -1,  img),
                self.simple_range_measurement(position, 1, -1,  img),
                self.simple_range_measurement(position, 1, 0,  img),
                self.simple_range_measurement(position, 1, 1,  img)
            )
        return [min(max_range, measurement) for measurement in self.measure_memo[position]]

    def simple_range_measurement(self, position, dy, dx, img=None):
        measurement = 0
        y, x = position[0], position[1]
        step = np.math.sqrt(dy ** 2 + dx ** 2)

        while 0 < y < self.occupancy.shape[0] and 0 < x < self.occupancy.shape[1]:
            if self.occupancy[y][x] == 1:
                break

            if img is not None:
                img[y, x] = (0, 255, 0)
            y += dy
            x += dx

            measurement += step

        return measurement

        # def get_range_measurement(self, position, azimuth, max_range=500):
        #     pass
        #
        # def pixels_to_check(self, azimuth, max_range):
        #     first_oct = azimuth % np.math.pi / 4
        #     xf = max_range * np.math.cos(first_oct)
        #     yf = max_range * np.math.sin(first_oct)
        #     error = -1
        #     delta_err = yf / xf
        #     y = 0
        #     first_oct_pix = []
        #     for x in xrange(int(np.math.ceil(xf))):
        #         first_oct_pix.append((x, y))
        #         error += delta_err
        #         if error >= 0:
        #             y += 1
        #             error -= 1
        #
        #     return first_oct_pix


def test():
    grid = OccupancyGrid("map.png", 5, 3)

    # img = Image.open("map.png").convert("RGB")
    #
    # pix = img.load()
    #
    # print pix[50, 23]
    # pix[50, 23] = (255, 0, 0)
    #
    # print grid.eight_way_measurement((50, 23), img=pix)
    # img.show()

    # print grid.occupancy
    # img = Image.fromarray(grid.occupancy)
    # img.show()


if __name__ == "__main__":
    test()
