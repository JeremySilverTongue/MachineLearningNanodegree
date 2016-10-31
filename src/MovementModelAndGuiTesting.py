import math
import random
from Tkinter import *

from PIL import Image, ImageTk

import algorithms.ParticleFilter as pf
import maps.OccupancyGrid as og
import movement.OdometryMovementModel as omm

MAX_RANGE = 500

HIT_VARIANCE = 20

grid = og.OccupancyGrid("maps/map.png")


def sample_measurement_distribution(actual_range, variance=HIT_VARIANCE):
    measurement = min(random.normalvariate(actual_range, variance), MAX_RANGE)
    return max(0, measurement)


def make_measurement(position, grid, img=None, variance=HIT_VARIANCE):
    true_measurement = grid.eight_way_measurement(position, max_range=MAX_RANGE, img=img)
    return [sample_measurement_distribution(measurement, variance) for measurement in true_measurement]


def range_likelihood(true_range, measurement):
    return 1 / math.sqrt(2 * math.pi * HIT_VARIANCE) * math.exp(-1 / 2 * (true_range - measurement) ** 2 / HIT_VARIANCE)


def measurement_likelihood(measurement, position):
    true_ranges = grid.eight_way_measurement((int(position[0]/3), int(position[1]/3)))
    return reduce(lambda a, b: a * b,
                  [range_likelihood(true_ranges[i], measurement[i]) for i in xrange(len(measurement))])


def prior_distribution():
    return random.randint(0, grid.occupancy.shape[0] - 1), random.randint(0, grid.occupancy.shape[1] - 1), 0


def movement_model(position, intended_movement):
    return omm.sample_motion_model_no_final_rotation(position, intended_movement)


filter = pf.ParticleFilter(prior_distribution)

# Window set up

pilImage = Image.open("maps/map.png")
pilImage = pilImage.resize((pilImage.width * 3, pilImage.height * 3), Image.NEAREST)
root = Tk()
canvas = Canvas(root, width=pilImage.width, height=pilImage.height)
canvas.pack()

image = ImageTk.PhotoImage(pilImage)
imagesprite = canvas.create_image(0, 0, image=image, anchor=NW)

reset_button = Button(root, text="Reset")
reset_button.pack()

bot = (100, 100, 0)

BOT_RADIUS = 10
GUESS_RADIUS = 1
BOT_TAG = "bot"


def draw_bots(real_bot, guesses=None):
    if guesses is None:
        guesses = []
    canvas.delete(BOT_TAG)
    canvas.create_oval(real_bot[0] - BOT_RADIUS, real_bot[1] - BOT_RADIUS, real_bot[0] + BOT_RADIUS,
                       real_bot[1] + BOT_RADIUS,
                       tags=BOT_TAG,
                       fill="red")

    canvas.create_line(real_bot[0],
                       real_bot[1],
                       real_bot[0] + 2 * BOT_RADIUS * math.cos(real_bot[2]),
                       real_bot[1] + 2 * BOT_RADIUS * math.sin(real_bot[2]),
                       tags=BOT_TAG)

    for guess in guesses:
        canvas.create_oval(
            guess[0] - GUESS_RADIUS,
            guess[1] - GUESS_RADIUS,
            guess[0] + GUESS_RADIUS,
            guess[1] + GUESS_RADIUS,
            tags=BOT_TAG,
            fill="green"
        )


def on_click(event):
    global bot
    bot = omm.target_rotation(bot, (event.x, event.y))

    filter.move((event.x, event.y), movement_model)

    measurement = grid.eight_way_measurement((int(bot[0]/3), int(bot[1]/3)))
    filter.measure(measurement, measurement_likelihood)

    draw_bots(bot, filter.particles)


def reset(event):
    filter = pf.ParticleFilter(prior_distribution)
    draw_bots(bot, filter.particles)


reset_button.bind("<Button-1>", reset)
canvas.bind("<Button-1>", on_click)

mainloop()
