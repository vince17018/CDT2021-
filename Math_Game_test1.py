# Importing need modules
import tkinter as tk
# Setting up constants
HEIGHT = 720
WIDTH = 1280

# Function for switching windows
# Inputs is the window_variable we are switching to
# Outputs by placing the called window on top
def switch_windows(window):
  new_window = tk.Toplevel(window)
  canvas = tk.Canvas(new_window,height=HEIGHT,width=WIDTH)
  canvas.pack()


#class main_menu():
#    def __init__(self):
#      Button(main)



def main():
  root = tk.Tk()
  root.title("Tk.etris")
  canvas = tk.Canvas(root,height=HEIGHT,width=WIDTH)
  canvas.pack()
  main_menu()
  root.mainloop()

if __name__ == "__main__":
    main()