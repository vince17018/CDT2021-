# Importing need modules
import tkinter as tk
# Setting up constants
HEIGHT = 720
WIDTH = 1280

# # Function for switching windows
# # Inputs is the window_variable we are switching to
# # Outputs by placing the called window on top
# def switch_windows(window):
#   new_window = tk.Toplevel(window)
#   canvas = tk.Canvas(new_window,height=HEIGHT,width=WIDTH)
#   canvas.pack()

class Tketris(tk.Tk):
  def __init__(self):
    tk.Tk.__init__(self)
    self._frame = None
    self.switch_frame(mainMenu)

  def switch_frame(self,frame_class):
    new_frame = frame_class(self)
    if self._frame is not None:
        self._frame.destroy()
    self._frame = new_frame
    self._frame.pack()

class StartPage(tk.Frame):
  def __init__(self, master):
      tk.Frame.__init__(self, master)
      tk.Label(self, text="This is the main menu placeholder").place()
      tk.Button(self, text="To the Game",
                command=lambda: master.switch_frame(Game)).place()
      tk.Button(self, text="To the options",
                command=lambda: master.switch_frame(Options)).place()
      tk.Button(self, text="To the leaderboard",
                command=lambda: master.switch_frame(leaderboard)).place()
      tk.Button(self, text="Quit",
                command=lambda: master.switch_frame(Options)).place()
  def quit

def main():
  root = tk.Tk()
  root.title("Tk.etris")
  root.mainloop()

if __name__ == "__main__":
    main()