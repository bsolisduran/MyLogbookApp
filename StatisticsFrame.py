import datetime as dt
import tkinter as tk

from globals import *
from models.HeaderFrame import HeaderFrame
from models.LogbookDataFrame import LogbookDataFrame


class StatisticsFrame(tk.Frame):

    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        # Data needed (TODO, pass as an arg):
        timeFilterVar = tk.StringVar(value='All Time')

        dfObj = LogbookDataFrame("data/sentbook_8anu.csv")
        df = dfObj.df
        yearsList = dfObj.get_yearsList()
        statsData = dfObj.get_statsData(df)

        # Main Frame of the class:
        statsFrame = tk.Frame(self, width=bodyWidth, height=400)
        statsFrame.pack()

        # Widgets in Navigation Frame:
        # -- Header Frame:
        headerText = "STATISTICS "
        headerFrame = HeaderFrame(statsFrame, headerText)
        headerFrame.grid(row=0, column=0, sticky='nsew')

        # -- Radiobuttons Frame:
        radioFrame = tk.Frame(statsFrame, bg=navGreyColor, height=100)
        radioFrame.grid(row=1, column=0, sticky='nsew', pady=5, padx=5)

        tableFrame = tk.Frame(statsFrame)
        tableFrame.grid(row=2, column=0, sticky='nsew')

        self.getRadioButtons(radioFrame, timeFilterVar, dfObj, tableFrame)

        # -- Table Frame:

        self.getStatisticsTable(tableFrame, statsData)

    def getRadioButtons(self, parent, variable, dataframeObject, TableParent):

        df = dataframeObject.df
        yearsList = dataframeObject.get_yearsList()

        rankingLabel = tk.Label(parent, text='Ranking Routes: ',
                                fg=whiteColor, bg=navGreyColor, font=navBoldFont)
        annualRb = tk.Radiobutton(parent, text='12 Months', variable=variable, value='12 Months', fg=whiteColor, bg=navGreyColor, font=navFont,
                                  command=lambda: self.update_frame(TableParent, variable.get(), dataframeObject))
        alltimeRb = tk.Radiobutton(parent, text='All Time', variable=variable, value='All Time', fg=whiteColor, bg=navGreyColor, font=navFont,
                                   command=lambda: self.update_frame(TableParent, variable.get(), dataframeObject))
        yearsLabel = tk.Label(parent, text='\tSelect year: ',
                              fg=whiteColor, bg=navGreyColor, font=navBoldFont)

        rankingLabel.pack(side=tk.LEFT, pady=15, padx=2)
        annualRb.pack(side=tk.LEFT, padx=2)
        alltimeRb.pack(side=tk.LEFT, padx=2)
        yearsLabel.pack(side=tk.LEFT, padx=2)

        for year in yearsList:
            radiobtn = tk.Radiobutton(parent, text=str(year), variable=variable, value=year, fg=whiteColor, bg=navGreyColor, font=navFont,
                                      command=lambda: self.update_frame(TableParent, variable.get(), dataframeObject))
            radiobtn.pack(side=tk.LEFT, padx=2)

    def update_frame(self, parent, var, dataframeObject):

        if var == '12 Months':
            dataframe = dataframeObject.annualdf
        elif var == 'All Time':
            dataframe = dataframeObject.df
        else:
            iniDate = dt.datetime(int(var), 1, 1)
            endDate = dt.datetime(int(var), 12, 31)
            dataframe = dataframeObject.get_yeardf(iniDate, endDate)

        # update the list of the data for the table plot:
        newStatsData = dataframeObject.get_statsData(dataframe)

        # update the table plot:
        for widget in parent.winfo_children():
            widget.destroy()
        self.getStatisticsTable(parent, newStatsData)

    def getStatisticsTable(self, parent, dataList):
        # get the total number of routes and the maximum routes of a grade:
        numRoutes = 0
        numRoutesxGrade = []
        for i in range(0, len(dataList)):
            numRoutes += dataList[i][4]
            numRoutesxGrade.append(dataList[i][4])
        maxRoutesxGrade = max(numRoutesxGrade)

        self.getHeaderStatisticsTable(parent, numRoutes)

        ind = 2
        for i in range(0, len(dataList)):
            if ind % 2 != 0:
                bgColor = whiteColor
            else:
                bgColor = lightGreyColor

            self.getRowStatisticsTable(
                parent, dataList[i], ind, maxRoutesxGrade, bgColor)
            ind += 1

    def getHeaderStatisticsTable(self, parent, totalRoutes):
        RPimg = tk.PhotoImage(file="images/RPicon.gif")
        FLimg = tk.PhotoImage(file="images/Ficon.gif")
        OSimg = tk.PhotoImage(file="images/OSicon.gif")

        # row 0: icons and total number of routes:
        OSicnLabel = tk.Label(parent, image=OSimg, width=90)
        OSicnLabel.image = OSimg
        FLicnLabel = tk.Label(parent, image=FLimg, width=90)
        FLicnLabel.image = FLimg
        RPicnLabel = tk.Label(parent, image=RPimg, width=90)
        RPicnLabel.image = RPimg
        totalNumLabel = tk.Label(
            parent, text=totalRoutes, font=totalFont, width=7)

        # row 1: labels of the icons:
        OSlabel = tk.Label(parent, text='ONSIGHT', fg=OSColor, font=headerFont)
        FLlabel = tk.Label(parent, text='FLASH', fg=FLColor, font=headerFont)
        RPlabel = tk.Label(parent, text='REDPOINT',
                           fg=RPColor, font=headerFont)
        totalLabel = tk.Label(parent, text='TOTAL', font=headerFont)
        # empty label to grid the bar plot rows and grades
        emptyLabel = tk.Label(parent, text=' ')

        # Layout:
        OSicnLabel.grid(row=0, column=0, sticky='nsew')
        FLicnLabel.grid(row=0, column=1, sticky='nsew')
        RPicnLabel.grid(row=0, column=2, sticky='nsew')
        totalNumLabel.grid(row=0, column=3, sticky='nsew')

        OSlabel.grid(row=1, column=0, sticky='nsew')
        FLlabel.grid(row=1, column=1, sticky='nsew')
        RPlabel.grid(row=1, column=2, sticky='nsew')
        totalLabel.grid(row=1, column=3, sticky='nsew')
        emptyLabel.grid(row=0, column=4, rowspan=2,
                        columnspan=2, sticky='nsew')

    def getRowStatisticsTable(self, parent, dataRow, index, maxRoutesInAGrade, bg):
        # Row numbers:
        for column in range(0, len(dataRow)-1):
            label = tk.Label(
                parent, text=dataRow[column+1], bg=bg, font=numberFont)
            label.grid(row=index, column=column, sticky='nsew')

        # Grade label:
        gradeLabel = tk.Label(
            parent, text=dataRow[0], bg=whiteColor, font=gradeFont)
        gradeLabel.grid(row=index, column=4, sticky='nsew', padx=15)

        # Bar Plot:
        barCanvas = tk.Canvas(parent, width=450, height=30, bg=bg)
        barCanvas.grid(row=index, column=5, sticky='nsew')

        xcenter = barCanvas.winfo_reqwidth() / 2
        ycenter = barCanvas.winfo_reqheight() / 2
        barLength = (dataRow[3] + dataRow[1] + dataRow[2]
                     ) / maxRoutesInAGrade * xcenter
        barCanvas.create_rectangle(xcenter - barLength, ycenter - 7, xcenter + barLength, ycenter + 7,
                                   fill=RPColor, outline=RPColor)

        if dataRow[2] != 0:
            barLength = (dataRow[1] + dataRow[2]) / maxRoutesInAGrade * xcenter
            barCanvas.create_rectangle(xcenter - barLength, ycenter - 7, xcenter + barLength, ycenter + 7,
                                       fill=FLColor, outline=FLColor)
        if dataRow[1] != 0:
            barLength = dataRow[1] / maxRoutesInAGrade * xcenter
            barCanvas.create_rectangle(xcenter - barLength, ycenter - 7, xcenter + barLength, ycenter + 7,
                                       fill=OSColor, outline=OSColor)
