import pandas as pd
import datetime as dt
import numpy as np


class LogbookDataFrame:

    def __init__(self, fileName):
        self.fileName = fileName
        self.df = self.read_file()
        self.df = self.append_8apoints()
        self.annualdf = self.get_annualdf()

    def read_file(self):
        self.df = pd.read_csv(self.fileName, delimiter=";")
        self.df["date"] = pd.to_datetime(self.df["date"], format='%d-%m-%Y')
        return self.df

    def points_8anu(self, grade, style, tries):
        GRADE2POINTS = {"8b": 1100, "8a+": 1050, "8a": 1000, "7c+": 950, "7c": 900, "7b+": 850, "7b": 800, "7a+": 750,
                        "7a": 700, "6c+": 650, "6c": 600, "6b+": 550, "6b": 500, "6a+": 450, "6a": 400}
        STYLE2POINTS = {"OS": 145, "F": 53, "RP": 0}

        if tries == 2:
            TRIES2POINTS = 2
        else:
            TRIES2POINTS = 0

        points = GRADE2POINTS[grade] + STYLE2POINTS[style] + TRIES2POINTS
        return points

    def append_8apoints(self):
        gradeList = self.df["grade"].tolist()
        styleList = self.df["style"].tolist()
        triesList = self.df["tries"].tolist()

        pointsList = []

        for route in range(len(gradeList)):
            routePoints = self.points_8anu(
                gradeList[route], styleList[route], triesList[route])
            pointsList.append(routePoints)

        self.df["points"] = pointsList
        return self.df

    def get_annualdf(self):
        today = dt.datetime.today()
        enddate = today.strftime("%Y-%m-%d")
        enddateList = enddate.split(sep="-", maxsplit=1)
        startdate = str(int(enddateList[0]) - 1) + "-" + enddateList[1]

        mask = (self.df["date"] > startdate) & (self.df["date"] < enddate)
        yeardf = self.df[mask]
        return yeardf

    def get_top10score(self, dataframe):
        topRoutesDf = dataframe.sort_values(
            by=["points"], ascending=False).head(10)
        scoreList = topRoutesDf["points"].tolist()
        scoreList = np.asarray(scoreList)
        score = np.sum(scoreList)

        return score

    def get_ascentsNumber(self, dataframe):
        ascents = dataframe.shape[0]
        return ascents

    def get_yearsList(self):
        dataframe = self.df
        iniYear = dataframe["date"].iloc[0].year
        endYear = dataframe["date"].iloc[-1].year

        yearsList = []
        for year in range(iniYear, endYear+1):
            yearsList.append(year)
        return yearsList

    def get_statsData(self, dataframe):
        GRADES = ['8c', '8b+', '8b', '8a+', '8a', '7c+', '7c', '7b+', '7b', '7a+', '7a', '6c+', '6c', '6b+', '6b', '6a+', '6a']
        countList = ()
        for grade in GRADES:
            gradeDf = dataframe[dataframe["grade"] == grade]
            totalcount = gradeDf.shape[0]
            OSgradeDf = gradeDf[gradeDf["style"] == "OS"]
            OScount = OSgradeDf.shape[0]
            FLgradeDf = gradeDf[gradeDf["style"] == "F"]
            FLcount = FLgradeDf.shape[0]
            RPcount = totalcount - OScount - FLcount
            countList += [grade, OScount, FLcount, RPcount, totalcount],

        statsDataList = []
        for grade in range(0, len(countList)):
            if countList[grade][4] != 0:
                statsDataList.append(countList[grade])

        return statsDataList

    def get_yeardf(self, ini, end):
        yeardf = self.df[(self.df["date"] > ini) & (self.df["date"] < end)]
        return yeardf

    def get_trendDict(self):
        df = self.df
        yearsList = self.get_yearsList()

        pointsList = []
        numRoutesList = []
        scoreRoutesList = []
        for year in yearsList:
            if year == yearsList[-1]:
                dataframe = self.annualdf
            else:
                startDate = str(year) + "-01-01"
                endDate = str(year) + "-12-31"
                dataframe = df[(df["date"] > startDate) & (df["date"] < endDate)]

            points = self.get_top10score(dataframe)
            numRoutes = self.get_numRoutes(dataframe)
            scoreRoutes = self.get_scoreRoutes(dataframe)

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
    
    def get_numRoutes(self, dataframe):
        RPdf = dataframe[ dataframe["style"] == "RP" ]
        Fldf = dataframe[ dataframe["style"] == "F" ]
        OSdf = dataframe[ dataframe["style"] == "OS" ]
        
        totalroutes = dataframe.shape[0]
        RProutes = RPdf.shape[0]
        Flroutes = Fldf.shape[0]
        OSroutes = OSdf.shape[0]
        numRoutes = [totalroutes, RProutes, Flroutes, OSroutes]
        
        return numRoutes

    def get_scoreRoutes(self, dataframe):
        RPdf = dataframe[ dataframe["style"] == "RP" ]
        Fldf = dataframe[ dataframe["style"] == "F" ]
        OSdf = dataframe[ dataframe["style"] == "OS" ]
        
        scoreRoutes = []
        for data in [dataframe, RPdf, Fldf, OSdf]:
            df_temp = data
            pointsList = df_temp["points"].tolist()
            points = np.sum(np.asarray(pointsList))
            scoreRoutes.append(points)
        
        return scoreRoutes

    def get_grade_df(self, grade):
        df = self.df
        grade_dataframe = df[df["grade"] == grade]
        return grade_dataframe



