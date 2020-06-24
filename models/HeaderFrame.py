import tkinter as tk
from globals import *


class HeaderFrame(tk.Frame):

	def __init__(self, parent, text):

		tk.Frame.__init__(self, parent)
		self.text = text

		self.textLabel = tk.Label(self, text=text, font=titleFont)
		self.textLabel.grid(row=0, column=0, sticky='w')

		labelWidth = self.textLabel.winfo_reqwidth()
		canvasWidth = bodyWidth - labelWidth

		self.sepCanvas = tk.Canvas(self, width=canvasWidth, height=20, bg=whiteColor)
		self.sepCanvas.grid(row=0, column=1, sticky='ew')

		yCenter = self.sepCanvas.winfo_reqheight() / 2
		self.sepCanvas.create_line(0, yCenter, canvasWidth, yCenter)
