import tkinter as tk

from AscentWindow import AscentWindow
from globals import *
from NavFrame import NavFrame
from RankingFrame import RankingFrame
from StatisticsFrame import StatisticsFrame
from TrendFrame import TrendFrame
from LogbookFrame import LogbookFrame


class MainApplication(tk.Frame):

    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        # Scrollable Frame:
        self.canvas = tk.Canvas(parent, borderwidth=0, background="#ffffff")
        self.frame = tk.Frame(self.canvas, background="#ffffff")
        self.vsb = tk.Scrollbar(parent, orient="vertical",
                                command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.vsb.set)
        self.vsb.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas.create_window((4, 4), window=self.frame, anchor="nw",
                                  tags="self.frame")
        self.frame.bind("<Configure>", self.onFrameConfigure)
        # self.canvas.bind('<MouseWheel>',self.canvas.yview)

        # Main Widgets
        self.navbar = NavFrame(self.frame)
        self.rankingbar = RankingFrame(self.frame)
        # self.statsframe = StatisticsFrame(self.frame)
        # self.trendframe = TrendFrame(self.frame)
        self.logframe = LogbookFrame(self.frame)


        self.navbar.grid(row=0, column=0, rowspan=4, sticky='ne')
        self.rankingbar.grid(row=0, column=1, padx=10, pady=10, sticky='nsew')
        # self.statsframe.grid(row=1, column=1, padx=10, pady=10, sticky='nsew')
        # self.trendframe.grid(row=2, column=1, padx=10, pady=10, sticky='nsew')
        self.logframe.grid(row=3, column=1, padx=10, pady=10, sticky='nsew')

    def size_screen(self):
        width = self.winfo_screenwidth()
        height = self.winfo_screenheight()
        return [width, height]

    def onFrameConfigure(self, event):
        '''Reset the scroll region to encompass the inner frame'''
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))


def main():
    root = tk.Tk()
    screenWidth = root.winfo_screenwidth()
    screenHeight = root.winfo_screenheight()
    root.geometry(f'{screenWidth}x{screenHeight}')
    root.title("8a.nu CLONE - Borja Solís ")

    app = MainApplication(root)
    app.pack(side='top', fill='both', expand=True)

    root.mainloop()


if __name__ == '__main__':
    main()
