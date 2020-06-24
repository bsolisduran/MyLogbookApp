import tkinter as tk

from globals import *
from models.HeaderFrame import HeaderFrame
from models.LogbookDataFrame import LogbookDataFrame


class RankingFrame(tk.Frame):

    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        rankingFrame = tk.Frame(self, bg=navGreyColor,
                                width=bodyWidth, height=400)
        rankingFrame.pack()

        # Widgets in Navigation Frame:
        # -- Header Frame:
        headerText = "SPORTCLIMBING RANKING"

        headerFrame = HeaderFrame(rankingFrame, headerText)
        headerFrame.grid(row=0, column=0, sticky='nsew')

        # -- Table Frame:
        tableFrame = tk.Frame(rankingFrame)
        tableFrame.grid(row=1, column=0, sticky='nsew')
        self.getRanking(parent=tableFrame, dataframe=None)

    def getRanking(self, parent, dataframe):
        # Get data from ranking.txt file:
        with open("data/ranking.txt", "r") as file:
            for rankingData in file:
                pass

        # Header Frame:
        labelList = ["", "SCORE", "", "ASCENTS", "",
                     "AVERAGE GRADE", "", "WORLD RANK", "", "COUNTRY RANK"]
        colCount = 0
        for item in labelList:
            label = tk.Label(parent, text=item, font=navFont,
                             fg=whiteColor, bg=navGreyColor, pady=10, padx=20)
            label.grid(row=0, column=colCount, sticky='nsew')
            colCount += 1

        # Time Labels:
        annualLabel = tk.Label(parent, text="LAST 12 MONTHS",
                               font=navFont, pady=20, padx=30)
        annualLabel.grid(row=1, column=0, sticky='nsew')
        alltimeLabel = tk.Label(parent, text="ALL TIME",
                                font=navFont, pady=20, padx=30)
        alltimeLabel.grid(row=2, column=0, sticky='nsew')

        # Logbook dataframe object:
        dfobj = LogbookDataFrame("data/sentbook_8anu.csv")
        # 12 Months:
        annualdf = dfobj.annualdf
        annualScore = dfobj.get_top10score(annualdf)
        annualAscents = dfobj.get_ascentsNumber(annualdf)
        annualGrade = rankingData.split(";")[1]
        annualWorld = rankingData.split(";")[2]
        annualCountry = rankingData.split(";")[3]
        # All time:
        alldf = dfobj.df
        allScore = dfobj.get_top10score(alldf)
        allAscents = dfobj.get_ascentsNumber(alldf)
        allGrade = rankingData.split(";")[4]
        allWorld = rankingData.split(";")[5]
        allCountry = rankingData.split(";")[6]

        labelsList = [annualScore, annualAscents, annualGrade, annualWorld, annualCountry,
                      allScore, allAscents, allGrade, allWorld, allCountry]
        rowsList = [1, 1, 1, 1, 1, 2, 2, 2, 2, 2]
        columnsList = [1, 3, 5, 7, 9, 1, 3, 5, 7, 9]
        for lbl in range(0, len(labelsList)):
            label = tk.Label(parent, text=labelsList[lbl], font=rankingFont)
            label.grid(row=rowsList[lbl],
                       column=columnsList[lbl], sticky='nsew')

        sepCols = [2, 4, 6, 8, 2, 4, 6, 8]
        sepRows = [1, 1, 1, 1, 2, 2, 2, 2]
        for sep in range(0, len(sepCols)):
            sepCanvas = tk.Canvas(parent, width=1, height=20, bg='black')
            sepCanvas.grid(row=sepRows[sep], column=sepCols[sep], sticky='ns')
