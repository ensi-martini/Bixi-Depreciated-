#bixi.py by Ensi Martini
#Completed on Thursday, Febuary 6, 2014
from urllib.request import *
from easygui import *
import webbrowser
file = urlopen(r'https://toronto.bixi.com/data/bikeStations.xml')
file = str(file.readline())

#Creating the parallel lists and counting the total amount of stations
stationNames = []
stationLong = []
stationLat = []
stationBikes = []
stationEmpties = []
stationAmount = file.count('<station>')

#Gather each station's data, and put that data in parallel lists
for station in range (stationAmount):
    #Extract the station name, latitude, longitude, how many bikes are available/unavailable
    stationNames.append(file[file.find('<name>') + 6:file.find('</name>')])
    stationLat.append(float(file[file.find('<lat>') + 5:file.find('</lat>')]))
    stationLong.append(float(file[file.find('<long>') + 6:file.find('</long>')]))
    stationBikes.append(int(file[file.find('<nbBikes>') + 9:file.find('</nbBikes')]))
    stationEmpties.append(int(file[file.find('<nbEmptyDocks>') + 14:file.find('</nbEmptyDocks')]))
    #Chop off everything left of "</station>" so each iteration grabs a different station's information
    file = file[file.find('</station>') + 10:]
    
#Present the user with a choicebox, and act accordingly 
choice = buttonbox('Select an option:', 'Bixi Data', ('System Data', 'Station Info', 'Quit'))
while choice != 'Quit':
    if choice == 'System Data':
        #Find the location of the greatest amount of bikes in the list, then use that same location to retrieve other information about the station using parallel lists
        index = stationBikes.index(max(stationBikes))
        msgbox("{} bikes total\nCentral location is ({:.3f},{:.3f})\n{} has {} bikes".format(sum(stationBikes), sum(stationLat)/stationAmount, sum(stationLong)/stationAmount, stationNames[index], max(stationBikes), "System Data", "OK"))
        webbrowser.open('http://maps.google.ca/maps?z=18&layer=c&cbll={},{}&cbp=0'.format(sum(stationLat)/stationAmount, sum(stationLong)/stationAmount))
    else:
        #Let the user choose a station, find that station's location in the list, and once again use parallel lists to retrieve other information about that station
        station = choicebox('Station Info', 'Please choose a station:', stationNames)
        index = stationNames.index(station)
        msgbox('{}: {} bikes, {} empty ({:.1f}% full)'.format(stationNames[index], stationBikes[index], stationEmpties[index], (stationBikes[index] / (stationBikes[index] + stationEmpties[index]) * 100 )), 'Station Info', 'See it!')
        webbrowser.open('http://maps.google.ca/maps?z=18&layer=c&cbll={},{}&cbp=0'.format(stationLat[index], stationLong[index]))
    choice = buttonbox('Select an option:', 'Bixi Data', ('System Data', 'Station Info', 'Quit'))