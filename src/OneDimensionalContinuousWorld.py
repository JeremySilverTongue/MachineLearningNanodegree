import math
import random

import matplotlib.pyplot as plt

from algorithms.ParticleFilter import ParticleFilter

WORLD_SIZE = 10
MARKERS = [1, 2, 5, 6, 8]

MAX_RANGE = 5

HIT_VARIANCE = .75
MOVEMENT_VARIANCE = 5


def sample_measurement_distribution(actual_range):
    measurement = min(random.normalvariate(actual_range, HIT_VARIANCE), MAX_RANGE)
    return max(0, measurement)


def true_ranges(position):
    left_markers = filter(lambda x: x < position, MARKERS)
    right_markers = filter(lambda x: x > position, MARKERS)

    true_left_range = MAX_RANGE if len(left_markers) == 0 else position - max(left_markers)

    true_right_range = MAX_RANGE if len(right_markers) == 0 else min(right_markers) - position
    return true_left_range, true_right_range


def make_measurement(position):
    true_left_range, true_right_range = true_ranges(position)
    return sample_measurement_distribution(true_left_range), sample_measurement_distribution(true_right_range)


def range_likelihood(true_range, measurement):
    return 1 / math.sqrt(2 * math.pi * HIT_VARIANCE) * math.exp(-1 / 2 * (true_range - measurement) ** 2 / HIT_VARIANCE)


def measurement_likelihood(measurement, position):
    left_range, right_range = true_ranges(position)
    left_measurement, right_measurement = measurement
    return range_likelihood(left_range, left_measurement) * range_likelihood(right_range, right_measurement)


def prior_distribution():
    return random.random() * WORLD_SIZE


def movement_model(position, intended_movement):
    return position + intended_movement * max(random.normalvariate(1, .1), 0)


def show_particles(particles):
    plt.hist(particles, bins=100, range=(0, WORLD_SIZE))
    plt.show()


def test():
    # random.seed(42)



    bot = 5.5
    print true_ranges(bot)
    print make_measurement(bot)
    particle_filter = ParticleFilter(prior_distribution)
    show_particles(particle_filter.particles)

    print MARKERS
    for move in [0, 1, 1, -3, -1, 5]:
        bot = movement_model(bot, move)
        print "Bot moving", move
        particle_filter.move(move, movement_model)
        show_particles(particle_filter.particles)

        print "Measuring with bot at", bot
        particle_filter.measure(make_measurement(bot), measurement_likelihood)
        show_particles(particle_filter.particles)




        # n, bins, patches = plt.hist(particle_filter.particles, 50, normed=1, facecolor='green', alpha=0.75)

        # plt.hist([sample_measurement_distribution(2) for _ in xrange(1000)])
        # plt.hist([movement_model(2, 2) for _ in xrange(1000)])


        # plt.show()


if __name__ == "__main__":
    test()
