# Importing needed modules
import tkinter as tk
import tkinter.messagebox
import tkinter.ttk as ttk
import os # for reading image files
import random # for selecting random question
import math # for rounding
import colorsys # for colouring the countdown bar
# Setting up constants
TITLEFONT = ('Segoe Print',32,'bold'); FONT = ('Segoe Print',16)
BUTTONWIDTH = 0.15
BUTTONHEIGHT = 0.15
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
    line = line.replace('"','')
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
      title = get_image('Tketris_title.png')
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
      if len(self.questions) > 0: # If there is still item inside list
        randomquestion = random.choice(self.questions) # Select random question
        print("random something:",randomquestion)
        self.Display.config(text=randomquestion[0]) # Display it on the window
        ORIGINALrandomquestion = randomquestion

        # Answer Buttons
        
        self.Buttons[0].config(text=randomquestion[1])
        randomquestion.remove(randomquestion[1])
        randomquestion.remove(randomquestion[0])
        ButtonPos = random.sample([[1,1],[1,2],[2,1],[2,2]],4)
        print(ButtonPos)
        for i in range(0,4):
          if i > 0:
            randomAnswer = random.choice(randomquestion)
            randomquestion.remove(randomAnswer)
            self.Buttons[i].config(text=randomAnswer)

          self.Buttons[i].place(relx=0.5+(0.15*int(ButtonPos[i][0])),rely=0.35+0.15*int(ButtonPos[i][1]),anchor='center',relheight=BUTTONHEIGHT,relwidth=BUTTONWIDTH)
          
        self.questions.remove(ORIGINALrandomquestion) # Remove it from list to prevent it from displaying again
          
      else:
        ## temporary, show no more buttons ###################################
        tk.Label(self,text="No more questions").place(relx=0.5,rely=0.5)
        print("No more questions")
    
    def MathGame(self):
      #### Temporary ####################################################################################################
      self.questions = readcsv('test_sampleQuestions.csv') # Gets a list from the csv file 'test_sampleQuestions.csv'  ##
      # Button (temp) which generates new math questions                                                               ##
      generatemathquestion = tk.Button(self,text='Generate New Problem',command=lambda:self.NewQuestion())             ##
      generatemathquestion.place(relx=0.6,rely=0.9,anchor='center')                                                    ##
      self.tempquestiontimer = 15 # seconds                                                                            ##
      ###################################################################################################################

      # Initialize Buttons
      self.Buttons = {}
      self.Buttons[0] = tk.Button(self)
      for i in range(1,4):
        self.Buttons[i] = tk.Button(self)

      # Display for the Math Game (Where the questions are displayed)
      self.Display = tk.Label(self, text="Game here",font=TITLEFONT)
      self.Display.place(relx=0.75, rely=0.3, anchor="center")
      # Countdown Timer
      self.s = ttk.Style()
      self.s.theme_use('clam')
      self.countdownTimer = ttk.Progressbar(self,style="timer.Horizontal.TProgressbar"
                                            ,orient='horizontal',length=500,mod='determinate')
      self.countdownTimer.place(relx=0.75,rely=0.1,anchor='center')
      self.countdownLabel = tk.Label(self,text='',width=20)
      self.countdownLabel.place(relx=0.75,rely=0.05,anchor='center')
      self.countdownTimer['maximum'] = self.tempquestiontimer
      self.countdown(self.tempquestiontimer) # Starts Countdown 
      
    # Countdown for mathgame
    def countdown(self, remaining = None):
      if remaining is not None:
        self.remaining = remaining
      if self.remaining <= 0:
        self.countdownTimer['value']=self.tempquestiontimer
        self.countdownLabel.configure(text='Times Up')
        self.BarColour = 'green'
        self.flashingBar() # flash bar green and red after time is up
      else:
        # colour = (math.floor(255-(self.remaining/100*255)),math.floor(self.remaining/100*255),0)
        colour = colorsys.hsv_to_rgb(self.remaining/(self.tempquestiontimer*4),1.0,1.0) # green to red gradient
        self.s.configure("timer.Horizontal.TProgressbar",background=self.htmlcolor(colour[0],colour[1],colour[2])) 

        # Changes the progress bar ad the label to display the remaining time
        self.countdownTimer.configure(style="timer.Horizontal.TProgressbar")
        self.countdownLabel.configure(text="Remaining Time: %g" % math.ceil(self.remaining))
        self.countdownTimer['value']=self.remaining
        self.remaining = self.remaining - 0.01 # decrement the time
        self.countingdown = self.after(10, self.countdown) # repeats the function after 10 milliseconds (0.01 seconds)

    # Changes the colour of the bar every 1 second after time is up. 
    def flashingBar(self):
      if self.BarColour == 'green':
        self.BarColour = 'red'
      elif self.BarColour == 'red':
        self.BarColour = 'green'
      self.s.configure("timer.Horizontal.TProgressbar",background=self.BarColour)
      self.after(1000,self.flashingBar)

    def htmlcolor(self,r, g, b):
      def _chkarg(a):
          if isinstance(a, int): # clamp to range 0--255
              if a < 0:
                  a = 0
              elif a > 255:
                  a = 255
          elif isinstance(a, float): # clamp to range 0.0--1.0 and convert to integer 0--255
              if a < 0.0:
                  a = 0
              elif a > 1.0:
                  a = 255
              else:
                  a = int(round(a*255))
          else:
              raise ValueError('Arguments must be integers or floats.')
          return a
      r = _chkarg(r)
      g = _chkarg(g)
      b = _chkarg(b)
      return '#{:02x}{:02x}{:02x}'.format(r,g,b)
  

    def TetrisGame(self):
      pass
      
# Option Menu
class Options(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.OptionLabel = tk.Label(self, text="Options Page",font=TITLEFONT).place(relx=0.5, rely=0.3, anchor="center")
        tk.Button(self, text="Return to main menu",
                  command=lambda:Options.updateSettings(self,master),font=FONT).place(relx=0.5, rely=0.5, anchor="center"
                  ,relheight=BUTTONHEIGHT, relwidth=BUTTONWIDTH)
        self.difficulty = tk.StringVar(self)
        self.difficulty.set("Normal") # Defualt Value
        difficultyMenu = tk.OptionMenu(self,self.difficulty,"Easy","Normal","Hard")
        difficultyMenu.config(width=50)
        difficultyMenu.place(relx=0.25,rely=0.8,anchor="center")
    def updateSettings(self,master):
      master.switch_frame(mainMenu)
      currentDifficulty = self.difficulty.get()
      print(currentDifficulty)


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