import random

from collections import Counter


class ParticleFilter:
    def __init__(self, prior_distribution, particle_count=1000):
        self.particle_count = particle_count
        self.particles = [prior_distribution() for _ in xrange(particle_count)]

    def move(self, movement, movement_model):
        self.particles = [movement_model(particle, movement) for particle in self.particles]

    def measure(self, measurement, measurement_likelihood):
        """ Algorithm from table 4.3 of Probabilistic Robotics by Herr Thrun """

        weights = [measurement_likelihood(measurement, particle) for particle in self.particles]
        if sum(weights) > 0:
            weights = [weight / sum(weights) for weight in weights]
            self.low_variance_sampler(self.particles, weights)
        else:
            print "We're totally off the scent"

    def low_variance_sampler(self, new_particles, weights):
        """ Algorithm from table 4.4 of Probabilistic Robotics by my boy Sebastian"""




        self.particles = []
        r = random.random() / self.particle_count
        c = weights[0]
        i = 0
        for m in xrange(self.particle_count):
            u = r + 1.0 * m / self.particle_count
            while u > c:
                i += 1
                c += weights[i]
            self.particles.append(new_particles[i])



