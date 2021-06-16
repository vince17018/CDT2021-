#Import all the necessary libraries
from tkinter import *
import os
import random
dir = os.path.dirname(__file__)
filename = os.path.join(dir, '..','Images',"clickme.png")
#Define the tkinter instance
win= Tk()
win.title("Rounded Button")

#Define the size of the tkinter frame
win.geometry("600x600")

#Define the working of the button

def my_command():
    print("jsadksa")
    #button.configure(width=500)
    #button.after(500,lambda:my_command())
    



#Import the image using PhotoImage function
click_btn= PhotoImage(file=filename)

#Let us create a label for button event
#img_label= Label(image=click_btn)

#Let us create a dummy button and pass the image
button= Label(win, image=click_btn,command= my_command(),
borderwidth=0)
button.place(relx = 0.5,rely=0.5,anchor='center')



win.mainloop()