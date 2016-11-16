import math
import random

from PIL import Image

from algorithms.ParticleFilter import ParticleFilter
from maps.OccupancyGrid import OccupancyGrid

WORLD_SIZE = 10
MARKERS = [1, 2, 5, 6, 8]

MAX_RANGE = 500

HIT_VARIANCE = 20
MOVEMENT_VARIANCE = .5

grid = OccupancyGrid("maps/map.png")


def sample_measurement_distribution(actual_range, variance=HIT_VARIANCE):
    measurement = min(random.normalvariate(actual_range, variance), MAX_RANGE)
    return max(0, measurement)


def make_measurement(position, grid, img=None, variance=HIT_VARIANCE):
    true_measurement = grid.eight_way_measurement(position, max_range=MAX_RANGE, img=img)
    return [sample_measurement_distribution(measurement, variance) for measurement in true_measurement]


def range_likelihood(true_range, measurement):
    return 1 / math.sqrt(2 * math.pi * HIT_VARIANCE) * math.exp(-1 / 2 * (true_range - measurement) ** 2 / HIT_VARIANCE)


def measurement_likelihood(measurement, position):
    true_ranges = grid.eight_way_measurement(position)
    return reduce(lambda a, b: a * b,
                  [range_likelihood(true_ranges[i], measurement[i]) for i in xrange(len(measurement))])


def movement_model(position, intended_movement):
    distance = math.sqrt(intended_movement[0] ** 2 + intended_movement[1] ** 2)
    x = position[0] + intended_movement[0] + distance * random.normalvariate(0, MOVEMENT_VARIANCE)
    y = position[1] + intended_movement[1] + distance * random.normalvariate(0, MOVEMENT_VARIANCE)

    return (x, y)


def show_particles(particles, bot):
    img = Image.open("maps/map.png").convert("RGB")
    pix = img.load()
    for particle in particles:
        pix[particle[1], particle[0]] = (255, 0, 255)

    pix[bot[1], bot[0]] = (0, 255, 0)

    img.show()


def test():
    # random.seed(42)



    bot = (75, 60)
    print grid.occupancy.shape

    def prior_distribution():
        return (random.randint(0, grid.occupancy.shape[0] - 1), random.randint(0, grid.occupancy.shape[1] - 1))
        # return (random.randint(0, 175), random.randint(0,175))

    particle_filter = ParticleFilter(prior_distribution, particle_count=1000)
    show_particles(particle_filter.particles, bot)

    measurement = make_measurement(bot, grid, variance=10)
    particle_filter.measure(measurement, measurement_likelihood)
    show_particles(particle_filter.particles, bot)

    move = (0, 20)
    bot = movement_model(bot, move)
    particle_filter.move(move, movement_model)
    show_particles(particle_filter.particles, bot)

    measurement = make_measurement(bot, grid, variance=10)
    particle_filter.measure(measurement, measurement_likelihood)
    show_particles(particle_filter.particles, bot)

    move = (0, 20)
    bot = movement_model(bot, move)
    particle_filter.move(move, movement_model)
    show_particles(particle_filter.particles, bot)

    measurement = make_measurement(bot, grid, variance=10)
    particle_filter.measure(measurement, measurement_likelihood)
    show_particles(particle_filter.particles, bot)


if __name__ == "__main__":
    test()
