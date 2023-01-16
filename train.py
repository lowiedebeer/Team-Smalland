import random

class Train():

    # Defining train_location, traject_length and destination
    def __init__(self, current_station, traject_length, list_of_destinations):
        self.train = current_station
        self.traject_length = traject_length # In minuten
        self.list_of_stations = [current_station]
        self.location = 0
        self.list_of_destinations = list_of_destinations
    
    
    def destinations(self):
        """
        Randomly choosing a new destination for a train based on its current location
        """
        destinations_per_train = []

        # Loop through all the options and save the possible destinations
        for destination in self.list_of_destinations:
            destinations_per_train.append(destination[self.train])

        # Randomly choosing a new destination
        new_destination = random.choice((destinations_per_train))
        
        return new_destination
    
    def movement(self):
        """
        The movement of a single train is defined by its speed if the destination
        is reached the station will be added to a list of stations on its traject.
        """
        self.location += 1
       
       # If the distance between the train and the station is 0 add it to the list of stations
        if self.traject_length[1] - self.location == 0:
            self.train = self.traject_length[0]
            self.list_of_stations.append(self.train)

            # Determining the next destination
            self.traject_length = self.destinations()
            
        return self.list_of_stations


