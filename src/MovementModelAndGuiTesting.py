import math
from Tkinter import *

from PIL import Image, ImageTk

import movement.OdometryMovementModel as omm

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
                       tags = BOT_TAG)

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
    new_bots = [omm.sample_motion_model_no_final_rotation(bot, (event.x, event.y)) for _ in xrange(100)]
    bot = omm.target_rotation(bot, (event.x, event.y))

    draw_bots(bot, new_bots)


def reset(event):
    bot = (100, 100, 0)
    draw_bots(bot)


reset_button.bind("<Button-1>", reset)
canvas.bind("<Button-1>", on_click)

mainloop()
