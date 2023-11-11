# Import the required libraries
from tkinter import *

# Create an instance of tkinter frame or window
win = Tk()

# Set the size of the window
win.geometry("700x350")

# Create a canvas widget
canvas = Canvas(win)
canvas.pack()

def on_button_pressed(event):
   start_x = canvas.canvasx(event.x)
   start_y = canvas.canvasy(event.y)
   print("start_x, start_y =", start_x, start_y)

def on_button_motion(event):
   end_x = canvas.canvasx(event.x)
   end_y = canvas.canvasy(event.y)
   print("end_x, end_y=", end_x, end_y)

# Bind the canvas with Mouse buttons
canvas.bind("<Button-1>", on_button_pressed)
canvas.bind("<Button1-Motion>", on_button_motion)

# Add a Label widget in the window
Label(win, text="Move the Mouse Pointer and click " "anywhere on the Canvas").pack()

win.mainloop()