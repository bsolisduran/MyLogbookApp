import tkinter as tk

from AscentWindow import AscentWindow
from globals import *


class NavFrame(tk.Frame):

    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        navFrame = tk.Frame(self, bg=navGreyColor, width=200, height=1000)
        navFrame.pack()
        navFrame.pack_propagate(0)

        # Widgets in Navigation Frame:
        # -- Username:
        userName = "Borja Solís"

        userCanvas = tk.Canvas(
            navFrame, width=100, height=100, bg=navGreyColor, bd=0, highlightthickness=0)
        userCanvas.pack(pady=20)
        self.create_circle(50, 50, 48, userCanvas)

        userLabel = tk.Label(navFrame, text=userName, font=navBoldFont,
                             fg=whiteColor, bg=navGreyColor, pady=10)
        userLabel.pack()

        # -- Separator:
        sepCanvas = tk.Canvas(navFrame, width=150, height=10,
                              bg=navGreyColor, bd=0, highlightthickness=0,)
        sepCanvas.pack(pady=10)
        ycenter = sepCanvas.winfo_reqheight() / 2
        sepCanvas.create_line(0, ycenter, 150, ycenter, width=2)

        # -- Add Ascent Button:
        addButton = tk.Button(navFrame, width=140, height=2, text="ADD ASCENT", font=navFont, highlightbackground=navGreyColor,
                              command=self.new_window)
        addButton.pack(pady=10)

        # -- Add Logbooks Buttons (Routes and Boulders)
        myLogLabel = tk.Label(navFrame, text="MY LOGBOOK ",
                              font=navFont, fg=whiteColor, bg=navGreyColor)
        myLogLabel.pack()

        routesButton = tk.Button(navFrame, width=140, height=2,
                                 text="ROUTES", font=navFont, highlightbackground=navGreyColor)
        routesButton.pack()
        bouldersButton = tk.Button(navFrame, width=140, height=2,
                                   text="BOULDERS", font=navFont, highlightbackground=navGreyColor)
        bouldersButton.pack()

    def new_window(self):
        self.ascentWindow = AscentWindow(self.parent)

    def create_circle(self, x, y, r, canvasName):
        x0 = x - r
        y0 = y - r
        x1 = x + r
        y1 = y + r
        return canvasName.create_oval(x0, y0, x1, y1, width=2, fill=lightGreyColor)
