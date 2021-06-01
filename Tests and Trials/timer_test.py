import tkinter as tk

class ExampleApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.label = tk.Label(self, text="", width=10)
        self.label.pack()
        self.remaining = 0
        self.countdown(10)
        self.button = tk.Button(self, text="Stop",command=lambda:self.cancelcountdown())
        self.resetbutton = tk.Button(self,text="Reset",command=lambda:self.reset())
        self.button.pack()

    def countdown(self, remaining = None):
        if remaining is not None:
            self.remaining = remaining

        if self.remaining <= 0:
            self.label.configure(text="time's up!")
            self.button.pack_forget()
            self.resetbutton.pack()
        else:
            self.label.configure(text="%g" % self.remaining)
            self.remaining = self.remaining - 0.001
            self.countingdown = self.after(1, self.countdown)

    def cancelcountdown(self):
        self.after_cancel(self.countingdown)
        self.button.config(text='Continue',command=lambda:self.startcountdown())
        self.resetbutton.pack()
        

    def startcountdown(self):
        self.countdown(self.remaining)
        self.resetbutton.pack_forget()
        self.button.config(text='Stop',command=lambda:self.cancelcountdown())

    def reset(self):
        self.resetbutton.pack_forget()
        self.button.config(text='Stop',command=lambda:self.cancelcountdown())
        self.button.pack()
        self.countdown(10)
if __name__ == "__main__":
    app = ExampleApp()
    app.mainloop()