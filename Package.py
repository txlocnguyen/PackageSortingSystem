import csv
from Hash import HashMap

# Create a nested dictionary of address location with data from CSV file table
with open('CSVFiles/WGUPS-Address-Table.csv', newline='') as fileAddrs:
    csvAddrsList = csv.DictReader(fileAddrs, delimiter=',')
    addrsTable = {}

    for row in csvAddrsList:
        name = row['address_id']
        del row['address_id']
        addrsTable[name] = dict(row)

# Load package data from CSV file table into a hash map
with open('CSVFiles/WGUPS-Package-Table.csv', newline='') as filePkgs:
    csvPkgsList = csv.reader(filePkgs, delimiter=',')
    pkgsTable = HashMap()

    # Create a list of package data
    for row in csvPkgsList:
        pkgId = row[0]
        address = row[1]
        city = row[2]
        state = row[3]
        postal = row[4]
        deadline = row[5]
        weight = row[6]
        special = row[7]
        timeStart = ''
        timeEnd = ''
        status = ''
        addrsId = ''
        value = [pkgId, address, city, state, postal, deadline, weight, special, timeStart, timeEnd, status, addrsId]
        pkgsTable.insertVal(int(pkgId) - 1, value)

    # Keep track of the total number of packages
    totalPkgs = int(pkgId)

# Map each package with the corresponding address ID of delivery location
for pkgIndex in range(40):
    pkgInfo = pkgsTable.getVal(pkgIndex)
    for addrsIndex in addrsTable:
        if pkgInfo[1] == addrsTable[addrsIndex]['address']:
            pkgInfo[11] = addrsIndex
            pkgsTable.updateVal(pkgIndex, pkgInfo)
            break
