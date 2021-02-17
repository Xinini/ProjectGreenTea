import pandas #pip install xlrd==1.2.0 for Excel files
import numpy
import matplotlib.pyplot as plt
import os

TEMP = "Temp. (cel)"
TIME = "Time (s)"

boilH = []
boilL = []
tapH = []
tapL = []
cup = []

class tempData():
    def __init__(self, filename, boil = False):
        self.filename = filename
        self.boil = boil #Bool if data is from a boiling water test
        self.tempDF = pandas.read_excel(self.filename)
        self.tempDF = self.tempDF.rename(columns={"Formula Result (Collected)" : TEMP, "Collected" : TIME}) #Renaming columns

        #Own attribute for plotting
        self.temp = self.tempDF[TEMP].to_numpy()
        self.time = self.tempDF[TIME]
        self.time = self.time.subtract(self.time[0]) #Subtract all elements by the start time so you start in time 0
        self.time = self.time / 1000 #Make to seconds
        #Interesting times
        if self.boil:
            self.time80 = min(self.tempDF[TIME].where(self.tempDF[TEMP] < 80).dropna()) #Time where the temperature first hits less than 80
    
    def soloPlot(self):
        plt.plot(self.time, self.temp)
    
    def plot(self):
        plt.plot(self.time, self.temp, label=self.filename)


def makeTempList(filenames, boil): #Converts the filenames to an actual object
    for i in range(len(filenames)):
        filenames[i] = tempData(filenames[i], boil)
    return filenames

def multiPlot(data): #Plot all the graphs you want. Need 2D list as paramter
    for i in data:
        for x in i:
            x.plot()
    plt.xlabel(TIME)
    plt.ylabel(TEMP)
    plt.legend(loc="lower left")

def avgPlot(temps): #temps is list of objects with .temp attribute 
    avgTemp = numpy.zeros(temps[0].temp.size)
    for i in temps:
        avgTemp += i.temp
    avgTemp = avgTemp/len(temps)
    plt.plot(temps[0].time, avgTemp)
    plt.xlabel(TIME)
    plt.ylabel(TEMP)
    plt.legend(loc = "lower left")



for i in os.listdir(): #Sort all the filenames into seperate lists
    if "boil_h" in i:
        boilH.append(i)
    elif "boil_l" in i:
        boilL.append(i)
    elif "cup" in i:
        cup.append(i)
    elif "tapl" in i:
        tapL.append(i)
    elif "taph" in i:
        tapH.append(i)

boilH = makeTempList(boilH, True)
boilL = makeTempList(boilL, True)
tapH = makeTempList(tapH, False)
tapL = makeTempList(tapL, False)
cup = makeTempList(cup, True)

avgPlot(boilH)


plt.show()
"""    
#Data
tempData = pandas.read_excel("boil_h1.xlsx")
tempData = tempData.rename(columns={"Formula Result (Collected)" : "Temperature (cel)", "Collected" : "Time (ms)"})

print(min(tempData["Time (ms)"].where(tempData["Temperature (cel)"] < 80).dropna()))


#Plotting
plt.plot(tempData["Time (ms)"], tempData["Temperature (cel)"])

plt.xlabel(tempData.columns.values[1])
plt.ylabel(tempData.columns.values[0])
plt.grid()
plt.title("Temperature of Thermistor")
plt.show()

"""