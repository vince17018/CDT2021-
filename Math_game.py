# Importing needed modules
import tkinter as tk
import tkinter.messagebox
import tkinter.ttk as ttk
import os # for reading image files
import random # for selecting random question
# Setting up constants
TITLEFONT = ('Segoe Print',32,'bold'); FONT = ('Segoe Print',16); BUTTONWIDTH = 0.2; BUTTONHEIGHT = 0.05

import math

def roundup(x):
    return int(math.ceil(x / 10.0))

# Function for reading out of the csv file whichever name you give
# Input: The file name, example: readcsv(TestQuestions.csv)
# Output: a list of all of the items inside the csv
def readcsv(csvname):
  temp_list = [] # Initialize the variable

  dir = os.path.dirname(__file__) # Find the directory of the current file
  filename = os.path.join(dir, 'csv',str(csvname)) # Finds the csv file
  f = open(filename,'r') # opens the csv file
  num_lines = sum(1 for line in open(filename,'r'))
  print("This file has",num_lines-1,"lines")
  line = f.readline()  # Skips the header line
  for i in range(1,num_lines): # for every line after that format and append to list
    line = f.readline()
    line = line.rstrip()
    questions = line.split(",")
    # append detials to list #
    temp_list.append(questions)
  f.close() # close the file
  #print(temp_list)
  return temp_list
# Function for creating image primarly used for the buttons
# Input: The file name, example: getimage(coolPicture.png)
# Output: the image as a PhotoImage variable
# This is able to used inside tkinter function with the 'image' argumnt
def get_image(image):
  dir = os.path.dirname(__file__) # Gets the path of where the program is
  filename = os.path.join(dir, 'Images',str(image)) # Gets the path of where the images are stored.
  img = tk.PhotoImage(file=filename)
  return img
# Quit button function
def close_program():
    # A confirmation whenever the player wants to quit to avoid accidental quits
    if tkinter.messagebox.askyesno("Quit","Would you like to quit?"):
      quit()
# Main App
class Tketris(tk.Tk):
  def __init__(self):
    # Sets up program and switches the frame to mainMenu
    tk.Tk.__init__(self)
    self._frame = None
    self.switch_frame(mainMenu) # Set starting frame
    self.title("Tk.etris")

    # Defines the switch frame function
  def switch_frame(self,frame_class):
    new_frame = frame_class(self)
    # Destroys past frame to save resources
    if self._frame is not None:
        self._frame.destroy()
    self._frame = new_frame
    self._frame.pack(fill="both",expand=True)
# Main Menu window
class mainMenu(tk.Frame): 
  def __init__(self, master):
      tk.Frame.__init__(self, master)
      ############################
      # All Widgets in Main Menu #
      ############################

      # Tketris Title Label
      title = get_image('tketris_title.png')
      title_label = tk.Label(self,image=title,borderwidth=0)
      title_label.place(relx=0.5,rely=0.2,anchor='center')
      title_label.img = title

      # Play Button
      play = get_image('play_button.png')
      play_button = tk.Button(self,command=lambda: master.switch_frame(Game), image=play,borderwidth=0)
      play_button.place(relx = 0.3,rely=0.5,anchor='center')
      play_button.img = play

      # Option Button
      option = get_image('option_button.png')
      option_button = tk.Button(self, command=lambda: master.switch_frame(Options),image=option,borderwidth=0)
      option_button.place(relx = 0.7,rely=0.5,anchor='center')
      option_button.img = option

      # Leaderboard Button
      leaderboard = get_image('leaderboard_button.png')
      leaderboard_button = tk.Button(self, command=lambda: master.switch_frame(Leaderboard),image=leaderboard,borderwidth=0)
      leaderboard_button.place(relx = 0.3,rely=0.8,anchor='center')
      leaderboard_button.img = leaderboard

      # Quit Button
      quit_image = get_image('quit_button.png')
      quit_button = tk.Button(self, command=lambda:quit(),image=quit_image,borderwidth=0)
      quit_button.place(relx = 0.7,rely=0.8,anchor='center')
      quit_button.img = quit_image

# Frame where the game occurs
class Game(tk.Frame):
    def __init__(self, master):
      tk.Frame.__init__(self, master)
      self.MathGame()
      self.TetrisGame()
      # Back Button to get back to the MainMenu
      back = get_image('back_button.png')
      back_button = tk.Button(self,command=lambda: master.switch_frame(mainMenu)
      , image=back,borderwidth=0)
      back_button.place(relx = 0.9,rely=0.9,anchor='center')
      back_button.img = back
    # Randomly Selects a Math Question from the questions list appended from the csv
    def NewQuestion(self):
      if len(self.questions) > 1: # If there is still item inside list
        randomquestion = random.choice(self.questions) # Select random question
        self.Display.config(text=randomquestion[0]) # Display it on the window
        self.questions.remove(randomquestion) # Remove it from list to prevent it from displaying again
        print(len(self.questions))
      else:
        ## temporary, show no more buttons ###################################
        tk.Label(self,text="No more questions").place(relx=0.5,rely=0.5)
        print("No more questions")
    
    def MathGame(self):
      #### Temporary ####################################################################################################
      self.questions = readcsv('test_sampleQuestions.csv') # Gets a list from the csv file 'test_sampleQuestions.csv'  ##
      # Button (temp) which generates new math questions                                                               ##
      generatemathquestion = tk.Button(self,text='Generate New Problem',command=lambda:self.NewQuestion())             ##
      generatemathquestion.place(relx=0.6,rely=0.9,anchor='center')                                                                    ##
      ###################################################################################################################

      # Display for the Math Game (Where the questions are displayed)
      self.Display = tk.Label(self, text="Game here",font=TITLEFONT) 
      self.Display.place(relx=0.75, rely=0.3, anchor="center")
      # Countdown Timer
      s = ttk.Style()
      s.theme_use('clam')
      s.configure("red.Horizontal.TProgressbar",foreground='red',background='red')
      self.countdownTimer = ttk.Progressbar(self,style="red.Horizontal.TProgressbar"
                                            ,orient='horizontal',length=500,mod='determinate')
      self.countdownTimer.place(relx=0.75,rely=0.1,anchor='center')
      self.countdownLabel = tk.Label(self,text='',width=20)
      self.countdownLabel.place(relx=0.75,rely=0.05,anchor='center')
      self.countdown(100)

    def countdown(self, remaining = None):
        if remaining is not None:
          self.remaining = remaining
        if self.remaining <= 0:
          self.countdownTimer['value']=0
          self.countdownLabel.configure(text='Times Up')
        else:
          if self.remaining > 35:
            s = ttk.Style()
            s.theme_use('clam')
            s.configure("green.Horizontal.TProgressbar",foreground='#001000',background='#001000')
            self.countdownTimer.configure(style="green.Horizontal.TProgressbar")
          else:
            self.countdownTimer.configure(style="red.Horizontal.TProgressbar")

          self.countdownLabel.configure(text="Remaining Time: %g" % roundup(self.remaining))
          self.countdownTimer['value']=self.remaining
          self.remaining = self.remaining - 0.01
          self.countingdown = self.after(1, self.countdown)
  
    def TetrisGame(self):
      pass
      
# Option Menu
class Options(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Label(self, text="Options Page",font=TITLEFONT).place(relx=0.5, rely=0.3, anchor="center")
        tk.Button(self, text="Return to main menu",
                  command=lambda: master.switch_frame(mainMenu),font=FONT).place(relx=0.5, rely=0.5, anchor="center"
                  ,relheight=BUTTONHEIGHT, relwidth=BUTTONWIDTH)
# Leaderboard Frame
class Leaderboard(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Label(self, text="Leaderboard Page",font=TITLEFONT).place(relx=0.5, rely=0.3, anchor="center")
        tk.Button(self, text="Return to main menu",
                  command=lambda: master.switch_frame(mainMenu),font=FONT).place(relx=0.5, rely=0.5
                  ,anchor="center",relheight=BUTTONHEIGHT, relwidth=BUTTONWIDTH)

def main():
  app = Tketris()
  app.geometry('1280x720')
  app.resizable(False,False)
  ############################app.protocol("WM_DELETE_WINDOW", close_program)################################################################## Set back when done with program
  app.mainloop()
  

if __name__ == "__main__":
  main()