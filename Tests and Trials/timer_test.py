import tkinter as tk

class ExampleApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.label = tk.Label(self, text="", width=10)
        self.label.pack()
        self.remaining = 0
        self.countdown(10)
        
        self.button = tk.Button(self, text="Stop",command=lambda:self.cancelcountdown()).pack()

    def countdown(self, remaining = None):
        if remaining is not None:
            self.remaining = remaining

        if self.remaining <= 0:
            self.label.configure(text="time's up!")
        else:
            self.label.configure(text="%d" % self.remaining)
            self.remaining = self.remaining - 1
            self.countingdown = self.after(1000, self.countdown)
    def cancelcountdown(self):
        self.after_cancel(self.countingdown)
    
    





if __name__ == "__main__":
    app = ExampleApp()
    app.mainloop()