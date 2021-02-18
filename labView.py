import pandas #pip install xlrd==1.2.0 for Excel files
import numpy
import matplotlib.pyplot as plt
import os

TEMP = "Temp. (cel)"
TIME = "Time (s)"


HIGH = True

dirname = os.path.dirname(__file__)

boilH = []
boilL = []
tapH = []
tapL = []
cup = []

class tempData(): #Class for each file
    def __init__(self, filename, boil = False):
        self.filename = filename
        self.boil = boil #Bool if data is from a boiling water test
        self.tempDF = pandas.read_excel(os.path.join(dirname, "temperatureData/" + self.filename))
        self.tempDF = self.tempDF.rename(columns={"Formula Result (Collected)" : TEMP, "Collected" : TIME}) #Renaming columns

        #Own attribute for plotting
        self.temp = self.tempDF[TEMP].to_numpy() #Convert to a numpy array for easier manipulation
        self.time = self.tempDF[TIME]
        self.time = self.time.subtract(self.time[0]) #Subtract all elements by the start time so you start in time 0
        self.time = self.time / 1000 #Make to seconds
        #Interesting times
        if self.boil:
            self.time80 = min(self.tempDF[TIME].where(self.tempDF[TEMP] < 80).dropna()) #Time where the temperature first hits less than 80
    
    
    def plot(self):
        plt.plot(self.time, self.temp, label=self.filename)


def makeTempList(filenames, boil): #Converts the filenames to an actual object
    for i in range(len(filenames)):
        filenames[i] = tempData(filenames[i], boil) #Puts each object to the original list
    return filenames

def multiPlot(data): #Plot all the graphs you want. Need 2D list as paramter
    for i in data:
        for x in i:
            x.plot()
    plt.xlabel(TIME)
    plt.ylabel(TEMP)
    plt.legend(loc="lower left")

def avgPlot(temps): #temps is list of objects with .temp attribute 
    lowestSize = temps[0].temp.size
    for i in temps:
        if lowestSize > i.temp.size:
            lowestSize = i.temp.size
            print("low: " + str(lowestSize))
    avgTemp = numpy.zeros(lowestSize)
    print(avgTemp.shape)
    for i in temps:
        print(i.temp[:lowestSize].shape)
        avgTemp += i.temp[:lowestSize]
    avgTemp = avgTemp/len(temps)
    plt.plot(temps[0].time[:lowestSize], avgTemp, label= "Average")
    plt.xlabel(TIME)
    plt.ylabel(TEMP)
    plt.legend(loc = "lower left")



for i in os.listdir(os.path.join(dirname, "temperatureData")): #Sort all the filenames into seperate lists
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
cup = makeTempList(cup, True)
tapH = makeTempList(tapH, True)
tapL = makeTempList(tapL, True)


# multiPlot([cup])
# plt.figure()
# avgPlot(cup)
# plt.figure()
# multiPlot([boilH])
# plt.figure()
# avgPlot(boilH)
# plt.figure()
# multiPlot([boilL])
# plt.figure()
# avgPlot(boilL)
# plt.figure()
# multiPlot([tapH])
# plt.figure()
avgPlot(tapH)
# plt.figure()
# multiPlot([tapL])
# plt.figure()
# avgPlot(tapL)



plt.grid()
plt.show()