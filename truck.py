# Create truck object
class Truck:
    def __init__(self, truck_number, capacity, speed, load, packages, mileage, address, departure):
        self.truck_number = truck_number
        self.capacity = capacity
        self.speed = speed
        self.load = load
        self.packages = packages
        self.mileage = mileage
        self.address = address
        self.departure = departure
        # Need this to track time throughout deliveries and use this to update package delivery times
        self.time = departure

    def __str__(self):  # overwrite
        return "%s, %s, %s,  %s, %s, %s, %s, %s, %s" % (self.truck_number, self.capacity, self.speed, self.load,
                                                        self.packages, self.mileage, self.address, self.departure,
                                                        self.truck_number)
