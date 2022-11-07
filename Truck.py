import datetime
import csv
from Package import pkgsTable
from Package import totalPkgs

# Using data from Distance table CSV file, create a list of distances between each address
with open('CSVFiles/WGUPS-Distance-Table.csv', newline='') as fileDist:
    csvDistList = csv.reader(fileDist, delimiter=',')
    distTable = list(csvDistList)

# Initialize variables
totalDist = 0
pkgMasterList = []
deliveryStartTime = ['8:00:00', '9:10:00', '10:20:00', '9:50:00']

# Load trucks in a nested dictionary. Truck number 4 is truck 1's second trip
truckTable = {1: {'status': 'at hub'}, 2: {'status': 'at hub'}, 3: {'status': 'at hub'}, 4: {'status': 'at hub'}}

# Load package master list with every package ID
for i in range(1, totalPkgs + 1):
    pkgMasterList.append(int(i))

# Load packages with special instruction on the trucks
for i in range(1, totalPkgs + 1):
    pkgInfo = pkgsTable.getVal(i - 1)
    # Load packages with time restriction or may need to be shipped together onto truck number 1
    if pkgInfo[5] != 'EOD' and pkgInfo[7] == 'None' or ('Must' in pkgInfo[7]) or pkgInfo[0] == '19':
        truckTable[1]["slot_{0}".format(len(truckTable[1]))] = i
        pkgMasterList.remove(int(i))
    # Load packages for 2nd trip of truck 1 with time restriction
    elif i == 25:
        truckTable[4]["slot_{0}".format(len(truckTable[4]))] = i
        pkgMasterList.remove(int(i))
    # Load packages that are delayed onto truck number 2
    elif 'truck 2' in pkgInfo[7] or 'Delayed' in pkgInfo[7]:
        truckTable[2]["slot_{0}".format(len(truckTable[2]))] = i
        pkgMasterList.remove(int(i))

    # Load packages that have wrong address onto truck number 3
    elif 'Wrong' in pkgInfo[7]:
        truckTable[3]["slot_{0}".format(len(truckTable[3]))] = i
        pkgMasterList.remove(int(i))
        pkgInfo[1] = '410 S State St.'
        pkgInfo[2] = 'Salt Lake City'
        pkgInfo[4] = '84111'
        pkgsTable.updateVal(i - 1, pkgInfo)

# Using nearest neighbor algorithm to sort packages onto trucks
# Time complexity is O(n³) + O(n)
for pkgInd in range(len(pkgMasterList)):
    minDist = 50
    prefTruck = 0
    emptyTruckList = []
    # Remove truck from sorting if it is full of 16 packages
    for truckInd in truckTable:
        if len(truckTable[truckInd]) < 17:
            emptyTruckList.append(truckInd)
    for truckInd in emptyTruckList:
        for i in range(len(truckTable[truckInd]) - 1):
            # Get the package data from last package on the truck
            pkgID = truckTable[truckInd]["slot_{0}".format(i + 1)]
            pkgInfo = pkgsTable.getVal(pkgID - 1)
            addrsID = pkgInfo[11]
            dist = distTable[int(pkgInd)][int(addrsID)]
            # if the distance from distance table is not valid, try again by flipping the order
            if dist == '':
                dist = distTable[int(addrsID)][int(pkgInd)]
            # Compare with minimum distance and save it if it is smaller
            if minDist > float(dist):
                minDist = float(dist)
                prefTruck = truckInd
    # Load the package onto the truck with the shortest distance
    truckTable[prefTruck]["slot_{0}".format(len(truckTable[prefTruck]))] = pkgMasterList[pkgInd]

# Using greedy algorithm to sort packages for delivery by the most minimal distance between each stop
# Time complexity is O(nlog(n))
for truckInd in truckTable:
    currentLoc = 0
    for pkgInd in range(1, len(truckTable[truckInd])):
        minDist = 100
        prefPkg = 0
        prefAddrs = 0
        addrsList = []
        for i in range(pkgInd - 1, len(truckTable[truckInd]) - 1):
            # Get the package data from last package on the truck
            pkgID = truckTable[truckInd]["slot_{0}".format(i + 1)]
            pkgInfo = pkgsTable.getVal(pkgID - 1)
            addrsID = pkgInfo[11]
            dist = distTable[int(currentLoc)][int(addrsID)]
            # if the distance from distance table is not valid, try again by flipping the order
            if dist == '':
                dist = distTable[int(addrsID)][int(currentLoc)]
            # Compare with minimum distance and save it if it is smaller
            if minDist > float(dist):
                minDist = float(dist)
                prefPkg = int(i) + 1
                prefAddrs = addrsID
        # Swap the package with the shortest distance to the next stop
        truckTable[truckInd]["slot_{0}".format(pkgInd)], truckTable[truckInd]["slot_{0}".format(prefPkg)] = truckTable[truckInd]["slot_{0}".format(prefPkg)], \
                                                                                                            truckTable[truckInd]["slot_{0}".format(pkgInd)]
        # Update total distance of the trucks
        totalDist += minDist
        # Update current location of the truck
        currentLoc = prefAddrs

# Assign start time and delivery time for each package
# Time complexity is O(n²)
for truckInd in truckTable:
    currentLoc = 0
    # Track the time of the truck from when it leaves the hub
    truckTrackedTime = deliveryStartTime[truckInd - 1]
    (h, m, s) = truckTrackedTime.split(':')
    truckTrackedTime = datetime.timedelta(hours=int(h), minutes=int(m), seconds=int(s))
    for pkgInd in range(0, len(truckTable[truckInd]) - 1):
        # Get the package data from last package on the truck
        pkgID = truckTable[truckInd]["slot_{0}".format(pkgInd + 1)]
        pkgInfo = pkgsTable.getVal(pkgID - 1)
        addrsID = pkgInfo[11]
        dist = distTable[int(currentLoc)][int(addrsID)]
        # if the distance from distance table is not valid, try again by flipping the order
        if dist == '':
            dist = distTable[int(addrsID)][int(currentLoc)]
        pkgInfo[8] = deliveryStartTime[truckInd - 1]
        # Calculate the time required for the truck to travel through the route and update the time
        time = float(dist) / 18
        timeConverted = '{0:02.0f}:{1:02.0f}'.format(*divmod(time * 60, 60)) + ':00'
        (h, m, s) = timeConverted.split(':')
        timeConverted = datetime.timedelta(hours=int(h), minutes=int(m), seconds=int(s))
        truckTrackedTime += timeConverted
        # Update hash map with the new time
        pkgInfo[9] = str(truckTrackedTime)
        pkgsTable.updateVal(int(pkgID) - 1, pkgInfo)
        currentLoc = addrsID
