import random

from environment import Agent, Environment
from planner import RoutePlanner
from simulator import Simulator

UNEXPLORED = -1000


class LearningAgent(Agent):
    """ An agent that learns to drive in the Smartcab world.
        This is the object you will be modifying. """

    def __init__(self, env, learning=False, epsilon=1.0, alpha=0.5):
        super(LearningAgent, self).__init__(env)  # Set the agent in the evironment
        self.planner = RoutePlanner(self.env, self)  # Create a route planner
        self.valid_actions = self.env.valid_actions  # The set of valid actions

        # Set parameters of the learning agent
        self.learning = learning  # Whether the agent is expected to learn
        self.Q = dict()  # Create a Q-table which will be a dictionary of tuples
        self.epsilon = epsilon  # Random exploration factor
        self.alpha = alpha  # Learning factor
        self.testing = False
        self.training_trips = -1
        self.starting_epsilon = epsilon

    def reset(self, destination=None, testing=False):
        self.planner.route_to(destination)

        self.training_trips += 1

        self.epsilon = self.starting_epsilon * 2 ** (-1. * self.training_trips / 10)

        print self.epsilon, self.training_trips

        # self.epsilon -= 0.05

        if testing:
            self.learning = True
            self.epsilon = 0
            self.alpha = 0
            self.testing = True

    def build_state(self):
        waypoint = self.planner.next_waypoint()
        inputs = self.env.sense(self)
        deadline = self.env.get_deadline(self)  # Remaining deadline

        if waypoint == 'forward':
            state = ("waypoint: " + waypoint, inputs["light"])
        elif waypoint == 'right':
            state = ("waypoint: " + waypoint, inputs["light"], "left: {}".format(inputs["left"]))
        else:
            state = ("waypoint: " + waypoint, inputs["light"], "oncoming: {}".format(inputs["oncoming"]))

        # state = (waypoint, inputs["light"], inputs["oncoming"], inputs["left"])

        if self.learning and state not in self.Q:
            self.Q[state] = {None: UNEXPLORED, 'forward': UNEXPLORED, 'left': UNEXPLORED, 'right': UNEXPLORED}

        return state

    def choose_action(self, state):
        """ The choose_action function is called when the agent is asked to choose
            which action to take, based on the 'state' the smartcab is in. """

        # Set the agent state and default action
        self.state = state
        self.next_waypoint = self.planner.next_waypoint()

        if self.testing:
            return max(self.Q[state].iteritems(), key=lambda x: x[1])[0]
        elif self.learning:
            for action, reward in self.Q[state].iteritems():
                if reward == UNEXPLORED:
                    # print "Aggressively exploring", state, self.Q[state]
                    return action

        if random.random() < 0 * self.epsilon or not self.learning:
            return random.choice([None, 'forward', 'left', 'right'])
        else:
            return max(self.Q[state].iteritems(), key=lambda x: x[1])[0]

    def learn(self, state, action, reward):
        if self.Q[state][action] == UNEXPLORED:
            self.Q[state][action] = reward
        else:
            self.Q[state][action] = (1 - self.alpha) * self.Q[state][action] + self.alpha * reward

    def update(self):
        """ The update function is called when a time step is completed in the
            environment for a given trial. This function will build the agent
            state, choose an action, receive a reward, and learn if enabled. """

        state = self.build_state()  # Get current state
        action = self.choose_action(state)  # Choose an action
        reward = self.env.act(self, action)  # Receive a reward
        self.learn(state, action, reward)  # Q-learn


def run():
    """ Driving function for running the simulation.
        Press ESC to close the simulation, or [SPACE] to pause the simulation. """

    env = Environment(verbose=False, num_dummies=100, grid_size=(8, 6))
    agent = env.create_agent(LearningAgent, learning=True, epsilon=1, alpha=.5)
    env.set_primary_agent(agent, enforce_deadline=True)
    sim = Simulator(env, optimized=True, log_metrics=True, display=False, update_delay=0, quiet=True)
    sim.run(n_test=10, tolerance=.01)


if __name__ == '__main__':
    run()
