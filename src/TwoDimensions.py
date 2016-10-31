import math
import random
from PIL import Image

from maps.OccupancyGrid import OccupancyGrid
import matplotlib.pyplot as plt

from algorithms.ParticleFilter import ParticleFilter

WORLD_SIZE = 10
MARKERS = [1, 2, 5, 6, 8]

MAX_RANGE = 500

HIT_VARIANCE = .75
MOVEMENT_VARIANCE = 5

grid = OccupancyGrid("maps/map.png")

def sample_measurement_distribution(actual_range):
    measurement = min(random.normalvariate(actual_range, HIT_VARIANCE), MAX_RANGE)
    return max(0, measurement)


def make_measurement(position, grid, img = None):
    true_measurement = grid.eight_way_measurement(position, max_range=MAX_RANGE, img=img)
    return map(sample_measurement_distribution, true_measurement)


def range_likelihood(true_range, measurement):
    return 1 / math.sqrt(2 * math.pi * HIT_VARIANCE) * math.exp(-1 / 2 * (true_range - measurement) ** 2 / HIT_VARIANCE)


def measurement_likelihood(measurement, position):
    true_ranges = grid.eight_way_measurement(position)
    return reduce(lambda a, b: a * b,
                  [range_likelihood(true_ranges[i], measurement[i]) for i in xrange(len(measurement))])





def show_particles(particles):
    img = Image.open("maps/map.png").convert("RGB")
    pix = img.load()
    for particle in particles:
        pix[particle[1], particle[0]] = (255, 0, 255)
    img.show()



def test():
    # random.seed(42)



    bot = (50, 50)
    print grid.occupancy.shape

    def prior_distribution():
        return (random.randint(0, grid.occupancy.shape[0] - 1), random.randint(0, grid.occupancy.shape[1]-1))
        # return (random.randint(0, 175), random.randint(0,175))

    particle_filter = ParticleFilter(prior_distribution)
    show_particles(particle_filter.particles)

    measurement = make_measurement(bot, grid)
    print measurement
    particle_filter.measure(measurement, measurement_likelihood)




if __name__ == "__main__":
    test()
