import tkinter as tk

from globals import *
from models.HeaderFrame import HeaderFrame
from models.LogbookDataFrame import LogbookDataFrame


class LogbookFrame(tk.Frame):

    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        rankingFrame = tk.Frame(self, bg=navGreyColor,
                                width=bodyWidth, height=400)
        rankingFrame.pack()

        # Widgets in Navigation Frame:
        # -- Header Frame:
        headerText = "LOGBOOK "

        headerFrame = HeaderFrame(rankingFrame, headerText)
        headerFrame.grid(row=0, column=0, sticky='nsew')

        # -- Table Frame:

        