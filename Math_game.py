# Importing needed modules
import tkinter as tk
import tkinter.messagebox
import tkinter.ttk as ttk
import os # for reading image files
import random # for selecting random question
import math # for rounding
import colorsys # for colouring the countdown bar
from threading import Lock
from fractions import Fraction

# Setting up constants
TITLEFONT = ('Segoe Print',32,'bold'); ANSFONT = ('Segoe Print',24,'bold'); FONT  = ('Segoe Print',16); 
BUTTONWIDTH = 0.15;BUTTONHEIGHT = 0.15;DROPHEIGHT = 1;DROPWIDTH = 20
DROPCOLOUR = 'gray'
COLOURSDEFUALT = ['gray', 'lightgreen','pink','blue','orange','purple']
COLOURS1 = ['gray', '#ED6A5A','#F4F1BB','#9BC1BC','#5CA4A9','#E6EBE0']
COLOURS2 = ['gray', '#EF3E36','#17BEBB','#2E282A','#EDB88B','#FAD8D6']
COLOURS3 = ['gray', '#BFAE48','#5FAD41','#2D936C','#391463','#3A0842']
COLOURS4 = ['gray', '#EDD3C4','#C8ADC0','#7765E3','#3B60E4','#080708']
COLOURS5 = ['gray', '#124E78','#F0F0C9','#F2BB05','#D74E09','#6E0E0A']

TETRISCOLOURS = [COLOURSDEFUALT,COLOURS1,COLOURS2,COLOURS3,COLOURS4,COLOURS5]
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
  firstTime = True
  difficultySelected = False
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
      title = get_image('Tketris.png')
      title_label = tk.Label(self,image=title,borderwidth=0)
      title_label.place(relx=0.5,rely=0.2,anchor='center')
      title_label.img = title

      # Play Button
      play = get_image('play_button.png')
      play_button = tk.Button(self,command=lambda: self.checkFirstRun(master), image=play,borderwidth=0)
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
      quit_button = tk.Button(self, command=lambda:close_program(),image=quit_image,borderwidth=0)
      quit_button.place(relx = 0.7,rely=0.8,anchor='center')
      quit_button.img = quit_image

  # First time check
  # if player's first start up there would be a popup asking if they want to read instructions
  def checkFirstRun(self,master):
      if Tketris.firstTime == False:
        if Tketris.difficultySelected: # if its not their first time and they have a topic selected 
          master.switch_frame(Game) # then start game
        else: # else popup that sends them to option menu to select topic
          if tkinter.messagebox.showwarning("No Topic","You haven't chosen a topic and a difficulty yet\nWould you like to go to Options?"):
            master.switch_frame(Options)
            
      else: # if it is their first time, popup that asks them if they would like to read instructions
        answer = tkinter.messagebox.askyesno("First Time Playing","Would like to read the instructions?")
        if answer: 
          master.switch_frame(Instructions1)
        else:
          Tketris.firstTime = False  # if user responds set first time to false so this doesn't run again
          if Tketris.difficultySelected:
            master.switch_frame(Game)
          else: # if no difficulty selected, take them to option page
            if tkinter.messagebox.showwarning("No Topic","You haven't chosen a topic and a difficulty yet\nWould you like to go to Options?"):
              master.switch_frame(Options)
            

  

# Frame where the game occurs
class Game(tk.Frame):
    # initilize variables
    score = 0 
    # all of the possible question
    list_of_bedmas_equations = [
      '__?__','(__?__)?__','__?__?__',
      '__?(__?__)','__**(__?__)','__**__?__'
      ] 
    operator_functions = {
          '+': lambda a, b: a + b, 
          '-': lambda a, b: a - b,
          '*': lambda a, b: a * b, 
    }
    operators = ["+","-","*",'/']
    colours = []
    # Setup widgets on the page
    def __init__(self, master):
      tk.Frame.__init__(self, master)
      Game.colours = random.choice(TETRISCOLOURS)
      print(Game.colours)
      self.master = master
      self.GameOverRun = False

      # Back Button to get back to the MainMenu
      back = get_image('back_button.png')
      self.back_button = tk.Button(self,command=lambda: master.switch_frame(mainMenu) 
      , image=back,borderwidth=0)
      self.back_button.place(relx = (5/6),rely=0.9,anchor='center')
      self.back_button.img = back

      # Finds the difficulty selected in Options and sets the correct multiplier
      if Options.currentDifficulty == "Easy":
        self.multiplier = 1
        self.tempquestiontimer = 60
      elif Options.currentDifficulty == "Normal":
        self.multiplier = 5
        self.tempquestiontimer = 40
      elif Options.currentDifficulty == "Hard":
        self.multiplier = 10
        self.tempquestiontimer = 15

      # after all setup is done
      # Initialize the 2 games  
      self.Tetris_Game()
      self.MathGame()


    # Assigns the Question from the function into the UI
    def NewQuestion(self):
      if not self.tetris.penalty:
          question = []
          # Generate question based on topic picked
          # returns a list with the question, answers and the wrong answers
          if Options.currentTopic == "Algebra":
                question = self.algebra()
          elif Options.currentTopic == "Bedmas":
                question = self.bedmas()
          elif Options.currentTopic == "Fractions":
                question = self.fraction()
          # Prevents the algorithm from generating absurd questions
          try:
            randomQuestion = question[0]
          except:
            self.NewQuestion()
          else:
            randomQuestion = question[0] 
            randomAnswer = question[1]
            wronganswers = question[2]
            
            # Displays the answer
            self.Display.config(text=randomQuestion) # Display it on the window
            self.countdown(self.tempquestiontimer)

            # Answer Buttons

            
            self.Buttons[0].config(text=randomAnswer,command=lambda:self.CorrectAns()) 
            # Colours of the Buttons assign it in a random order
            ButtonInfo = random.sample([[1,1,'#93c47d'],[1,2,'#e06666'],[2,1,'#6fa8dc'],[2,2,'#f1c232']],4) 
            for i in range(0,4):
              if i > 0:
                self.Buttons[i].config(text=wronganswers[i-1],command=lambda:self.WrongAns())
              self.Buttons[i].config(bg=ButtonInfo[i][2],font=ANSFONT)
              self.Buttons[i].place(relx=0.525+(0.15*int(ButtonInfo[i][0])),rely=0.35+0.15*int(ButtonInfo[i][1]),
              anchor='center',relheight=BUTTONHEIGHT,relwidth=BUTTONWIDTH)
    
          
    # When player has pressed the correct answer
    # run this subroutine
    def CorrectAns(self):
      self.after_cancel(self.tick) # Reset Timer
      self.tetris.score += 1*self.multiplier # add score according to difficulty
      self.NewQuestion() # Generates new question
    
    # When player has pressed the wrong answer 
    # run this subroutine
    def WrongAns(self):
      # returns the buttons to normal
      def callback():
        if not self.tetris.game_over:
          for i in range(0,4):
            self.Buttons[i]["state"] = "normal"
            self.tetris.penalty = False
      # Set the buttons to disabled so that they cannot be used.
      for i in range(0,4):
        self.tetris.penalty = True
        self.Buttons[i]["state"] = "disabled"
        self.wronganswer = self.after(min(int(self.tempquestiontimer)*250,5000),callback)
    

    def MathGame(self):
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
      self.countdownLabel = tk.Label(self,text='',width=20,font=FONT)
      self.countdownLabel.place(relx=0.75,rely=0.05,anchor='center')
      self.countdownTimer['maximum'] = self.tempquestiontimer
      self.NewQuestion()

    # Countdown for mathgame
    def countdown(self, remaining = None):
      if remaining is not None:
        self.remaining = remaining
      # When time is up, Game Over
      if self.remaining <= 0:
        self.countdownTimer['value']=self.tempquestiontimer
        self.countdownLabel.configure(text='Times Up')
        self.tetris.game_over = True
        self.after(5000,lambda:self.master.switch_frame(GameOverScreen))
        self.back_button.place_forget()
        self.flashingBar() # flash bar green and red after time is up
      else: # else change the colour of the bar
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
      # Disable the buttons when Game is Over
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
      # Returns a value that tkinter can read
      return '#{:02x}{:02x}{:02x}'.format(r,g,b)

    def Tetris_Game(self):
      # Starts the Tetris class
      self.tetris = Tetris()
      self.create_widgets()
      self.update_clock()
    # The rate the game updates
    def update_clock(self):
      if not self.tetris.game_over:
        self.tetris.move(1,0) # continuous falling of the tetrominos
        self.update()
        self.after(int(1000*(0.975**self.tetris.score)),self.update_clock) # speeds up with higher score

    def create_widgets(self):
      PIECE_SIZE = 33
      # Playing field
      self.canvas = tk.Canvas(self,height=PIECE_SIZE * self.tetris.FIELD_HEIGHT
                                  ,width=PIECE_SIZE * self.tetris.FIELD_WIDTH
                                  ,bg='black')
      self.score_label = tk.Label(self,font=FONT)
      self.score_label.place(anchor='center',relx = 7/12,rely=0.9)
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
      # draw the block on the canvas
      self.rectangles = [
      self.canvas.create_rectangle(c*PIECE_SIZE,r*PIECE_SIZE
                                  ,(c+1)*PIECE_SIZE,(r+1)*PIECE_SIZE,outline='white')
          for r in range(self.tetris.FIELD_HEIGHT) for c in range(self.tetris.FIELD_WIDTH)
      ]
      self.canvas.place(anchor="center",relx=0.25,rely=0.5)
      self.update()

    def update(self):
      if not self.tetris.game_over:
        # gets colour of the entire field
        for i, _id in enumerate(self.rectangles):
          colour_num = self.tetris.get_colour(i // self.tetris.FIELD_WIDTH,i % self.tetris.FIELD_WIDTH)
          self.canvas.itemconfig(_id,fill=Game.colours[colour_num])
          
      else:
        # if Game is over
        if not self.GameOverRun:
          self.after_cancel(self.tick) # stops the bar in the Math subroutine
          self.countdownLabel.configure(text='GAME OVER')
          self.countdownTimer['value'] = self.tempquestiontimer
          self.GameOverRun = True
          self.after(5000,lambda:self.master.switch_frame(GameOverScreen)) # switch to game over screen in 5 seconds
          self.back_button.place_forget()
          if self.remaining > 0:
            self.flashingBar()
      self.score_label['text'] = "Score: {}".format(self.tetris.score)
      Game.score = self.tetris.score
    # Generate bedmas questions
    def bedmas(self):
        if Options.currentDifficulty == "Hard":
          string = random.choice(Game.list_of_bedmas_equations) # all formats are picked from
        else:
          string = Game.list_of_bedmas_equations[random.randint(0,3)] # no exponential formats are picked
        wronganswers = []
        # The range of the random numbers
        easy_multipliers = [(1,10),(1,2),(1,5)]
        normal_multipliers = [(1,50),(1,3),(1,10)]
        hard_multipliers = [(1,99),(1,3),(1,12)]

        if Options.currentDifficulty == "Easy":
            difficulty_multiplier = easy_multipliers
        elif Options.currentDifficulty == "Normal":
            difficulty_multiplier = normal_multipliers
        else:
            difficulty_multiplier = normal_multipliers  # I have changed it to normal as hard was too hard

        # Replace every ? with a random operator
        for i in range(string.count('?')):
            if string.count('**'):
                operator = Game.operators[random.randint(0,1)]
            else:
                operator = random.choice(Game.operators)
            
            string = string.replace('?',operator,1)

        # if division problem, there is a different way to generate answer
        # to avoid decimals
        if string == ('__/__'):
            answer = random.randint(difficulty_multiplier[2][0],difficulty_multiplier[2][1])
            random_num = random.randint(difficulty_multiplier[2][0],difficulty_multiplier[2][1])
            string = string.replace('__',str(answer*random_num),1)
            string = string.replace('__',str(random_num),1)
        # exponential problems also have a different way to prevent huge numbers
        elif string.count('**')>0:
            for i in range(string.count('__')):
                randomrange = random.randint(difficulty_multiplier[1][0],difficulty_multiplier[1][1])
                string = string.replace('__',str(randomrange),1)
        # otherwise generate the numbers normally
        else:
            for i in range(string.count('__')):
                if string.count('*')>0 or string.count('/'):
                    randomrange = random.randint(difficulty_multiplier[2][0],difficulty_multiplier[2][1])
                else:
                    randomrange = random.randint(difficulty_multiplier[0][0],difficulty_multiplier[0][1])
                string = string.replace('__',str(randomrange),1)

        answer = eval(string)
        # Generate the wrong answers by picking an offset randomly from a range
        if abs(answer) < 10:
            randomlist = random.sample(range(1,5), 3)
        else:
            randomlist = random.sample(range(1,50),3)
        
        for i in range(0,3):
            operator = Game.operators[random.randint(0,1)]
            wronganswers.append(
              round(Game.operator_functions[operator](answer, randomlist[i]),2)
              )
        # replace the coding signs for more widely accepted signs
        # as not everybody knows '**' means exponential
        if string.count('**')>0:
            string = string.replace('**','^')
        if string.count('*')>0:
            string = string.replace('*','x')
        answer = round(answer,3)
        
        return [string,answer,wronganswers]
        print(str(string)+'='+str(answer),str(wronganswers[0]),str(wronganswers[1]),str(wronganswers[2]))
    # Generates a random fraction question
    def fraction(self):
        easy_multipliers = (1,5)
        normal_multipliers = (1,10)
        hard_multipliers = (1,20)
        # generate the questions differently depending on the difficulty
        # Easy, denominator is the same, and the range is only between 1-5
        if Options.currentDifficulty == "Easy":
            difficulty_multiplier = easy_multipliers
            df1 = random.randint(difficulty_multiplier[0],difficulty_multiplier[1])
            nf1 = random.randint(difficulty_multiplier[0],difficulty_multiplier[1])
            nf2 = random.randint(difficulty_multiplier[0],difficulty_multiplier[1])
            df2 = df1
            # prevents whole numbers from generating
            while float(nf1/df1).is_integer():
                df1 = random.randint(difficulty_multiplier[0],difficulty_multiplier[1])
                nf1 = random.randint(difficulty_multiplier[0],difficulty_multiplier[1])
                df2 = df1
                nf2 = random.randint(difficulty_multiplier[0],difficulty_multiplier[1])
        # Normal, denominator is same and the range is only between 1-10
        elif Options.currentDifficulty == "Normal":
            difficulty_multiplier = normal_multipliers
            df1 = random.randint(difficulty_multiplier[0],difficulty_multiplier[1])
            nf1 = random.randint(difficulty_multiplier[0],difficulty_multiplier[1])
            nf2 = random.randint(difficulty_multiplier[0],difficulty_multiplier[1])
            df2 = df1
          
            while float(nf1/df1).is_integer():
                df1 = random.randint(difficulty_multiplier[0],difficulty_multiplier[1])
                nf1 = random.randint(difficulty_multiplier[0],difficulty_multiplier[1])
                df2 = df1
                nf2 = random.randint(difficulty_multiplier[0],difficulty_multiplier[1])
        # Hard, denominator is completely random, and range is between 1-20
        else:
            difficulty_multiplier = hard_multipliers
            nf1 = random.randint(difficulty_multiplier[0],difficulty_multiplier[1])
            df1 = random.randint(difficulty_multiplier[0],difficulty_multiplier[1])
            nf2 = random.randint(difficulty_multiplier[0],difficulty_multiplier[1])
            df2 = random.randint(difficulty_multiplier[0],difficulty_multiplier[1])
            # prevents any of the fractions from being a whole number
            while float(nf1/df1).is_integer():
                df1 = random.randint(difficulty_multiplier[0],difficulty_multiplier[1])
                nf1 = random.randint(difficulty_multiplier[0],difficulty_multiplier[1])
            while float(nf2/df2).is_integer():
                nf2 = random.randint(difficulty_multiplier[0],difficulty_multiplier[1])
                df2 = random.randint(difficulty_multiplier[0],difficulty_multiplier[1])

        wronganswers = []

      
        fraction1 = Fraction(nf1,df1) 
        fraction2 = Fraction(nf2,df2)
        # pick a random operator  
        operator = random.choice(Game.operators)
        string = '('+str(fraction1)+') '+str(operator)+' ('+str(fraction2)+')'
        answer = Fraction(eval(string)).limit_denominator()
        for i in range(3):
            wrong_fraction = Fraction(random.randint(1,20),random.randint(1,20))
            operator = Game.operators[random.randint(0,1)]
            wronganswers.append(
              Game.operator_functions[operator](answer, wrong_fraction)
            )
        return [string,answer,wronganswers]
        print(str(string)+'='+str(answer),wronganswers[0],wronganswers[1],wronganswers[2])
    # Generates random algebra question
    def algebra(self):
        # base template
        question = ('__*x=__')
        runs = 0 # prevents overcomplicated questions
        wronganswers = []
        easy_multipliers = [(1,5),0.8]
        normal_multipliers = [(1,10),0.7]
        # assign range of questions and chance
        if Options.currentDifficulty == "Easy":
            difficulty_multiplier = easy_multipliers
        # Normal and hard have same questions, hard just has less time to answer them
        else:
            difficulty_multiplier = normal_multipliers

        # randomly assign __ into either __*x or (__?__) or both
        # do this until there are no more __
        while question.count('__') > 0:
            if random.random() > difficulty_multiplier[1]+(0.25*runs):
                question = question.replace('__','(__?__)',1)
            elif random.random()>difficulty_multiplier[1]+(0.2*runs):
                question = question.replace('__*x','(__*x?__)',1) 
            # if more than 1 x, to simiplify question, chance to remove them.
            if question.count('x')>1:
                if question.count(')*x')>0:
                        question = question.replace(")*x",')',1)
        
            multiplier = 1
            # 40% chance of having a negative number
            if random.random()>0.6:
                multiplier = -multiplier

            question = question.replace('__',str(multiplier*(random.randint(difficulty_multiplier[0][0],difficulty_multiplier[0][1]))),1)
            runs += 1
        # pick random operator    
        for i in range(question.count('?')):
            operator = random.choice(Game.operators)
            question = question.replace('?',operator,1)
        # this prevents unsolvable questions ie; 2x + 5= 2x
        # which is not possible
        try:
            answer = self.solve(question)
        except:
            self.algebra()
        else:
            answer = self.solve(question)
            if isinstance(answer,float):
                answer = Fraction(answer).limit_denominator()
            
            randomlist = random.sample(range(1,5), 3)
            for i in range(3):
                operator = Game.operators[random.randint(0,1)]
                wronganswers.append(
                  Game.operator_functions[operator](answer, randomlist[i])
                  )
                # if answer has decimals, have the answer in decimal form
                if isinstance (wronganswers[i],float):
                    wronganswers[i] = 'x='+str(Fraction(wronganswers[i]))
                else: wronganswers[i] = 'x='+str(wronganswers[i])
            return [question,('x='+str(answer)),wronganswers]
            print(str(question)+'='+str(answer),wronganswers[0],wronganswers[1],wronganswers[2])

    # equation for finding the answer
    def solve(self,equation,var='x'):
        expression = equation.replace("=","-(")+")"
        grouped = eval(expression.replace(var,'1j'))
        return -grouped.real/grouped.imag


class Tetris():
  # tetris canvas size 
  # 20 x 10  
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
  # set up the field
  def __init__(self):
    self.field = [[0 for c in range(Tetris.FIELD_WIDTH)] for r in range(Tetris.FIELD_HEIGHT)]
    self.move_lock = Lock()
    self.reset_tetromino()
    self.game_over = False
    self.penalty = False
    self.score = 0
  # generate a random tetromino with a random colour
  def reset_tetromino(self):
    self.tetromino = random.choice(Tetris.TETROMINOS)[:]
    self.tetromino_colour = random.randint(1,len(Game.colours)-1)
    print(Game.colours[self.tetromino_colour])
    self.tetromino_offset = [-2,Tetris.FIELD_WIDTH//2]
    self.game_over = any(not self.is_cell_free(r,c) for (r,c) in self.get_tetromino_coords())
  # Get the coordinate of the tetromino
  def get_tetromino_coords(self):
    return [(r + self.tetromino_offset[0], c + self.tetromino_offset[1]) for r,c in self.tetromino]
  # when a line is cleared, remove line and generate new line at the top.
  def apply_tetromino(self):
    for (r,c) in self.get_tetromino_coords():
      self.field[r][c] = self.tetromino_colour
    new_field = [row for row in self.field if any(tile == 0 for tile in row)]
    lines_eliminated = len(self.field) - len(new_field)
    self.field = [[0]*Tetris.FIELD_WIDTH for x in range(lines_eliminated)] + new_field
    self.reset_tetromino()
  # gets the colour of the tetrominos
  def get_colour(self,r,c):
    return self.tetromino_colour if (r,c) in self.get_tetromino_coords() else self.field[r][c]
  # returns True if any of the cells are free
  def is_cell_free(self,r,c):
    return r < Tetris.FIELD_HEIGHT and 0 <= c < Tetris.FIELD_WIDTH and (r< 0 or self.field[r][c] == 0)
  # moves the tetromino
  def move(self,dr,dc):
    with self.move_lock:
      if self.game_over:
        return
      if not self.penalty:
        # check if space is free
        if all(self.is_cell_free(r + dr,c + dc) for r,c in self.get_tetromino_coords()):
          self.tetromino_offset = [self.tetromino_offset[0] + dr, self.tetromino_offset[1] + dc]
        elif dr == 1 and dc == 0:
          self.game_over = any(r < 0 for (r,c) in self.get_tetromino_coords())
          if not self.game_over:
            self.apply_tetromino()
      # if space is not free check if there is any place for the new block otherwise Game Over
      elif dr == 1 and dc == 0 and all(self.is_cell_free(r + dr,c + dc) for r,c in self.get_tetromino_coords()):
        self.tetromino_offset = [self.tetromino_offset[0] + dr, self.tetromino_offset[1] + dc]
      elif dr == 1 and dc == 0 and not all(self.is_cell_free(r + dr,c + dc) for r,c in self.get_tetromino_coords()):
        self.game_over = any(r < 0 for (r,c) in self.get_tetromino_coords())
        if not self.game_over:
          self.apply_tetromino()
  # rotates the block
  def rotate(self):
    with self.move_lock:
      if self.game_over:
        return
      if self.penalty:
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
  if not Tketris.difficultySelected:
    currentTopic = "Select Topic"
    currentDifficulty = "Normal"
  topics = ["Algebra","Bedmas","Fractions"]

  def __init__(self, master):
    tk.Frame.__init__(self, master)
    # Tketris Title Label
    title = get_image('Options.png')
    title_label = tk.Label(self,image=title,borderwidth=0)
    title_label.place(relx=0.5,rely=0.2,anchor='center')
    title_label.img = title
    # Back Button to get back to the MainMenu
    back = get_image('back_button.png')
    back_button = tk.Button(self,command=lambda:self.updateSettings(master,mainMenu)
    , image=back,borderwidth=0)
    back_button.place(relx = (5/6),rely=0.9,anchor='center')
    back_button.img = back

    tk.Button(self,text='Read Instructions',font=FONT,bg=DROPCOLOUR,command=lambda:self.updateSettings(master,Instructions1)).place(relx=0.2,rely=0.9,anchor='center')
    # Difficulty Dropbox
    self.difficulty = tk.StringVar(self)
    self.difficulty.set(Options.currentDifficulty) # Defualt Value
    difficultyMenu = tk.OptionMenu(self,self.difficulty,"Easy","Normal","Hard")
    difficultyMenu['menu'].config(font=FONT)
    difficultyMenu.config(font=ANSFONT ,width=DROPWIDTH,height=DROPHEIGHT,bg=DROPCOLOUR,activebackground=DROPCOLOUR)
    difficultyMenu.place(relx=0.75,rely=0.4,anchor="center") 
    # Labels
    tk.Label(self,text='Select topic above\nThe topic which decides what question would be given',font=FONT).place(relx=0.25,rely=0.6,anchor="center")
    tk.Label(self,text='Select difficulty above\nDifficulty decides how hard the problems are\na higher difficulty also gives more points\nbut less time to answer them',font=FONT).place(relx=0.75,rely=0.6,anchor="center")
    # Topic Dropbox
    self.topic = tk.StringVar(self)
    self.topic.set(Options.currentTopic)
    topicMenu = tk.OptionMenu(self,self.topic,*Options.topics)
    topicMenu['menu'].config(font=FONT)
    topicMenu.config(font=ANSFONT ,width=DROPWIDTH,height=DROPHEIGHT,bg=DROPCOLOUR,activebackground=DROPCOLOUR)
    topicMenu.place(relx=0.25,rely=0.4,anchor="center") 
  # Checks if player has select a topic and assigns it
  def updateSettings(self,master,frame):
    if self.topic.get() == "Select Topic":
        if tkinter.messagebox.showwarning("No Topic","You haven't chosen a topic and a difficulty yet"):
          return
    else:
      Options.currentDifficulty = self.difficulty.get()
      Options.currentTopic = self.topic.get()
      Tketris.difficultySelected = True
      master.switch_frame(frame)

# Leaderboard Frame
class Leaderboard(tk.Frame):
  def __init__(self, master):
    tk.Frame.__init__(self, master)
    # Tketris Title Label
    title = get_image('Leaderboard.png')
    title_label = tk.Label(self,image=title,borderwidth=0)
    title_label.place(relx=0.5,rely=0.1,anchor='center')
    title_label.img = title
    # Back Button to get back to the MainMenu
    back = get_image('back_button.png')
    back_button = tk.Button(self,command= lambda:master.switch_frame(mainMenu)
    , image=back,borderwidth=0)
    back_button.place(relx = (5/6),rely=0.9,anchor='center')
    back_button.img = back
    topic = tk.StringVar(self,value=Options.topics[0])
    # Topic dropbox
    topics = tk.OptionMenu(self,topic,*Options.topics,command=lambda x:self.UpdateLeaderboard(x))
    topics.config(font=ANSFONT ,width=DROPWIDTH-5,height=DROPHEIGHT,bg=DROPCOLOUR,activebackground=DROPCOLOUR)
    topics['menu'].config(font=FONT)
    topics.place(relx=5/6,rely=0.3,anchor='center')
    tk.Label(self,
    text='Use the dropdown box above\nto select the leaderboard',
    font=FONT).place(relx=5/6,rely=0.5,anchor='center')
    ## NUMBER LABELS
    self.boardName = {}
    self.boardScore = {}
    COLOURS = ['#FFD700','#C0C0C0','#CD7F32','#3c89d0'] # Gold, Silver, Bronze, Blue
    # Assign the labels the colours;
    # 1 - Gold
    # 2 - Silver
    # 3 - Bronze
    # 4-7 - Blue
    for i in range(0,7):
      self.boardName[i] = tk.Label(self,font=ANSFONT,fg=COLOURS[3])
      self.boardName[i].place(relx=0.25,rely=0.25+0.1*i,anchor='center')
      self.boardScore[i] = tk.Label(self,font=ANSFONT,fg=COLOURS[3])
      self.boardScore[i].place(relx=0.35,rely=0.25+0.1*i,anchor='center')
      if i <= 3:
        self.boardName[i].config(fg=COLOURS[i])
        self.boardScore[i].config(fg=COLOURS[i])
      tk.Label(self,text=i+1,font=FONT).place(relx=0.1,rely=0.25+0.1*i,anchor='center')
    
  def UpdateLeaderboard(self,option):
    # When player selects a topic
    # read the csv file and prints name on UI
    for i in range(0,7):
      self.boardName[i].config(text='')
      self.boardScore[i].config(text='')
    leaderboard = readcsv(str((option)+'_leaderboard.csv').lower())
    if len(leaderboard)>7:
      for i in range(0,7):
        self.boardName[i].config(text=leaderboard[i][0])
        self.boardScore[i].config(text=leaderboard[i][1])
    # if no entries then print "No Entries Yet"
    elif len(leaderboard)==0:
      self.boardName[3].config(text='No Entries Yet')
    else:
      for i in range(len(leaderboard)):
        self.boardName[i].config(text=leaderboard[i][0])
        self.boardScore[i].config(text=leaderboard[i][1])
    
# Game Over Screen
class GameOverScreen(tk.Frame):
  # All possible slash text
  gameOverText = ["Nice Job!", 
  "Well Done!","Fantastic Job!",
  "Amazing!!","Wow! That was a great run",
  "What an amazing run!","That was great!",
  "Better than Taeho!","Beautiful!",
  "Have a great day!","Easy Peasy",
  "That was easy","Nice try","Oof that was close!",
  "Go again?","C'mon you can do better",
  "Lets have another go","Lets do it again",
  "ONE MORE!!","Wonderful!","So Close...",
  "Sovan's apple sticker stash","All original code here",
  "Wow Tetris is so fun!", "Get a life! Your score is too \n low for life support - Sovan Chap",
  "INSANE","Thats not possible","Godly","Are you sure you aren't cheating?",
  "Hah, my grandma could do better","Better luck next time","Lets have another go"]    
  def __init__(self, master):
    tk.Frame.__init__(self, master)
    # Tketris Title Label
    self.default_text = True
    title = get_image('GameOver.png')
    title_label = tk.Label(self,image=title,borderwidth=0)
    title_label.place(relx=0.5,rely=0.2,anchor='center')
    title_label.img = title
    # Back Button to get back to the MainMenu
    back = get_image('back_button.png')
    back_button = tk.Button(self,command= lambda:self.update(master)
    , image=back,borderwidth=0)
    back_button.place(relx = (5/6),rely=0.9,anchor='center')
    back_button.img = back
    self.leaderboard = readcsv(str((Options.currentTopic)+'_leaderboard.csv').lower())
    ## GAME OVER TEXT
    # if score is greater than last high score then print "New Highscore"
    # otherwise show one of the slash text from list
    if len(self.leaderboard)>0:
      if int(Game.score) > int(self.leaderboard[0][1]):
        text = 'New Highscore!!'
      else:
        text = random.choice(self.gameOverText)

    else:
      text = 'New Highscore!!'
      
    tk.Label(self,text=text,font=ANSFONT).place(relx=0.5,rely=0.35,anchor='center')
    tk.Label(self,text=('Your final score is '+str(Game.score)+'.'),font=ANSFONT).place(relx=0.5,rely=0.5,anchor='center')
    textEntry = tk.StringVar(self,value='Enter Name; max 5 characters')
    
    self.name = tk.Entry(self,textvariable = textEntry,width=25,font=ANSFONT,justify='center')
    self.name.place(relx=0.5,rely=0.7,anchor='center')
    self.name.bind("<Button-1>",lambda x:self.delete_text())
    textEntry.trace("w",lambda *args: self.limitNameSize(textEntry))
    
  # Deletes text when clicked on, - to delete the defualt text 
  def delete_text(self):
    if self.default_text:
      self.name.delete(0,'end')
      self.default_text = False
  # Limits the name to 5 characters and prevents symbols and numbers
  def limitNameSize(self,entrytext):
    if entrytext.get().isalpha():
      if len(entrytext.get()) > 0: entrytext.set(entrytext.get()[:5])
    else:
      if len(entrytext.get()) > 0: entrytext.set(entrytext.get()[:len(entrytext.get())-1])
  # Update the score to the csv file
  def update(self,master):
    if self.name.get() == 'Enter Name; max 5 characters' or len(self.name.get())==0:
      tkinter.messagebox.showinfo("Error","Please Enter in a name")
    else:
      entry = [self.name.get(),Game.score]
      # Find out where to append the score
      if len(self.leaderboard) == 0:
        self.leaderboard.insert(0,entry)
        
      else:
        for i in range(len(self.leaderboard)):
          if Game.score > int(self.leaderboard[i][1]):
            self.leaderboard.insert(i,entry)
            
            break
        if int(self.leaderboard[len(self.leaderboard)-1][1]) >= int(Game.score):
            self.leaderboard.insert(len(self.leaderboard),entry)
      print(self.leaderboard)
      # Writes it to the csv file
      dir = os.path.dirname(__file__) # Find the directory of the current file
      filename = os.path.join(dir, 'csv',str((Options.currentTopic)+'_leaderboard.csv').lower()) # Finds the csv file
      f = open(filename,'w') # opens the csv file
      print(filename)

      f.write('Name,Score\n')
      for i in range(0,len(self.leaderboard)): # for every line after that format and append to list
        print(self.leaderboard[i])
        print("its this one")
        line = "{0},{1}\n".format(self.leaderboard[i][0],self.leaderboard[i][1])
        f.write(line)
      f.close() # close the file

      master.switch_frame(mainMenu)

# Objective Instructions Frame
class Instructions1(tk.Frame):
  def __init__(self, master):
    tk.Frame.__init__(self, master)
    # Tketris Title Label
    Tketris.firstTime = False
    title = get_image('Instructions.png')
    title_label = tk.Label(self,image=title,borderwidth=0)
    title_label.place(relx=0.5,rely=0.2,anchor='center')
    title_label.img = title
    # Back Button to get back to the MainMenu
    back = get_image('back_button.png')
    back_button = tk.Button(self,command= lambda:master.switch_frame(Options)
    , image=back,borderwidth=0)
    back_button.place(relx = (5/6),rely=0.9,anchor='center')
    back_button.img = back
    # Next instructions page
    next = get_image('next_button.png')
    next_button = tk.Button(self,command= lambda:master.switch_frame(Instructions2)
    , image=next,borderwidth=0)
    next_button.place(relx = (1/6),rely=0.9,anchor='center')
    next_button.img = next
    # Objective
    Objective = tk.Label(self,text='Objective',font=TITLEFONT)
    Objective.place(relx=0.5,rely=0.35,anchor='center')
    Objectivetext = tk.Label(self,text='The objective of the game is to get the highest score you can!\n'+
                        'You can get a point for getting a math question correct\n\n'+
                        'However there is a catch, you would have to play tetris at the same time\n'+
                        'The goal is to get the highest score you can and get on the leaderboard',font=FONT)
    Objectivetext.place(relx=0.5,rely=0.6,anchor='center')
# Controls Instructions Frame
class Instructions2(tk.Frame):
  def __init__(self, master):
    tk.Frame.__init__(self, master)
    # Tketris Title Label
    
    title = get_image('Instructions.png')
    title_label = tk.Label(self,image=title,borderwidth=0)
    title_label.place(relx=0.5,rely=0.2,anchor='center')
    title_label.img = title
    # Back Button to get back to the MainMenu
    back = get_image('back_button.png')
    back_button = tk.Button(self,command= lambda:master.switch_frame(Instructions1)
    , image=back,borderwidth=0)
    back_button.place(relx = (5/6),rely=0.9,anchor='center')
    back_button.img = back
    # Next instructions page
    next = get_image('next_button.png')
    next_button = tk.Button(self,command= lambda:master.switch_frame(Instructions3)
    , image=next,borderwidth=0)
    next_button.place(relx = (1/6),rely=0.9,anchor='center')
    next_button.img = next
    # Controls
    Control = tk.Label(self,text='Controls',font=TITLEFONT)
    Control.place(relx=0.5,rely=0.35,anchor='center')
    Controltext = tk.Label(self,text='This game requires you to multitask\n'+
                        'You answer the math problem with your mouse by selecting the correct answer\n'+
                          'and you use "wasd" or the arrow keys to control the tetris block\n\n'+
                          'up to rotate the block\n'+
                        'down to drop faster and\n'+
                        'left and right to move the block',font=FONT)
    Controltext.place(relx=0.5,rely=0.6,anchor='center')
# Penalty Instructions Frame
class Instructions3(tk.Frame):
  def __init__(self, master):
    tk.Frame.__init__(self, master)
    # Tketris Title Label
    
    title = get_image('Instructions.png')
    title_label = tk.Label(self,image=title,borderwidth=0)
    title_label.place(relx=0.5,rely=0.2,anchor='center')
    title_label.img = title
    # Back Button to get back to the MainMenu
    back = get_image('back_button.png')
    back_button = tk.Button(self,command= lambda:master.switch_frame(Instructions2)
    , image=back,borderwidth=0)
    back_button.place(relx = (5/6),rely=0.9,anchor='center')
    back_button.img = back
    # Next instructions page
    next = get_image('next_button.png')
    next_button = tk.Button(self,command= lambda:master.switch_frame(Instructions4)
    , image=next,borderwidth=0)
    next_button.place(relx = (1/6),rely=0.9,anchor='center')
    next_button.img = next
    # Penalty
    Penalty = tk.Label(self,text='Careful when answering',font=TITLEFONT)
    Penalty.place(relx=0.5,rely=0.35,anchor='center')
    Penaltytext = tk.Label(self,text="Be careful when answering the math question, because\n"+
                        "when you get the question wrong, you would be stunned and you wouldn't be \n"+
                        'able to do anything for a long while.\n\n'+
                        "Be wary of the timer, make sure it doesn't reach 0 or you would lose\n"+
                        'You would also lose if the tetris block reaches the top of the playing field',font=FONT)
    Penaltytext.place(relx=0.5,rely=0.6,anchor='center')
# Changing Topic Instructions Frame
class Instructions4(tk.Frame):
  def __init__(self, master):
    tk.Frame.__init__(self, master)
    # Tketris Title Label
    
    title = get_image('Instructions.png')
    title_label = tk.Label(self,image=title,borderwidth=0)
    title_label.place(relx=0.5,rely=0.2,anchor='center')
    title_label.img = title
    # Back Button to get back to the MainMenu
    back = get_image('back_button.png')
    back_button = tk.Button(self,command= lambda:master.switch_frame(Instructions3)
    , image=back,borderwidth=0)
    back_button.place(relx = (5/6),rely=0.9,anchor='center')
    back_button.img = back
    # Play Button
    play = get_image('play_button.png')
    play_button = tk.Button(self,command=lambda: mainMenu.checkFirstRun(self,master), image=play,borderwidth=0)
    play_button.place(relx = 1/6,rely=0.9,anchor='center')
    play_button.img = play
    # Topic
    Topic = tk.Label(self,text='Choose the right difficulty',font=TITLEFONT)
    Topic.place(relx=0.5,rely=0.35,anchor='center')
    Topictext = tk.Label(self,text='Before you start you would need to choose a topic and your perfered difficulty\n'+
                        "in the Option menu if you haven't already, this will decide the question\n"+
                        'that would be displayed in the math game, and would have its\n'+
                        'own leaderboard',font=FONT)
    Topictext.place(relx=0.5,rely=0.6,anchor='center')
  
def main():
  app = Tketris()
  app.geometry('1280x720')
  app.resizable(False,False)
  app.protocol("WM_DELETE_WINDOW", close_program)
  app.mainloop()
  

if __name__ == "__main__":
  main()