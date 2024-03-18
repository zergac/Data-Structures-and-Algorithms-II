# Carolina Zerga
# 000996689

import csv
from datetime import datetime, date, timedelta, time
from tkinter import *
from tkinter import ttk
import tkinter as tk 
from tkinter import messagebox
from tkinter.ttk import Treeview


#HashTable Class
class HashTable:

    def __init__(self):
        self.keys = []
        for i in range(0,10):
            alist = []
            self.keys.append(alist)

    def insert(self, id, pack):
        index = id%10
        self.keys[index].append(pack)

    def lookUp(self,id):
        index = id%10
        for i in range(0,len(self.keys[index])):
            if id == int(self.keys[index][i].packageID):
                return self.keys[index][i]



class Truck:

    def __init__(self):
        self.maxPacks = 16
        self.packs = []
        self.starTime = None
        self.finishTIme = None
        self.number = 0



class Package:

    def __init__(self):
        self.packageID = 0
        self.address = ""
        self.city = ""
        self.state = ""
        self.zip = 0
        self.time = None
        self.weight = 0
        self.deliveryStatus = "Hub"
        self.deliveredTime = None
        self.requiredTruck = ""
        self.truck = 0
        self.startTime = None

    def __str__(self):
        return "Package ID# " + str(self.packageID) + " with " + str(self.weight) + " kilos needs to delivered by " + str(self.time) + " at " + self.address + " " + self.city + " " + self.state + " " +  str(self.zip)  



def availablePackages(assignedPacks):
    #receives a list of packages that have been assigned to a truck
    #returns a list of packages that have not been assigned to a truck
    unassignedPacks = []
    for i in range(0,len(packageList)):
        areEqual = False
        for j in range(0, len(assignedPacks)):
            if packageList[i].packageID == assignedPacks[j].packageID:
                areEqual = True
        if areEqual == False:
            unassignedPacks.append(packageList[i])
    return unassignedPacks


def availableCombinedPackages(t1, t2):
    #receives a list of packages from one truck and another list from the other truck
    #returns a list of unassigned packages 
    packsFromTrucks = []
    for i in range(0, len(t1)):
        packsFromTrucks.append(t1[i])
    for i in range(0, len(t2)):
        packsFromTrucks.append(t2[i])
    return availablePackages(packsFromTrucks)


def getCombinedPackages (t1, t2):
    #receives a list of packages from one truck and another list from the other truck
    #returns all packages from both trucks into one list
    addedPacks = []
    for i in range(0, len(t1)):
        addedPacks.append(t1[i])
    for i in range(0, len(t2)):
        addedPacks.append(t2[i])
    return addedPacks


def distanceBtwnPackagess(p1, p2):
    #receives 2 packages
    #returns the distance between those 2 packages
    for i in range(0, len(distBtwn2Addrss)):
        if p1.address in distBtwn2Addrss[i][0] and p2.address in distBtwn2Addrss[i][1]:
            return distBtwn2Addrss[i][2]
        if p1.address in distBtwn2Addrss[i][1] and p2.address in distBtwn2Addrss[i][0]:
            return distBtwn2Addrss[i][2]
        if p1.address == p2.address:
            return 0
        

def whichTruck(usedPacksT1, usedPacksT2, unassignedPacks):
    #receives list of packages from one truck, a list of packages from another truck and a list of unassigned packages
    #returns a list of list of packages where the unassigned packages are now assigned with a specific truck
    trucks = []
    minDistTruck1 = 999
    minDistTruck2 = 999
    for i in range(0, len(usedPacksT1)):
        for j in range(0, len(unassignedPacks)):
            dist = distanceBtwnPackagess(usedPacksT1[i], unassignedPacks[j])
            if float(dist) < minDistTruck1:
                minDistTruck1 = float(dist)
                pack1 = unassignedPacks[j]
    for i in range(0, len(usedPacksT2)):
        for j in range(0, len(unassignedPacks)):
            dist = distanceBtwnPackagess(usedPacksT2[i], unassignedPacks[j])
            if float(dist) < minDistTruck2:
                minDistTruck2 = float(dist)
                pack2 = unassignedPacks[j]
    if ((minDistTruck1 < minDistTruck2 or minDistTruck1 == minDistTruck2) and len(usedPacksT1) < 16):
        usedPacksT1.append(pack1)
    elif (minDistTruck2 < minDistTruck1) and len(usedPacksT2) < 16:
        usedPacksT2.append(pack2)
    elif ((minDistTruck1 < minDistTruck2 or minDistTruck1 == minDistTruck2) and (len(usedPacksT1) == 16 and len(usedPacksT2) < 16)):
        usedPacksT2.append(pack1)
    elif ((minDistTruck2 < minDistTruck1) and (len(usedPacksT2) == 16 and len(usedPacksT1) < 16)):
        usedPacksT1.append(pack2)
    trucks.append(usedPacksT1)
    trucks.append(usedPacksT2)
    return trucks


def assignPackages():
    #it assigns packages to either truck 1 or truck 2
    availablePacks = availableCombinedPackages(getCombinedPackages(truckOne.packs, truckTwo.packs), truckThree.packs)
    for i in range(0, truckOne.maxPacks * 2):
        alist = whichTruck(truckOne.packs, truckTwo.packs, availablePacks)
        availablePacks = availableCombinedPackages(getCombinedPackages(truckOne.packs, truckTwo.packs), truckThree.packs)
    truckOne.packs = alist[0]
    truckTwo.packs = alist[1]
    

def getRestrictedPackages(packList):
    #receives a list of packages
    #returns a list of packages that need to be delivered before the end of day
    restricted = []
    for i in range(0, len(packList)):
        if packList[i].time < eod:
            restricted.append(packList[i])
    return restricted


def closestPackage(assignedPacks, unassignedPacks):
    #receives a list of packages that have been assigned to a truck and a list of packages that need to be assigned to a truck
    #returns the uanssigned package the is the closest to one of the assigned packages
    minDist = 999
    for i in range(0, len(assignedPacks)):
        for j in range(0, len(unassignedPacks)):
            dist = distanceBtwnPackagess(assignedPacks[i], unassignedPacks[j])
            if float(dist) < minDist:
                minDist = float(dist)
                pack = unassignedPacks[j]
    return pack


def addRestrictedPackagesInTruck(restricted, truck1, truck2, truck3):
    #receives a list of packages that need to be delivered before the end of date, list of packages from truck1 and list of packages from truck2
    #adds the list of packages that need to be delivered in either truck one or truck two (whichever is closest in distance)
    closer1 = closestPackage(restricted, truck1)
    closer2 = closestPackage(restricted, truck2)
    for i in range(0, len(restricted)):
        p = restricted[i]
        dist1 = distanceBtwnPackagess(p, closer1)
        dist2 = distanceBtwnPackagess(p, closer2)
        if float(dist1) < float(dist2):
            truck1.append(p)
            truck3.remove(p)
        elif float(dist2) < float(dist1):
            truck2.append(p)
            truck3.remove(p)
        elif float(dist1) == float(dist2):
            truck1.append(p)
            ttruck3.remove(p)


def furthestPackFromHubNoRestrictions(packList):
    #receives a list of packages
    #returns the furthest package from the hub (package needs to be delivered at the end of day)
    maxDist = 0
    for i in range(0, len(packList)):
        for j in range(0, len(distBtwn2Addrss)):
            if ((packList[i].address in distBtwn2Addrss[j][0]) and distBtwn2Addrss[j][1] == theHub) and packList[i].time == eod:
                if float(distBtwn2Addrss[j][2]) > float(maxDist):
                    maxDist = float(distBtwn2Addrss[j][2])
                    furthestPack = packList[i]
            elif (packList[i].address in distBtwn2Addrss[j][1] and distBtwn2Addrss[j][0] == theHub) and packList[i].time == eod:
                if float(distBtwn2Addrss[j][2]) > float(maxDist):
                    maxDist = float(distBtwn2Addrss[j][2])
                    furthestPack = packList[i]
    return furthestPack


def switchPackages(overMax):
    #receives a list of packages
    #adds a package to truck3 and removes it from the list of packages
    additionalPacks = len(overMax) - truckOne.maxPacks
    for i in range(0, additionalPacks):
        pack = furthestPackFromHubNoRestrictions(overMax)
        truckThree.packs.append(pack)
        overMax.remove(pack)
        # for j in range(0, len(overMax)):
        #     if overMax[j].packageID == p.packageID:
        #         overMax.remove(overMax[j])
        #         break;


def distance2Hub(package):
    #receives a package
    #returns the distance to the hub
    for i in range(0, len(distBtwn2Addrss)):
        if (package.address in distBtwn2Addrss[i][0]) and (distBtwn2Addrss[i][1] == theHub):
            return float(distBtwn2Addrss[i][2])
        elif (package.address in distBtwn2Addrss[i][1]) and (distBtwn2Addrss[i][0] == theHub):
            return float(distBtwn2Addrss[i][2])
        

def closestPackage2Hub(packList):
    #receives a list a packages
    #return the closest package to the Hub
    minDist = 999
    for i in range(0, len(packList)):
        dist = distance2Hub(packList[i])
        if float(dist) < minDist:
            minDist = float(dist)
            pack = packList[i]
    return pack  


def getClosestPackageWithinList(pack, packList):
    #receives a package and a list of packages
    #returns a package that is closest to the package that was received
    minDist = 999
    for i in range( 0, len(packList)):
        dist = distanceBtwnPackagess(pack, packList[i])
        if float(dist) != -1:
            if float(dist) < minDist or dist == 0:
                minDist = float(dist)
                closestPack = packList[i]
    return closestPack             


def inOrder(packList):
    #receives a list of packages
    #returns the list of packages to be delivered in order(by distance)
    pack = closestPackage2Hub(packList)
    usedPacks = []
    usedPacks.append(pack)
    availablePacks = []
    for i in range(0, len(packList)):
        availablePacks.append(packList[i])
    for i in range(0, len(availablePacks)):
        if pack.packageID == availablePacks[i].packageID:
            availablePacks.pop(i)
            break
    for j in range(0, (len(packList) - 1)):
        pack = getClosestPackageWithinList(pack, availablePacks)
        usedPacks.append(pack)
        for i in range(0, len(availablePacks)):
            if pack.packageID == availablePacks[i].packageID:
                availablePacks.pop(i)
                break
    return usedPacks


def getDeadlineList(packList):
    #receives a list of packages
    #return a list of packages that need to be delivered before end of day
    earlyList = []
    for i in range(0, len(packList)):
        if packList[i].time < eod:
            earlyList.append(packList[i])
    for i in range(0, len(earlyList)):
        index = i
        pack = earlyList[i]
        early = earlyList[i].time
        for j in range(i + 1, len(earlyList)):
            if earlyList[j].time < early:
                early = earlyList[j].time
                pack = earlyList[j]
                index = j
        earlyList.pop(index)
        earlyList.insert(i, pack)
    return earlyList


def miles2Min(miles):
    #receives the miles
    #returns Minutes and Seconds
    minNsecs = []
    min = (miles *60)/18
    justMin = int(min)
    toSecs = min - justMin
    toSecs = toSecs * 60
    toSecs = round(toSecs)
    noDecimal = toSecs
    minNsecs.append(justMin)
    minNsecs.append(noDecimal)
    return minNsecs

def isEnoughTime(package, time, packList):
    #receives a package, the time the package would be delivered and the list of packages from a truck that need to be delivered at a specific time
    #returns true if we have enough time to delivered the package and still make it on time for the other packages that hace a set delivery time. else it will return false
    for i in range(0, len(packList)):
        dist = float(distanceBtwnPackagess(package, packList[i]))
        minNsec = miles2Min(dist)
        newTime = time + timedelta(minutes=minNsec[0], seconds=minNsec[1])
        isEnough = time < newTime or time == newTime
        if isEnough == False:
            return False
    return True
                                               
    
def getRoute(truck, deadlineList):
    #received the a truck and a list of packages that are to be delivered before the end of day 
    #returns the list of packages with the correct route verying that the deliveries will be on time
    packs = truck.packs
    route = []
    hubDist = float(distance2Hub(packs[0]))
    minsNsecs = miles2Min(hubDist)
    time = truck.startTime + timedelta(minutes=minsNsecs[0], seconds=minsNsecs[1])
    enoughTime = isEnoughTime(packs[0], time, deadlineList)
    if enoughTime == True:
        route.append(packs[0])
        packs[0].deliveredTime = time
    else:
        route.append(deadlineList[0])
        deadlineList.remove(deadlineList[0])
    for i in range(0, len(packs) - 1):
        dist = float(distanceBtwnPackagess(packs[i], packs[i + 1]))
        minsNsecs = miles2Min(dist)
        time = time + timedelta(minutes=minsNsecs[0], seconds=minsNsecs[1])
        enoughTime = isEnoughTime(packs[i+1], time, deadlineList)
        if enoughTime == True:
            route.append(packs[i + 1])
            packs[i + 1].deliveredTime = time
            if packs[i + 1].packageID == deadlineList[0].packageID:
                deadlineList.remove(deadlineList[0])
        else:
            route.append(deadlineList[0])
            deadlineList.remove(deadlineList[0])
    hubDist = float(distance2Hub(packs[len(packs) - 1]))
    minsNsecs = miles2Min(hubDist)
    time = time + timedelta(minutes=minsNsecs[0], seconds=minsNsecs[1])
    truck.pack = route
    truck.finishTime = time
    return route


def getRoute2(truck):
    #receives a truck
    #returns a list of packages with the best route
    route = []
    hubDist = float(distance2Hub(truck.packs[0]))
    minsNsecs = miles2Min(hubDist)
    time = truck.startTime + timedelta(minutes=minsNsecs[0], seconds=minsNsecs[1])
    truck.packs[0].deliveredTime = time
    route.append(truck.packs[0])
    for i in range (0, len(truck.packs) - 1):
        dist = float(distanceBtwnPackagess(truck.packs[i], truck.packs[i+1]))
        minsNsecs = miles2Min(dist)
        time = time + timedelta(minutes=minsNsecs[0], seconds=minsNsecs[1])
        route.append(truck.packs[i+1])
        truck.packs[i+1].deliveredTime = time
    hubDist = float(distance2Hub(truck.packs[len(truck.packs) - 1]))
    minsNsecs = miles2Min(hubDist)
    time = time + timedelta(minutes=minsNsecs[0], seconds=minsNsecs[1])
    truck.packs = route
    truck.finishTime = time
    return route                        


def setTruck(truck):
    #receives a truck
    #set each package within the truck with a truck number
    for i in range(0, len(truck.packs)):
        truck.packs[i].truck = truck.number


def setStartTime(truck):
    #receives a truck
    #set each package in that truck with a start time
    for i in range(0, len(truck.packs)):
        truck.packs[i].startTime = truck.startTime


def getTotalDistance(packList):
    #receives a list of packages from a truck
    #returns the total distance starting at the hub and ending at the hub
    total = 0
    dist = float(distance2Hub(packList[0]))
    total = total + dist
    for i in range(0, len(packList) - 1):
        dist = float(distanceBtwnPackagess(packList[i], packList[i+1]))
        total = total + dist
    dist = float(distance2Hub(packList[len(packList) - 1]))
    total = total + dist
    return total



eod = '05:00:00 PM'
eod = datetime.strptime(eod, '%I:%M:%S %p').time()

excelAddresses = []
with open("Address.csv", "r") as file:
  csvfileReader = csv.reader(file)
  for row in csvfileReader:
    excelAddresses.append(row)

allPackages = []
with open("Package.csv", "r") as filePackage:
    csvfilePackageReader = csv.reader(filePackage)
    for row in csvfilePackageReader:
        allPackages.append(row)

theHub = excelAddresses[0][1]

packageList = []
for i in range(1, len(allPackages)):
    p = Package()
    p.packageID = allPackages[i][0]
    p.address = allPackages[i][1]
    p.city = allPackages[i][2]
    p.state = allPackages[i][3]
    p.zip = allPackages[i][4]       
    tempTime = allPackages[i][5]
    if tempTime == "EOD":
        p.time = eod
    else:
        tempTime = datetime.strptime(tempTime, '%I:%M:%S %p').time()
        p.time = tempTime
    p.weight = allPackages[i][6]
    p.requiredTruck = allPackages[i][7]
    packageList.append(p)

distBtwn2Addrss = []
for i in range(1, len(excelAddresses[0])):
    for j in range(1, len(excelAddresses)):
        addressRow = excelAddresses[0][i]
        addressColumn = excelAddresses[j][0]
        distance = excelAddresses[j][i]
        if distance != "":
            alist = []
            alist.append(addressRow)
            alist.append(addressColumn)
            alist.append(distance)
            distBtwn2Addrss.append(alist)

hTable = HashTable()
for i in range(1, len(allPackages)):
    id = int(allPackages[i][0])
    hTable.insert(id, packageList[i - 1])

# print(hTable.lookUp(5)) -- example where you put the package ID and return all the package information requested
    
truckOne = Truck()
truckOne.number = 1;
truckOne.packs.append(hTable.lookUp(13))
truckOne.packs.append(hTable.lookUp(14))
truckOne.packs.append(hTable.lookUp(15))
truckOne.packs.append(hTable.lookUp(16))
truckOne.packs.append(hTable.lookUp(19))
truckOne.packs.append(hTable.lookUp(20))

truckTwo = Truck()
truckTwo.number = 2;
truckTwo.packs.append(hTable.lookUp(3))
truckTwo.packs.append(hTable.lookUp(6))
truckTwo.packs.append(hTable.lookUp(18))
truckTwo.packs.append(hTable.lookUp(25))
truckTwo.packs.append(hTable.lookUp(28))
truckTwo.packs.append(hTable.lookUp(32))
truckTwo.packs.append(hTable.lookUp(36))
truckTwo.packs.append(hTable.lookUp(38))

truckThree = Truck()
truckThree.number = 3;
truckThree.packs.append(hTable.lookUp(9))

assignPackages()
truckThree.packs = availableCombinedPackages(truckOne.packs, truckTwo.packs)
restrictedPackages = getRestrictedPackages(truckThree.packs)
addRestrictedPackagesInTruck(restrictedPackages, truckOne.packs, truckTwo.packs, truckThree.packs)

if len(truckOne.packs) > 16:
    switchPackages(truckOne.packs)

if len(truckTwo.packs) > 16:
    switchPackages(truckTwo.packs)

truckOne.packs = inOrder(truckOne.packs)
truckTwo.packs = inOrder(truckTwo.packs)
truckThree.packs = inOrder(truckThree.packs)

truckOneDeadlineList = getDeadlineList(truckOne.packs)
truckTwoDeadlineList = getDeadlineList(truckTwo.packs)

startOne = "08:00:00 AM"
startTwo = "09:05:00 AM"
preferredTime = "10:20:00 AM"

truckOne.startTime = datetime.strptime(startOne, '%I:%M:%S %p')
truckTwo.startTime = datetime.strptime(startTwo, '%I:%M:%S %p')
truckThree.startTime = datetime.strptime(preferredTime, '%I:%M:%S %p')

truckOne.packs = getRoute(truckOne, truckOneDeadlineList)
truckTwo.packs = getRoute(truckTwo, truckTwoDeadlineList)

setTruck(truckOne)
setTruck(truckTwo)
setStartTime(truckOne)
setStartTime(truckTwo)

if truckOne.finishTime > truckThree.startTime and truckTwo.finishTime > truckThree.startTime:
    if truckOne.finishTime < truckTwo.finishTime:
        truckThree.startTime = truckOne.finishTime
    else:
        truckThree.startTime = truckTwo.finishTime

truckThree.packs = getRoute2(truckThree)
setTruck(truckThree)
setStartTime(truckThree)

completeDistance = getTotalDistance(truckOne.packs) + getTotalDistance(truckTwo.packs) + getTotalDistance(truckThree.packs)
print("Truck 1: " + str(getTotalDistance(truckOne.packs)) + " miles")
print("Truck 2: " + str(getTotalDistance(truckTwo.packs)) + " miles")
print("Truck 3: " + str(getTotalDistance(truckThree.packs)) + " miles")
print("Total mileage traveled by all trucks: " + str(completeDistance))

#input section

print("Enter the time to find the package status Ex HH:MM:SS AM or HH:MM:SS PM  - HH can not be 00")
inputTime = input()

hours = inputTime[0:2]
minutes = inputTime[3:5]
seconds = inputTime[6:8]
ampm = inputTime[-2:]

while (hours == "00"):
    print("Error, Please provide the correct information - see example")
    inputTime = input()
    hours = inputTime[0:2]
    minutes = inputTime[3:5]
    seconds = inputTime[6:8]
    ampm = inputTime[-2:]
    
time = datetime.strptime(inputTime, '%I:%M:%S %p')

for i in range(0, len(packageList)):
    if time < packageList[i].startTime:
        packageList[i].deliveryStatus = "Hub"
    elif time > packageList[i].startTime and time < packageList[i].deliveredTime:
        packageList[i].deliveryStatus = "En Route"
    elif time == packageList[i].deliveredTime or time > packageList[i].deliveredTime:
        packageList[i].deliveryStatus = "Delivered " + str(packageList[i].deliveredTime.time())

statusList = []
for i in range(0,len(packageList)):
    packageStatusList = []
    packageStatusList.append(packageList[i].packageID)
    packageStatusList.append(packageList[i].deliveryStatus)
    if packageList[i].deliveryStatus == "Delivered":
        packageStatusList.append(packageList[i].deliveredTime.time())
    packageStatusList.append(packageList[i].truck)
    statusList.append(packageStatusList)

for i in range(0,len(statusList)):
    print(statusList[i])





