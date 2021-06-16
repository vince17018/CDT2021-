from tkinter import *
from PIL import Image, ImageTk

import os
dir = os.path.dirname(__file__) # Gets the path of where the program is
filename = os.path.join(dir, '..','Images','quit_button.png') # Gets the path of where the images are stored.
filename2 = os.path.join(dir, '..','Images','play_button.png')
root = Tk() 

# Create a photoimage object of the image in the path
test1 = ImageTk.PhotoImage(file=filename)
test2 = ImageTk.PhotoImage(file=filename2)
canvas = Canvas(root,width=1280,height=720)
canvas.pack()
canvas.config(bg="blue")
canvas.create_image(200,250,image=test1)
canvas.create_image(150,150,image=test2)
canvas.create_image(100,150,image=test2)
canvas.create_image(200,150,image=test2)
canvas.create_image(250,200,image=test2)
canvas.create_image(250,150,image=test2)
canvas.create_image(100,100,image=test2)



# image2 = Image.open(filename2)
# image2 = image2.convert("RGBA")
# test2 = ImageTk.PhotoImage(image2)

# label2 = Label(image=test2)
# label2.image = test2
#label2.place(x=110,y=120)
root.geometry("1280x720")
root.mainloop()