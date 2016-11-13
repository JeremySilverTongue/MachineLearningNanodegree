import random

from environment import Agent, Environment
from planner import RoutePlanner
from simulator import Simulator


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

        ###########
        ## TO DO ##
        ###########
        # Set any additional class parameters as needed

    def reset(self, destination=None, testing=False):
        """ The reset function is called at the beginning of each trial.
            'testing' is set to True if testing trials are being used
            once training trials have completed. """

        # Select the destination as the new location to route to
        self.planner.route_to(destination)

        self.epsilon -= 0.005

        if testing:
            self.epsilon = 0
            self.alpha = 0

        return None

    def build_state(self):
        """ The build_state function is called when the agent requests data from the
            environment. The next waypoint, the intersection inputs, and the deadline
            are all features available to the agent. """

        waypoint = self.planner.next_waypoint()
        inputs = self.env.sense(self)
        deadline = self.env.get_deadline(self)  # Remaining deadline

        state = (waypoint, inputs["light"], inputs["oncoming"], inputs["right"], inputs["left"])

        if self.learning and state not in self.Q:
            self.Q[state] = {None: 10, 'forward': 10, 'left': 10, 'right': 10}

        return state

    def get_max_q(self, state):
        """ The get_max_Q function is called when the agent is asked to find the
            maximum Q-value of all actions based on the 'state' the smartcab is in. """

        if state not in self.Q:
            return random.choice([None, 'forward', 'left', 'right'])
        else:
            return max(self.Q[state].iteritems(), key=lambda x: x[1])[0]

    def choose_action(self, state):
        """ The choose_action function is called when the agent is asked to choose
            which action to take, based on the 'state' the smartcab is in. """

        # Set the agent state and default action
        self.state = state
        self.next_waypoint = self.planner.next_waypoint()

        if not self.learning or random.random() < self.epsilon:
            return random.choice([None, 'forward', 'left', 'right'])
        else:
            return self.get_max_q(state)

    def learn(self, state, action, reward):
        """ The learn function is called after the agent completes an action and
            receives an award. This function does not consider future rewards
            when conducting learning. """

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
    agent = env.create_agent(LearningAgent, learning=True, epsilon=1, alpha=.7)
    env.set_primary_agent(agent, enforce_deadline=True)
    sim = Simulator(env, optimized=False, log_metrics=True, display=False, update_delay=.001)
    sim.run(n_test=10, tolerance=.05)


if __name__ == '__main__':
    run()
