import tkinter as tk
from globals import *


class AscentWindow(tk.Toplevel):
    def __init__(self, *args, **kwargs):
        tk.Toplevel.__init__(self, *args, **kwargs)
        
        self.title("Add Ascent Window")
        self.geometry("600x600")

        self.label1 = tk.Label(self, text="Add Ascent manager", font=numberFont)
        self.label1.pack()
        self.button1 = tk.Button(self, text = 'Close Window', width = 25, command = self.close_window)
        self.button1.pack()

    def close_window(self):
        self.destroy()