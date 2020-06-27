import datetime as dt
import tkinter as tk
from tkinter import ttk
import math

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
        self.sortVar = tk.StringVar(value='byGrade')
        self.dfObj = LogbookDataFrame("data/sentbook_8anu.csv")

        # Widgets in Navigation Frame:
        # -- Header Frame:
        headerText = "LOGBOOK "

        headerFrame = HeaderFrame(logbookFrame, headerText)
        headerFrame.grid(row=0, column=0, sticky='nsew')

        # -- Navigation Frame:
        navFrame = tk.Frame(logbookFrame)
        navFrame.grid(row=1, column=0, sticky='nsew')

        # -- Table Frame:
        tableFrame = tk.Frame(logbookFrame)
        tableFrame.grid(row=2, column=0, sticky='nsew')

        self.get_navFrame(navFrame, tableFrame)
        self.get_log_table(tableFrame)

    def show_table(self, table_parent):
        for widget in table_parent.winfo_children():
            widget.destroy()

        # sortVar = self.sortVar.get()
        # timeVar = self.timeFilterCombo.get()
        self.get_log_table(table_parent)

    def get_navFrame(self, parent, table_parent):
        sortLabel = tk.Label(parent, text="Sort by: ", font=navFont)
        sortLabel.pack(side=tk.LEFT)

        df = self.dfObj.df
        yearsList = self.dfObj.get_yearsList()
        variable = self.sortVar

        gradeRb = tk.Radiobutton(parent, text='Grade ', variable=variable, value='byGrade', font=navFont,
                                 command=lambda: self.show_table(table_parent))
        dateRb = tk.Radiobutton(parent, text='Date ', variable=variable, value='byDate', font=navFont,
                                command=lambda: self.show_table(table_parent))
        gradeRb.pack(side=tk.LEFT, padx=10, pady=10)
        dateRb.pack(side=tk.LEFT, padx=10)

        timeLabel = tk.Label(parent, text='Time filter: ', font=navFont)
        timeLabel.pack(side=tk.LEFT, padx=10)
        comboValues = ["12 Months", "All Time"] + yearsList
        self.get_comboList(parent, comboValues, table_parent)

    def get_comboList(self, parent, values, table_parent):
        self.timeFilterCombo = ttk.Combobox(
            parent, values=values, font=navFont, state='readonly')
        parent.option_add('*TCombobox*Listbox.font', navFont)
        self.timeFilterCombo.current(1)
        # self.timeFilterCombo.bind("<<ComboboxSelected>>", lambda event: self.callbackFunc(self.timeFilterCombo.get()))
        self.timeFilterCombo.bind(
            "<<ComboboxSelected>>", lambda event: self.show_table(table_parent))

        # print(dfObj.df)
        self.timeFilterCombo.pack(side=tk.LEFT, padx=10)

    def callbackFunc(self, value):
        print(self.dfObj.df)
        print(value)

    def get_table_header(self, parent, grade):
        if grade:
            labelList = ["", "GRADE", "NAME", "CRAG",
                         "DATE", "NOTES", "RATING", ""]
        else:
            labelList = ["", "NAME", "CRAG", "DATE", "NOTES", "RATING", ""]

        col = 0
        for text in labelList:
            self.get_header_label(parent, text, col)
            col += 1

    def get_header_label(self, parent, text, column):
        if text == 'NOTES':
            font = tableIFont
        else:
            font = tableFont
        label = tk.Label(parent, text=text, bg=navGreyColor, fg='white', font=font, padx=15, pady=7,
                         anchor='w')
        label.grid(row=0, column=column, sticky='nsew')

    def get_log_table(self, parent):

        timeVar = self.timeFilterCombo.get()
        if timeVar == '12 Months':
            dataframe = self.dfObj.annualdf
        elif timeVar == 'All Time':
            dataframe = self.dfObj.df
        else:
            iniDate = dt.datetime(int(timeVar), 1, 1)
            endDate = dt.datetime(int(timeVar), 12, 31)
            dataframe = self.dfObj.get_yeardf(iniDate, endDate)

        dataframe = dataframe.sort_values(by="date", ascending=False)
        variable = self.sortVar.get()

        if variable == 'byGrade':
            GRADES = ['8c', '8b+', '8b', '8a+', '8a', '7c+', '7c', '7b+', '7b', '7a+', '7a', '6c+', '6c', '6b+', '6b',
                      '6a+', '6a']

            self.get_table_header(parent, False)
            row = 1
            for grade in GRADES:
                gradeDf = dataframe[dataframe["grade"] == grade]
                routeIndex = gradeDf.index.tolist()
                routesXGrade = gradeDf.shape[0]
                if routesXGrade > 0:
                    self.get_grade_header(parent, grade, row, False)
                    row += 1
                    bg = 0
                    for route in range(0, routesXGrade):
                        self.get_table_row(
                            parent, routeIndex[route], row, grade=False, bg=bg)
                        row += 1
                        bg += 1

        elif variable == 'byDate':
            self.get_table_header(parent, grade=True)

            row = 1
            bg = 0
            routeIndex = dataframe.index.tolist()
            for route in range(0, dataframe.shape[0]):
                self.get_table_row(parent,
                                   routeIndex[route], row, grade=True, bg=bg)
                row += 1
                bg += 1

    def get_table_row(self, parent, routeIndex, row, grade, bg):
        df = self.dfObj.df

        if bg % 2 == 0:
            bg = tblGreyColor
        else:
            bg = whiteColor

        # RP/F/OS icon label
        RPimg = tk.PhotoImage(file="images/RPicon.gif")
        FLimg = tk.PhotoImage(file="images/Ficon.gif")
        OSimg = tk.PhotoImage(file="images/OSicon.gif")

        if df["style"][routeIndex] == 'OS':
            styleLabel = tk.Label(parent, image=OSimg, bg=bg, padx=5)
            styleLabel.image = OSimg
        elif df["style"][routeIndex] == 'F':
            styleLabel = tk.Label(parent, image=FLimg, bg=bg, padx=5)
            styleLabel.image = FLimg
        else:
            styleLabel = tk.Label(parent, image=RPimg, bg=bg, padx=5)
            styleLabel.image = RPimg

        # Route name Label:
        nameText = df["name"][routeIndex]
        nameLabel = tk.Label(parent, text=nameText, font=tableFont,
                             anchor='w', justify='left', bg=bg, padx=5)

        # crag:
        sectorText = df['sector'][routeIndex]
        subsectorText = df['subsector'][routeIndex]
        if str(subsectorText) == 'nan':
            cragText = sectorText
        else:
            cragText = sectorText + '/' + subsectorText
            if len(cragText) > 25:
                words = cragText.split(" ")
                words[-1] = '\n' + words[-1]
                cragText = " ".join(words)

        cragLabel = tk.Label(parent, text=cragText, font=tableFont,
                             anchor='w', justify='left', bg=bg, padx=5)

        # Date:
        dateLabel = tk.Label(parent, text=df['date'][routeIndex].date(
        ), font=tableFont, anchor='w', justify='left', bg=bg, padx=5)

        # Comments:
        commentsText = df['com1'][routeIndex]
        maxLength = 46
        commentsText = self.split_comments(commentsText, maxLength)

        commentsLabel = tk.Label(
            parent, text=commentsText, font=tableIFont, anchor='w', justify='left', bg=bg, padx=5)

        # Rating:
        ratingText = df['stars'][routeIndex]
        ratingLabel = tk.Label(parent, text=ratingText, font=tableFont,
                               anchor='c', justify='center', bg=bg, padx=5)

        # Edit Ascent:
        editimg = tk.PhotoImage(file="images/editIcon.gif")
        editLabel = tk.Label(parent, image=editimg, bg=bg, padx=5)
        editLabel.image = editimg

        # Grade:
        gradeLabel = tk.Label(parent, text=df['grade'][routeIndex],
                              font=tableFont, justify='center', anchor='c', bg=bg, padx=5)

        # Layout:
        styleLabel.grid(row=row, column=0, sticky='nsew')
        nameLabel.grid(row=row, column=1, sticky='nsew')
        if grade:
            gradeLabel.grid(row=row, column=2, sticky='nsew')
            cragLabel.grid(row=row, column=3, sticky='nsew')
            dateLabel.grid(row=row, column=4, sticky='nsew')
            commentsLabel.grid(row=row, column=5, sticky='nsew')
            ratingLabel.grid(row=row, column=6, sticky='nsew')
            editLabel.grid(row=row, column=7, sticky='nsew')
        else:
            cragLabel.grid(row=row, column=2, sticky='nsew')
            dateLabel.grid(row=row, column=3, sticky='nsew')
            commentsLabel.grid(row=row, column=4, sticky='nsew')
            ratingLabel.grid(row=row, column=5, sticky='nsew')
            editLabel.grid(row=row, column=6, sticky='nsew')

    def get_grade_header(self, parent, text, row, grade):
        gradeHeaderLabel = tk.Label(parent, text=text, font=tableBFont, justify='center',
                                    bg=darkGreyColor, pady=7)
        if grade:
            gradeHeaderLabel.grid(
                row=row, column=0, columnspan=7, sticky='nsew')
        else:
            gradeHeaderLabel.grid(
                row=row, column=0, columnspan=8, sticky='nsew')


    def split_comments(self, text, max_length):

        if str(text) == "nan":  # no comments
            new_text = ""
            return new_text
        
        text_length = len(text)
        if text_length > max_length:  # long comments
            lines = math.ceil(text_length / max_length)
            new_text = ""

            ini = 0
            end = max_length
            for line in range(0,lines):
                if line == lines - 1:
                    new_text = new_text + text[ini:end]
                else:
                    # new_text = new_text + text[ini:end] + "\n"
                    if text[end] == " ":
                        new_text = new_text + text[ini:end] + "\n"
                    elif text[end-1] == " ":
                        new_text = new_text + text[ini:end-1] + "\n"
                    elif text[end-2] == " ":
                        new_text = new_text + text[ini:end-2] + "\n"
                        ini -= 1
                    else:
                        new_text = new_text + text[ini:end] + "-\n"

                ini = len(new_text)
                end = ini + max_length

                # ini += max_length
                # end += max_length
        else:
            new_text = text

        return new_text