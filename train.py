import random

class Train():

    # Defining train_location, traject_length and destination
    def __init__(self, current_station, list_of_destinations):
        self.list_of_destinations = list_of_destinations
        self.current_station = current_station # In minuten
        self.list_of_stations = [current_station]
        self.location = 0
        self.set_of_destinations = set(list_of_destinations[current_station])
        self.destination = self.destinations()

    def destinations(self):
        """
        Randomly choosing a new destination for a train based on its current location and
        its possible destinations
        """

        # Loop through all the options and save the possible destinations
        destinations_per_train = self.set_of_destinations

        for i in range(len(destinations_per_train)):
            new_destination = random.choice(list(destinations_per_train))
            if new_destination[0] in self.list_of_stations:
                destinations_per_train.remove(new_destination)
            else:
                return new_destination

        new_destination = random.choice(list(destinations_per_train))

        return new_destination


    def movement(self):
        """
        The movement of a single train is defined by its speed if the destination
        is reached the station will be added to a list of stations on its traject.
        """
        self.location += 1
        list_of_stations_distance = self.list_of_destinations[self.current_station]

        # If the distance between the train and the station is 0 add it to the list of stations
        if list_of_stations_distance[self.destination] - self.location == 0:
            self.current_station = self.destination
            self.list_of_stations.append(self.current_station)

            # Determining the next destination
            self.destination = self.destinations()
            self.location = 0
