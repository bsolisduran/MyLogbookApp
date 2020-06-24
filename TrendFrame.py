import datetime as dt
import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


from globals import *
from models.HeaderFrame import HeaderFrame
from models.LogbookDataFrame import LogbookDataFrame


class TrendFrame(tk.Frame):

    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        # Main Frame of the class:
        trendFrame = tk.Frame(self, width=bodyWidth, height=400)
        trendFrame.pack()

        # Widgets in Navigation Frame:
        # -- Header Frame:
        headerText = "TREND "
        headerFrame = HeaderFrame(trendFrame, headerText)
        headerFrame.grid(row=0, column=0, sticky='nsew')

        # -- Navigation Frame:
        navFrame = tk.Frame(trendFrame)
        navFrame.grid(row=1, column=0, sticky='nsew')

        # -- Plots Frame:
        plotFrame = tk.Frame(trendFrame)
        plotFrame.grid(row=2, column=0, sticky='nsew')

        # ---- Data for plots:
        dfObj = LogbookDataFrame("data/sentbook_8anu.csv")
        df = dfObj.df
        trendDict = dfObj.get_trendDict()

        # ---- Plots:
        figSize = [10, 3.5]
        trendFig = self.get_trendPlot(trendDict, figSize)
        scoresFig = self.get_scoresPlot(trendDict, figSize)
        routesFig = self.get_routesPlot(trendDict, figSize)
        plotsList = [trendFig, scoresFig, routesFig]

        canvas = FigureCanvasTkAgg(trendFig, plotFrame)
        canvas.draw()
        canvas.get_tk_widget().grid(row=0, column=0, sticky='nsew')

        self.insert_button(parent=navFrame, text="TREND", ind=0, figList=plotsList, plotParent=plotFrame)
        self.insert_button(parent=navFrame, text="SCORES", ind=1, figList=plotsList, plotParent=plotFrame)
        self.insert_button(parent=navFrame, text="ROUTES", ind=2, figList=plotsList, plotParent=plotFrame)

    def insert_button(self, parent, text, ind, figList, plotParent):
        button = tk.Button(parent, text=text, cursor="hand", font=navFont, padx=40, pady=5,
                             command=lambda: self.show_plot(plotParent, figList[ind]))
        button.grid(row=0, column=ind, sticky='w')

    def show_plot(self, parent, figure):
        canvas = FigureCanvasTkAgg(figure, parent)
        canvas.draw()
        canvas.get_tk_widget().grid(row=0, column=0, sticky='nsew')

    def get_trendPlot(self, dataDict, figsize):
        years = dataDict["years"]
        points = dataDict["top10"]

        fig = plt.figure(figsize=figsize)
        ax = fig.add_subplot()
        plt.plot(range(len(years)), points, '-ks')
        plt.tick_params(
            axis='x', 
            which='both',
            bottom=True,
            top=False,
            labelbottom=True)

        ax.spines['top'].set_visible(False)    
        ax.spines['left'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['bottom'].set_visible(False)

        years[-1] = "Today"
        plt.xticks(range(len(years)), labels=years)
        plt.yticks([])
        # plt.ylim(top=1.025 * np.max(points))

        for i, v in enumerate(points):
            ax.text(i, v + 150, "%d" % v, ha="center")

        return fig

    def get_scoresPlot(self, dataDict, figsize):
        years = dataDict["years"]
        scores = dataDict["scoreRoutes"]
        
        totalList, RPList, FlList, OSList = [], [], [], []
        for i in range(0, len(scores)):
            totalList.append(scores[i][0])
            RPList.append(scores[i][1])
            FlList.append(scores[i][2])
            OSList.append(scores[i][3])
        xData = range(len(years))

        fig = plt.figure(figsize=figsize)
        ax = fig.add_subplot()
        plt.plot(xData, totalList, color=navGreyColor, linewidth=2)
        plt.plot(xData, RPList, color=RPColor, linewidth=2)
        plt.plot(xData, FlList, color=FLColor, linewidth=2)
        plt.plot(xData, OSList, color=OSColor, linewidth=2)

        plt.tick_params(
            axis='x', 
            which='both',
            bottom=True,
            top=False,
            labelbottom=True)

        ax.spines['top'].set_visible(False)    
        ax.spines['left'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['bottom'].set_visible(False)

        years[-1] = "Today"
        plt.xticks(range(len(years)), labels=years)
        plt.yticks([])
        # plt.ylim(top=1.025 * np.max(points))

        for i, v in enumerate(totalList):
            ax.text(i, v + 1200, "%d" % v, ha="center", color=navGreyColor)

        return fig

    def get_routesPlot(self, dataDict, figsize):
        years = dataDict["years"]
        numRoutes = dataDict["numRoutes"]
        
        totalList, RPList, FlList, OSList = [], [], [], []
        for i in range(0, len(numRoutes)):
            totalList.append(numRoutes[i][0])
            RPList.append(numRoutes[i][1])
            FlList.append(numRoutes[i][2])
            OSList.append(numRoutes[i][3])
        xData = range(len(years))

        fig = plt.figure(figsize=figsize)
        ax = fig.add_subplot()
        plt.plot(xData, totalList, color=navGreyColor, linewidth=2)
        plt.plot(xData, RPList, color=RPColor, linewidth=2)
        plt.plot(xData, FlList, color=FLColor, linewidth=2)
        plt.plot(xData, OSList, color=OSColor, linewidth=2)

        plt.tick_params(
            axis='x', 
            which='both',
            bottom=True,
            top=False,
            labelbottom=True)

        ax.spines['top'].set_visible(False)    
        ax.spines['left'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['bottom'].set_visible(False)

        years[-1] = "Today"
        plt.xticks(range(len(years)), labels=years)
        plt.yticks([])
        # plt.ylim(top=1.025 * np.max(points))

        for i, v in enumerate(totalList):
            ax.text(i, v + 2, "%d" % v, ha="center", color=navGreyColor)

        return fig

"""
frame functions:
def get_trend_data(df=df):
    import datetime as dt
    import numpy as np

    df = app.append_8apoints(df)

    firstYear = df["date"].iloc[0].year
    lastYear = dt.datetime.today().year
    yearsList = np.arange(firstYear, lastYear + 1).tolist()

    pointsList = []
    numRoutesList = []
    scoreRoutesList = []
    for year in yearsList:
        if year == yearsList[-1]:
            dataframe = app.get_12months_df(df)
        else:
            startDate = str(year) + "-01-01"
            endDate = str(year) + "-12-31"
            dataframe = df[(df["date"] > startDate) & (df["date"] < endDate)]

        points = app.get_top10score(dataframe)
        numRoutes, scoreRoutes = app.get_score_data(dataframe)
    
        pointsList.append(points)
        numRoutesList.append(numRoutes)
        scoreRoutesList.append(scoreRoutes)

    dataDict = {
        "years" : yearsList,
        "top10" : pointsList,
        "numRoutes" : numRoutesList,
        "scoreRoutes" : scoreRoutesList
    }
    
    return dataDict

def get_trendPlot(dataDict, figsize):
    years = dataDict["years"]
    points = dataDict["top10"]

    fig = plt.figure(figsize=figsize)
    ax = fig.add_subplot()
    plt.plot(range(len(years)), points, '-ks')
    plt.tick_params(
        axis='x', 
        which='both',
        bottom=True,
        top=False,
        labelbottom=True)

    ax.spines['top'].set_visible(False)    
    ax.spines['left'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)

    years[-1] = "Today"
    plt.xticks(range(len(years)), labels=years)
    plt.yticks([])
    # plt.ylim(top=1.025 * np.max(points))

    for i, v in enumerate(points):
        ax.text(i, v + 150, "%d" % v, ha="center")

    return fig

def get_scoresPlot(dataDict, figsize):
    years = dataDict["years"]
    scores = dataDict["scoreRoutes"]
    
    totalList, RPList, FlList, OSList = [], [], [], []
    for i in range(0, len(scores)):
        totalList.append(scores[i][0])
        RPList.append(scores[i][1])
        FlList.append(scores[i][2])
        OSList.append(scores[i][3])
    xData = range(len(years))

    fig = plt.figure(figsize=figsize)
    ax = fig.add_subplot()
    plt.plot(xData, totalList, color=navGrey, linewidth=2)
    plt.plot(xData, RPList, color=RPcolor, linewidth=2)
    plt.plot(xData, FlList, color=FLcolor, linewidth=2)
    plt.plot(xData, OSList, color=OScolor, linewidth=2)

    plt.tick_params(
        axis='x', 
        which='both',
        bottom=True,
        top=False,
        labelbottom=True)

    ax.spines['top'].set_visible(False)    
    ax.spines['left'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)

    years[-1] = "Today"
    plt.xticks(range(len(years)), labels=years)
    plt.yticks([])
    # plt.ylim(top=1.025 * np.max(points))

    for i, v in enumerate(totalList):
        ax.text(i, v + 1200, "%d" % v, ha="center", color=navGrey)

    return fig

def get_routesPlot(dataDict, figsize):
    years = dataDict["years"]
    numRoutes = dataDict["numRoutes"]
    
    totalList, RPList, FlList, OSList = [], [], [], []
    for i in range(0, len(numRoutes)):
        totalList.append(numRoutes[i][0])
        RPList.append(numRoutes[i][1])
        FlList.append(numRoutes[i][2])
        OSList.append(numRoutes[i][3])
    xData = range(len(years))

    fig = plt.figure(figsize=figsize)
    ax = fig.add_subplot()
    plt.plot(xData, totalList, color=navGrey, linewidth=2)
    plt.plot(xData, RPList, color=RPcolor, linewidth=2)
    plt.plot(xData, FlList, color=FLcolor, linewidth=2)
    plt.plot(xData, OSList, color=OScolor, linewidth=2)

    plt.tick_params(
        axis='x', 
        which='both',
        bottom=True,
        top=False,
        labelbottom=True)

    ax.spines['top'].set_visible(False)    
    ax.spines['left'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)

    years[-1] = "Today"
    plt.xticks(range(len(years)), labels=years)
    plt.yticks([])
    # plt.ylim(top=1.025 * np.max(points))

    for i, v in enumerate(totalList):
        ax.text(i, v + 2, "%d" % v, ha="center", color=navGrey)

    return fig

# update plot function:
def showPlot(ind):
    canvas = FigureCanvasTkAgg(plotsList[ind], plotFrame)
    canvas.draw()
    canvas.get_tk_widget().grid(row=0, column=0, sticky='nsew')


# Main Frame = Score Frame:
trendFrame = tk.Frame(root, width=800, height=400, bg=white)
trendFrame.pack()


# Child Frames:


# Plot Frame:
plotFrame = tk.Frame(trendFrame, bg=lightGrey)
plotFrame.grid(row=2, column=0, sticky='nsew')


trendDict = get_trend_data()
figSize = [10, 3.5]
trendFig = get_trendPlot(trendDict, figSize)
scoresFig = get_scoresPlot(trendDict, figSize)
routesFig = get_routesPlot(trendDict, figSize)
plotsList = [trendFig, scoresFig, routesFig]

canvas = FigureCanvasTkAgg(trendFig, plotFrame)
canvas.draw()
canvas.get_tk_widget().grid(row=0, column=0, sticky='nsew')

# mainloop:
root.mainloop()

"""
