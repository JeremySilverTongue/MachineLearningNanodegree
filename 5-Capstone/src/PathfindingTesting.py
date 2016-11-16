from Tkinter import *

from PIL import Image, ImageTk

import algorithms.Navigation as nav
from maps.OccupancyGrid import OccupancyGrid

pilImage = Image.open("maps/map.png")
pilImage = pilImage.resize((pilImage.width * 3, pilImage.height * 3), Image.NEAREST)
root = Tk()
root.wm_title("Navigation testing")
canvas = Canvas(root, width=pilImage.width, height=pilImage.height)
canvas.pack()

image = ImageTk.PhotoImage(pilImage)
imagesprite = canvas.create_image(0, 0, image=image, anchor=NW)

frame = Frame()
frame.pack(fill=X)

instructions_text = StringVar()
Label(frame, textvariable=instructions_text).pack(side=LEFT)

set_goal_button = Button(frame, text="Set Goal")
set_goal_button.pack(side=RIGHT)

setting_goal = True
goal = None

PATH_TAG = "path"
GOAL_TAG = "goal"

RADIUS = 5

grid = OccupancyGrid("maps/map.png")
plan = []


def begin_setting_goal(event):
    canvas.delete(GOAL_TAG)
    canvas.delete(PATH_TAG)
    global setting_goal
    setting_goal = True
    instructions_text.set("Click to set the goal location")


def on_click(event):
    location = int(event.y / 3), int(event.x / 3)
    global goal, setting_goal, plan
    if setting_goal:
        goal = location
        setting_goal = False
        instructions_text.set("Coming up with a new plan of attack!")
        plan = nav.process_grid(goal, grid.occupancy, grid.danger, danger_weight=100)
        instructions_text.set("Click to see the proposed path!")

        canvas.create_oval(event.x - RADIUS, event.y - RADIUS,
                           event.x + RADIUS, event.y + RADIUS,
                           fill="red",
                           tags=GOAL_TAG
                           )

    else:
        path = nav.get_path(location, plan)
        canvas.delete(PATH_TAG)
        canvas.create_line(list(sum([(3 * x + 1.5, 3 * y + 1.5) for y, x in path], ())), tags=PATH_TAG)
        canvas.create_oval(event.x - RADIUS, event.y - RADIUS,
                           event.x + RADIUS, event.y + RADIUS,
                           fill="green",
                           tags=PATH_TAG
                           )


canvas.bind("<Button-1>", on_click)
set_goal_button.bind("<Button-1>", begin_setting_goal)
root.bind("s", begin_setting_goal)

begin_setting_goal(None)

mainloop()
