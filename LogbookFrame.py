import tkinter as tk

from globals import *
from models.HeaderFrame import HeaderFrame
from models.LogbookDataFrame import LogbookDataFrame


class LogbookFrame(tk.Frame):

    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        logbookFrame = tk.Frame(self, bg=navGreyColor,
                                width=bodyWidth, height=400)
        logbookFrame.pack()

        # Widgets in Navigation Frame:
        # -- Header Frame:
        headerText = "LOGBOOK "

        headerFrame = HeaderFrame(logbookFrame, headerText)
        headerFrame.grid(row=0, column=0, sticky='nsew')

        # -- Navigation Frame:
        navFrame = tk.Frame(logbookFrame)
        navFrame.grid(row=1, column=0, sticky='nsew')

        sortVar = tk.StringVar(value='byGrade')

        # self.get_navFrame(navFrame, sortVar)

        # -- Table Frame:
        tableFrame = tk.Frame(logbookFrame)
        tableFrame.grid(row=2, column=0, sticky='nsew')

        self.get_log_table(tableFrame, sortVar)

        
        
    def get_navFrame(self, parent, sortVar):
        sortLabel = tk.Label(parent, text="Sort by: ", font=navFont)
        sortLabel.pack(side=tk.LEFT)

        gradeRb = tk.Radiobutton(parent, text='Grade ', variable=sortVar, value='byGrade', font=navFont)
        dateRb = tk.Radiobutton(parent, text='Date ', variable=sortVar, value='byDate', font=navFont)
        gradeRb.pack(side=tk.LEFT, padx=10)
        dateRb.pack(side=tk.LEFT, padx=10)


    def get_table_header(self, parent, grade):
        if grade:
            labelList = ["", "GRADE", "NAME", "CRAG", "DATE", "NOTES", "RATING", ""]
        else:
            labelList = ["", "NAME", "CRAG", "DATE", "NOTES", "RATING", ""]
        
        col = 0
        for text in labelList:
            self.get_header_label(parent, text, col)
            col +=1
        print(labelList)

    def get_header_label(self, parent, text, column):
        if text == 'NOTES':
            font = tableIFont
        else:
            font = tableFont
        label = tk.Label(parent, text=text, bg=navGreyColor, fg='white', font=font, padx=15, pady=7,
                            anchor='w')
        label.grid(row=0, column=column, sticky='nsew') 
        print(text, column)


    def get_log_table(self, parent, sortVar):
        print(sortVar)
        if sortVar == 'byGrade':
            GRADES = ['8c', '8b+', '8b', '8a+', '8a', '7c+', '7c', '7b+', '7b', '7a+', '7a', '6c+', '6c', '6b+', '6b',
                      '6a+', '6a']

            self.get_table_header(parent, sortVar)

        