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

        # Data:
        sortVar = tk.StringVar(value='byGrade')

        dfObj = LogbookDataFrame("data/sentbook_8anu.csv")
        # df = dfObj.df

        # Widgets in Navigation Frame:
        # -- Header Frame:
        headerText = "LOGBOOK "

        headerFrame = HeaderFrame(logbookFrame, headerText)
        headerFrame.grid(row=0, column=0, sticky='nsew')

        # -- Navigation Frame:
        navFrame = tk.Frame(logbookFrame)
        navFrame.grid(row=1, column=0, sticky='nsew')

        self.get_navFrame(navFrame, sortVar)

        # -- Table Frame:
        tableFrame = tk.Frame(logbookFrame)
        tableFrame.grid(row=2, column=0, sticky='nsew')

        self.get_log_table(tableFrame, sortVar.get(), dfObj)

    def show_table(self, parent, variable):
        print(variable)

        
    def get_navFrame(self, parent, variable):
        sortLabel = tk.Label(parent, text="Sort by: ", font=navFont)
        sortLabel.pack(side=tk.LEFT)

        gradeRb = tk.Radiobutton(parent, text='Grade ', variable=variable, value='byGrade', font=navFont,
                                 command=lambda: self.show_table(parent, variable.get()))
        dateRb = tk.Radiobutton(parent, text='Date ', variable=variable, value='byDate', font=navFont,
                                command=lambda: self.show_table(parent, variable.get()))
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


    def get_header_label(self, parent, text, column):
        if text == 'NOTES':
            font = tableIFont
        else:
            font = tableFont
        label = tk.Label(parent, text=text, bg=navGreyColor, fg='white', font=font, padx=15, pady=7,
                            anchor='w')
        label.grid(row=0, column=column, sticky='nsew') 


    def get_log_table(self, parent, variable, dfObj):

        dataframe = dfObj.df
        dataframe = dataframe.sort_values(by='date', ascending=False)
        dataframe = dataframe.head(10)
        
        if variable == 'byGrade':
            GRADES = ['8c', '8b+', '8b', '8a+', '8a', '7c+', '7c', '7b+', '7b', '7a+', '7a', '6c+', '6c', '6b+', '6b',
                      '6a+', '6a']

            self.get_table_header(parent, variable)

            row = 1
            for grade in GRADES:
                gradeDf = dataframe[dataframe["grade"] == grade]
                routeIndex = gradeDf.index.tolist()
                routesXGrade = gradeDf.shape[0]
                if routesXGrade > 0:
                    self.insert_grade_header(parent, grade, row, False)
                    row += 1
                    bg = 0
                    for route in range(0, routesXGrade):
                        self.get_table_row(parent, dataframe, routeIndex[route], row, grade=False, bg=bg)


    def get_table_row(self, parent, df, index, row, grade, bg):
        if bg % 2 == 0:
            bg = tblGreyColor
        else:
            bg = whiteColor

        



    def insert_grade_header(self, parent, text, row, grade):
        gradeHeaderLabel = tk.Label(parent, text=text, font=tableBFont, justify='center',
                                    bg=darkGreyColor, pady=7)
        if grade:
            gradeHeaderLabel.grid(row=row, column=0, columnspan=7, sticky='nsew')  
        else:
            gradeHeaderLabel.grid(row=row, column=0, columnspan=8, sticky='nsew')  


        