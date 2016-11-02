import math
import random
from Tkinter import *

from PIL import Image, ImageTk



# Window set up

pilImage = Image.open("maps/map.png")
pilImage = pilImage.resize((pilImage.width * 3, pilImage.height * 3), Image.NEAREST)
root = Tk()
canvas = Canvas(root, width=pilImage.width, height=pilImage.height)
canvas.pack()

image = ImageTk.PhotoImage(pilImage)
imagesprite = canvas.create_image(0, 0, image=image, anchor=NW)

frame = Frame()
frame.pack(fill=X)


instructions_text = StringVar()
Label(frame,textvariable = instructions_text).pack(side=LEFT)


reset_button = Button(frame, text="Restart")
reset_button.pack(side=RIGHT)



instructions_text.set("Welcoem to ")



# reset_button.bind("<Button-1>", reset)
# canvas.bind("<Button-1>", on_click)
# measure_button.bind("<Button-1>", measure)

mainloop()
