# Importing needed modules
import tkinter as tk
import tkinter.messagebox
import tkinter.ttk as ttk
import os # for reading image files
import random # for selecting random question
import math # for rounding
import colorsys # for colouring the countdown bar
from threading import Lock
# Setting up constants
TITLEFONT = ('Segoe Print',32,'bold'); ANSFONT = ('Segoe Print',24,'bold'); FONT  = ('Segoe Print',16)
BUTTONWIDTH = 0.15;BUTTONHEIGHT = 0.15
COLOURS = ['gray', 'lightgreen','pink','blue','orange','purple']
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
    dir = os.path.dirname(__file__) # Gets the path of where the program is
    filename = os.path.join(dir, 'Images',"TkIcon.ico") # Gets the path of where the images are stored.
    self.iconbitmap(filename)

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
      # Back Button to get back to the MainMenu
      back = get_image('back_button.png')
      back_button = tk.Button(self,command=lambda: master.switch_frame(mainMenu)
      , image=back,borderwidth=0)
      back_button.place(relx = (5/6),rely=0.9,anchor='center')
      back_button.img = back
      self.score = 0
      self.MathGame()
      self.Tetris_Game()
      self.GameOverRun = False


    # Randomly Selects a Math Question from the questions list appended from the csv
    def NewQuestion(self):
      if not self.penalty:
        if len(self.questions) > 0: # If there is still item inside list
          randomquestion = random.choice(self.questions) # Select random question
          self.Display.config(text=randomquestion[0]) # Display it on the window
          ORIGINALrandomquestion = randomquestion
          self.countdown(self.tempquestiontimer)

          # Answer Buttons
          print(randomquestion[1])
          self.Buttons[0].config(text=randomquestion[1],command=lambda:self.CorrectAns())
          randomquestion.remove(randomquestion[1])
          randomquestion.remove(randomquestion[0])
          ButtonInfo = random.sample([[1,1,'#93c47d'],[1,2,'#e06666'],[2,1,'#6fa8dc'],[2,2,'#f1c232']],4)
          for i in range(0,4):
            if i > 0:
              randomAnswer = random.choice(randomquestion)
              randomquestion.remove(randomAnswer)
              self.Buttons[i].config(text=randomAnswer,command=lambda:self.WrongAns())
            self.Buttons[i].config(bg=ButtonInfo[i][2],font=ANSFONT)
            self.Buttons[i].place(relx=0.525+(0.15*int(ButtonInfo[i][0])),rely=0.35+0.15*int(ButtonInfo[i][1]),anchor='center',relheight=BUTTONHEIGHT,relwidth=BUTTONWIDTH)
            
          self.questions.remove(ORIGINALrandomquestion) # Remove it from list to prevent it from displaying again
          
        else:
          # TEMP MAKE IT READ FROM THE TOPIC THAT PLAYER CHOSE
          self.questions = readcsv('sampleQuestion.csv')
          print('looping')
          self.NewQuestion()

    def CorrectAns(self):
      self.after_cancel(self.tick)
      self.score += 1
      
      self.NewQuestion()
    def WrongAns(self):
      def callback():
        if not self.tetris.game_over:
          for i in range(0,4):
            self.Buttons[i]["state"] = "normal"
      for i in range(0,4):
        self.Buttons[i]["state"] = "disabled"
        self.wronganswer = self.after(self.tempquestiontimer*250,callback)
    
    def MathGame(self):
      #### Temporary ####################################################################################################
      self.questions = readcsv('sampleQuestion.csv') # Gets a list from the csv file 'test_sampleQuestions.csv'        ##
      # Button (temp) which generates new math questions                                                               ##
      self.tempquestiontimer = 10 # seconds                                                                            ##
      ###################################################################################################################
      self.penalty = False
      self.score_label = tk.Label(self,font=FONT)
      self.score_label.place(anchor='center',relx = 7/12,rely=0.9)
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
      self.NewQuestion()
    # Countdown for mathgame
    def countdown(self, remaining = None):
      if remaining is not None:
        self.remaining = remaining
      if self.remaining <= 0:
        self.countdownTimer['value']=self.tempquestiontimer
        self.countdownLabel.configure(text='Times Up')
        self.tetris.game_over = True
        
        self.flashingBar() # flash bar green and red after time is up
      else:
        # colour = (math.floor(255-(self.remaining/100*255)),math.floor(self.remaining/100*255),0)
        colour = colorsys.hsv_to_rgb(self.remaining/(self.tempquestiontimer*4),1.0,1.0) # green to red gradient
        self.s.configure("timer.Horizontal.TProgressbar",background=self.htmlcolor(colour[0],colour[1],colour[2])) 

        # Changes the progress bar ad the label to display the remaining time
        self.countdownTimer.configure(style ="timer.Horizontal.TProgressbar")
        self.countdownLabel.configure(text="Remaining Time: %g" % math.ceil(self.remaining))
        self.countdownTimer['value']=self.remaining
        self.remaining = self.remaining - 0.01 # decrement the time
        self.tick = self.after(10, self.countdown) # repeats the function after 10 milliseconds (0.01 seconds)

    # Changes the colour of the bar every 1 second after time is up.
    def flashingBar(self):
      try:
        self.BarColour
      except:
        self.BarColour = 'red'
      if self.BarColour == 'green':
        self.BarColour = 'red'
      elif self.BarColour == 'red':
        self.BarColour = 'green'
      self.s.configure("timer.Horizontal.TProgressbar",background=self.BarColour)
      for i in range(0,4):
        self.Buttons[i]["state"] = "disabled"
      self.after_cancel(self.tick)
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

    def Tetris_Game(self):
      self.tetris = Tetris()
      self.create_widgets()
      self.update_clock()
    def update_clock(self):
      if not self.tetris.game_over:
        self.tetris.move(1,0)
        self.update()
        self.after(int(1000*(0.9**self.score)),self.update_clock)
    def create_widgets(self):
      PIECE_SIZE = 33
      self.canvas = tk.Canvas(self,height=PIECE_SIZE * self.tetris.FIELD_HEIGHT
                                  ,width=PIECE_SIZE * self.tetris.FIELD_WIDTH
                                  ,bg='black')
      self.canvas.focus_set()

      ## ARROW KEYS
      self.canvas.bind("<Left>",lambda _:(self.tetris.move(0,-1),self.update()))
      self.canvas.bind("<Right>",lambda _:(self.tetris.move(0,1),self.update()))
      self.canvas.bind("<Down>",lambda _:(self.tetris.move(1,0),self.update()))
      self.canvas.bind("<Up>",lambda _:(self.tetris.rotate(),self.update()))

      ## WASD KEYS
      self.canvas.bind("a",lambda _:(self.tetris.move(0,-1),self.update()))
      self.canvas.bind("d",lambda _:(self.tetris.move(0,1),self.update()))
      self.canvas.bind("s",lambda _:(self.tetris.move(1,0),self.update()))
      self.canvas.bind("w",lambda _:(self.tetris.rotate(),self.update()))

      self.rectangles = [
      self.canvas.create_rectangle(c*PIECE_SIZE,r*PIECE_SIZE
                                  ,(c+1)*PIECE_SIZE,(r+1)*PIECE_SIZE,outline='white')
          for r in range(self.tetris.FIELD_HEIGHT) for c in range(self.tetris.FIELD_WIDTH)
      ]
      self.canvas.place(anchor="center",relx=0.25,rely=0.5)
      self.update()

    def update(self):
      if not self.tetris.game_over:
        for i, _id in enumerate(self.rectangles):
          colour_num = self.tetris.get_colour(i // self.tetris.FIELD_WIDTH,i % self.tetris.FIELD_WIDTH)
          self.canvas.itemconfig(_id,fill=COLOURS[colour_num])
      else:
        if not self.GameOverRun:
          self.after_cancel(self.tick)
          self.countdownLabel.configure(text='GAME OVER')
          self.countdownTimer['value'] = self.tempquestiontimer
          self.GameOverRun = True
          self.flashingBar()
      self.score_label['text'] = "Score: {}".format(self.score)
     
        
class Tetris():
  FIELD_WIDTH = 10
  FIELD_HEIGHT = 20
  TETROMINOS = [
    [(0,0),(0,1),(1,0),(1,1)], # 0
    [(0,0),(0,1),(1,1),(2,1)], # L
    [(0,1),(1,1),(2,1),(2,0)], # J
    [(0,1),(1,0),(1,1),(2,0)], # Z
    [(0,1),(1,0),(1,1),(2,1)], # T
    [(0,0),(1,0),(1,1),(2,1)], # S
    [(0,1),(1,1),(2,1),(3,1)], # I

  ]
  def __init__(self):
    self.field = [[0 for c in range(Tetris.FIELD_WIDTH)] for r in range(Tetris.FIELD_HEIGHT)]
    self.move_lock = Lock()
    self.reset_tetromino()
    self.game_over = False
  def reset_tetromino(self):
    self.tetromino = random.choice(Tetris.TETROMINOS)[:]
    self.tetromino_colour = random.randint(1,len(COLOURS)-1)
    self.tetromino_offset = [-2,Tetris.FIELD_WIDTH//2]
    self.game_over = any(not self.is_cell_free(r,c) for (r,c) in self.get_tetromino_coords())
  
  def get_tetromino_coords(self):
    return [(r + self.tetromino_offset[0], c + self.tetromino_offset[1]) for r,c in self.tetromino]

  def apply_tetromino(self):
    for (r,c) in self.get_tetromino_coords():
      self.field[r][c] = self.tetromino_colour
    new_field = [row for row in self.field if any(tile == 0 for tile in row)]
    lines_eliminated = len(self.field) - len(new_field)
    self.field = [[0]*Tetris.FIELD_WIDTH for x in range(lines_eliminated)] + new_field
    self.reset_tetromino()
    
  def get_colour(self,r,c):
    return self.tetromino_colour if (r,c) in self.get_tetromino_coords() else self.field[r][c]
  
  def is_cell_free(self,r,c):
    return r < Tetris.FIELD_HEIGHT and 0 <= c < Tetris.FIELD_WIDTH and (r< 0 or self.field[r][c] == 0)

  def move(self,dr,dc):
    with self.move_lock:
      if self.game_over:
        return 
      if all(self.is_cell_free(r + dr,c + dc) for r,c in self.get_tetromino_coords()):
        self.tetromino_offset = [self.tetromino_offset[0] + dr, self.tetromino_offset[1] + dc]
      elif dr == 1 and dc == 0:
        self.game_over = any(r < 0 for (r,c) in self.get_tetromino_coords())
        if not self.game_over:
          self.apply_tetromino()

  def rotate(self):
    with self.move_lock:
      if self.game_over:
        return
      ys = [r for (r,c) in self.tetromino]
      xs = [c for (r,c) in self.tetromino]
      size = max(max(ys) - min(ys),max(xs)-min(xs))
      rotated_tetromino = [(c,size - r) for (r,c) in self.tetromino]
      wallkick_offset = self.tetromino_offset[:]
      tetromino_coord = [(r+self.tetromino_offset[0],c+self.tetromino_offset[1]) for r,c in rotated_tetromino]
      min_x = min(c for r,c in tetromino_coord)
      max_x = max(c for r,c in tetromino_coord)
      max_y = max(r for r,c in tetromino_coord)
      wallkick_offset[1] -= min(0,min_x)
      wallkick_offset[1] += min(0,Tetris.FIELD_WIDTH - (1+max_x))
      wallkick_offset[0] += min(0,Tetris.FIELD_HEIGHT - (1+max_y))
      tetromino_coord = [(r+wallkick_offset[0],c+wallkick_offset[1]) for r,c in rotated_tetromino]
      if all(self.is_cell_free(r,c) for r,c in tetromino_coord):
        self.tetromino, self.tetromino_offset= rotated_tetromino, wallkick_offset

        

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