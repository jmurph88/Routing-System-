# Jennifer Murphy
# Student ID: 001532028

# References:
# zyBooks. Figure 7.8.2: Hash table using chaining
# Alyssa Walker. Travelling Salesman Problem: Python, C++ Algorithm.
#                   https://www.guru99.com/travelling-salesman-problem.html
# Medium. Traveling Salesman Problem.
#                   https://blog.devgenius.io/traveling-salesman-problem-nearest-neighbor-algorithm-solution-e78399d0ab0c
# Reed, Mark. Python Programming and SQL The #1 Coding Course From Beginner to Advanced.
#                   Independently Published, 2023.

import csv
import datetime
from hashtable import ChainingHashTable
from package import Package
from truck import Truck

# Read file with distances
with open('distanceCSV.csv') as csvfile1:
    Distance_Only = csv.reader(csvfile1)
    Distance_Only = list(Distance_Only)

# Read file with address information
with open('addressCSV.csv') as csvfile2:
    Address_Only = csv.reader(csvfile2)
    Address_Only = list(Address_Only)

with open('packageCSV.csv') as csvfile3:
    Package_File = csv.reader(csvfile3)
    Package_File = list(Package_File)


# Load pacakge data from csv file into hash table
def load_package_data(file_name, my_hash_table):
    # Read package from the CSV file
    with open(file_name) as package_file:
        package_data = csv.reader(package_file, delimiter=',')
        for package in package_data:
            p_id = int(package[0])
            p_address = package[1]
            p_city = package[2]
            p_state = package[3]
            p_zipcode = package[4]
            p_deadline = package[5]
            p_weight = package[6]
            p_notes = package[7]
            p_t_num = package[8]
            p_status = "At Hub"

            # Create the package object
            package_obj = Package(p_id, p_address, p_city, p_state, p_zipcode, p_deadline,
                                  p_weight, p_notes, p_t_num, p_status)

            # insert package data into hash table using key and value (package)
            my_hash_table.insert(p_id, package_obj)


# O(n) - The time it takes to find an address increase linearly with size of data
# Search for address in addressCSV file using list created when reading CSV file
# and get package id to use when searching for distances between packages.
def find_address(address):
    for row in Address_Only:
        if address in row[2]:
            return int(row[0])


# O(1) - just retrieving information; constant time
# Find the distance between two addresses and returns it as a float
def distance_between(row_index, column_index):
    if row_index < column_index:
        # switch row and column if row is smaller
        row_index, column_index = column_index, row_index
    # Retrieve data stored at the row, column location in the file.
    distance = Distance_Only[row_index][column_index]
    return float(distance)


# Nearest neighbor algorithm to load the trucks based on addresses O(n^2)
def nearest_neighbor(truck):
    # All packages that have not been delivered yet in array.
    not_delivered = []
    # Any package that is not delivered is added to the array -Is this my error?
    for package_id in truck.packages:
        package = hash_table.search(package_id)
        not_delivered.append(package)
    # Clear list so packages can be placed in order of closest address(nearest neighbor)
    truck.packages.clear()

    # O(n^2) - nested loops
    # While the not delivered list is not empty
    while len(not_delivered) > 0:
        closest_address = float('inf')  # initialized with large value for address
        next_package = None

        # Iterate over packages that are still at hub and not delivered yet and add to trucks by
        # nearest address.
        for package in not_delivered:
            # Calculates distance between truck's current location and package's address
            current_package_distance = distance_between(find_address(truck.address),
                                                        find_address(package.address))
            # Determine if current package is closer than the next package in line and update next_address and
            # next_package
            if current_package_distance <= closest_address:
                closest_address = current_package_distance
                next_package = package
        # Add the next closest package to the truck's list of packages
        truck.packages.append(next_package.package_id)
        # Remove this package from the list of not delivered packages
        not_delivered.remove(next_package)
        # Set the package's loaded time to the truck departure time, so it can be used in update_status to set status to
        # En Route.
        next_package.loaded_time = truck.departure
        # Add the distance to the next package's address to the truck's mileage
        truck.mileage += closest_address
        # Update truck's address to the current package's address to allow comparison.
        truck.address = next_package.address
        # Update truck time by using the distance to next_address and dividing by 18 mph
        truck.time += datetime.timedelta(hours=closest_address / 18)
        # Update the package delivery time to the new truck time
        next_package.delivery_time = truck.time
        # Need this to be updated to truck departure time to set status to At Hub because off user time
        next_package.departure_time = truck.departure
        # Update the truck number for the package
        next_package.truck_number = truck.truck_number


# Create instance of hash table to load data
hash_table = ChainingHashTable()

# Load package data into hash table
load_package_data('packageCSV.csv', hash_table)

# Create truck objects and assign packages manually
truck1 = Truck(
    truck_number="Truck 1",
    capacity=16,
    speed=18,
    load=0,
    packages=[1, 4, 5, 13, 14, 15, 16, 19, 20, 29, 30, 31, 34, 37, 39, 40],  # loads packages based on ID
    mileage=0.0,
    address="4001 South 700 East",  # All start at the HUB
    departure=datetime.timedelta(hours=8, minutes=0)
)

truck2 = Truck(
    truck_number="Truck 2",
    capacity=16,
    speed=18,
    load=0,
    packages=[2, 3, 7, 8, 9, 10, 18, 22, 24, 26, 27, 33, 35, 36, 38],
    # loads packages based on ID - Package with address change goes here
    mileage=0.0,
    address="4001 South 700 East",  # All start at the HUB
    departure=datetime.timedelta(hours=10, minutes=20)
)

truck3 = Truck(
    truck_number="Truck 3",
    capacity=16,
    speed=18,
    load=0,
    packages=[6, 11, 12, 17, 19, 21, 23, 25, 28, 32],  # loads packages based on ID
    mileage=0.0,
    address="4001 South 700 East",  # All start at the HUB
    departure=datetime.timedelta(hours=9, minutes=5)
)

# Load the trucks for delivery of packages
nearest_neighbor(truck1)
nearest_neighbor(truck2)

# Need to make sure truck 3 does not leave until these two trucks are finished -
# only two drivers available - truck3's departure time is set to depart as soon as truck1 or truck2 has completed
# deliveries ensuring it cannot leave until one of those trucks is finished.
truck3.departure = min(truck1.time, truck2.time)

# Load truck 3
nearest_neighbor(truck3)


class Main:

    global convert_user_input
    total_mileage = (truck1.mileage + truck2.mileage + truck3.mileage)
    round_mileage = round(total_mileage, 1)

    while True:
        print("WGUPS Routing System")
        print("The route mileage is: " + str(round_mileage))
        user_time = input("Enter a selected time in HH:MM and 24 hour format or Q to quit:")
        # Allows user to enter Q to close program
        if user_time.upper() == 'Q':
            print("Closing Program")
            break
        # Checks to make sure user input is in HH:MM format by checking for exactly 5 characters,
        # that the character in index 2 is semicolon, the first two characters are numbers and the last two
        # characters are numbers. If not, it prints an error message.
        if len(user_time) == 5 and user_time[2] == ":" and user_time[:2].isdigit() \
                and user_time[3:].isdigit():
            # Reformat user input into a datetime object for comparison in Package status_update method
            (h, m) = user_time.split(":")
            convert_user_input = datetime.timedelta(hours=int(h), minutes=int(m))
        else:
            print("Invalid input. Please enter selected time in HH:MM and 24 hour format.")

        print("Menu Options:")
        print("1 - Print the status of a selected package.")
        print("2 - Print the status of all packages.")
        print("3 - Exit the program")
        user_input = input("Please enter the number of the option you would like to select:")

        # Need to add check that they actually enter a number
        if user_input == "1":
            # User input is saved in user_package_id variable and used to search the hashtable.
            # If found, it returns the package object. If not found, user receives error message.
            user_package_id = int(input("Please enter the package ID: "))
            user_package = hash_table.search(user_package_id)
            if user_package is not None:
                print("Package ID, Address, City, State, Zipcode, Deadline, Weight (KILO), Notes, Truck, Status")
                print("-----------------------------------------------------------------------------------------")
                user_package.update_status(convert_user_input)
                print(str(user_package))
            # else:
            # print("Package ID is not found")
            else:
                print("Invalid entry.")
        # User will be prompted to enter a time that will be used to update that status of all packages. All packages
        # will be print to screen.
        elif user_input == "2":
            print("Package ID, Address, City, State, Zipcode, Deadline, Weight (KILO), Notes, Truck, Status")
            print("-----------------------------------------------------------------------------------------")
            for package_id in range(1, 41):
                package = hash_table.search(package_id)
                package.update_status(convert_user_input)
                print(str(package))
        # Closes the program is the user input is 3.
        elif user_input == "3":
            print("Closing program...")
            break

        else:
            print("Invalid choice. Please try again.")
