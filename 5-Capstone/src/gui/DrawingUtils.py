import math

BOT_TAG = "bots"
MEASUREMENT_TAG = "measurement"
GOAL_TAG = "goal"


def clear_all(canvas):
    clear_bots(canvas)
    clear_measurement(canvas)
    clear_goal(canvas)


def clear_bots(canvas):
    canvas.delete(BOT_TAG)


def draw_bots(canvas, real_bot, guesses=None, scale=3, bot_radius=5, guess_radius=1):
    if guesses is None:
        guesses = []
    clear_bots(canvas)

    for guess in guesses:
        canvas.create_oval(
            scale * guess[1] - guess_radius,
            scale * guess[0] - guess_radius,
            scale * guess[1] + guess_radius,
            scale * guess[0] + guess_radius,
            tags=BOT_TAG,
            fill="yellow")

    canvas.create_oval(scale * real_bot[1] - bot_radius,
                       scale * real_bot[0] - bot_radius,
                       scale * real_bot[1] + bot_radius,
                       scale * real_bot[0] + bot_radius,
                       tags=BOT_TAG,
                       fill="green")


def clear_goal(canvas):
    canvas.delete(GOAL_TAG)


def draw_goal(canvas, location, scale=3, radius=5):
    clear_bots(canvas)
    canvas.create_oval(scale * location[1] - radius,
                       scale * location[0] - radius,
                       scale * location[1] + radius,
                       scale * location[0] + radius,
                       tags=GOAL_TAG,
                       fill="red")


def clear_measurement(canvas):
    canvas.delete(MEASUREMENT_TAG)


def draw_measurement(canvas, bot, measurement, scale=3):
    clear_measurement(canvas)
    canvas.create_line(scale * bot[1], scale * bot[0],
                       scale * bot[1] + scale * measurement[0],
                       scale * bot[0],
                       tags=MEASUREMENT_TAG,
                       fill="purple"
                       )

    canvas.create_line(scale * bot[1], scale * bot[0],
                       scale * bot[1] + scale * measurement[1] / math.sqrt(2),
                       scale * bot[0] - scale * measurement[1] / math.sqrt(2) + scale,
                       tags=MEASUREMENT_TAG,
                       fill="purple"
                       )

    canvas.create_line(scale * bot[1], scale * bot[0],
                       scale * bot[1],
                       scale * bot[0] - scale * measurement[2] + scale,
                       tags=MEASUREMENT_TAG,
                       fill="purple"
                       )

    canvas.create_line(scale * bot[1], scale * bot[0],
                       scale * bot[1] - scale * measurement[scale] / math.sqrt(2) + scale,
                       scale * bot[0] - scale * measurement[scale] / math.sqrt(2) + scale,
                       tags=MEASUREMENT_TAG,
                       fill="purple"
                       )

    canvas.create_line(scale * bot[1], scale * bot[0],
                       scale * bot[1] - scale * measurement[4] + scale,
                       scale * bot[0],
                       tags=MEASUREMENT_TAG,
                       fill="purple"
                       )

    canvas.create_line(scale * bot[1], scale * bot[0],
                       scale * bot[1] - scale * measurement[5] / math.sqrt(2) + scale,
                       scale * bot[0] + scale * measurement[5] / math.sqrt(2),
                       tags=MEASUREMENT_TAG,
                       fill="purple"
                       )

    canvas.create_line(scale * bot[1], scale * bot[0],
                       scale * bot[1],
                       scale * bot[0] + scale * measurement[6],
                       tags=MEASUREMENT_TAG,
                       fill="purple"
                       )

    canvas.create_line(scale * bot[1], scale * bot[0],
                       scale * bot[1] + scale * measurement[7] / math.sqrt(2),
                       scale * bot[0] + scale * measurement[7] / math.sqrt(2),
                       tags=MEASUREMENT_TAG,
                       fill="purple"
                       )
