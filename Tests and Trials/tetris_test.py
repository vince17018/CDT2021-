import tkinter as tk
import random
import math
class Tketris():
  def __init__(self):
    app.bind("<Key>",self.MovingBlock)
    self.canvas = tk.Canvas(app,height=500,width=250,bg='grey')
    app.after(1000,lambda:self.Falling())
    self.canvas.pack()
    self.TetrisGame()
  def TetrisGame(self):
    # Game Variables
    self.score = 0
    self.field = []
    height = 20
    width = 10
    figure = None
    self.activeblock = {}
    for i in range(1,4):
      self.activeblock[i] = None

    for i in range(height):
        new_line = []
        for j in range(width):
            new_line.append(0)
        self.field.append(new_line)
    figure = Figure()
    self.block = figure.image()
    print(self.block)
    blockClear = 0
    for i in list(self.block):
      row = math.floor(i/4)
      colomn = i%4
      if self.field[row][colomn+3] == 0:
        blockClear += 1
    if blockClear == 4:
      for i in list(self.block):
        row = math.floor(i/4)
        colomn = i%4
        
        
  def Falling(self):
    global moving
    moving = None
    for i in range(0,4):
      self.canvas.move(self.activeblock[i],0,25)
      coordinates = self.canvas.coords(self.activeblock[3])
    if coordinates[3]<500:
      moving = app.after(1000,lambda:self.Falling())

  def MovingBlock(self,event):
    x, y =0, 0
    # find furthest down
    downcoord = self.canvas.coords(self.activeblock[3])
    # find furthest right
    rightcoord = self.activeblock.index(max([x%4 for x in self.activeblock]))
    # find furthest left
    leftcoord = self.activeblock.index(min([x%4 for x in self.activeblock]))
    if downcoord[3]<500:
      if event.char == "a":
        if leftcoord[0] > 0:
          x = -25
      elif event.char == "d":
        if rightcoord[2]<250:
          x = 25
      elif event.char == " ":
        y = 500-downcoord[3]
        app.after_cancel(moving)
      for i in range(0,4):
        self.canvas.move(self.activeblock[i],x,y)
# Tetris Block Codes
class Figure:
  ## Tutorial from https://levelup.gitconnected.com/writing-tetris-in-python-2a16bddb5318
  ## Only the first bit, the second half of the guide does not help me as I am not using pygame

  # RGB colours defined here
  colours = [
  (0, 0, 0),
  (120, 37, 179),
  (100, 179, 179),
  (80, 34, 22),
  (80, 134, 22),
  (180, 34, 22),
  (180, 34, 122),
  ]
  # 0  1  2  3
  # 4  5  6  7
  # 8  9  10 11
  # 12 13 14 15
  figures = [
      [[1, 5, 9, 13], [4, 5, 6, 7]], # line block (2 rotation)
      [[1, 2, 5, 9], [0, 4, 5, 6], [1, 5, 9, 8], [4, 5, 6, 10]], # J block (4 rotations)
      [[1, 2, 6, 10], [5, 6, 7, 9], [2, 6, 10, 11], [3, 5, 6, 7]], # L block (4 rotations)
      [[1, 4, 5, 6], [1, 4, 5, 9], [4, 5, 6, 9], [1, 5, 6, 9]], # T block (4 rotations)
      [[1, 2, 5, 6]], # Square O block (1 rotation)
      [[5,6,8,9],[1,5,6,10],[5,6,8,9],[0,4,5,9]], # S block (4 rotations)
      [[4,5,9,10],[2,5,6,9],[4,5,9,10],[1,4,5,8]] # Z block (4 rotations)
  ]

  def __init__(self,x=0,y=0):
    self.x = x
    self.y = y
    self.type = random.randint(0,len(self.figures) - 1)
    self.colour = random.randint(1,len(self.colours)-1)
    self.rotation = 0
  def image(self):
    return self.figures[self.type][self.rotation]
  def rotate(self):
    self.rotation = (self.rotation + 1) % len(self.figures[self.types])


app = tk.Tk()
Tketris()
app.mainloop()
  


