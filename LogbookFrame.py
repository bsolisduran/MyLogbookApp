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
        dataframe = dfObj.df
        dataframe = dataframe.sort_values(by='date', ascending=False)
        dataframe = dataframe.head(30)

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

        self.get_navFrame(navFrame, sortVar, dataframe, tableFrame)
        self.get_log_table(tableFrame, sortVar.get(), dataframe)

    def show_table(self, parent, variable, dataframe, table_parent):
        for widget in table_parent.winfo_children():
            widget.destroy()
        
        self.get_log_table(table_parent, variable, dataframe)



    def get_navFrame(self, parent, variable, df, table_parent):
        sortLabel = tk.Label(parent, text="Sort by: ", font=navFont)
        sortLabel.pack(side=tk.LEFT)

        gradeRb = tk.Radiobutton(parent, text='Grade ', variable=variable, value='byGrade', font=navFont,
                                 command=lambda: self.show_table(parent, variable.get(), df, table_parent))
        dateRb = tk.Radiobutton(parent, text='Date ', variable=variable, value='byDate', font=navFont,
                                command=lambda: self.show_table(parent, variable.get(), df, table_parent))
        gradeRb.pack(side=tk.LEFT, padx=10, pady=10)
        dateRb.pack(side=tk.LEFT, padx=10)


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

    def get_log_table(self, parent, variable, dataframe):

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
                    self.insert_grade_header(parent, grade, row, False)
                    row += 1
                    bg = 0
                    for route in range(0, routesXGrade):
                        self.get_table_row(
                            parent, dataframe, routeIndex[route], row, grade=False, bg=bg)
                        row += 1
                        bg += 1
        elif variable == 'byDate':
            self.get_table_header(parent, grade=True)

            row = 1
            bg = 0
            routeIndex = dataframe.index.tolist()
            for route in range(0, dataframe.shape[0]):
                self.get_table_row(parent, dataframe,
                                   routeIndex[route], row, grade=True, bg=bg)
                row += 1
                bg += 1

    def get_table_row(self, parent, df, routeIndex, row, grade, bg):
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
        maxLength = 54

        if str(commentsText) == 'nan':          # no comments
            commentsText = ' '
        elif len(commentsText) > maxLength:     # long comment
            if commentsText[maxLength] == " ":
                commentsText = commentsText[:maxLength] + \
                    "\n" + commentsText[maxLength + 1:]
            elif commentsText[maxLength - 1] == " ":
                commentsText = commentsText[:maxLength] + \
                    "\n" + commentsText[maxLength:]
            else:
                commentsText = commentsText[:maxLength] + \
                    "-\n" + commentsText[maxLength:]
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

    def insert_grade_header(self, parent, text, row, grade):
        gradeHeaderLabel = tk.Label(parent, text=text, font=tableBFont, justify='center',
                                    bg=darkGreyColor, pady=7)
        if grade:
            gradeHeaderLabel.grid(
                row=row, column=0, columnspan=7, sticky='nsew')
        else:
            gradeHeaderLabel.grid(
                row=row, column=0, columnspan=8, sticky='nsew')
