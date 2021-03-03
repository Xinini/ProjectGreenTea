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
            self.time80 = min(self.tempDF[TIME].where(self.tempDF[TEMP] < 85).dropna()) #Time where the temperature first hits less than 80
            #self.max = min(self.tempDF[TIME][self.tempDF[TEMP].max.index])
    
    
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
    plt.legend(loc="upper left")

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
    plt.legend(loc = "0")



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

# cup = makeTempList(cup, True)
# boilL = makeTempList(boilL, True)
boilH = makeTempList(boilH, True)
# tapH = makeTempList(tapH, True)
# tapL = makeTempList(tapL, True)
#multiPlot([cup])
avgPlot(boilH)
plt.plot(903.2, 39.355, 'ro', label = "1 tau (41.2s after step)")
plt.legend()

plt.show()

# multiPlot([cup])
# plt.savefig('cup.png')
# plt.figure()
# avgPlot(cup)
# plt.savefig('cupAvg.png')
# plt.figure()
# multiPlot([boilH])
# plt.savefig('boilH.png')
# plt.figure()
# avgPlot(boilH)
# plt.savefig('boilHAvg.png')
# plt.figure()
# multiPlot([boilL])
# plt.savefig('boilL.png')
# plt.figure()
# avgPlot(boilL)
# plt.savefig('boilLAvg.png')
# plt.figure()
# multiPlot([tapH])
# plt.savefig('tapH.png')
# plt.figure()
# avgPlot(tapH)
# plt.savefig('tapHAVG.png')
# plt.figure()
# multiPlot([tapL])
# plt.savefig('tapL.png')
# plt.figure()
# avgPlot(tapL)
# plt.savefig('tapLAVG.png')


