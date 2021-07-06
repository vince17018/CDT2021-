import tkinter as tk
import random

def TetrisGame():
    # Game Variables
    score = 0
    field = []
    height = 40
    width = 10
    figure = None
    for i in range(height):
        new_line = []
        for j in range(width):
            new_line.append(0)
        field.append(new_line)
def MoveBlockDown():
  moving = None
  canvas.move(activeblock,0,25)
  coordinates = canvas.coords(activeblock)
  if coordinates[3]<500:
    moving = root.after(1000,lambda:MoveBlockDown())

def MovingBlock(event):
  x, y =0, 0
  coordinates = canvas.coords(activeblock)
  if event.char == "a":
    if coordinates[0] > 0:
      x = -10
  elif event.char == "d":
    if coordinates[2]<250:
      x = 10
  elif event.char == " ":
    y = 500-coordinates[3]
  print(coordinates)
  canvas.move(activeblock,x,y)
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
      [[8,9,5,6],[1,5,6,10],[8,9,5,6],[0,4,5,9]], # S block (4 rotations)
      [[4,5,9,10],[2,6,5,9],[4,5,9,10],[8,4,5,1]] # Z block (4 rotations)
  ]

  def __init__(self,x,y):
    self.x = x
    self.y = y
    self.type = random.randint(0,len(self.figures) - 1)
    self.colour = random.randint(1,len(self.colours)-1)
    self.rotation = 0
  def image(self):
    return self.figures[self.type][self.rotation]
  def rotate(self):
    self.rotation = (self.rotation + 1) % len(self.figures[self.types])

root = tk.Tk()
root.bind("<Key>",MovingBlock)
canvas = tk.Canvas(root,height=500,width=250,bg='grey')
activeblock = canvas.create_rectangle(125,2,125+25,2+25,fill='green',tags='activeblock')

canvas.pack()
TetrisGame()
MoveBlockDown()

root.mainloop()
