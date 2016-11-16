import math
import random
from Tkinter import *

from PIL import Image, ImageTk

import algorithms.ParticleFilter as pf
import maps.OccupancyGrid as og

MAX_RANGE = 20

HIT_VARIANCE = 10
MOVEMENT_VARIANCE = .1

grid = og.OccupancyGrid("maps/map.png", 0, 0)


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


# def movement_model(position, intended_movement):
#     return omm.sample_motion_model(position, intended_movement[0], intended_movement[1])

def movement_model(position, intended_movement):
    distance = math.sqrt(intended_movement[0] ** 2 + intended_movement[1] ** 2)
    x = position[0] + intended_movement[0] + distance * random.normalvariate(0, MOVEMENT_VARIANCE)
    y = position[1] + intended_movement[1] + distance * random.normalvariate(0, MOVEMENT_VARIANCE)

    return (x, y)


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

reset_button = Button(button_frame, text="Reset")
reset_button.pack(side=RIGHT)
measure_button = Button(button_frame, text="Measure")
measure_button.pack(side=RIGHT)
preprocess_button = Button(button_frame, text="Preprocess")
preprocess_button.pack(side=RIGHT)

BOT_RADIUS = 5
GUESS_RADIUS = 1
BOT_TAG = "bot"
MEASUREMENT_TAG = "measure"


def draw_bots(real_bot, guesses=None):
    if guesses is None:
        guesses = []
    canvas.delete(BOT_TAG)

    for guess in guesses:
        canvas.create_oval(
            3 * guess[1] - GUESS_RADIUS,
            3 * guess[0] - GUESS_RADIUS,
            3 * guess[1] + GUESS_RADIUS,
            3 * guess[0] + GUESS_RADIUS,
            tags=BOT_TAG,
            fill="green")

    canvas.create_oval(3 * real_bot[1] - BOT_RADIUS,
                       3 * real_bot[0] - BOT_RADIUS,
                       3 * real_bot[1] + BOT_RADIUS,
                       3 * real_bot[0] + BOT_RADIUS,
                       tags=BOT_TAG,
                       fill="red")


def draw_measurement(bot, measurement):
    canvas.delete(MEASUREMENT_TAG)
    canvas.create_line(3 * bot[1], 3 * bot[0],
                       3 * bot[1] + 3 * measurement[0],
                       3 * bot[0],
                       tags=MEASUREMENT_TAG,
                       fill="purple"
                       )

    canvas.create_line(3 * bot[1], 3 * bot[0],
                       3 * bot[1] + 3 * measurement[1] / math.sqrt(2),
                       3 * bot[0] - 3 * measurement[1] / math.sqrt(2) + 3,
                       tags=MEASUREMENT_TAG,
                       fill="purple"
                       )

    canvas.create_line(3 * bot[1], 3 * bot[0],
                       3 * bot[1],
                       3 * bot[0] - 3 * measurement[2] + 3,
                       tags=MEASUREMENT_TAG,
                       fill="purple"
                       )

    canvas.create_line(3 * bot[1], 3 * bot[0],
                       3 * bot[1] - 3 * measurement[3] / math.sqrt(2) + 3,
                       3 * bot[0] - 3 * measurement[3] / math.sqrt(2) + 3,
                       tags=MEASUREMENT_TAG,
                       fill="purple"
                       )

    canvas.create_line(3 * bot[1], 3 * bot[0],
                       3 * bot[1] - 3 * measurement[4] + 3,
                       3 * bot[0],
                       tags=MEASUREMENT_TAG,
                       fill="purple"
                       )

    canvas.create_line(3 * bot[1], 3 * bot[0],
                       3 * bot[1] - 3 * measurement[5] / math.sqrt(2) + 3,
                       3 * bot[0] + 3 * measurement[5] / math.sqrt(2),
                       tags=MEASUREMENT_TAG,
                       fill="purple"
                       )

    canvas.create_line(3 * bot[1], 3 * bot[0],
                       3 * bot[1],
                       3 * bot[0] + 3 * measurement[6],
                       tags=MEASUREMENT_TAG,
                       fill="purple"
                       )

    canvas.create_line(3 * bot[1], 3 * bot[0],
                       3 * bot[1] + 3 * measurement[7] / math.sqrt(2),
                       3 * bot[0] + 3 * measurement[7] / math.sqrt(2),
                       tags=MEASUREMENT_TAG,
                       fill="purple"
                       )


def on_click(event):
    global bot

    event_location = event.y / 3, event.x / 3

    particle_filter.move((event_location[0] - bot[0], event_location[1] - bot[1]), movement_model)
    bot = event_location
    draw_bots(bot, particle_filter.particles)

    measurement = make_measurement(bot, grid, variance=0)
    draw_measurement(bot, measurement)


def reset(event):
    global particle_filter
    particle_filter = pf.ParticleFilter(prior_distribution, particle_count=1000)
    draw_bots(bot, particle_filter.particles)


def measure(event):
    measurement = make_measurement(bot, grid, variance=0)
    particle_filter.measure(measurement, measurement_likelihood)
    draw_bots(bot, particle_filter.particles)
    print measurement

    draw_measurement(bot, measurement)


def preprocess_grid(event):
    for y in xrange(grid.occupancy.shape[0]):
        for x in xrange(grid.occupancy.shape[1]):
            grid.eight_way_measurement((y, x))


reset_button.bind("<Button-1>", reset)
canvas.bind("<Button-1>", on_click)
measure_button.bind("<Button-1>", measure)
preprocess_button.bind("<Button-1>", preprocess_grid)

root.bind("r", reset)
root.bind("m", measure)

bot = (80, 100, 0)
particle_filter = None

reset(None)

mainloop()
