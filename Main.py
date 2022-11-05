# Loc Nguyen
# Student ID: 010388223
# Student Email: lngu242@wgu.edu
# Data Structures and Algorithms II - Performance Assessment

import datetime
from Truck import totalDist
from Truck import pkgsTable
from Package import totalPkgs


class Main:
    # Variables for user input
    usrInput = 0
    usrTime = 0
    rangeOfPkgs = 0

    # Display the name of the program and the total distance
    print("WGUPS Package Delivery System - Loc Nguyen")
    print("The estimated total distance of delivery for all trucks is", totalDist.__round__(2), "miles")

    # While loop to check and see if the user wants to quit the program
    while usrInput != "quit":
        # Reset the starting index of the package
        pkgIndex = 1

        # New line for better formatting
        print()

        # Request for the user to enter a time
        print("Please enter 'quit' whenever you want to exit this program.")

        # Another while loop to check and see if the user wants to quit the program
        while usrInput != "quit":
            # Ask the user to enter a specific time
            print("Please input a defined time in hh:mm::ss format in order to view it. Or simply type 'all' to view "
                  "the completed route")
            usrInput = input("Time: ")

            # View the completed route by setting time to last second of the day when user type in 'all'
            if usrInput == "all":
                usrTime = "23:59:59"
                (h, m, s) = usrTime.split(":")
                usrTime = datetime.timedelta(hours=int(h), minutes=int(m), seconds=int(s))
                # end the while loop when done by using break
                break

            # Check to see if the user input is in a valid time format
            else:
                # Convert what the user input into a valid time format
                try:
                    (h, m, s) = usrInput.split(":")
                    usrTime = datetime.timedelta(hours=int(h), minutes=int(m), seconds=int(s))
                    # end the while loop when done by using break
                    break

                # If the user input is invalid, ask the user to enter again
                except ValueError:
                    if usrInput == "quit":
                        exit()
                    print("Your input is invalid. Please try again kindly.")

        # Another while loop to check and see if the user wants to quit the program
        while usrInput != "quit":
            # Ask the user to enter a specific package ID
            print("Please input a package ID of choice or type 'all' to see all packages.")
            usrInput = input("Package ID: ")

            # View all packages when user type in 'all'
            if usrInput == "all":
                rangeOfPkgs = totalPkgs + 1
                # end the while loop when done by using break
                break

            # Check to see if the user input is valid (between 1 and 40). Ask the user for a new input in case it is
            # invalid
            elif not 1 <= int(usrInput) <= totalPkgs:
                if usrInput == "quit":
                    exit()
                print("Your input is invalid. Please try again kindly.")

            # If the user input is valid, set the range of packages to view
            else:
                rangeOfPkgs = int(usrInput) + 1
                pkgIndex = int(usrInput)
                # end the while loop when done by using break
                break

        # Display the packages that are being delivered at the time the user input
        while pkgIndex < rangeOfPkgs:
            # convert the package information into datetime format to compare with the user input time
            pkgInfo = pkgsTable.getVal(pkgIndex - 1)
            (h, m, s) = pkgInfo[9].split(":")
            pkgTime = datetime.timedelta(hours=int(h), minutes=int(m), seconds=int(s))

            # Compare the package time against user time and display status of the package accordingly
            if usrTime < pkgTime:
                pkgStatus = "In Transit"
            else:
                pkgStatus = "Delivered"

            # Display the package information
            print("ID:%3d   Address:%40s   Deadline:%15s    Status: %10s    Delivery Time: %7s " % (pkgIndex, pkgInfo[1], pkgInfo[5], pkgStatus, pkgTime))

            # Increment the package index
            pkgIndex += 1

        # Ask for user input again to loop the program over and over until the user type in 'quit'
        usrInput = input("Please enter 'quit' to exit the program or press enter to continue: ")