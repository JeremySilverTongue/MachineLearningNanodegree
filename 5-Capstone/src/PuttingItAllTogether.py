import math
import random
from Tkinter import *
from collections import defaultdict

from PIL import Image, ImageTk

import algorithms.Navigation as nav
import algorithms.ParticleFilter as pf
import maps.OccupancyGrid as og
import src.gui.DrawingUtils as ui

HIT_VARIANCE = 10
MOVEMENT_VARIANCE = .2
WIGGLE_VARIANCE = .5
MAX_RANGE = 30


def sample_measurement_distribution(actual_range, variance=HIT_VARIANCE):
    measurement = min(random.normalvariate(actual_range, variance), MAX_RANGE)
    return max(0, measurement)


def make_measurement(position, grid, img=None, variance=HIT_VARIANCE):
    true_measurement = grid.eight_way_measurement(position, max_range=MAX_RANGE, img=img)
    return [sample_measurement_distribution(measurement, variance) for measurement in true_measurement]


def range_likelihood(true_range, measurement):
    return 1 / math.sqrt(2 * math.pi * HIT_VARIANCE) * math.exp(-1 / 2 * (true_range - measurement) ** 2 / HIT_VARIANCE)


def measurement_likelihood(measurement, position):
    true_ranges = grid.eight_way_measurement(position, max_range=MAX_RANGE)
    # print true_ranges
    # print [range_likelihood(true_ranges[i], measurement[i]) for i in xrange(len(measurement))]
    return reduce(lambda a, b: a * b,
                  [range_likelihood(true_ranges[i], measurement[i]) for i in xrange(len(measurement))])


def prior_distribution():
    return random.randint(0, grid.occupancy.shape[0] - 1), random.randint(0, grid.occupancy.shape[
        1] - 1), random.random() * 2 * math.pi


def vote():
    votes = []
    for particle in particle_filter.particles:
        y, x = int(particle[0]), int(particle[1])
        direction = plan[y][x][1]
        danger = grid.danger[y][x]
        votes.append((direction, danger + 1))

    total = defaultdict(int)

    total_danger = 0
    for vote, danger in votes:
        total_danger += danger
        total[vote] += danger

    clean_totals = [(danger / total_danger, direction) for direction, danger in total.iteritems()]
    print list(reversed(sorted(clean_totals)))
    return sorted(clean_totals)[-1][1]
    # return sorted(total.iteritems(), key=lambda i: i[1])[-1][0]


def movement_model(position, direction, movement_variance=MOVEMENT_VARIANCE, wiggle_variance=WIGGLE_VARIANCE):
    intended_movement = nav.directions[direction]
    distance = math.sqrt(intended_movement[0] ** 2 + intended_movement[1] ** 2)
    y = position[0] + intended_movement[0] + distance * random.normalvariate(0, movement_variance)
    x = position[1] + intended_movement[1] + distance * random.normalvariate(0, movement_variance)
    y += random.normalvariate(0, wiggle_variance)
    x += random.normalvariate(0, wiggle_variance)
    return y, x


# Window set up

pilImage = Image.open("maps/map.png")
pilImage = pilImage.resize((pilImage.width * 3, pilImage.height * 3), Image.NEAREST)
root = Tk()
root.wm_title("Particle Filter Fun!")
canvas = Canvas(root, width=pilImage.width, height=pilImage.height)
canvas.pack()

image = ImageTk.PhotoImage(pilImage)
canvas.create_image(0, 0, image=image, anchor=NW)

button_frame = Frame()
button_frame.pack(fill=X)

instructions_text = StringVar()
Label(button_frame, textvariable=instructions_text).pack(side=LEFT)

step_button = Button(button_frame, text="Step", underline=0)
step_button.pack(side=RIGHT)

reset_button = Button(button_frame, text="Reset Filter", underline=6)
reset_button.pack(side=RIGHT)

restart_button = Button(button_frame, text="Restart", underline=0)
restart_button.pack(side=RIGHT)

preprocess_button = Button(button_frame, text="Preprocess mesasuments")
preprocess_button.pack(side=RIGHT)

setting_goal = True
setting_bot = False
should_filter_reset = False

done = False

grid = og.OccupancyGrid("maps/map.png", danger_variance=10, preprocess=False)
plan = []
goal = None


def reset_goal(event):
    ui.clear_all(canvas)
    global setting_goal, done
    done = False
    setting_goal = True
    instructions_text.set("Click to set the goal location")


def on_click(event):
    location = int(event.y / 3), int(event.x / 3)
    global bot, setting_goal, plan, setting_bot, goal
    if setting_goal:
        goal = location
        setting_goal = False
        setting_bot = True
        ui.draw_goal(canvas, goal)
        instructions_text.set("Click to set bot location (hold while nav is computed)")
    elif setting_bot:
        bot = location
        setting_bot = False
        plan = nav.process_grid(goal, grid.occupancy, grid.danger, danger_weight=100)
        # grid.preprocess()
        instructions_text.set("Click the step button or press S to get started!")
        reset_filter(None)


def reset_filter(event):
    global particle_filter
    particle_filter = pf.ParticleFilter(prior_distribution, particle_count=10000)
    ui.draw_bots(canvas, bot, particle_filter.particles)


STEPS_BETWEEN_MEASUREMENTS = 10
blind_steps = 0

GOAL_RADIUS = 2
GOAL_PROPORTION_NEEDED = .8
SAFETY_BUFFER = .5


def step(event):
    global done, blind_steps, should_filter_reset
    if done:
        return

    if grid.occupancy[int(bot[0])][int(bot[1])] == 1:
        instructions_text.set("CRASH! Please try again")
        done = True
        return

    if should_filter_reset:
        reset_filter(None)
        should_filter_reset = False
        return

    for particle in particle_filter.particles:
        y, x = int(particle[0]), int(particle[1])
        if grid.occupancy[y][x] == 1:
            instructions_text.set("Particle in wall! Stopping to measure.")
            measure()
            return

    goal_proportion = 1. * sum([math.sqrt((goal[0] - particle[0]) ** 2 + (goal[1] - particle[1]) ** 2) < GOAL_RADIUS \
                                for particle in particle_filter.particles]) / len(particle_filter.particles)

    if goal_proportion > GOAL_PROPORTION_NEEDED:
        instructions_text.set("I think we're there!")
        done = True
    elif blind_steps > STEPS_BETWEEN_MEASUREMENTS:
        instructions_text.set("It's been a while since we measured. Let's do that.")
        measure()
    else:
        instructions_text.set("Forging ahead!")
        move()


def move():
    ui.clear_measurement(canvas)
    global bot, blind_steps, should_filter_reset
    blind_steps += 1
    direction = vote()
    bot = movement_model(bot, direction, .1, 0)
    particle_filter.move(direction, movement_model)
    ui.draw_bots(canvas, bot, particle_filter.particles)
    measurement = make_measurement(bot, grid, variance=1)
    if min(measurement) <= SAFETY_BUFFER:
        instructions_text.set("I'm awfully close to a wall. Lemme reset the filter.")
        should_filter_reset = True


def measure():
    global blind_steps
    blind_steps = 0
    measurement = make_measurement(bot, grid, variance=1)
    particle_filter.measure(measurement, measurement_likelihood)
    ui.draw_bots(canvas, bot, particle_filter.particles)
    ui.draw_measurement(canvas, bot, measurement)


reset_button.bind("<Button-1>", reset_filter)
restart_button.bind("<Button-1>", reset_goal)
step_button.bind("<Button-1>", step)
preprocess_button.bind("<Button-1>", grid.preprocess)

canvas.bind("<Button-1>", on_click)
root.bind("f", measure)
root.bind("r", reset_goal)
root.bind("s", step)
root.bind("p", grid.preprocess)

particle_filter = None

reset_goal(None)

mainloop()
