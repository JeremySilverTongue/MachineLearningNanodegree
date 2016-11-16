import random
from collections import Counter

from src.algorithms.ParticleFilter import ParticleFilter


def particle_filter_integration_test():
    """
    This test follow's Sebastian's example of a one dimensional toroidal world with red or green walls.
    Don't ask me how a one dimensional world has walls. That's above my pay grade.

    The world looks like this:
    [Red, Green, Green, Red, Red]

    The robot can move left or right. With probability .8 it moves correctly, and with probability .1 it moves one space
    too far, and with probability .1 is doesn't move at all.

    The sensors have .8 probability of getting the color right, and .2 probability of getting the color wrong.
    """

    RED = "Red"
    GREEN = "Green"
    LEFT = "Left"
    RIGHT = "Right"
    STAY_PUT = "Stay Put"

    # random.seed(42)

    def prior_distribution():
        return random.randint(0, 4)

    def measurement_model(measurement, state):
        if state in [0, 3, 4] and measurement == RED:
            return .8
        elif state in [1, 2] and measurement == GREEN:
            return .8
        else:
            return .2

    def movement_model(state, movement):
        if movement == STAY_PUT:
            return state

        r = random.random()
        distance = 0
        if r < .1:
            distance = 2
        elif r < .9:
            distance = 1

        unwrapped = state + (distance if movement == RIGHT else -distance)
        return unwrapped % 5

    def print_filter(my_filter):
        print sorted(Counter(my_filter.particles).items())

    print "[RED, GREEN, GREEN, RED, RED]"

    particle_filter = ParticleFilter(prior_distribution)

    print sorted(Counter(particle_filter.particles).items())

    print "Measure Red"
    particle_filter.measure(RED, measurement_model)
    print_filter(particle_filter)

    print "Measure Green"
    particle_filter.measure(GREEN, measurement_model)
    print_filter(particle_filter)

    print "Measure Red"
    particle_filter.measure(RED, measurement_model)
    print "Measure Red"
    particle_filter.measure(RED, measurement_model)
    print_filter(particle_filter)

    print "Move right"
    particle_filter.move(RIGHT, movement_model)
    print_filter(particle_filter)

    print "Measure Green"
    particle_filter.measure(GREEN, measurement_model)
    print_filter(particle_filter)

    print "Move right"
    particle_filter.move(RIGHT, movement_model)

    print "Measure Green"
    particle_filter.measure(GREEN, measurement_model)
    print_filter(particle_filter)

    print "Move right"
    particle_filter.move(RIGHT, movement_model)

    print "Measure Red"
    particle_filter.measure(RED, measurement_model)
    print_filter(particle_filter)


if __name__ == "__main__":
    particle_filter_integration_test()
