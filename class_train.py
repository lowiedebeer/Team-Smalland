import random

class Train():

    # Defining train_location, traject_length and destination
    def __init__(self, current_station, list_of_destinations):
        self.total_min = 0
        self.already_taken = 0
        self.location = 0
        self.list_of_stations = []
        self.current_station = current_station
        self.list_of_destinations = list_of_destinations
        self.destination = self.destinations()


    def destinations(self):
        """
        Randomly choosing a new destination for a train based on its current location and
        its possible destinations
        """
        counter = 0

        # Loop through all the options and save the possible destinations
        destinations_per_train = self.list_of_destinations[self.current_station]

        # Randomly choosing a new destination
        new_destination = random.choice(list(destinations_per_train.items()))

        while {self.current_station, new_destination[0]} in self.list_of_stations:
            counter += 1
            new_destination = random.choice(list(destinations_per_train.items()))
            
            if len(list(destinations_per_train.items())) == counter:
                return new_destination

        return new_destination

    def movement(self):
        """
        The movement of a single train is defined by its speed if the destination
        is reached the station will be added to a list of stations on its traject.
        """
        self.location += 1

        # If the distance between the train and the station is 0 add it to the list of stations
        if self.destination[1] - self.location == 0:
            self.list_of_stations.append({self.current_station, self.destination[0]})
            self.current_station = self.destination[0]
            
            # Determining the next destination
            self.destination = self.destinations()

            # Resetting the counter for the location
            self.total_min += self.location
            self.location = 0

        return self.list_of_stations
