import random

class Train():

    # Defining train_location, traject_length and destination
    def __init__(self, current_station, list_of_destinations):
        self.current_station = current_station
        self.previous = 0
        self.list_of_stations = [current_station]
        self.location = 0
        self.list_of_destinations = list_of_destinations
        self.destination = self.destinations()


    
    def destinations(self):
        """
        Randomly choosing a new destination for a train based on its current location and
        its possible destinations
        """

        # Loop through all the options and save the possible destinations
        destinations_per_train = self.list_of_destinations[self.current_station]
        
        # Randomly choosing a new destination
        new_destination = random.choice(list(destinations_per_train.items()))
        print(new_destination)
        if self.current_station != "Dordrecht" and self.current_station != "Den Helder":
            while new_destination[0] == self.previous:
                new_destination = random.choice(list(destinations_per_train.items()))
        
        return new_destination
    
    def movement(self):
        """
        The movement of a single train is defined by its speed if the destination
        is reached the station will be added to a list of stations on its traject.
        """
        self.location += 1
        
        # If the distance between the train and the station is 0 add it to the list of stations
        if self.destination[1] - self.location == 0:
            self.previous = self.current_station
            self.current_station = self.destination[0]
            self.list_of_stations.append(self.current_station)

            # Determining the next destination
            self.destination = self.destinations()

            # Resetting the counter for the location
            self.location = 0

        return self.list_of_stations


