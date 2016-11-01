import numpy as np
from PIL import Image


class OccupancyGrid:
    def __init__(self, file_name):
        img = Image.open(file_name)
        # self.occupancy = np.array(img.convert("L").getdata()).reshape(img.width, img.height)
        self.occupancy = np.array(img.convert("L"))

    def eight_way_measurement(self, position, max_range=500, img=None):
        """
        Gives the result of eight perfect depth sensors, arranged at the compass points, starting with the positive
        x axis and moving counter clockwise
        """
        measurement = (
            self.simple_range_measurement(position, 1, 0, max_range, img),
            self.simple_range_measurement(position, 1, 1, max_range, img),
            self.simple_range_measurement(position, 0, 1, max_range, img),
            self.simple_range_measurement(position, -1, 1, max_range, img),
            self.simple_range_measurement(position, -1, 0, max_range, img),
            self.simple_range_measurement(position, -1, -1, max_range, img),
            self.simple_range_measurement(position, 0, -1, max_range, img),
            self.simple_range_measurement(position, 1, -1, max_range, img)
        )

        return measurement

    def simple_range_measurement(self, position, dx, dy, max_range=500, img=None):
        measurement = 0
        x, y = position[0], position[1]
        x, y = int(x), int(y)
        step = np.math.sqrt(dx ** 2 + dy ** 2)

        # print self.occupancy.shape, x, y
        while measurement < max_range and 0 < x < self.occupancy.shape[0] and 0 < y < self.occupancy.shape[1] and \
                        self.occupancy[x][y] == 255:

            # print self.occupancy.shape, x, y

            if img is not None:
                img[x, y] = (0, 255, 0)
            x += dx
            y += dy
            # print self.occupancy.shape, x, y


            measurement += step

        return measurement

    def get_range_measurement(self, position, azimuth, max_range=500):
        pass

    def pixels_to_check(self, azimuth, max_range):
        first_oct = azimuth % np.math.pi / 4
        xf = max_range * np.math.cos(first_oct)
        yf = max_range * np.math.sin(first_oct)
        error = -1
        delta_err = yf / xf
        y = 0
        first_oct_pix = []
        for x in xrange(int(np.math.ceil(xf))):
            first_oct_pix.append((x, y))
            error += delta_err
            if error >= 0:
                y += 1
                error -= 1

        return first_oct_pix


def test():
    grid = OccupancyGrid("maps.png")

    img = Image.open("maps.png").convert("RGB")

    pix = img.load()

    print pix[50, 23]
    pix[50, 23] = (255, 0, 0)

    print grid.eight_way_measurement((50, 23), img=pix)
    img.show()

    # print grid.occupancy
    # img = Image.fromarray(grid.occupancy)
    # img.show()


if __name__ == "__main__":
    test()
