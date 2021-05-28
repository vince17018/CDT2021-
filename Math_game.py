# Importing needed modules
import tkinter as tk
import tkinter.messagebox
# Setting up constants
BUTTONWIDTH = 60
BUTTONHEIGHT = 30

# Quit button function
def close_program():
    if tkinter.messagebox.askyesno("Quit","Would you like to quit?"):
      quit()
# Main App
class Tketris(tk.Tk):
  def __init__(self):
    # Sets up program and switches the frame to mainMenu
    tk.Tk.__init__(self)
    self._frame = None
    self.switch_frame(mainMenu)
    self.title("Tk.etris")

    # Defines the switch frame function
  def switch_frame(self,frame_class):
    new_frame = frame_class(self)
    # Destroys past frame to save resources
    if self._frame is not None:
        self._frame.destroy()
    self._frame = new_frame
    self._frame.pack()
# Main Menu window
class mainMenu(tk.Frame):
  def __init__(self, master):
      tk.Frame.__init__(self, master)
      tk.Label(self, text="This is the main menu placeholder").pack()
      tk.Button(self, text="To the Game",
                command=lambda: master.switch_frame(Game)).pack()
      tk.Button(self, text="To the options",
                command=lambda: master.switch_frame(Options)).pack()
      tk.Button(self, text="To the leaderboard",
                command=lambda: master.switch_frame(Leaderboard)).pack()
      tk.Button(self, text="Quit",
                command=lambda: close_program()).pack()
# Tetris main window
class Game(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Label(self, text="Game here").pack(side="top", fill="x", pady=10)
        tk.Button(self, text="Return to main menu",
                  command=lambda: master.switch_frame(mainMenu)).pack()
# Option Menu
class Options(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Label(self, text="Options Page").pack(side="top", fill="x", pady=10)
        tk.Button(self, text="Return to main menu",
                  command=lambda: master.switch_frame(mainMenu)).pack()
# Leaderboard
class Leaderboard(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Label(self, text="Leaderboard Page").pack(side="top", fill="x", pady=10)
        tk.Button(self, text="Return to main menu",
                  command=lambda: master.switch_frame(mainMenu)).pack()

def main():
  app = Tketris()
  app.geometry('1280x720')
  app.protocol("WM_DELETE_WINDOW", close_program)
  app.mainloop()

if __name__ == "__main__":
    main()